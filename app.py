from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from pymysql.err import OperationalError
from sqlalchemy.exc import OperationalError
from datetime import datetime
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False

db=SQLAlchemy(app)

@app.route('/')
def check_connection():
    try:
        db.session.execute(text("SELECT *from users"))
        return "Connection to MySQL database successful!"
    except OperationalError as e:
        return f"Connection failed: {str(e)}"
    
class Users(db.Model):
   __tablename__="users"
   id=db.Column(db.Integer,primary_key=True)
   email=db.Column(db.String(100))
   username=db.Column(db.String(100))
   password=db.Column(db.String(200))
   status=db.Column(db.String)

@app.route('/user')
def user_register():
    return render_template('register.html')

@app.route('/register',methods=['POST'])
def register_user():
    username=request.form['username']
    email=request.form['email']
    id=request.form['id']
    password=request.form['password']
    status=request.form['status']
    
    new_user= Users(username=username, email=email, id=id, password=password, status=status)
    db.session.add(new_user)
    db.session.commit()

    return "Data inserted."

@app.route('/Listuser')
def list_user():
    users=Users.query.first()
    return f"username: {users.username}"

@app.route('/Listalluser')
def all_user():
    users=Users.query.all()
    return render_template("users.html", users=users)

#@app.route('/delete')
#def delete(id):

#return redirect("/Listalluser")

@app.route('/updateuser/<int:id>')
def updateuser(id):
    users=Users.query.get(id)
    return render_template('updateuser.html', users=users)

 
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    users = Users.query.get(id)
    if request.method == 'POST':
        users.username = request.form['username']
        users.email = request.form['email']
        users.password = request.form['password']
        users.status = request.form['status']
        db.session.commit()
        return redirect(url_for('all_user'))  # Correct use of url_for
    return render_template('updateuser.html', users=users)

@app.route('/deleteuser/<int:id>')
def deleteuser(id):
    users=Users.query.get(id)   #users=Users.query.get(id=404)
    if users:
        db.session.delete(users)
        db.session.commit()
        return redirect('/Listalluser')
    
#Create application to collect a visitor information of pokhara university. Appliction should collect following information.
#- visitor name, address, contact number, gender, purpose of visit, visit date, visit time, concerned department.

class Visitors(db.Model):
    __tablename__ = "visitor"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),)
    address = db.Column(db.String(20),)
    number = db.Column("number", db.String(300))
    gender = db.Column(db.String(400), nullable=False)
    Description = db.Column("Description", db.Text,)
    visitdate = db.Column("visitdate", db.Date,)
    visittime = db.Column("visittime", db.Time,)
    Department = db.Column("Department", db.String(500),)

   # Route to show the form
# @app.route('/form')
# def form():
#     return render_template('visitor_info.html')

#route to render the form data
@app.route('/visitorinformation', methods=['GET', 'POST'])
def visitorinformation():
  if request.method=='POST':
    new_user=Visitors(
    username=request.form['username'],
    address=request.form['address'],
    number=request.form['number'],
    gender=request.form['gender'],
    Description=request.form['Description'],
    visitdate=request.form['visitdate'],
    visittime=request.form['visittime'],
    Department=request.form['Department']
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect('/Listallvisitor')
  return render_template('visitor_info.html')

@app.route('/Listallvisitor')
def all_visitor():
    visitors=Visitors.query.all()
    return render_template("visitors.html", visitors=visitors)
    
    
if __name__ == '__main__':
    app.run(debug=True)