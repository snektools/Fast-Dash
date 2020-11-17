{% sql 'station_data', connection_string='DRIVER=SQL Server;SERVER=DLNWTSR170;Trusted_Connection=Yes' %}
    SELECT TOP
    {% if top %}
        {{top}}
    {% else %}
        10
    {% endif %}
    *
    FROM [{{database}}].dbo.[{{station}}]
    ORDER BY [TimeStamp] DESC
{% endsql %}