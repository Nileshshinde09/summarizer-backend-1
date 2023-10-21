from flask import Flask, jsonify, request
from datastorage import *
from userAuthentication import create_user,authenticate_user,showall
from summeriser import summerize
from subfunc import *
app = Flask(__name__)

# auth = UserAuthentication("user_auth.db")



@app.route('/')
def index():
    return "Welcome to the index page"
# This function contains process_data + register user tasks
@app.route('/process_data', methods=['GET', 'POST'])
def process_data():
    if request.method == 'GET':
        # Access data from query parameters
        data = request.args.get('input_data')
    elif request.method == 'POST':
        # Access data from the request body
        data = request.form.get('input_data')
    else:
        return "Method not allowed", 405

    if data:
        
        # Perform input validation and sanitization
        if is_valid_input(data)==True:
            
            sanitized_data = sanitize_input(data)
            # Process the data
            response = jsonify(summerize(sanitized_data))
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response
        

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        # Access data from query parameters
        data = request.args.get('input_data')
    elif request.method == 'POST':
        # Access data from the request body
        data = request.form.get('input_data')
    else:
        return "Method not allowed", 405

    if data:
        
        username,fname,lname,email,password= input_for_ca(data)
        if create_user(username, email, fname, lname, password) ==True:
            returnstatement=200
        else:
            returnstatement=404
        response = jsonify({'res':returnstatement})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    else:
        return "Invalid input", 400




@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Access data from query parameters
        username = request.args.get('username')
        password = request.args.get('password')
    elif request.method == 'POST':
        # Access data from the request body
        username = request.form.get('username')
        password = request.form.get('password')
    else:
        return "Method not allowed", 405
    if username and password:
        print(authenticate_user(username, password))
        if authenticate_user(username, password) is False:
            res=0
        else:
            res=1
        response = jsonify({'res':res})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response


@app.route("/showusers", methods=['GET', 'POST'])
def showusers():
    if request.method == 'GET':
        # Access data from query parameters
        password = request.args.get('password')
    else:
        return "Method not allowed", 405
    with open('userspass.key','r') as key:
        storedpass=key.read()
        key.close()

    if password==storedpass:
        data=showall()
        response = jsonify({'res':data})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

@app.route("/addqa", methods=['GET', 'POST'])
def addqa():
    if request.method == 'GET':
        # Access data from query parameters
        username = request.args.get('username')
        q = request.args.get('q')
        a = request.args.get('a')
    elif request.method == 'POST':
        # Access data from the request body
        username = request.form.get('username')
        q = request.form.get('q')
        a = request.form.get('a')
    else:
        return "Method not allowed", 405
    if username and a and q:
        add_qa(username,q,a)


@app.route("/getqa", methods=['GET', 'POST'])
def getqa():
    if request.method == 'GET':
        # Access data from query parameters
        username = request.args.get('username')
        
    elif request.method == 'POST':
        # Access data from the request body
        username = request.form.get('username')
        
    else:
        return "Method not allowed", 405
    if username:
        print(username)
        data=get_qa(username)
        if data==[]:
            response = jsonify({'res':-1})
        else:
            response = jsonify({'res':data})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
   
@app.route("/delqa", methods=['GET', 'POST'])
def delqa():
    if request.method == 'GET':
        # Access data from query parameters
        username = request.args.get('username')
        password = request.args.get('password')
    elif request.method == 'POST':
        # Access data from the request body
        username = request.form.get('username')
        password = request.form.get('password')
    else:
        return "Method not allowed", 405
    if username and password:
        print(authenticate_user(username, password))
        if authenticate_user(username, password) is False:
            res= "Wrong credentials"
        else:
            res=del_qa(username)
        response = jsonify({'res':res})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    

if __name__ == "__main__":
    app.run(debug=True)

