import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class FirebaseInterface:

    def __init__(self):
        self.db = firestore.client()

    def addData(self, data, collection, document=None):
        doc_ref = self.db.collection(collection).document(document)
        data['id'] = doc_ref.id
        doc_ref.set(data)

    def updateData(self, data, collection, document=None):
        doc_ref = self.db.collection(collection).document(document)
        doc_ref.update(data)

    def setData(self, data, collection, document=None):
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

    def deleteData(self, collection, document):
        doc_ref = self.db.collection(collection).document(document)
        doc_ref.delete()

    def deleteItemFromArray(self, collection, document, field, data):
        doc_ref = self.db.collection(collection).document(document)
        doc_ref.update({
            field: firestore.firestore.ArrayRemove([data])
        })

    def addItemToArray(self, collection, document, field, data):
        doc_ref = self.db.collection(collection).document(document)
        doc_ref.update({
            field: firestore.firestore.ArrayUnion([data])
        })

    def getDataByField(self, collection, field, data):
        doc_ref = self.db.collection(collection).where(field, '==', data)
        docs = doc_ref.get()
        result = []

        for doc in docs:
            result.append(doc.to_dict())

        return result

    def getDataByTwoFields(self, collection, field, data, second_field, second_data):
        doc_ref = self.db.collection(collection).where(field, '==', data).where(second_field, '==', second_data)
        docs = doc_ref.get()
        result = []

        for doc in docs:
            result.append(doc.to_dict())

        return result
