

from uuid import uuid4
from flask import Flask, make_response, request
import dbhelpers as dh
import apihelpers as a
import json
import dbcreds as d


app = Flask(__name__)

@app.post('/api/client')

# this method for creating new client
def create_new_client():
    # passing through 5 expected inputs to see if it is valid, nothing happens if it is
    valid_check = a.check_endpoint_info(request.json, ['email', 'username', 'first_name', 'last_name', 'img_url', 'password'])
    if(valid_check != None):
        return make_response(json.dumps(valid_check, default=str), 400)
    
    # salt is generated using uuid4 and .hex converts it to hexadecimal so python mariadb can use it 
    salt = uuid4().hex
    # the 7th argument is the salt that's added to password which then by using hash method to make it less easy to guess 
    result=dh.run_statement('CALL new_client(?,?,?,?,?,?,?)', [request.json.get('email'), request.json.get('username'), request.json.get('first_name'),
    request.json.get('last_name'), request.json.get('img_url'), request.json.get('password'), salt])
    if(type(result) == list):
        return make_response(json.dumps(result, default=str), 200)
    else:
        return make_response(json.dumps(result, default=str), 400)

@app.get('/api/client')

#this method shows client info and needs 1 argument the id for input
def get_client_info():
    valid_check = a.check_endpoint_info(request.args, ['id'])
    if(valid_check != None):
        return make_response(json.dumps(valid_check, default=str), 400)

    result=dh.run_statement('CALL client_info(?)', [request.args.get('id')])
    if(type(result) == list):
        return make_response(json.dumps(result, default=str), 200)
    else:
        return make_response(json.dumps(result, default=str), 400)

# deletes the client from database if token and password matches
@app.delete('/api/client')

def delete_client():
    valid_check = a.check_endpoint_info(request.json, ['token', 'password'])
    if (valid_check != None):
        return make_response(json.dumps(valid_check, default=str), 400)

    result = dh.run_statement('CALL delete_client(?,?)', [request.json.get('token'), request.json.get('password')])
    if (type(result) == list):
        return make_response(json.dumps(result, default=str), 200)
    else:
        return make_response(json.dumps(result, default=str), 400)

# uses 2 argument and returns token value.  the value is checkd and argument is checked first before token is generated in python
@app.post('/api/client-login')

def client_login():
    valid_check = a.check_endpoint_info(request.json, ['email', 'password'])
    token = uuid4().hex
    if (valid_check != None):
        return make_response(json.dumps(valid_check, default=str), 400)

    result = dh.run_statement('CALL client_login(?,?,?)', [request.json.get('email'), request.json.get('password'), token])
    if (type(result) == list):
        return make_response(json.dumps(result, default=str), 200)
    else:
        return make_response(json.dumps(result, default=str), 400)

# @app.patch('/api/client') will get back to this

# def update_client():
#     valid_check=a.check_endpoint_info(request.json, ['token', 'email', 'username'])

@app.delete('/api/client-login')
def delete_client_token():
    valid_check=a.check_endpoint_info(request.json, ['token'])
    if(valid_check != None):
        return make_response(json.dumps(valid_check, default=str), 400)

    result = dh.run_statement('CALL delete_client_token(?)', [request.json.get('token')])
    if (type(result) == list):
        return make_response(json.dumps(result, default=str), 200)
    else:
        return make_response(json.dumps(result, default=str), 400)


# add new restaurant with 10 arguments from called procedure
@app.post('/api/restaurant')

def new_restaurant():
    salt = uuid4().hex
    valid_check=a.check_endpoint_info(request.json, ['email', 'password', 'name', 'address', 'phone', 'bio', 'city', 'profile_url', 'banner_url'])
    if(valid_check != None):
        return make_response(json.dumps(valid_check, default=str), 400)
    
    result = dh.run_statement('CALL new_restaurant(?,?,?,?,?,?,?,?,?,?)', [request.json.get('email'), request.json.get('password'), request.json.get('name'), 
    request.json.get('address'), request.json.get('phone'), request.json.get('bio'), request.json.get('city'), 
    request.json.get('profile_url'), request.json.get('banner_url'), salt])
    if (type(result) == list):
        return make_response(json.dumps(result, default=str), 200)
    else:
        return make_response(json.dumps(result, default=str), 400)

# get request, provide 1 argument, the restaurant id, and then it returns information regarding that 1 restaurant

@app.get('/api/restaurant')
def get_restaurant_info():
    valid_check=a.check_endpoint_info(request.args, ['restaurant_id'])
    if(valid_check != None):
        return make_response(json.dumps(valid_check, default=str), 400)
    
    result = dh.run_statement('CALL restaurant_info(?)', [request.args.get('restaurant_id')])
    if(type(result) == list):
        return make_response(json.dumps(result, default=str), 200)
    else:
        return make_response(json.dumps(result, default=str), 400)

# delete restaurant from database it needs token and password as argument
@app.delete('/api/restaurant')
def delete_restaurant():
    valid_check=a.check_endpoint_info(request.json, ['token', 'password'])
    if (valid_check != None):
        return make_response(json.dumps(valid_check, default=str), 400)

    result = dh.run_statement('CALL delete_restaurant(?,?)', [request.json.get('token'), request.json.get('password')])
    if(type(result) == list):
        return make_response(json.dumps(result, default=str), 200)
    else:
        return make_response(json.dumps(result, default=str), 400)

# restaurant login needs email, password, token as argument
@app.post('/api/restaurant-login')
def restaurant_login():
    token = uuid4().hex
    valid_check = a.check_endpoint_info(request.json, ['email', 'password'])
    if(valid_check != None):
        return make_response(json.dumps(valid_check, default=str), 400)

    result = dh.run_statement('CALL restaurant_login(?,?,?)', [request.json.get('email'), request.json.get('password'), token])
    if(type(result) == list):
        return make_response(json.dumps(result, default=str), 200)
    else:
        return make_response(json.dumps(result, default=str), 400)

# restaurant delete token for logging out only needs token as argument
@app.delete('/api/restaurant-login')
def delete_restaurant_token():
    valid_check = a.check_endpoint_info(request.json, ['token'])
    if(valid_check != None):
        return make_response(json.dumps(valid_check, default=str), 400)
    
    result = dh.run_statement('CALL delete_restaurant_token(?)', [request.json.get('token')])
    if (type(result) == list):
        return make_response(json.dumps(result, default=str), 200)
    else:
        return make_response(json.dumps(result, default=str), 400)


# this does not need argument and returns all restaurant in database
@app.get('/api/restaurants')
def show_all_restaurant():
    result = dh.run_statement('CALL show_all_restaurant()')
    if(type(result) == list):
        return make_response(json.dumps(result, default=str), 200)
    else:
        return make_response(json.dumps(result, default=str), 400)


if(d.production_mode == True):
    print("Running in Production Mode")
    import bjoern #type:ignore
    bjoern.run(app, "0.0.0.0", 5000)
    app.run(debug=True)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode")
    app.run(debug=True)