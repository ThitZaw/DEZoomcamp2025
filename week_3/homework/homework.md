#### create external table

```sql
CREATE OR REPLACE EXTERNAL TABLE `sacred-dahlia-449815-m5.nytaxi.fhv_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dezoomcamp_hw3_sacred_dehlia/yellow_tripdata_2024-*.parquet']
);
```

#### create materialized table

```sql
CREATE OR REPLACE TABLE `sacred-dahlia-449815-m5.nytaxi.fhv_nonpartitioned_tripdata`
AS SELECT * FROM `sacred-dahlia-449815-m5.nytaxi.fhv_tripdata`;
```

#### Question -1

```sql
SELECT COUNT(DISTINCT(PULocationID)) FROM `sacred-dahlia-449815-m5.nytaxi.fhv_tripdata`
```


### Question - 2

```sql
SELECT COUNT(DISTINCT(PULocationID)) FROM `sacred-dahlia-449815-m5.nytaxi.fhv_tripdata`
```
![hw_q2_external.png](https://github.com/ThitZaw/DEZoomcamp2025/blob/main/week_3/homework/hw_q2_external.png)


```sql
SELECT COUNT(DISTINCT(PULocationID)) FROM `sacred-dahlia-449815-m5.nytaxi.fhv_nonpartitioned_tripdata`
```
![hw_q2_materialized.png](https://github.com/ThitZaw/DEZoomcamp2025/blob/main/week_3/homework/hw_q2_materialized.png)


### Question -3
retrieve the PULocationID from the table (not the external table)
```sql
SELECT PULocationID FROM `sacred-dahlia-449815-m5.nytaxi.fhv_nonpartitioned_tripdata`
```

retrieve the PULocationID and DOLocationID from the table (not the external table)
```sql
SELECT PULocationID,DOLocationID FROM `sacred-dahlia-449815-m5.nytaxi.fhv_nonpartitioned_tripdata`
```
![hw_q3.png](https://github.com/ThitZaw/DEZoomcamp2025/blob/main/week_3/homework/hw_q3.png)

#### Question - 4
```sql
SELECT COUNT(fare_amount) 
FROM `sacred-dahlia-449815-m5.nytaxi.fhv_tripdata`
WHERE fare_amount = 0
```
![hw_q4.png](https://github.com/ThitZaw/DEZoomcamp2025/blob/main/week_3/homework/hw_q4.png)

#### Question - 5 - create partation table
```sql
CREATE OR REPLACE TABLE `sacred-dahlia-449815-m5.nytaxi.fhv_partitioned_tripdata`
PARTITION BY DATE(dropoff_datetime)
CLUSTER BY dispatching_base_num AS (
  SELECT * FROM `sacred-dahlia-449815-m5.nytaxi.fhv_tripdata`
);
```

#### Question - 6 

```sql
SELECT DISTINCT(VendorID)
FROM `sacred-dahlia-449815-m5.nytaxi.fhv_nonpartitioned_tripdata`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';
```
![hw_q6_nonpartationed.png](https://github.com/ThitZaw/DEZoomcamp2025/blob/main/week_3/homework/hw_q6_nonpartationed.png)

```sql
SELECT distinct(VendorID) FROM `sacred-dahlia-449815-m5.nytaxi.fhv_partitioned_tripdata` 
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';
```
![hw_q6_partationed.png](https://github.com/ThitZaw/DEZoomcamp2025/blob/main/week_3/homework/hw_q6_partationed.png)
