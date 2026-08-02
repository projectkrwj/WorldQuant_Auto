from database.database import Database
from parameters import DEFAULT_SETTINGS
import time
DATASET_URL = "https://api.worldquantbrain.com/data-sets"
FIELD_URL = "https://api.worldquantbrain.com/data-fields"

def update_datasets(session):

    db = Database()

    db.create_tables()
    
    offset = 0
    limit = 20

    while True:

        response = session.get(
            DATASET_URL,
            params={
                "delay": DEFAULT_SETTINGS["delay"],
                "instrumentType": DEFAULT_SETTINGS["instrumentType"],
                "limit": limit,
                "offset": offset,
                "region": DEFAULT_SETTINGS["region"],
                "universe": DEFAULT_SETTINGS["universe"]
            }
        )

        response.raise_for_status()

        data = response.json()

        rows = []

        for dataset in data["results"]:

            rows.append((
                dataset["id"],
                dataset["name"],
                dataset["description"],
                dataset["category"]["id"],
                dataset["category"]["name"],
                dataset["subcategory"]["id"],
                dataset["subcategory"]["name"]
            ))

        if rows:
            print(f"저장할 rows: {len(rows)}")
            db.insert_datasets(rows)

        offset += limit

        time.sleep(1.5)

        if offset >= data["count"]:
            break

    db.close()


def update_fields(session, dataset_id):

    db = Database()
    db.create_tables()

    offset = 0
    limit = 20

    while True:

        response = session.get(
            FIELD_URL,
            params={
                "dataset.id": dataset_id,
                "delay": DEFAULT_SETTINGS["delay"],
                "instrumentType": DEFAULT_SETTINGS["instrumentType"],
                "region": DEFAULT_SETTINGS["region"],
                "universe": DEFAULT_SETTINGS["universe"],
                "limit": limit,
                "offset": offset
            }
        )

        response.raise_for_status()

        data = response.json()

        rows = []

        for field in data["results"]:

            rows.append((
                field["id"],
                field["dataset"]["id"],
                field["region"],
                field["type"],
                field["category"]["id"],
                field["category"]["name"],
                field["description"]
            ))

        if rows:
            db.insert_fields(rows)

        offset += limit
        time.sleep(1.5)

        if offset >= data["count"]:
            break

    db.close()


def update_all_fields(session):

    db = Database()

    db.cursor.execute("SELECT id FROM datasets")

    dataset_ids = [row[0] for row in db.cursor.fetchall()]

    db.close()

    for dataset_id in dataset_ids:

        print(f"Updating {dataset_id}")

        update_fields(session, dataset_id)