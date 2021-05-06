from fast_dash.components.visualizations import Plot
import pandas as pd
import plotly.graph_objs as go
from collections.abc import Callable

import itertools


def get_bucket_parameter(timeframe):
    if "week" in timeframe.lower():
        return "Week %U, %Y"
    if "month" in timeframe.lower():
        return "%Y-%m"
    if "day" in timeframe.lower():
        return "%Y-%m-%d "
    if "hour" in timeframe.lower():
        return "%Y-%m-%d %H:%m"


def find_time_column(df):
    for column in df:
        if "time" in column.lower():
            return column
    raise Exception(
        'No column found for time. Try passing in a column name with the "time_column" argument'
    )


def group(
    data,
    aggregate_column,
    grouped_columns,
    x_column,
    y_column,
):
    pass


def nrft(
    data,
    aggregate_column,
    grouped_columns,
    x_column,
    y_column,
):
    all_aggregates_total = qty(
        data,
        aggregate_column,
        grouped_columns,
        x_column,
        y_column,
    )

    time_bucket_totals = data.groupby(x_column)[aggregate_column].count()

    all_aggregates_total = all_aggregates_total.merge(
        time_bucket_totals, how="left", left_on=x_column, right_index=True
    )

    all_aggregates_total["result"] = (
        all_aggregates_total["result"] / all_aggregates_total[aggregate_column]
    ) * 100

    return all_aggregates_total


def qty(
    data,
    aggregate_column,
    grouped_columns,
    x_column,
    y_column,
):
    data = data.copy(deep=True)
    aggregate_columns = [x_column] + grouped_columns
    all_aggregates_total = data.groupby(aggregate_columns)[aggregate_column].sum()

    if len(aggregate_columns) == 1:
        output_data = {x_column: [data for data in all_aggregates_total.index]}
    else:
        output_data = {
            column: [data[index] for data in all_aggregates_total.index]
            for index, column in enumerate(aggregate_columns)
        }

    output_data.update({"result": [value for value in all_aggregates_total]})

    return pd.DataFrame(output_data)


def find_aggregate_function(desc: str = "nrft") -> Callable:
    if "nrft" in desc.lower():
        return nrft
    if "qty" in desc.lower():
        return qty


class VeriticalBar(Plot):
    # TODO Create a Bar plot parent class

    _calcmode_arg = "_calcmode"
    _aggregate_column_arg = "_aggregate_column"
    _grouped_columns_arg = "_grouped_columns"
    _time_bucket_arg = "_time_bucket"
    _x_column_arg = "_x_column"
    _y_column_arg = "_y_column"

    def _set_default_columns(self):
        self._calcmode_default = "nrft"
        self._aggregated_column_default = "failed"
        self._grouped_columns_default = []
        self._time_bucket_default = "hour"
        self._x_column_default = "TimeStamp"
        self._y_column_default = "failed"

    def _get_arguments(self, **kwargs):
        self._calcmode = self._check_args(
            self._calcmode_arg, self._calcmode_default, **kwargs
        )
        self._aggregate_column = self._check_args(
            self._aggregate_column_arg, self._aggregated_column_default, **kwargs
        )
        self._grouped_columns = self._check_args(
            self._grouped_columns_arg, self._grouped_columns_default, **kwargs
        )
        self._time_bucket = self._check_args(
            self._time_bucket_arg, self._time_bucket_default, **kwargs
        )
        self._x_column = self._check_args(
            self._x_column_arg, self._x_column_default, **kwargs
        )
        self._y_column = self._check_args(
            self._y_column_arg, self._y_column_default, **kwargs
        )

    def _aggregate_data(self):
        aggregating_function = find_aggregate_function(self._calcmode)
        self._processed_data = aggregating_function(
            data=self._processed_data,
            aggregate_column=self._aggregate_column,
            grouped_columns=self._grouped_columns,
            x_column=self._x_column,
            y_column=self._y_column,
        )

    def _post_process_data(self, **kwargs):

        if "passed" not in self._processed_data:
            raise Exception(
                'There is not "passed" column in the data. Please update the query or add a "post_process_func" to rename or create a column names "passed"'
            )

        self._processed_data["failed"] = ~self._processed_data["passed"]

        self._time_bucket_string = get_bucket_parameter(self._time_bucket)
        self._processed_data[self._x_column] = self._processed_data[
            self._x_column
        ].dt.strftime(self._time_bucket_string)

    def _build_plot_data(self, **kwargs):
        combinations = []
        failed_data = self._processed_data.loc[self._processed_data.result > 0]
        for combination in itertools.product(
            *[sorted(set(failed_data[column])) for column in self._grouped_columns]
        ):
            combinations.append(
                {
                    column: value
                    for column, value in zip(self._grouped_columns, combination)
                }
            )
        self._go_data = []
        for combination in combinations:
            temp_data = self._processed_data.copy(deep=True)

            if combination:
                for column, criteria in combination.items():
                    temp_data = temp_data.loc[temp_data[column] == criteria]

            self._go_data.append(
                go.Bar(
                    x=temp_data[self._x_column],
                    y=temp_data["result"],
                    name=", ".join([str(value) for value in combination.values()]),
                )
            )

    def _build_layout(self, **kwargs):
        self._stacked = self._check_args("_barmode", "stack", **kwargs)
        self._go_layout = go.Layout(
            barmode=self._stacked,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        )
