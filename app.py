# Import Flask, jsonify, and requests
from urllib.parse import urlparse, parse_qs
import json
import jwt
from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
# Create a Flask app and an API with Connexion
app = Flask(__name__)
app.config['SECRET_KEY'] = "my-secret-key"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/food_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Sapat1925@192.168.0.103:3309/food_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


# import connexion
# api = connexion.App(__name__, specification_dir="./")
# api.add_api("app_a.yaml")

# Food Model
class Food(db.Model):
    id = db.Column('food_id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('food_name', db.String(300))
    detail = db.Column('food_detail', db.String(300))
    price = db.Column('food_price', db.String(300))


print('Food Table is Created...')
db.create_all()


# Define a resource for the /hello endpoint
@app.route("/")
def hello():
    # Return a greeting message
    return jsonify({"message": "Hello!! Welcome to Food App! Food Service is Working."})


# Define a resource for the /call_app_b endpoint
@app.route("/get")  # DONE
def get_food():
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split()[1]
    except:
        return jsonify({"error": "Token missing, Please login again foodapp.food/get"})
    try:
        isvalid = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    except:
        return jsonify({"error": "token is invalid, Please login again foodapp.food/get"})
    result = Food.query.all()
    # print("result is:", result)
    # if no products in db -- return -- simple message --
    if not result:
        return json.dumps({"ERROR": "No Food Details...!"})
    else:
        final_result = []
        for f in result:
            food_dict = {'food_id': f.id, 'food_name': f.name, 'food_detail': f.detail, 'food_price': f.price}
            # print("food dict is:", food_dict)
            # add that dict every time inside final list
            final_result.append(food_dict)
        # print("final :", final_result)
        return json.dumps(final_result)  # [{ },{ }] json
    # try:
    #     auth_header = request.headers.get('Authorization')
    #     token = auth_header.split()[1]
    # except:
    #     return jsonify({"error": "Token missing, Please login again foodapp.food/get"})
    # if session.get('LOGGED_IN') is not False:
    #     try:
    #         isvalid = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    #     except:
    #         return jsonify({"error": "token is invalid, Please login again foodapp.food/get"})
    #     result = Food.query.all()
    #     print("result is:",result)
    #     # if no products in db -- return -- simple message --
    #     if not result:
    #         return json.dumps({"ERROR": "No Food Details...!"})
    #     else:
    #         final_result = []
    #         for f in result:
    #             food_dict = {'food_id': f.id, 'food_name': f.name, 'food_detail': f.detail, 'food_price': f.price}
    #             print("food dict is:",food_dict)
    #             # add that dict every time inside final list
    #             final_result.append(food_dict)
    #         # print("final :", final_result)
    #         return json.dumps(final_result)
    # else:
    #     return redirect("http://localhost:5000")


# Define a resource for the /call_app_b endpoint
@app.route("/create")  # not done yet
def create_food():
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split()[1]
    except:
        return jsonify({"error": "Token missing, Please login again foodapp.food/create"})
    if session.get('LOGGED_IN') is not False:
        try:
            isvalid = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({"error": "token is invalid, Please login again foodapp.food/create"})
        result = Food.query.all()
        if not result:
            return json.dumps({"ERROR": "No Food Details...!"})
        else:
            final_result = []
            for f in result:
                food_dict = {'food_id': f.id, 'food_name': f.name, 'food_detail': f.detail, 'food_price': f.price}
                # add that dict every time inside final list
                final_result.append(food_dict)
            # print("final :", final_result)
            return json.dumps(final_result)
    else:
        return jsonify({"error": "Token missing, Please login again foodapp.food/create"})

        # try:
        #
        #     food_dict = request.args.get('food_dict')
        #     food_name = request.args.get('food_name')
        #     food_detail = request.args.get('food_detail')
        #     food_price = request.args.get('food_price')
        #     print(food_dict)
        #     return food_dict
        # except:
        #     return "food_dict not available"
    #     result = Food.query.all()
    #     if not result:
    #         return json.dumps({"ERROR": "No Food Details...!"})
    #     else:
    #         final_result = []
    #         for f in result:
    #             food_dict = {'food_id': f.id, 'food_name': f.name, 'food_detail': f.detail, 'food_price': f.price}
    #             # add that dict every time inside final list
    #             final_result.append(food_dict)
    #         # print("final :", final_result)
    #         return json.dumps(final_result)
    # else:
    #     return jsonify({"error": "Token missing, Please login again foodapp.food/create"})

    # Make a GET request to App B's /hello endpoint
    # bearer_token =
    # print("head is ", bearer_token)
    '''
    result = Food.query.all()
    # if no products in db -- return -- simple message --
    if not result:
        return json.dumps({"ERROR": "No Food Details...!"})

    final_result = []
    # iterate one by and prepare dict -
    for f in result:
        food_dict = {}
        food_dict['foodid'] = f.id
        food_dict['foodname'] = f.name
        food_dict['fooddetail'] = f.detail
        food_dict['foodprice'] = f.price
        # add that dict every time inside final list
        final_result.append(food_dict)
    # print(final_result)
    return json.dumps(final_result)
    '''
    # return jsonify({"message": "Food List", "food": final_result})
    # response = requests.get("http://localhost:5002/")
    # Return the response from App B
    # return jsonify({"message": "App A called App B", "response": response.json()}) #json result


@app.route("/get/<fid>")
def get_order_food(fid):
    # Make a GET request to App B's /hello endpoint
    id = int(fid)
    result = Food.query.filter_by(id=id).first()
    # if no products in db -- return -- simple message --
    if not result:
        return json.dumps({"ERROR": "No Food Details...!"})

    final_result = []
    # iterate one by and prepare dict
    food_dict = {'foodid': result.id, 'foodname': result.name, 'foodprice': result.price}
    # add that dict every time inside final list
    final_result.append(food_dict)
    # print(final_result[0])
    # @ params = urllib.parse.urlencode(final_result[0], doseq=True)
    # req = requests.PreparedRequest()
    # req.prepare_url("http://localhost:5002/create/" + str(id), final_result)
    # print(req.url)
    # @ url = "http://localhost:5002/create/" + str(fid) + "?" + params
    # @ print(url)
    # @ redirect(url)
    return json.dumps(final_result[0])


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
