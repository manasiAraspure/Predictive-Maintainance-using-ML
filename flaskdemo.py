from flask import Flask, redirect, render_template, request,make_response,json
from flask_sqlalchemy import  SQLAlchemy
import random  
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:code123@localhost/customer"
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)


class Pumps(db.Model):
    # sno = db.Column(db.Integer,autoincrement = True)
    pId = db.Column(db.String(200),nullable=False,primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

class Customer(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    address = db.Column(db.String(500),nullable=False)
    phno = db.Column(db.String(200),nullable=False)
    WpId = db.Column(db.String(200), db.ForeignKey(Pumps.pId),nullable=False, )
    

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route("/")
def front():
    return render_template("frontPdM.html")

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if request.method=="POST":
        name=request.form['name']
        address=request.form['address']
        phno=request.form['phno']
        pId=request.form['pId']
        customer= Customer(name=name, address=address, phno=phno, WpId=pId)
        pumps = Pumps(pId= pId, name = name)
        db.session.add(customer)
        db.session.add(pumps)
        db.session.commit()
    allCustomer= Customer.query.all()    
    return render_template("dashboardPdM.html",allCustomer=allCustomer)

@app.route("/delete/<int:sno>")
def delete(sno):
    customer=Customer.query.filter_by(sno=sno).first()
    db.session.delete(customer)
    db.session.commit()
    return redirect('/dashboard')

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        name=request.form['name']
        address=request.form['address']
        phno=request.form['phno']
        pId=request.form['pId']
        customer=Customer.query.filter_by(sno=sno).first()
        customer.name=name
        customer.address=address
        customer.phno=phno
        customer.pId=pId
        db.session.add(customer) 
        db.session.commit()
        return redirect("/dashboard")
    customer=Customer.query.filter_by(sno=sno).first()
    return render_template("updatePdM.html", customer=customer)


@app.route("/addpump/<name>", methods=['GET', 'POST'])
def addpump(name):
    if request.method == 'POST':
        pId=request.form['pId']
        cust = Customer.query.filter_by(name=name).first()
        print(pId,cust.name)
        pumps=Pumps(pId=pId,name=cust.name)
        db.session.add(pumps)
        print(cust.name,cust.address,cust.phno,cust.WpId)
        customer = Customer(name=cust.name,address=cust.address,phno=cust.phno,WpId=pId) 
        db.session.add(customer)
        db.session.commit()
        return redirect("/dashboard")
    
    allPumps= Pumps.query.filter_by(name=name).first()    
    return render_template("addpumpPdM.html",allPumps=allPumps,name=name)





@app.route("/pumps/<int:sno>",methods=['GET', 'POST'])
def pump(sno):
    if request.method=="POST":
        name=request.form['name']
        address=request.form['address']
        phno=request.form['phno']
        pId=request.form['pId']
        customer= Customer(name=name, address=address, phno=phno, pId=pId)
        db.session.add(customer)
        db.session.commit()
    allCustomer= Customer.query.filter_by(sno=sno).first()
    return render_template("pumpDataPdM.html",allCustomer=allCustomer)


@app.route("/pumpData")
# def pumpData():
    # @app.route('/data', methods=["GET", "POST"])
def data():
    # Data Format
    # [TIME, Temperature, Voltage, Vibration , Accoustic]
    # data = requests.get("http://localhost:3000/sensors").json()
    # values = []
    # labels = []
    # values.append(time() * 1000)
    # for d in data:
    #     labels.append(d)
    #     values.append(data[d])
    # print(values)

    values = [random.randint(1,200),random.randint(1,200),random.randint(30,100),random.randint(100,200)]

    response = make_response(json.dumps(values))
    # print(response.json())
    response.content_type = 'application/json'
    return response

    

if __name__=="__main__":
    app.run(debug=True)