from google.cloud import storage
import config

log_bucket_name = 'nanazhou_hermes_us_log'

class Storage:
    def __init__(self):
        self.__client = storage.Client.from_service_account_json(config.service_credential_file_name)
    
    def upload(self, bucket_name, source_file_name, destination_file_name):
        bucket = self.__client.bucket(bucket_name)
        destination = bucket.blob(destination_file_name)
        destination.upload_from_filename(source_file_name)

    def upload_log(self, source_file_name, destination_file_name):
        self.upload(log_bucket_name, source_file_name, destination_file_name)

    def delete(self, bucket_name, blob_name):
        blob = self.__client.bucket(bucket_name).blob(blob_name)
        blob.delete()

    def delete_log(self, log_name):
        self.delete(log_bucket_name, log_name)

    def list_logs(self):
        return self.__client.list_blobs(log_bucket_name)
