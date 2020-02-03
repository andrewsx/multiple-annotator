import prodigy
from prodigy.components.db import Database, connect
from flask import Flask, render_template, redirect, request, url_for
import socket
from config import users, FN_FLASK_SECRET_KEY, coder_list
import atexit
from multi_user import MultiUser

# Sometimes note: create and delete dataset, throws an error in page refresh

app = Flask(__name__)
app.secret_key = FN_FLASK_SECRET_KEY
ip = socket.gethostbyname(socket.gethostname())

@app.route('/')
def index():
    return redirect("/login", code=302)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        _user = request.form['user']
        if _user in users:
            return redirect(url_for('options', name=_user))
    return render_template("login.html")


@app.route('/options/?user=<name>', methods=['GET', 'POST'])
def options(name):
    sentinel = False
    db = connect()
    if request.method == 'POST':
        if request.form['action'] == 'List':
            
            return render_template("options.html", greeting=name, lst=db.datasets, db=db)
        elif request.form['action'] == 'Create':
            stripped_input = request.form['create'].strip()
            description = request.form['describe'].strip()
            print(stripped_input)
            if stripped_input in db.datasets:  
                return render_template("error.html", msg="User must not use a dataset name that already exists")
            if stripped_input == "":  
                return render_template("error.html", msg="User must provide non empty dataset name")
            if ' ' in stripped_input or ',' in stripped_input:  
                return render_template("error.html", msg="Dataset name can't include commas or whitespace")
            db.add_dataset(stripped_input, {"description" : description, "author" : name})
        elif request.form['action'] == 'Delete':
            
            dataset_name = request.form['dataset_name']
        
            if not db.drop_dataset(dataset_name):
                return render_template("error.html", msg="Failed to drop dataset")
            return render_template("options.html", greeting=name, lst=db.datasets, db=db)
        elif request.form['action'] == 'Continue':
            
            dataset_name = request.form['continue']
            print('Dataset_name', dataset_name)
            
            spacy_model = request.form.get("models", None)
            print('Spacy_model', spacy_model)
            
        
            input_data = request.form['input_data'].strip()
            print('User_input', input_data)
            if input_data == '':
                return render_template("error.html", msg="User must provide an input dataset")
            # user labels (this should be a string separated by commas)
            input_labels = request.form['labels'].strip()
            print('User_input', input_labels)

            for coder_info in enumerate(coder_list):
                coder_info = coder_info[1]
                if name in coder_info['name']:
                    sentinel = True
                    mp = MultiUser(name, coder_info['port'])
                    atexit.register(mp.kill_prodigies)
                    mp.make_prodigies(dataset_name, input_data, spacy_model, input_labels.split(","))
                    mp.start_prodigies()
            if not sentinel:
                return render_template("error.html", msg="Username does not exist")
                

        elif request.form['action'] == 'Print':
            dataset_name = request.form['dataset_name']
            lst = db.get_dataset(dataset_name)
            return render_template("output.html", lst=lst, name=dataset_name)
    
    return render_template("options.html", greeting=name, lst=db.datasets, db=db)
    


@app.route('/logout')
def logout():
    return 'Logged out'
