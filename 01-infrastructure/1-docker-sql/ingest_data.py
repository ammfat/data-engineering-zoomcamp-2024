import argparse
import os
from time import time
import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table = params.table
    url = params.url

    if url.endswith(".csv.gz"):
        csv_name = "output.csv.gz"
    else:
        csv_name = "output.csv"

    # Download dataset
    os.system(f"wget {url} -O {csv_name}")

    # Create Engine
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    engine.connect()

    # Load into PG
    # # Chunking Dataframe
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df = next(df_iter)

    # # Transform Datetime
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # # Create PG Table from Dataset Header
    df.head(n=0).to_sql(name=table, con=engine, if_exists="replace")
    df.to_sql(name=table, con=engine, if_exists="append")

    # # Load the Data
    while True:
        try:
            t_start = time()

            df = next(df_iter)
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            df.to_sql(name=table, con=engine, if_exists="append")

            t_end = time()

            print("inserted another chunk, took %.3f second" % (t_end - t_start))
        except StopIteration:
            print("Finished ingesting data into PostgreSQL")
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV into PostgreSQL")

    parser.add_argument(
        "--user", type=str, help="Username for the database", required=True
    )
    parser.add_argument(
        "--password", type=str, help="Password for the database", required=True
    )
    parser.add_argument("--host", type=str, help="Host for the database", required=True)
    parser.add_argument("--port", type=str, help="Port for the database", required=True)
    parser.add_argument("--db", type=str, help="Database name", required=True)
    parser.add_argument("--table", type=str, help="Table name", required=True)
    parser.add_argument("--url", type=str, help="URL for the CSV", required=True)

    args = parser.parse_args()
    main(args)
