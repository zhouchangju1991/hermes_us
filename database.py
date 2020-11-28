import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import config

class Database:
    def __init__(self):
        # fetch credential from the private key and get database instance.
        cred = credentials.Certificate(config.service_credential_file_name)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def udpate_product_to_database(self, product, merge):
        self.update_document('hermes_us_product', product['sku'], product, merge)

    def update_document(self, collection_name, document_name, data, merge):
        if merge:
            self.document(collection_name, document_name).update(data)
        else:
            self.document(collection_name, document_name).set(data)

    def collection(self, collection_name):
        return self.db.collection(collection_name)

    def document(self, collection_name, document_name):
        return self.collection(collection_name).document(document_name)
