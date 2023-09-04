from flask import Flask,jsonify,render_template, request, redirect,session
from db import *
from flask_login import *
from werkzeug.security import check_password_hash

app=Flask(__name__)

# configuring mongodb
app.config['MONGODB_HOST']=url
app.config['SECRET_KEY'] = 'zealousrazzak'
mydb.init_app(app)

loginManager=LoginManager(app)
loginManager.login_view='/login'


@loginManager.user_loader
def loadUser(userId):
    return User.objects(id=userId).first()

@app.after_request
def add_cache_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/login",methods=['GET','POST'])
def loggingIn():
    if request.method=="GET":
        return render_template("login.html")
    else:
        user=User.objects(username=request.form['username']).first()
        if user and check_password_hash(user.password,request.form['password']):
            login_user(user)
            print("login success")
            return redirect("/home")
        else:
            return redirect("/login")
        
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route("/signup",methods=['GET','POST'])
def register():
    if request.method=="GET":
        return render_template('signup.html')
    else:
        user=User()
        user.username=request.form['username']
        user.email=request.form['email']
        pas=request.form['password']
        user.set_password(pas)
        print(user.username,user.password,user.email)
        
        user.save()
        
        return redirect("/login")
        

@app.route("/shortlist",methods=['GET','POST'])
@login_required
def performFilter():
    if request.method=="GET":
        return render_template("filter.html")
    else:
        mod=request.form['model']
        tp=request.form['type']
        ram=request.form['ram']
        cost=request.form['price']
        
        if mod!="" and tp=="Select type" and ram=="" and cost=="":
            collected=Laptop.objects(model__startswith=mod)
            return render_template("view.html",data=collected)
        elif mod=="" and tp!="Select type" and ram=="" and cost=="":
            collected=Laptop.objects(type__iexact=tp)
            return render_template("view.html",data=collected)
        elif mod=="" and tp=="Select type" and ram!="" and cost=="":
            ram=int(ram)
            collected=Laptop.objects(ram__gte=ram)
            return render_template("view.html",data=collected)
        elif mod=="" and tp=="Select type" and ram=="" and cost!="":
            cost=int(cost)
            collected=Laptop.objects(price__lte=cost)
            return render_template("view.html",data=collected)
        else:
            return render_template("filter.html")

@app.route("/erase/<mod>")
@login_required
def performDelete(mod):
    collected=Laptop.objects(model=mod).first()
    collected.delete()
    return redirect("/list")

@app.route("/update/<mod>",methods=["GET","POST"])
@login_required
def performEdit(mod):
    if request.method=="GET":
        collected=Laptop.objects(model=mod).first()
        return render_template("edit.html",data=collected)
    else:
        model=request.form['model']
        serial=request.form['serial']
        ram=int(request.form['ram'])
        ssd=int(request.form['ssd'])
        price=int(request.form['price'])
        stock=int(request.form['stock'])
        type=request.form['type']
        
        Laptop.objects(model=model).update_one(set__serial=serial,set__ram=ram,
                                               set__ssd=ssd,set__price=price,set__stock=stock,
                                               set__type=type)
        return redirect("/list")

@app.route("/pick/<mod>")
@login_required
def showRead(mod):
    collected=Laptop.objects(model=mod).first()
    return render_template("read.html",data=collected)

@app.route("/new",methods=['GET','POST'])
@login_required
def newOne():
    if request.method=="GET":
        return render_template("newlaptop.html")
    else:
        laptop=Laptop()
        laptop.model=request.form['model']
        laptop.serial=request.form['serial']
        laptop.ram=int(request.form['ram'])
        laptop.ssd=int(request.form['ssd'])
        laptop.price=int(request.form['price'])
        laptop.stock=int(request.form['stock'])
        laptop.type=request.form['type']
        
        laptop.save()
        
        return redirect("/list")

@app.route("/home")
@login_required
def showHome():
    return render_template("navigation.html")

@app.route("/list")
@login_required
def listAll():
    collected=Laptop.objects.all()
    return render_template("view.html",data=collected)

@app.route("/test")
@login_required
def checkConnection():
    #return make_response("<h1>Hell</h1>")
    return jsonify(Laptop.objects.all())

if __name__=="__main__":
    app.run(debug=True,port=9988)