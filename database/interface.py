import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class FirebaseInterface:

    def __init__(self):
        self.db = firestore.client()

    def addData(self, data, collection, document):
        doc_ref = self.db.collection(collection).document(document)
        doc_ref.set(data)

    def getData(self, collection, document=None):
        if document:
            data_ref = self.db.collection(collection).document(document)
            doc = data_ref.get()
            result = doc.to_dict()
        else:
            data_ref = self.db.collection(collection)
            docs = data_ref.get()
            result = []
            for doc in docs:
                result.append(doc.to_dict())

        return result
