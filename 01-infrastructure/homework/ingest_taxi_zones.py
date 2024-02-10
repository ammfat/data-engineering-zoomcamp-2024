import argparse
import os
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
        csv_name = "taxi_zones.csv.gz"
    else:
        csv_name = "taxi_zones.csv"

    # Download dataset
    os.system(f"wget {url} -O {csv_name}")

    # Create Engine
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    conn = engine.connect()

    # Load into PG
    df = pd.read_csv(csv_name)
    df.to_sql(name=table, con=conn, if_exists="replace", index=False)


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

"""
python3 ingest_taxi_zones.py \
    --user ammfat \
    --password ammfat \
    --host localhost \
    --port 5432 \
    --db taxi_trips \
    --table taxi_zones \
    --url https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv
 """
