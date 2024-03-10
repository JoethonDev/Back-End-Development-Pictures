from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    images_list = []
    for img in data :
        images_list.append({'pic_url' : img['pic_url']})
    
    if images_list:
        return images_list, 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################
# pytest -k 'test_health or test_count or test_data_contains_10_pictures or test_get_picture or test_get_pictures_check_content_type_equals_json or test_pictures_json_is_not_empty or test_post_picture or test_post_picture_duplicate or test_update_picture_by_id'

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    image = None
    for img in data :
        if id == img['id'] :
            image = img
            break
    
    if image:
        return image, 200

    return {"message": "picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    incoming_data = request.json
    incoming_id = incoming_data['id']

    for image in data :
        if incoming_id == image['id']:
            return {"Message": f"picture with id {image['id']} already present"}, 302
    
    data.append(incoming_data)
    # with open(json_url, 'w') as pictures_file :
    #    json.dump(data, pictures_file, indent=2)

    
    return incoming_data, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    incoming_data = request.json

    for index, image in enumerate(data) :
        if id == image['id']:
            data[index] = incoming_data
            return image, 200
    
    return {"message": "picture not found"}, 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for index, image in enumerate(data) :
        if id == image['id']:
            del data[index]
            return "", 204
    
    return {"message": "picture not found"}, 404
