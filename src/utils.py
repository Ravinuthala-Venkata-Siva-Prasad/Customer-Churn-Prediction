import os 
import json
import joblib

def create_directories(paths):
    for path in paths:
        os.makedirs(path,exist_ok=True)

def save_object(file_path,obj):
    os.makedirs(os.path.dirname(file_path),exist_ok=True)
    joblib.dump(obj,file_path)

def load_object(file_path):
    return joblib.load(file_path)

def save_json(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path,"w") as file:
        json.dump(data,file,indent=4)

def load_json(file_path):
    with open(file_path,"r") as file:
        return json.load(file)