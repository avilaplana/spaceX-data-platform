## Problem - Part 4: SQL Queries

- Write an SQL query to find the maximum number of times a core has been reused.

```
SELECT MAX(reuse_count) as max_reused_core FROM dim_core;
```
with the following result:
```
 max_reused_core 
-----------------
              13
(1 row)
```

or 

```
SELECT (COUNT(core_id) - 1) as max_reused_core 
FROM bridge_launch_core 
GROUP BY core_id 
ORDER BY max_reused_core 
DESC LIMIT 1;
``` 
with the following result:
```
 max_reused_core 
-----------------
              13
(1 row)
```

- Write an SQL query to find the cores that have been reused in less than 50 days after the previous
launch.

```
WITH core_launches AS (
    SELECT
        blc.core_id,
        DATE(fl.date_utc) AS launch_date,
        ROW_NUMBER() OVER (PARTITION BY blc.core_id ORDER BY DATE(fl.date_utc)) AS rn
    FROM
        bridge_launch_core blc
    JOIN fact_launches fl ON fl.id = blc.launch_id
),
core_launch_pairs AS (
    SELECT
        curr.core_id,
        curr.launch_date AS current_launch,
        prev.launch_date AS previous_launch,
        curr.launch_date - prev.launch_date AS days_between
    FROM
        core_launches curr
    JOIN core_launches prev
        ON curr.core_id = prev.core_id
        AND curr.rn = prev.rn + 1
)
SELECT
    core_id,
    previous_launch,
    current_launch,
    days_between
FROM
    core_launch_pairs
WHERE
    days_between < 50
ORDER BY
    core_id,
    current_launch;
```  

with the following result:

```
 core_id | previous_launch | current_launch | days_between 
---------+-----------------+----------------+--------------
      58 | 2020-12-13      | 2021-01-20     |           38
      59 | 2022-01-31      | 2022-03-09     |           37
      59 | 2022-08-04      | 2022-09-05     |           32
      65 | 2020-12-06      | 2021-01-24     |           49
      65 | 2021-01-24      | 2021-03-11     |           46
      65 | 2021-03-11      | 2021-04-07     |           27
      65 | 2021-04-07      | 2021-05-15     |           38
      65 | 2022-01-13      | 2022-02-21     |           39
      66 | 2021-01-08      | 2021-02-04     |           27
      66 | 2021-02-04      | 2021-03-24     |           48
      66 | 2021-03-24      | 2021-04-29     |           36
      66 | 2021-12-01      | 2022-01-19     |           49
      66 | 2022-01-19      | 2022-03-03     |           43
      66 | 2022-03-03      | 2022-04-21     |           49
      66 | 2022-04-21      | 2022-06-01     |           41
      67 | 2021-04-23      | 2021-06-06     |           44
      67 | 2022-05-25      | 2022-06-19     |           25
      68 | 2022-04-08      | 2022-04-29     |           21
      68 | 2022-04-29      | 2022-06-08     |           40
      68 | 2022-06-08      | 2022-07-24     |           46
      68 | 2022-07-24      | 2022-08-19     |           26
      73 | 2021-11-11      | 2021-12-19     |           38
      77 | 2022-06-18      | 2022-07-21     |           33
      79 | 2022-05-14      | 2022-06-29     |           46
      79 | 2022-06-29      | 2022-08-09     |           41
(25 rows)
```
