# Week 1 - Homework Submission

## Question 1. Knowing docker tags

- Run `docker run --help`

- Which tag has the following text? - Automatically remove the container when it exits

- `--rm`

## Question 2. Understanding docker first run

- Run `docker run -it python:3.9 /bin/bash`

- Check the python modules that are installed (use `pip list`).

- `Wheel` version: `0.42.0`


## Question 3. Count records

- Query

    ```
    SELECT COUNT(*)
    FROM green_trips
    WHERE DATE(lpep_pickup_datetime) = '2019-09-18'
    AND DATE(lpep_pickup_datetime) = '2019-09-18';
    ```

- Result: `15767`


## Question 4. Longest trip for each day

- Query

  ```
  SELECT 
    DATE(lpep_pickup_datetime) AS max_distance_pickup_date
  FROM green_trips
  WHERE trip_distance = (
    SELECT MAX(trip_distance)
    FROM green_trips
  );
  ```

- Result: `2019-09-26`

## Question 5. Three biggest pick up Boroughs


- Query

  ```
  WITH get_borough AS (
    SELECT
      tz."Borough",
      SUM(total_amount) AS total_amount
    FROM
      green_trips AS gt
    LEFT JOIN 
      taxi_zones AS tz ON gt."PULocationID" = tz."LocationID"
    WHERE
      DATE(lpep_pickup_datetime) = '2019-09-18'
      AND tz."Borough" != 'Unknown'
    GROUP BY
      tz."Borough"
  )
  SELECT *
  FROM get_borough
  WHERE total_amount >= 50000
  ORDER BY total_amount DESC;
  ```

- Result

  ```
  "Brooklyn"	96333.23999999932
  "Manhattan"	92271.29999999842
  "Queens"	78671.7099999989
  ```

## Question 6. Largest tip

- Query

  ```
  WITH get_zone AS (
    SELECT
      tzend."Zone" AS dropoff_zone,
      MAX(tip_amount) AS largest_tip
    FROM
      green_trips AS t
      LEFT JOIN taxi_zones AS tzstart ON t."PULocationID" = tzstart."LocationID"
      LEFT JOIN taxi_zones AS tzend ON t."DOLocationID" = tzend."LocationID"
    WHERE
      DATE_TRUNC('month', lpep_pickup_datetime) = '2019-09-01'
      AND tzstart."Zone" = 'Astoria'
    GROUP BY
      dropoff_zone
  )
  SELECT *
  FROM
    get_zone
  ORDER BY
    largest_tip DESC
  LIMIT 1;
  ```

- Result

  ```
  "JFK Airport"	62.31
  ```
