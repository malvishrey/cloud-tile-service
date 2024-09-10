from google.cloud import storage
import pandas as pd

def update_txt_files():
    """Updates text files in GCS bucket."""
    # bucket_name = "your-bucket-name"
    # file_name = "your-file.txt"

    # client = storage.Client()
    # bucket = client.get_bucket(bucket_name)
    # blob = bucket.blob(file_name)

    # data = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    # new_content = data.to_csv(index=False)
    print('triggered sample file successfully')

    # blob.upload_from_string(new_content)
    # print(f"Updated {file_name} in bucket {bucket_name}")

if __name__ == "__main__":
    update_txt_files()
