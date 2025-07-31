from flask import Flask,render_template,request
from flask import current_app as app 
import matplotlib
matplotlib.use('Agg') # to avoid GUI related warnings . It renders plots to image files not to the screen.
import matplotlib.pyplot as plt
from .models import *
from datetime import datetime

@app.route("/")
def home():
    return "<h2>Welcome to the App</h2>"

@app.route("/login",methods=["GET","POST"])
def user_login():
    
    if request.method=="POST":
        uname=request.form.get("uname")
        pwd=request.form.get("pwd")
        if uname == "admin@gmail.com" and pwd == "123":
            lot=ParkingLots.query.all()
            users=Users.query.all()  
            a()
            b()
            return render_template("admin_dashboard.html",lot=lot,users=users)
        usr=Users.query.filter_by(username=uname, password=pwd).first()
        if usr :
            info=user_info(usr.id)
            c(usr.id)
            return render_template("user_dashboard.html",info=info)
        else:
            return render_template("login.html",msg=1,message="Invalid input !!!")
    return render_template("login.html")

@app.route("/user_register",methods=["GET","POST"])
def user_register():
    if request.method=="POST":
        uname=request.form.get("uname")
        pwd=request.form.get("pwd")
        name=request.form.get("fullname")
        address=request.form.get("address")
        pincode=int(request.form.get("pincode"))
        phone=int(request.form.get("phone"))
        usr=Users.query.filter_by(username=uname, role=1).first()
        if not usr:
            new_user=Users(username=uname, password=pwd, role=1, name=name, address=address,pincode=pincode,phone=phone)
            db.session.add(new_user)
            db.session.commit()
            return render_template("login.html",msg=2)
        else:
            return render_template("user_register.html",msg="error")
    return render_template("user_register.html")


@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/user_dashboard")
def professional_dashboard():
    return render_template("professional_dashboard.html")


#-----------query fetch-----------------------------
def user_info(id):
    info=Users.query.filter_by(id=id).first()
    return info

def occupied_spots(id):
    spots=ParkingSpots.query.filter_by(lid=id)
    count=0
    for spot in spots:
        if spot.status == "Occupied":
            count += 1
    return count



#------------------------------------Search-------------------------------------------------
@app.route("/search",methods=["GET","POST"])
def search():
    a=request.form.get("txt")
    role=int(request.form.get("role"))
    search_by=int(request.form.get("search_by"))
    search_value=[]
    value=0
    if role == 0:
        if search_by == 2:
            value=1
            if a:
                search_value=ParkingLots.query.filter(ParkingLots.name.icontains(a) | ParkingLots.pincode.icontains(a) | ParkingLots.address.icontains(a) | ParkingLots.id.icontains(a)).all()
            else:
                a=""
                search_value=ParkingLots.query.filter(ParkingLots.name.icontains(a) | ParkingLots.pincode.icontains(a) | ParkingLots.address.icontains(a) | ParkingLots.id.icontains(a)).all()
        else:
            if a:
                search_value=Users.query.filter(Users.name.icontains(a) | Users.username.icontains(a) | Users.pincode.icontains(a) | Users.address.icontains(a) | Users.id.icontains(a)).all()
            else:
                a=""
                search_value=Users.query.filter(Users.name.icontains(a) | Users.username.icontains(a) | Users.pincode.icontains(a) | Users.address.icontains(a) | Users.id.icontains(a)).all()
        lot=ParkingLots.query.all()
        users=Users.query.all()     
        return render_template("admin_dashboard.html",search_value=search_value,value=value,lot=lot,users=users)
    if role == 1:
        id=int(request.form.get("id"))
        info=user_info(id)
        if a:
            search_value=ParkingLots.query.filter(ParkingLots.name.icontains(a) | ParkingLots.pincode.icontains(a) | ParkingLots.address.icontains(a) | ParkingLots.id.icontains(a)).all()
        else:
            a=""
            search_value=ParkingLots.query.filter(ParkingLots.name.icontains(a) | ParkingLots.pincode.icontains(a) | ParkingLots.address.icontains(a) | ParkingLots.id.icontains(a)).all()
        if search_value:
            for lot in search_value:
                if (lot.t_spots-lot.o_spots) > 0:
                    for spot in lot.spot:
                        if spot.status=="Available":
                            lot.available_spot = spot
                            break   
        return render_template("user_dashboard.html",search_value=search_value,info=info)



#----------------------Parking Lot-------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/lotadd",methods=["GET","POST"])
def new_lot():
    if request.method=="POST":
        name=request.form.get("name")
        price=int(request.form.get("price"))
        address=request.form.get("address")
        pincode=int(request.form.get("pincode"))
        t_spots=int(request.form.get("t_spots"))
        o_spots=int(request.form.get("o_spots"))
        new_lot=ParkingLots(name=name,price=price,address=address,pincode=pincode,t_spots=t_spots,o_spots=o_spots)
        db.session.add(new_lot)
        db.session.commit()
        for i in range(t_spots):
            new_spot=ParkingSpots(status="Available",lid=new_lot.id)
            db.session.add(new_spot)
        db.session.commit()
        lots=ParkingLots.query.all()
        users=Users.query.all()
        a()
        b()
        return render_template("admin_dashboard.html",lot=lots,users=users,msg=2,message="New Parking Lot Created Successfully.")
    
@app.route("/lotedit",methods=["GET","POST"])
def edit_lot():
    if request.method=="POST":
        id=int(request.form.get("lot_id"))
        lot=ParkingLots.query.filter_by(id=id).first()
        t_spots=int(request.form.get("t_spots"))
        if (t_spots < lot.o_spots) :
            lots=ParkingLots.query.all()
            users=Users.query.all()
            a()
            b()
            return render_template("admin_dashboard.html",lot=lots,users=users,msg=1,message="Total Spots cannot be less than Occupied Spots.")
        original= lot.t_spots
        if (t_spots>original):
            for i in range(t_spots-original):
                new_spot=ParkingSpots(status="Available",lid=id)
                db.session.add(new_spot)
        elif (t_spots<original): 
            count=original-t_spots
            for spot in reversed(lot.spot):
                if spot.status == "Available" and count>0:
                    db.session.delete(spot)
                    count-=1
        lot.t_spots=t_spots
        lot.o_spots=occupied_spots(id)
        lot.name=request.form.get("name")
        lot.price=int(request.form.get("price"))
        lot.address=request.form.get("address")
        lot.pincode=int(request.form.get("pincode"))
        db.session.commit() 
        lots=ParkingLots.query.all()
        users=Users.query.all()
        a()
        b()
        return render_template("admin_dashboard.html",lot=lots,users=users,msg=2,message="Parking Lot Updated Successfully.")
    
@app.route("/lotdelete",methods=["GET","POST"])
def delete_lot():
    if request.method=="POST":
        id=int(request.form.get("lot_id"))
        lot=ParkingLots.query.filter_by(id=id).first()
        if (lot.o_spots) :
            lots=ParkingLots.query.all()
            users=Users.query.all()
            a()
            b()
            return render_template("admin_dashboard.html",lot=lots,users=users,msg=1,message="Cannot delete: All spots in the parking lot must be empty.")
        db.session.delete(lot)
        db.session.commit()
        lots=ParkingLots.query.all()
        users=Users.query.all()
        a()
        b()
        return render_template("admin_dashboard.html",lot=lots,users=users,msg=2,message="Parking Lot Deleted Successfully.")


#----------Parking Spots--------------------------------------
@app.route("/book/<int:userid>",methods=["GET","POST"])
def book_spot(userid):
    if request.method=="POST":
        vehicle=request.form.get("vehicle")
        sid=int(request.form.get("sid"))
        lid=int(request.form.get("lid"))
        uid=int(request.form.get("uid"))
        ptime= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reserve=Reserves(vehicle=vehicle,sid=sid,uid=uid,status="Parked In",action=1,parking_timestamp=ptime)
        db.session.add(reserve)      
        spot=ParkingSpots.query.filter_by(id=sid).first()
        spot.status="Occupied"
        lot=ParkingLots.query.filter_by(id=lid).first()
        lot.o_spots=occupied_spots(lid)
        db.session.commit()
        info=user_info(userid) 
        c(uid)
        return render_template("user_dashboard.html",info=info,msg=2,message="Parking Spot Booked.")
    
@app.route("/release/<int:userid>",methods=["GET","POST"])
def release_spot(userid):
    if request.method=="POST":
        rid=int(request.form.get("rid"))
        r=Reserves.query.filter_by(id=rid).first()
        time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        r.leaving_timestamp= time
        r.status="Parked Out"
        r.action=2
        spot=ParkingSpots.query.filter_by(id=r.sid).first()
        spot.status="Available"
        lot=ParkingLots.query.filter_by(id=r.spot.lid).first()
        lot.o_spots=occupied_spots(r.spot.lid)          # count occupied spots
        p=datetime.strptime(r.parking_timestamp,"%Y-%m-%d %H:%M:%S")
        l=datetime.strptime(time,"%Y-%m-%d %H:%M:%S")
        r.cost= round(lot.price * ((l-p).total_seconds()/3600),2)
        db.session.commit()
        info=user_info(userid) 
        c(userid)
        return render_template("user_dashboard.html",info=info,msg=2,message="Parking Spot Released.")
    
@app.route("/payment/<int:userid>",methods=["GET","POST"])
def action_request(userid):
    if request.method=="POST":
        rid=int(request.form.get("rid"))
        r=Reserves.query.filter_by(id=rid).first()
        r.action=3
        db.session.commit()
        info=user_info(userid) 
        c(userid)
        return render_template("user_dashboard.html",info=info,msg=2,message="Payment Successful.")
    
#--------------------------Graph---------------------------------------

def a(): #graph for Available and occupied parking spots
    occupied=len(ParkingSpots.query.filter_by(status="Occupied").all())
    available=len(ParkingSpots.query.filter_by(status="Available").all())
    total=len(ParkingSpots.query.all())
    spots=["Total Spots","Available","Occupied"]
    count=[total,available,occupied]
    plt.figure(figsize=(5, 5))
    plt.bar(spots,count, color=["skyblue","lightgreen","orange"])
    plt.xlabel('Parking Spots')
    plt.ylabel('Numbers')
    plt.title('Spots Status')
    for i, value in enumerate(count):
        plt.annotate((count[i]),(spots[i], count[i]))
    plt.tight_layout()
    plt.savefig("static/spot.png")

def b(): # pie charts for revenues

    total=sum(r.cost for r in Reserves.query.filter_by(status="Parked Out").all())
    values=[] 
    labels=[]
    lots= ParkingLots.query.all()
    for l in lots:
        lot_revenue=0
        labels.append("Lot "+str(l.id))
        for s in l.spot:
            lot_revenue+=sum(r.cost for r in Reserves.query.filter_by(status="Parked Out", sid=s.id).all())
        values.append(lot_revenue)
    plt.figure(figsize=(5, 5))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(f'Total Revenue: ₹{total:.2f}')
    plt.tight_layout()
    plt.savefig("static/revenue.png")

def c(id): #line chart for parked hours of user in each spot
    reserves = Reserves.query.filter_by(uid=id, status="Parked Out").all()
    reserve_ids= []
    durations=[]
    cost=[]
    for r in reserves:
        try:
            p = datetime.strptime(r.parking_timestamp, "%Y-%m-%d %H:%M:%S")
            l = datetime.strptime(r.leaving_timestamp, "%Y-%m-%d %H:%M:%S")
            hour = round((l-p).total_seconds()/3600,2)
            cost.append(str(r.cost))
            reserve_ids.append(f"Reserve {r.id}")
            durations.append(hour)
        except Exception as e:
            print(f"Error: {e}")
            continue             #skip for invalid timestamps
    plt.figure(figsize=(10, 5))
    plt.plot(reserve_ids,durations, marker='o',color="orange")
    plt.xlabel('Parking Reserve ID')
    plt.ylabel('Duration (hours)')
    plt.title('Parking duration per Reservations')
    for i, value in enumerate(durations):
        plt.annotate(('('+str(value)+'hr, ₹'+cost[i]+')'),(reserve_ids[i], durations[i]),textcoords="offset points")
    plt.tight_layout()
    plt.savefig(f"static/{id}_time.png")
    
plt.close()
    