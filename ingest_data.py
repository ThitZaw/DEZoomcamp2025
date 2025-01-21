#!/usr/bin/env python
# coding: utf-8

import os
from sqlalchemy import create_engine

import pandas as pd

from time import time

import argparse

def main(params):

	user = params.user
	password = params.password
	host = params.host
	port = params.port
	db = params.db
	table_name = params.table_name
	# url = params.url

	csv_name = 'yellow_tripdata_2021-01.csv'

	# download the csv
	# os system function can run command line arguments from Python
	# os.system(f"wget {url} -O {csv_name}")
	
	# engine = create_engine('postgresql://root1:root1@localhost:5434/ny_taxi')
	engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

	df_iter = pd.read_csv(csv_name,
						parse_dates=['tpep_pickup_datetime','tpep_dropoff_datetime'],
						iterator=True,chunksize=100000)
	df = next(df_iter)

	#  adding the column names
	df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")

	# adding the first batch of rows
	df.to_sql(name=table_name, con=engine, if_exists="append")

	while True:
		# benchmark time start
		t_start = time()

		# iterates through 100000 chunks of rows
		df = next(df_iter)

		# appends data to existing table
		df.to_sql(name=table_name, con=engine, if_exists="append")

		# benchmark time ends
		t_end = time()

		# prints the time it took to execute the code
		print('Inserted another chunk... took %.3f second(s)' % (t_end - t_start))

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")
	parser.add_argument('--user', help="user name for postgres")
	parser.add_argument('--password', help="password for postgres")
	parser.add_argument('--host', help="host for postgres")
	parser.add_argument('--port', help="port for postgres")
	parser.add_argument('--db', help="database name for postgres")
	parser.add_argument('--table_name', help="name of the table where we will write the results to")
	# parser.add_argument('--url', help="url of the CSV")

	args = parser.parse_args()

	# xprint(args.accumulate(args.integers))

	main(args)


