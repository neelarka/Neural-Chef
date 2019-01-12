
from flask import Flask, jsonify, render_template, url_for, request, redirect
import json
import os
import glob
from models import PredictRawVeggies
import pandas as pd
from recipes import getRecipes, getdict, getLinksFromcsv
from random import shuffle

# import app
#from app import app
# from app import retrieve_population_data
#from app import models


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
my_pred = PredictRawVeggies()


# # Define routes ###############################################################
@app.route("/",  methods=['GET', 'POST'])
def index():
    print("upload click")
    if request.method == 'POST':
        if request.files.get('file'):
#
            images = request.files.getlist("file") #convert multidict to dict
            print(f"Images: {images}")
            # Remove all the files
            files = glob.glob(app.config['UPLOAD_FOLDER']+'/*')
            # print(files)
            for f in files:
                os.remove(f)

            filenames = []
            #save the image
            for image in images:     #image will be the key
                # create a path to the uploads folder
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                image.save(filepath)
                filenames.append(image.filename)
                print(filenames)

            predictions = my_pred.call_predict(filenames, app.config['UPLOAD_FOLDER'])

        return jsonify({'result': 'success', 'predictions': predictions})
    else:
        # Get the cusines from the file list
        cuisines_list = glob.glob("recipes/*.csv")
        print(cuisines_list)
        cuisines_df = pd.read_csv(cuisines_list[0])

        print(list(cuisines_df))

    return render_template('index.html', cuisines = list(cuisines_df)[1:])

#####################################################################################
# Define routes ###############################################################
@app.route("/find_recipe", methods=['POST'])
def find_recipe():
    data = {"success": False}
    if request.method == 'POST':
        print("find_recipe")
        print("-------------------------------------")
        data = request.get_json()
        ingredients = data['ingredients']
        cuisine = data['cuisine']
        #Get the links
        recipe_links = getLinksFromcsv(cuisine, ingredients)
        shuffle(recipe_links)
        print(recipe_links)

        #fine the recepies
        recipes_list = getRecipes(recipe_links[0:2]);
        #if any recipe found retun success
        for recipe in recipes_list:
            if bool(recipe):
                return jsonify({'data': render_template('recipes.html', object_list=recipes_list)})

        return json.dumps({ "error": "Cannot find the recipe" }), 500

# ###########################################################################
# ###########################################################################

if __name__ == '__main__':
    app.run(debug=True)
