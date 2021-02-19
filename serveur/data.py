from pymongo import MongoClient
import pprint
from bson.objectid import ObjectId # représenter du json en binaire 


class DataAccess :
    size = 0

    @classmethod
    def connexion(cls) :
        cls.client = MongoClient()
        cls.db = cls.client['conso']
        #collection = cls.db.energie

    @classmethod #les données pour une filière (soit gaz, soit électricité)
    def filiere(cls, sector):
        data = cls.db.energie.aggregate([{"$match":{"fields.filiere":sector}},{"$unset":"_id"}])
        return list(data)

    @classmethod #les données pour une région
    def region(cls,region):
        data = cls.db.energie.aggregate([{"$match":{"fields.code_region":region}},{"$unset":"_id"}])
        return list(data)

    @classmethod # les données pour une filière et une région 
    def filiere_region(cls, sector, region):
        data = cls.db.energie.aggregate([{"$match":{"fields.filiere":sector,"fields.code_region":region}}, { "$sort" : { "fields.code_region":1}},{"$unset":"_id"}])
        return list(data)

    @classmethod  #la consommation total pour une filière,
    def conso_filiere(cls, sector):
        data = cls.db.energie.aggregate([{"$match":{"fields.filiere":sector}}, {"$group":{"_id":"null", "total" : { "$sum" : "$fields.conso"}}}])
        return list(data)


    
    @classmethod# modifier un document précis
    def update_doc(cls, id, operateur, filiere):
        doc = {"filiere":filiere, "operateur":operateur}
        cls.db.energie.update_one({"_id":id}, {'$set':doc})
        return data

    @classmethod # supprimer un document précis
    def delete_doc(cls, id):
        cls.db.energie.delete_one({'_id': ObjectId(id)})

    @classmethod # recherhcher un document précis
    def get_doc(cls, id):
        data = cls.db.energie.find_one({'_id': ObjectId(id)})
        return data
        

    
    @classmethod  #la consommation d'une filière pour un département
    def conso_filiere_dept(cls,filiere,code_dept):

        filiere = str(filiere)
        code_dept = str(code_dept)
        
        data = cls.db.energie.aggregate([{'$match':{"fields.filiere":filiere,"fields.code_departement":code_dept}},
                                    {"$group": {"_id" :(code_dept,filiere), "total": { "$sum": "$fields.conso" }}}])# on force à ce que l'id soit le code departement
        
        return list(data)
        
    @classmethod
    def deconnexion(cls) :
        cls.client.close()
