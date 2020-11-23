{% sql 'station_data', connection_string='DRIVER=SQL Server;SERVER=DLNWTSR170;Trusted_Connection=Yes' %}
    SELECT TOP
    {% if top %}
        {{top}}
    {% else %}
        1000
    {% endif %}
    *
    FROM [{{database}}].dbo.[{{station}}]
    {% if start_date and end_date %}
        WHERE [TimeStamp] between '{{ start_date }}' and '{{ end_date }}'
    {% endif %}
    ORDER BY [TimeStamp] DESC
{% endsql %}