
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#init app
app = Flask(__name__)

basedir=os.path.abspath(os.path.dirname(__file__))

#database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init db
db = SQLAlchemy(app)
#init marshmallow
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

    def __init__(self, username):
        self.username = username

class UserSchema(ma.Schema):
      class Meta:
        fields = ('id', 'username')
        

#init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

#create a user
@app.route('/user', methods=['POST'])
def add_user():
    username = request.json['username']
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/user/<id>', methods=['GET'])   
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    location = db.Column(db.String(120))
    cuisine=db.Column(db.String(120))
    rating=db.Column(db.Float)
    phone=db.Column(db.String(15))
    email=db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, name, location, cuisine, rating, phone, email, user_id):
        self.name = name
        self.location = location
        self.cuisine = cuisine
        self.rating = rating
        self.phone = phone
        self.email = email
        self.user_id = user_id

class RestaurantSchema(ma.Schema):
      class Meta:
        fields = ('id', 'name', 'location', 'cuisine', 'rating', 'phone', 'email', 'user_id')
        

#init schema
restaurant_schema = RestaurantSchema()
restaurants_schema = RestaurantSchema(many=True)

#create a restaurant
@app.route('/restaurant/add', methods=['POST'])
def add_restaurant():
    name = request.json['name']
    location = request.json['location']
    cuisine = request.json['cuisine']
    rating = request.json['rating']
    phone = request.json['phone']
    email = request.json['email']
    user_id = request.json['user_id']
    new_restaurant = Restaurant(name=name, location=location, cuisine=cuisine, rating=rating, phone=phone, email=email, user_id=user_id)
    db.session.add(new_restaurant)
    db.session.commit()

    return restaurant_schema.jsonify(new_restaurant)

#get a restaurant
@app.route('/restaurant/<name>', methods=['GET'])
def get_restaurant(name):
    restaurant = Restaurant.query.get(name)
    return restaurant_schema.jsonify(restaurant)

#get all restaurants
@app.route('/restaurant', methods=['GET'])
def get_restaurants():
    all_restaurants = Restaurant.query.all()
    result = restaurants_schema.dump(all_restaurants)
    return jsonify(result)

#update a restaurant
@app.route('/restaurant/<id>', methods=['PUT'])
def update_restaurant(id):  
    restaurant = Restaurant.query.get(id)
    name = request.json['name']
    location = request.json['location']
    cuisine = request.json['cuisine']
    rating = request.json['rating']
    phone = request.json['phone']
    email = request.json['email']
    user_id = request.json['user_id']
    restaurant.name = name
    restaurant.location = location
    restaurant.cuisine = cuisine    
    restaurant.rating = rating
    restaurant.phone = phone
    restaurant.email = email
    restaurant.user_id = user_id
    db.session.commit()
    return restaurant_schema.jsonify(restaurant)

#find restaurant by location
@app.route('/restaurant/find location/<location>', methods=['GET'])
def  get_restaurant_by_location(location):
    restaurant = Restaurant.query.filter_by(location=location).first()
    return restaurant_schema.jsonify(restaurant)

#find restaurant by cuisine
@app.route('/restaurant/find cuisine/<cuisine>', methods=['GET'])
def  get_restaurant_by_cuisine(cuisine):
    restaurant = Restaurant.query.filter_by(cuisine=cuisine).first()
    return restaurant_schema.jsonify(restaurant)

#delete a restaurant
@app.route('/restaurant/<id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    db.session.delete(restaurant)
    db.session.commit()
    return restaurant_schema.jsonify(restaurant)

if __name__ == '__main__':
    app.run(debug=True)

