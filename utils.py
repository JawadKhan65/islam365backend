import shutil
import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

source = r'C:\Users\HP\OneDrive\Desktop\Islam365online\data'
destination = r'D:\PYTHONLEARNING\100MLDays\data\islamic'


def move_data_after_saving():
    try:
        list_of_files = os.listdir(source)
        if len(list_of_files) != 0:
            for file in list_of_files:
                joined = os.path.join(source, file)
                if os.path.exists(os.path.join(destination, file)):
                    print("Already exist")
                else:
                    shutil.move(joined, destination)
            print(f"Moved {len(source)} files. ")
        else:
            print("No files")
    except Exception as e:
        print(f"Error occured: {e}")


def upload_s3():
    s3 = boto3.client('s3')
    bucket_name = 'islamrag-365'
    object_name = 'islamic'
    try:
        data_path = r'C:\Users\HP\OneDrive\Desktop\Islam365online\data'
        response = s3.list_buckets()

        print('Existing buckets:')
        for bucket in response['Buckets']:
            print(f'  {bucket["Name"]}')

        list_of_files = os.listdir(
            r'C:\Users\HP\OneDrive\Desktop\Islam365online\data')

        for file in list_of_files:
            joined_path = os.path.join(data_path, file)
            if os.path.isfile(joined_path):
                s3.upload_file(joined_path, bucket_name, object_name)
                print(f"Uploaded {file} to S3 bucket")

    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Error occured: {e}")


if __name__ == '__main__':
    # move_data_after_saving()
    print("ADD SOME FUNCTIONS")
