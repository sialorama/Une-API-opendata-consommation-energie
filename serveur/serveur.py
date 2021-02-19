from flask import Flask, render_template, request, jsonify
from data import DataAccess as da

app = Flask(__name__)

# données filière
@app.route("/api/filiere/<string:sector>", methods=['GET'])# methode GET pour récupération des données
def aff_filiere(sector):

    da.connexion()
    data = da.filiere(sector) #[:100]
    da.deconnexion()

    return jsonify(data), 200

#données région
@app.route("/api/region/<int:region>", methods=['GET'])
def aff_region(region:int):
    da.connexion()
    data = da.region(region)
    da.deconnexion()

    return jsonify(data), 200


#code_région
@app.route("/api/code_region/<code_region>", methods=['GET'])
def aff_code_region():
    da.connexion()
    data = da.code_region()
    da.deconnexion()

    return jsonify(data), 200

    
#liste des régions
@app.route("/api/libelle_region/<string:libelle_region>", methods=['GET'])
def get_region(libelle_region:str):
    da.connexion()
    data = da.libelle_region(libelle_region)
    da.deconnexion()

    return jsonify(data), 200


#données pour une filière et une région
@app.route("/api/filiereregion/<string:sector>/<int:region>", methods=['GET'])
def aff_filiere_region(sector, region):

    da.connexion()
    data = da.filiere_region(sector, region)
    da.deconnexion()

    return jsonify(data), 200

# consommation par filiere
@app.route("/api/consofiliere/<sector>", methods=['GET'])
def aff_conso_filiere(sector):
    #sector = "Gaz"
    da.connexion()
    data = da.conso_filiere(sector)
    da.deconnexion()
    return jsonify(data), 200


#suppression de document
@app.route("/api/document/delete/<id>", methods=['DELETE'])
def delete_doc(id):
    da.connexion()
    da.delete_doc(id)
    da.deconnexion()
    return jsonify({"message":"ok"}), 200

@app.route("/api/env/<id>", methods=['DELETE'])
def del_doc(cls, id):
    da.connexion()
    da.delete_doc(id)
    da.deconnexion()
    return jsonify({"message":"document supprimé avec succès"}), 200

#modification operateur et filiere    

@app.route("/api/modification/<int:id>", methods=['PUT'])
def modif_doc(id):
    operateur = request.values.get("operateur")
    filiere = request.values.get("filiere")
    da.connexion()
    da.update_doc(id, operateur, filiere)
    da.deconnexion()
    return jsonify({"message":"ok"}), 200


# consommation d'une filiere par departement
@app.route("/api/consofiliere_dept/<string:sector>/<string:code_dept>", methods=['GET'])
def aff_conso_filiere_dept(sector, code_dept):
    da.connexion()
    print(sector, code_dept)
    data = da.conso_filiere_dept(sector,code_dept)
    da.connexion()
    print(data)
    return jsonify(data), 200


@app.errorhandler(404)
def page_not_found(e):
    return "erreur", 404

if __name__ == "__main__" :
    app.run(debug=True, port=5001)


