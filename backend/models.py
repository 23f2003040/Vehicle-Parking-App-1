from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Users(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String, unique=True, nullable=False)
    password=db.Column(db.String, nullable=False)
    name=db.Column(db.String, nullable=False)
    address=db.Column(db.String, nullable=False)
    pincode=db.Column(db.Integer, nullable=False)
    phone=db.Column(db.Integer, nullable=False)
    role=db.Column(db.Integer, nullable=False)
    reserve= db.relationship("Reserves", backref="user")


class ParkingLots(db.Model):
    __tablename__="lots"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, nullable=False) #prime_location_name
    price=db.Column(db.Integer, nullable=False)
    address=db.Column(db.String, nullable=False)
    pincode=db.Column(db.Integer, nullable=False)
    t_spots=db.Column(db.Integer, nullable=False, default=0) # total spots
    o_spots=db.Column(db.Integer, nullable=False, default=0) #occupies spots
    spot= db.relationship("ParkingSpots", cascade="all,delete", backref="lot")


class ParkingSpots(db.Model):
    __tablename__="spots"
    id=db.Column(db.Integer, primary_key=True)
    status=db.Column(db.String, nullable=False, default="Available")
    lid=db.Column(db.Integer, db.ForeignKey("lots.id"))
    reserve= db.relationship("Reserves", backref="spot")    
    

class Reserves(db.Model):   #Reserve Parking Spots
    __tablename__="reserves"
    id=db.Column(db.Integer, primary_key=True)
    action=db.Column(db.Integer, default=0) # 1=booked , 2=released, 3=bill paid
    status=db.Column(db.String, default="Parked In") # Parked In , Parked Out
    parking_timestamp=db.Column(db.String)
    leaving_timestamp=db.Column(db.String, default='')
    vehicle=db.Column(db.String) #vehicle no.
    cost=db.Column(db.Numeric(10,2), default=0) #parking_cost
    sid=db.Column(db.Integer, db.ForeignKey("spots.id"))
    uid=db.Column(db.Integer, db.ForeignKey("users.id"))


