from flask import Flask, jsonify, render_template, url_for, request, redirect
import json
import os
import glob
from models import PredictRawVeggies
#from bson import json_util
# import app
#from app import app
# from app import retrieve_population_data
#from app import models


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Uploads'
my_pred = PredictRawVeggies()


# # Define routes ###############################################################
@app.route("/",  methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.files.get('file'):
#
            images = request.files.getlist("file") #convert multidict to dict
            # Remove all the files
            files = glob.glob(app.config['UPLOAD_FOLDER']+'/*')
            print(files)
            for f in files:
                os.remove(f)

            #save the image
            for image in images:     #image will be the key
                # create a path to the uploads folder
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                image.save(filepath)
                print(filepath)
        return ('', 204)
    print(my_pred.labels)
    return render_template('index.html')

#####################################################################################
@app.route('/update', methods=['POST'])
def update():

    print(my_pred.labels)
    # get the list
    filenames = []
    image_names = request.form.getlist('image[]')

    if (image_names == []):
        filenames = ["No Images to predict"]
        print("No Images to predict")
    else:
        for image_name in image_names:
            filenames.append(image_name.split('\\')[-1:][0])

        predictions = my_pred.call_predict(filenames, app.config['UPLOAD_FOLDER'])
        print(f"predictions : {predictions}")
    # print(filenames)

    return jsonify({'result': 'success', 'predictions': predictions})


# Define routes ###############################################################
# @app.route("/", methods=['GET', 'POST'])
# def upload_file():
#     data = {"success": False}
#     if request.method == 'POST':
#         print("In post")
#         print("-------------------------------------")
#
#         if request.files.get('file'):
#
#             images = request.files.getlist("file") #convert multidict to dict
#             for image in images:     #image will be the key
#
#                 # create a path to the uploads folder
#                 filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
#                 image.save(filepath)
#                 print(filepath)
#
#         return ("", 204) #redirect(url_for('upload_file'))
#     return render_template('index.html')


# ###########################################################################
# ###########################################################################

if __name__ == '__main__':
    app.run(debug=True)
