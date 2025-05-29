import os
import urllib.request
import gzip
import shutil
from concurrent.futures import ThreadPoolExecutor
from google.cloud import storage
import time

# Change this to your bucket name
BUCKET_NAME = "green_trip_data_dezoomcamp_w4"

# If you authenticated through the GCP SDK you can comment out these two lines
CREDENTIALS_FILE = "week_3/keys/gcs.json"
client = storage.Client.from_service_account_json(CREDENTIALS_FILE)

BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-"
MONTHS = [f"{i:02d}" for i in range(1, 13)]
DOWNLOAD_DIR = "."
CHUNK_SIZE = 8 * 1024 * 1024

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

bucket = client.bucket(BUCKET_NAME)

def download_file(month):
    gz_file_path = os.path.join(DOWNLOAD_DIR, f"green_tripdata_2020-{month}.csv.gz")
    print("gz_file_path ------"+gz_file_path)
    csv_file_path = gz_file_path.replace(".csv.gz", ".csv")
    print("csv_file_path --------"+csv_file_path)
    url = f"{BASE_URL}{month}.csv.gz"

    try:
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, gz_file_path)
        print(f"Downloaded: {gz_file_path}")

        # Extract the .csv.gz file
        with gzip.open(gz_file_path, 'rb') as f_in:
            with open(csv_file_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"Extracted: {csv_file_path}")

        os.remove(gz_file_path)  # Delete .csv.gz to save space
        print(f"Deleted: {gz_file_path}")
        
        return csv_file_path
    except Exception as e:
        print(f"Failed to process {url}: {e}")
        return None

def upload_to_gcs(file_path, max_retries=3):
    blob_name = os.path.basename(file_path)
    blob = bucket.blob(blob_name)
    blob.chunk_size = CHUNK_SIZE  
    
    for attempt in range(max_retries):
        try:
            print(f"Uploading {file_path} to {BUCKET_NAME} (Attempt {attempt + 1})...")
            blob.upload_from_filename(file_path)
            print(f"Uploaded: gs://{BUCKET_NAME}/{blob_name}")
            return
        except Exception as e:
            print(f"Failed to upload {file_path} to GCS: {e}")
        
        time.sleep(5)  
    
    print(f"Giving up on {file_path} after {max_retries} attempts.")

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as executor:
        csv_file_paths = list(executor.map(download_file, MONTHS))

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(upload_to_gcs, filter(None, csv_file_paths))  # Remove None values

    print("All files processed and uploaded.")
