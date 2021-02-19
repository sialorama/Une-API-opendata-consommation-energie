function changerPage(){
    var secteur = document.getElementById('secteur').value;
    var region = document.getElementById('region').value;

    if(secteur && region){
        console.log('secteur et region');
        window.location = 'http://localhost:5000/filiereregion/'+secteur+'/'+region;
    }
    else if (secteur){
        console.log('secteur');
        window.location = 'http://localhost:5000/filiere/'+secteur;
    }
    else if(region){
        console.log('region');
        window.location = 'http://localhost:5000/region/'+region;
    }
   
}