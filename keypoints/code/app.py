import threading

from flask import Flask, request, flash, redirect, jsonify, url_for
from launch_nodet import detect
from multiprocessing import Pool
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/home/enviablejimi/jm.iniko@gmail.com/jmi20130707/i-technologies/developpement/fitsize/pythonapp/noma/code/code/data/images/trouser'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'testthefrench\n\xec]/'


@app.route('/')
def hello_world():  # put application's code here
    return """
     <!DOCTYPE html>                                                                                                                                                        
        <html lang="en">                                                                                                                                                       
        <head>                                                                                                                                                                 
            <meta charset="UTF-8">                                                                                                                                             
            <title>Hello, World!!</title>                                                                                                                                               
        </head>                                                                                                                                                                
        <body>  Hello World!
        </body>
        </html>
        """


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/saveimage', methods=['GET','POST'])
def run_no_det():
    print("DBG10000:::")
    if request.method == 'POST':
        print("DBG20000::::")
        # check if the post request has the file part
        if 'picture' not in request.files:
            print("DBG30000:::")
            flash('No file part')
            print("DBG40000:::")
            return redirect(request.url)
        file = request.files['picture']
        print("DBG50000:::")
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print("DBG60000:::")
            flash('No selected file')
            print("DBG70000:::")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("DB80000:::")
            filename = secure_filename(file.filename)
            print("DBG90000:::")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("DBG100000:::")

            th = threading.Thread(target=detect, daemon=True)
            th.start()
            return jsonify({"response": "success"})
    else:
        return """                                                                                                                                                     
        <!DOCTYPE html>                                                                                                                                                        
        <html lang="en">                                                                                                                                                       
        <head>                                                                                                                                                                 
            <meta charset="UTF-8">                                                                                                                                             
            <title>Title</title>                                                                                                                                               
        </head>                                                                                                                                                                
        <body>                                                                                                                                                                 
        <form action="http://localhost:5000/saveimage" method="post" enctype="multipart/form-data">                                                                      
          <input type="file" name="picture" multiple="multiple">                                                                                                               
          <input type="submit">                                                                                                                                                
        </form>                                                                                                                                                                
        </body>                                                                                                                                                                
        </html>                                                                                                                                                                
                """


if __name__ == '__main__':
    app.run()
