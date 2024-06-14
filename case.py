from sqlalchemy import create_engine
from sqlalchemy import Integer, ForeignKey, String, Column,Float,VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

# Define a User table
class User(Base):
    __tablename__ = 'users'
    id = Column("id",Integer, primary_key=True)
    name = Column("name",String(32))
    
    def __init__(self,name):
         self.name=name 

# Define a Restaurant table
class Restaurant(Base):
     __tablename__ = 'restaurants'
     id = Column("id",Integer, primary_key=True,autoincrement=True)
     name=Column("name",String)
     location=Column("location",String)
     cuisine=Column("cuisine",String)
     rating=Column("rating",Float)    
     phone=Column("phone",VARCHAR)
     email=Column("email",VARCHAR)  
     user_id=Column("user_id",Integer,ForeignKey('users.id'))
     
     def __init__(self,name,location,cuisine,rating,phone,email,user_id):
         self.name=name
         self.location=location
         self.cuisine=cuisine
         self.rating=rating
         self.phone=phone
         self.email=email
         self.user_id=user_id

def addUser(name,session):
    user=User(name)
    session.add(user)
    session.commit()
    print("User added")

def addRestaurant(name,location,cuisine,rating,phone,email,user_id,session):
    restaurant=Restaurant(name,location,cuisine,rating,phone,email,user_id)
    session.add(restaurant)
    session.commit()
    print("Restaurant added")

def updateRestaurant(name,location,cuisine,rating,phone,email,user_id,session):   
    restaurant=session.query(Restaurant).filter(Restaurant.name==name).first()
    restaurant.location=location
    restaurant.cuisine=cuisine
    restaurant.rating=rating
    restaurant.phone=phone
    restaurant.email=email
    restaurant.user_id=user_id
    session.commit()
    print("Restaurant updated")

def addUser(name,session):
    user=User(name)
    session.add(user)
    session.commit()
    print("User added")

## Create a SQLite database engine

#option1
#engine=create_engine("sqlite:///test.db")

#option2
#dialect+driver://username:password@host:port/existing database
engine=create_engine('postgresql://postgres:123456@localhost/testdb',echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

user_all = session.query(User).all()
print("All User id and name")
for user in user_all:
    print(user.id,user.name)

signUp=input("Do you want to signup?(y/n)")
if signUp=="y":
    name=input("Enter user name:")
    user=session.query(User).filter(User.name==name).first()
    if user is not None:
        print("User found")
    else:
        print("User not found")
        addUser(name,session)
else:
    print("Exiting")

viewOrNot=input("Do you want to view restaurant?(y/n)") 
if viewOrNot=="y":
    restaurant_all = session.query(Restaurant).all()
    for restaurant in restaurant_all:
        print(restaurant.name,restaurant.location,restaurant.cuisine,restaurant.rating,restaurant.phone,restaurant.email,restaurant.user_id)
else:
    print("Exiting")

retrieveOrNot=input("Do you want to retrieve restaurant?(y/n)")
if retrieveOrNot=="y":
    name=input("Enter restaurant name:")
    restaurant_all=session.query(Restaurant).filter(Restaurant.name==name).all()
    if len(restaurant_all)>0 :
        for restaurant in restaurant_all:
            print(restaurant.name,restaurant.location,restaurant.cuisine,restaurant.rating,restaurant.phone,restaurant.email,restaurant.user_id)

    else:
        print("Restaurant not found")
else:
    print("Exiting")

addOrNot=input("Do you want to add restaurant?(y/n)")
if addOrNot=="y":
    name=input("Enter restaurant name:")
    location=input("Enter restaurant location:")
    cuisine=input("Enter restaurant cuisine:")
    rating=input("Enter restaurant rating:")
    phone=input("Enter restaurant phone:")
    email=input("Enter restaurant email:")
    user_id=input("Enter user id:")
    if session.query(Restaurant).filter(Restaurant.user_id==user_id).first() is not None:
       addRestaurant(name,location,cuisine,rating,phone,email,user_id,session)      
    else:
        print("User not found")
else:
    print("Exiting")

updateOrNot = input("Do you want to update restaurant?(y/n)")
if updateOrNot=="y":
    name=input("Enter restaurant name:")
    location=input("Enter restaurant location:")
    cuisine=input("Enter restaurant cuisine:")
    rating=input("Enter restaurant rating:")
    phone=input("Enter restaurant phone:")
    email=input("Enter restaurant email:")
    user_id=input("Enter user id:")
    if session.query(Restaurant).filter(Restaurant.user_id==user_id).first() is not None:
        updateRestaurant(name,location,cuisine,rating,phone,email,user_id,session) 
    else:
        print("User not found")
else:
    print("Exiting")

deleteOrNot = input("Do you want to delete restaurant?(y/n)")
if deleteOrNot=="y":
    name=input("Enter restaurant name:")
    if len(session.query(Restaurant).filter(Restaurant.name==name).all())>0:
       session.query(Restaurant).filter(Restaurant.name==name).delete()
       session.commit()
       print("Restaurant deleted")
    else:
        print("Restaurant not exist")
else:
    print("Exiting")

find=input("Enter filter criteria:(location/cuisine)")
if find=="location":
    location=input("Enter location:")
    restaurant_all = session.query(Restaurant).filter(Restaurant.location==location).all()
    if len(restaurant_all)>0:
        for restaurant in restaurant_all:
            print(restaurant.name,restaurant.location,restaurant.cuisine,restaurant.rating,restaurant.phone,restaurant.email)
    else:
        print("Restaurant not found")
elif find=="cuisine":
    cuisine=input("Enter cuisine:")
    restaurant_all = session.query(Restaurant).filter(Restaurant.cuisine==cuisine).all()
    if len(restaurant_all)>0:
        for restaurant in restaurant_all:
            print(restaurant.name,restaurant.location,restaurant.cuisine,restaurant.rating,restaurant.phone,restaurant.email)
    else:
        print("Restaurant not found")
else:
    print("Exiting")

