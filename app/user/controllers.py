from flask import Blueprint, request, session, jsonify, render_template, redirect, Response
import os
from sqlalchemy.exc import IntegrityError
from app import db, UPLOAD_FOLDER#, logout_required, login_manager, load_user
import app
from werkzeug.utils import secure_filename
import re
import pathlib
from app.scenedetect import sd
from app.facedetect import fd
from app.KNN import KNN
import pickle

mod_user = Blueprint('mod_user', __name__, url_prefix="")
ALLOWED_EXTENSIONS = set(['mp4', 'png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@mod_user.route("/upload_photos", methods=["POST"])
def upload_photos():
    file = request.files['file']
    print(file.filename)
    if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        dr = 'server/dataset/' + filename.split('_')[0] + '/'
        pathlib.Path(dr).mkdir(parents=True, exist_ok=True) 
        file.save(dr + filename.split('_')[1])
    return jsonify({"success":"success"})

@mod_user.route("/prepareKNN", methods=["POST"])
def prepare_KNN():
    print("reached here!!")
    KNN.train_on_dataset()
    return jsonify({"success":"success"})

@mod_user.route("/upload_video", methods=["POST"])
def upload_video():
    file = request.files['file']
    print(file.filename)
    if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        dr = 'server/video/'
        pathlib.Path(dr).mkdir(parents=True, exist_ok=True) 
        file.save(dr + 'video.' + filename.split('.')[-1])
    return jsonify({"success":"success"})

@mod_user.route("/detect_faces", methods=["POST"])
def detect_faces():
    with open('scene_people.pkl', 'rb') as f:
        scene_people =  pickle.load(f)
    with open('scenes.pkl', 'rb') as f:
        scenes = pickle.load(f)
    with open('faces.pkl', 'rb') as f:
        faces = pickle.load(f)

    fd.display(scenes, faces, scene_people)
    return jsonify({"success":"success"})

    scenes = sd.detect(dr + 'video.' + filename.split('.')[-1])
    faces = fd.facedetection(dr + 'video.mp4', scenes)
    scene_people = KNN.test_on_dataset(faces)
    with open('scene_people.pkl', 'wb') as f:
        pickle.dump(scene_people, f)
    with open('scenes.pkl', 'wb') as f:
        pickle.dump(scenes, f)
    with open('faces.pkl', 'wb') as f:
        pickle.dump(faces, f)
    return jsonify({"success":"success"})
