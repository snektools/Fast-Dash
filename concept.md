# Concept
## Main Idea
The primary goal of Fast Dash is to provide a tool that allows quick generation of dashboards using code. The current plan is to use Plotly Dash as the basis of this tool, but provide a layer of abstraction on top that simplifies everything, but still allows modifying any details you need.
## Structure
Below are the structures that will be used for dashboard creation, from the lowest to highest level.
### Element
An element can be both a visualization such as a table or a graph, as well as a control element such as an input box or drop down.
<br>
Specific elements will be defined for each general type (bar graph, line graph, drop down, etc). Based on the type of element, different parameters can be provided that either provide static values for the parameter (ie width) or a pointer to a data source for dynamic population of the parameter (checkbox items based on de-duplicated column).
<br>
An example of what an element might look like can be found below:

```python
from FastDash.elements import BarChart, DropDown, mean, count_distinct
from datasource import data
failure_category = BarChart(
    x = data.date,
    y = data.failures,
    y_agg = count_distint,
    key = data['failure_code']
)

line_dd = DropDown(
    options = data.assembly_lines
)
```

By default, any columns provided for x, y, key, options, etc will be active filters. This means, that selecting an item in the drop down will affect the other elements in a given page UNLESS a different scope is defined or the parameter for an element is excluded.
```python
from FastDash.elements import BarChart, DropDown, mean, count_distinct
from datasource import data

failure_category = BarChart(
    x = data.date,
    y = data.failures,
    y_agg = count_distinct,
    key = data['failure_code'],
    exclude = [BarChart.x,BarChart.key]
)

failure_category.y.filter = False

line_dd = DropDown(
    options = data.assembly_lines
)
```

```python
from FastDash.elements import BarChart, DropDown, mean, count_distinct
from datasource import data

agg_type = DropDown(
    options = [mean, count_distinct, max, min],
    single = True,
    default = mean,
)

failure_category = BarChart(
    x = data.date,
    y = data.failures,
    y_agg = agg_type.selection,
    key = data['failure_code'],
    exclude = [BarChart.x,BarChart.key]
)

failure_category.y.filter = False

line_dd = DropDown(
    options = data.assembly_lines
)


```

### Data

Stuff about data, will likely be (2) stages (pass filters down to query layer, operate on in-memory data).

### Page
A page represents a screen that contains elements. By default, any elements sharing a common data source on a page will use the same underlying filters.
<br>
Navigation between pages can be configured as either tabs or links in a drop down.
<br>
If no page objects are created, each `.py` file that contains element objects in the directory wil be considered seperate pages. The examples above would all be single page dashboards, because there is no explicit asignment and all of the elements are in a single file.
<br>
If a page object is created but no elements are assigned, the page will be blank and any elements in the same file will not show up. To assign an element to a page, they can either be passed in a list when the page is created, or by using the `+=` operator:

```python
from FastDash.elements import BarChart, DropDown, mean, count_distinct
from FastDash.pages import Page
from datasource import data

agg_type = DropDown(
    options = [mean, count_distinct, max, min],
    single = True,
    default = mean,
)

failure_category = BarChart(
    x = data.date,
    y = data.failures,
    y_agg = agg_type.selection,
    key = data['failure_code'],
    exclude = [BarChart.x,BarChart.key]
)

failure_category.y.filter = False

line_dd = DropDown(
    options = data.assembly_lines
)

home = Page(
    title='Welcome home!',
    elements = [failure_category, line_dd]
)

home += agg_type



```

A page will also be where the layout rules are established. By default, the layout will be generated based on the order that the elements are added to the page.
## App
An app will contain the pages. An app may be a standard dashboard, or it can also be a sequence (pages cycle through based on conditions on a each page).
<br> 
By default, an app is a dashboard, and it will be composed of an pages that were created either explicitly or implicitly (via .py files). 

