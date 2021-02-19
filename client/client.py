from flask import Flask, render_template, jsonify, redirect, url_for, request
import json
import requests

#chemin commun dans serveur
URL_API = "http://127.0.0.1:5001/api"



app = Flask(__name__)

@app.route("/")
def accueil():
    return render_template("accueil.html")

# chemin pour données filiere
@app.route("/filiere/<sector>")
def get_filiere(sector):
    url = URL_API + "/filiere/" + sector
    reponse = requests.get(url)
    filiere = json.loads(reponse.content.decode("utf-8"))
    if(len(filiere)==0):
        return render_template("datanotfound.html")
    else:
        return render_template("filiere.html",filiere=filiere)
# chemin pour données region
@app.route("/region/<region>")
def get_region(region):
    url = URL_API + "/region/" + region
    reponse = requests.get(url)
    region = json.loads(reponse.content.decode("utf-8"))
    if(len(region)==0):    
        return render_template("datanotfound.html")
    else:
        return render_template("region.html", region=region)

# chemin pour données filiere et region 
@app.route("/filiereregion/<sector>/<region>")
def get_filiereregion(sector,region):
    url = URL_API + "/filiereregion/" + sector +"/" +region
    reponse = requests.get(url)
    filiereregion = json.loads(reponse.content.decode("utf-8"))
    if(len(filiereregion)==0):
        return render_template("datanotfound.html")
    else:
        return render_template("filiereregion.html", filiereregion=filiereregion)


# chemin pour la conso total pour une filiere
@app.route("/consofiliere/<string:sector>", methods = ("POST","GET"))
def get_consofiliere(sector):
    if request.method =="POST":
        sector = str(request.values.get("conso"))
        url = URL_API + "/consofiliere/" + sector
        reponse = requests.get(url)
        consofiliere = json.loads(reponse.content.decode("utf-8"))
        print(sector)
        return render_template("consofiliere.html", sector=sector, consofiliere=consofiliere[0]['total'])
        

    url = URL_API + "/consofiliere/" + sector
    reponse = requests.get(url)
    consofiliere = json.loads(reponse.content.decode("utf-8"))
    print("après if", sector)
    return render_template("consofiliere.html", consofiliere=consofiliere[0]['total'])
    

# chemin pour la conso total pour une filiere par département
@app.route("/consofiliere_dept/<string:sector>/<string:code_dept>", methods = ("POST","GET"))
def get_consofiliere_dept(sector, code_dept):
    if request.method =="POST":
        sector = str(request.values.get("filiere"))
        code_dept = str(request.values.get("departement"))
        urls = []
        
        if not sector:
            urls.append(URL_API + "/consofiliere_dept/" + "Electricité" + "/" + code_dept)
            urls.append(URL_API + "/consofiliere_dept/" + "Gaz" + "/" + code_dept)
            print("=====apres_if=====")
        else:
            print("=====apres_else=====")
            urls.append(URL_API + "/consofiliere_dept/" + sector + "/" + code_dept)
        
        reponses = []
        for url in urls:
            reponses.append(requests.get(url))
        consofiliere_dept = []
        for reponse in reponses:
            consofiliere_dept.append(json.loads(reponse.content.decode("utf-8")))
        print("==========",consofiliere_dept)

        return render_template("consofiliere_dept.html",sector=sector, code_dept=code_dept, consofiliere_dept=consofiliere_dept)

    url = URL_API + "/consofiliere_dept/" + sector + "/" + code_dept
    reponse = requests.get(url)
    consofiliere_dept = json.loads(reponse.content.decode("utf-8"))
    print("après if", sector)
    return render_template("consofiliere_dept.html", sector=sector, code_dept=code_dept, consofiliere_dept=consofiliere_dept)


# Route qui propose la modification du document
@app.route("/suppression_choix")
def suppression_choix():

    return render_template("suppression.html")


#Suppression d'un document
@app.route("/suppression", methods=["POST"])
def supp_doc():
    data = request.form.to_dict()

    url = URL_API + "/document/delete/" + str(data['id'])
    reponse = requests.delete(url)
    dataPy =json.loads(reponse.content.decode("utf-8"))
    return render_template("test.html", donnee = dataPy)

@app.route("/modification/<string:id>")
def modif_doc(id):
    url = URL_API + "/" + id
    reponse = requests.get(url)
    modif_doc = json.loads(reponse.content.decode("utf-8"))

    modification = {"title":"Modification", "subtitle":"Modifier", "url":url_for('modif_doc', id=id), "operateur":modif_doc['operateur'], "filiere":modif_doc['filiere']}
    return render_template("modification.html", modification=modification)





if __name__ == "__main__" :
    app.run(debug=True, port=5000)