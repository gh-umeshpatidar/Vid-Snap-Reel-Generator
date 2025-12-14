from flask import Flask, render_template, request, jsonify
import uuid
import random
from werkzeug.utils import secure_filename
import os
import generate_process
import shutil

os.makedirs('user_upload', exist_ok=True)

UPLOAD_FOLDER = 'user_upload'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg','mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def home():
    folder = "static/projectimages" 
    images = os.listdir(folder)      
    images = [img for img in images if img.endswith((".jpg", ".png", ".jpeg"))]
    selected_images = random.sample(images, min(4, len(images)))
    return render_template("index.html", images=selected_images)

@app.route("/create", methods = ["GET","POST"])
def create():
    my_id = uuid.uuid1()
    if request.method == "POST":
         req_id = request.form.get("uuid")
         desc =  request.form.get("text")
         input_files = []
         for key,value in request.files.items():
        # Get Uplaoded the files
            file = request.files[key]
            # Get Uploaded the image           
            if file:
                    filename = secure_filename(file.filename)
                    if(not(os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], req_id)))):
                          os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], req_id))               
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], req_id, filename))
                    input_files.append(file.filename)
        # Get Uploaded the text
         with open(os.path.join(app.config['UPLOAD_FOLDER'], req_id, "desc.txt"),"w") as f:
                f.write(desc)
         
         input_audio = [aud for aud in input_files if aud.endswith((".mp3"))]
        #  #Get Uploaded the audio
         if input_audio :
                with open(os.path.join(app.config['UPLOAD_FOLDER'], req_id, "audio.txt"),"w") as f:
                    f.write(input_audio[0])
         
         input_images = [img for img in input_files if img.endswith((".jpg", ".png", ".jpeg"))]
         if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], req_id, "input.txt")):
                with open(os.path.join(app.config['UPLOAD_FOLDER'], req_id, "input.txt"), "w") as f:
                        f.write("") 
         for f1 in input_images:                
                with open(os.path.join(app.config['UPLOAD_FOLDER'],req_id,"input.txt"),"a") as f:
                   f.write(f"file '{f1}'\nduration 1\n")
        
         generate_process.run_task()
                
    return render_template("create.html",myid = my_id)
    

@app.route("/gallery")
def gallery():
    folder = "static/projectimages"  
    images = os.listdir(folder)
    print(folder)       
    images = [img for img in images if img.endswith((".jpg", ".png", ".jpeg"))]
    selected_images = random.sample(images, min(4, len(images)))
    reels = os.listdir("static/reels")
    return render_template("gallery.html", reels= reels,images=selected_images)

SOURCE_FOLDER = "static/reels"
DEST_FOLDER = r"C:\ReelGenerator\Reels" 

os.makedirs(DEST_FOLDER, exist_ok=True)
@app.route('/save_video', methods=['POST'])
def save_video():
    filename = request.json.get("filename")
    source_path = os.path.join(SOURCE_FOLDER, filename)
    dest_path = os.path.join(DEST_FOLDER, filename)

    try:
        shutil.copy(source_path, dest_path)
        return jsonify({"status": "success", "message": f"{filename} saved successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

@app.route('/delete_video', methods=['POST'])
def delete_video():
    filename = request.json.get("filename")
    file_path = os.path.join(SOURCE_FOLDER, filename)

    try:
        if os.path.exists(file_path):
            os.remove(file_path)   # delete file
            return jsonify({"status": "success", "message": f"{filename} deleted successfully"})
        else:
            return jsonify({"status": "error", "message": "File not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
app.run(debug=True)