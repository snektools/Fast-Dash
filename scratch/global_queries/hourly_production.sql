
-- Query parameters example:
params = {'shift_1_start': '06:45:00',
          'shift_2_start': '14:45:00',
          'shift_3_start': '22:45:00',
          'hour_ends_on_min':  '45',
          'end_date':      datetime.datetime.now().replace(microsecond=0),
          'start_date':    datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(days=3),
          'db_table':      'BMW2.dbo.View_Station151',
          'server':        'DLNWTSR140',
          }


{% sql 'hourly_production', note='Counts output by Shift/Hour and GKNdate assumes 3rd shift crosses midnight' %}
WITH Filter_Data AS

(
	SELECT
		*
		,ROW_NUMBER() OVER(PARTITION BY [Database ID] ORDER BY Timestamp) AS RowNum
	FROM {{ db_table }}
)

SELECT
	   [GKNDate]
	  ,[Shift]
	  ,[Hour_Bin]
	  ,COUNT([Database ID]) [Count]

FROM(
	SELECT _Offload.*,
	CASE WHEN (CONVERT(CHAR(8), Timestamp, 114) between '{{ shift_1_start|guards.regexp('^\d{2}:\d{2}:\d{2}$') }}' AND '{{ shift_2_start }}')        THEN '1'
         WHEN (CONVERT(CHAR(8), Timestamp, 114) between '{{ shift_2_start|guards.regexp('^\d{2}:\d{2}:\d{2}$') }}' AND '{{ shift_3_start }}')        THEN '2'
		 WHEN (CONVERT(CHAR(8), Timestamp, 114) between '{{ shift_3_start|guards.regexp('^\d{2}:\d{2}:\d{2}$') }}' AND '24:00:00')                   THEN '3'
		 WHEN (CONVERT(CHAR(8), Timestamp, 114) between '00:00:00'                                                 AND '{{ shift_1_start }}')        THEN '3'
				END AS [Shift]

   ,CASE WHEN (CONVERT(CHAR(8), Timestamp, 114) between '{{ shift_1_start }}' AND '{{ shift_2_start }}')        THEN convert(varchar, CAST(TimeStamp AS DATE), 1)
         WHEN (CONVERT(CHAR(8), Timestamp, 114) between '{{ shift_2_start }}' AND '{{ shift_3_start }}')        THEN convert(varchar, CAST(TimeStamp AS DATE), 1)
		 WHEN (CONVERT(CHAR(8), Timestamp, 114) between '{{ shift_3_start }}' AND '24:00:00')                   THEN convert(varchar, CAST(DATEADD(DAY, 1, TimeStamp) AS DATE), 1)
		 WHEN (CONVERT(CHAR(8), Timestamp, 114) between '00:00:00' AND '{{ shift_1_start }}')                   THEN convert(varchar, CAST(TimeStamp AS DATE), 1)
		 		END AS [GKNDate]

   ,CASE WHEN (RIGHT(CONVERT(CHAR(8), Timestamp, 114),5) between '{{ hour_ends_on_min|guards.regexp('^\d{2}$') }}' + ':00:00' and '60:00:00')    THEN RIGHT('0' + convert(varchar,DATEPART(HOUR, DATEADD(HOUR, 0,Timestamp))),2) + ':' + '{{ hour_ends_on_min }}'
		 WHEN (RIGHT(CONVERT(CHAR(8), Timestamp, 114),5) between '00:00:00' and '{{ hour_ends_on_min }}' + ':00:00')                             THEN RIGHT('0' + convert(varchar,DATEPART(HOUR, DATEADD(HOUR, -1,Timestamp))),2)+ ':' + '{{ hour_ends_on_min }}'
		  		END AS [Hour_Bin]

    FROM Filter_Data _Offload
) _Offload

where TimeStamp BETWEEN {{ start_date|guards.datetime }} AND {{ end_date|guards.datetime }}

  GROUP by [GKNDate] ,[Shift],[Hour_Bin]
  ORDER by [GKNDate] desc,
		CASE [Shift]
			WHEN 3 THEN 3
			WHEN 1 THEN 2
			WHEN 2 THEN 1
			ELSE 4 END
	   ,CASE [Hour_Bin]
			WHEN '0:' +  '{{ hour_ends_on_min }}' THEN  24
			WHEN '1:' +  '{{ hour_ends_on_min }}' THEN  23
			WHEN '2:' +  '{{ hour_ends_on_min }}' THEN  22
			WHEN '3:' +  '{{ hour_ends_on_min }}' THEN  21
			WHEN '4:' +  '{{ hour_ends_on_min }}' THEN  20
			WHEN '5:' +  '{{ hour_ends_on_min }}' THEN  19
			WHEN '6:' +  '{{ hour_ends_on_min }}' THEN  18
			WHEN '7:' +  '{{ hour_ends_on_min }}' THEN  17
			WHEN '8:' +  '{{ hour_ends_on_min }}' THEN  16
			WHEN '9:' +  '{{ hour_ends_on_min }}' THEN  15
			WHEN '10:' + '{{ hour_ends_on_min }}' THEN  14
			WHEN '11:' + '{{ hour_ends_on_min }}' THEN  13
			WHEN '12:' + '{{ hour_ends_on_min }}' THEN  12
			WHEN '13:' + '{{ hour_ends_on_min }}' THEN  11
			WHEN '14:' + '{{ hour_ends_on_min }}' THEN  10
			WHEN '15:' + '{{ hour_ends_on_min }}' THEN   9
			WHEN '16:' + '{{ hour_ends_on_min }}' THEN   8
			WHEN '17:' + '{{ hour_ends_on_min }}' THEN   7
			WHEN '18:' + '{{ hour_ends_on_min }}' THEN   6
			WHEN '19:' + '{{ hour_ends_on_min }}' THEN   5
			WHEN '20:' + '{{ hour_ends_on_min }}' THEN   4
			WHEN '21:' + '{{ hour_ends_on_min }}' THEN   3
			WHEN '22:' + '{{ hour_ends_on_min }}' THEN  26
			WHEN '23:' + '{{ hour_ends_on_min }}' THEN  25
			ELSE 25	END
{% endsql %}