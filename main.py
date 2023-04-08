
from flask import Flask, render_template, request,  flash, redirect, url_for, session
from flask_mysqldb import MySQL
import mysql.connector
import MySQLdb.cursors
import re
from datetime import datetime

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = "achyut"
app.config['MYSQL_HOST'] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "achyut"
app.config["MYSQL_DB"] = "salesquaredb"
mysql = MySQL(app)



@app.route('/', methods = ['GET', 'POST'])
def index():
    # Fetch data from 'users' table
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM electronics LIMIT 4")
    elec = cur.fetchall()
    cur.execute("SELECT * FROM beauty LIMIT 4")
    beau = cur.fetchall()
    cur.execute("SELECT * FROM fashion LIMIT 4")
    fas = cur.fetchall()
    # cur.execute("select * FROM brands")
    # bra = cur.fetchall()
    cur.close()
    return render_template('index.html',elec=elec,beau=beau,fas=fas)

@app.route('/home', methods = ['GET', 'POST'])
def home():
    # Fetch data from 'users' table
    id = request.args.get('id')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM electronics LIMIT 4")
    elec = cur.fetchall()
    cur.execute("SELECT * FROM beauty LIMIT 4")
    beau = cur.fetchall()
    cur.execute("SELECT * FROM fashion LIMIT 4")
    fas = cur.fetchall()
    # cur.execute("select * FROM brands")
    # bra = cur.fetchall()
    cur.close()
    return render_template('home.html',elec=elec,beau=beau,fas=fas, id = id)


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        em = email.split("@")[0]
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        if user:
            flash('Email already exists, please use a different email address.', 'error')
            return redirect(url_for('signup'))
        elif password != confirm_password:
            flash('Passwords do not match, please try again.', 'error')
            return redirect(url_for('signup'),)
        else:
            cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            mysql.connection.commit()
            cur.close()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("USE cart")
            cursor.execute("CREATE TABLE {} LIKE Achyut".format(em))
            cursor.execute("USE orders")
            cursor.execute("CREATE TABLE {} LIKE Achyut".format(em))
            cursor.execute("USE supplies")
            cursor.execute("CREATE TABLE {} LIKE Achyut".format(em))
            cursor.execute("USE salesquaredb")
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/team.html')
def team():
    return render_template('team.html')


@app.route('/sellcategory')
def sell():
    id = request.args.get('id')
    return render_template('categories_sell.html',id=id)

@app.route('/buycategory')
def buy():
    id = request.args.get('id')
    return render_template('categories_buy.html',id=id)

@app.route('/formelectronics', methods = ['GET','POST'])
def add_electronics():
    supplierid=request.args.get('id')
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("show databases")
        name_product = request.form.get('name_product')
        price = request.form.get('price')
        desc = request.form.get('desc')
        category = "electronics"
        now = datetime.now()
        productid = now.strftime("%Y%m%d%H%M%S")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO electronics (productname,unit_price,description,productid,supplierid) VALUES (%s, %s, %s, %s,%s)",(name_product,price,desc,productid,supplierid))
        cur.execute("INSERT INTO products (productname,unit_price,description,category,productid,supplierid) VALUES (%s, %s, %s, %s, %s ,%s)",(name_product,price,desc,category,productid,supplierid))       
        mysql.connection.commit()
        cur.close()
        flash('Product Added Successfully', 'success')
        return redirect(url_for('add_electronics',id=supplierid))
    return render_template('formelectronics.html',id=supplierid )

@app.route('/formbeauty', methods = ['GET','POST'])
def add_beauty():
    supplierid=request.args.get('id')
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("show databases")
        name_product = request.form.get('name_product')
        price = request.form.get('price')
        desc = request.form.get('desc')
        category = "beauty"
        now = datetime.now()
        productid = now.strftime("%Y%m%d%H%M%S")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO beauty (productname,unit_price,description,productid) VALUES (%s, %s, %s, %s)",(name_product,price,desc,productid))
        cur.execute("INSERT INTO products (productname,unit_price,description,category,productid) VALUES (%s, %s, %s, %s, %s)",(name_product,price,desc,category,productid))       
        mysql.connection.commit()
        cur.close()
        flash('Product Added Successfully', 'success')
        return redirect(url_for('add_beauty',id = supplierid))
    return render_template('formbeauty.html',id = supplierid)

@app.route('/formfashion', methods = ['GET','POST'])
def add_fashion():
    supplierid=request.args.get('id')
    if request.method == 'POST':
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("show databases")
        name_product = request.form.get('name_product')
        price = request.form.get('price')
        desc = request.form.get('desc')
        category = "fashion"
        now = datetime.now()
        productid = now.strftime("%Y%m%d%H%M%S")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO fashion (productname,unit_price,description,productid,supplierid) VALUES (%s, %s, %s, %s, %s)",(name_product,price,desc,productid,id))
        cur.execute("INSERT INTO products (productname,unit_price,description,category,productid,supplierid) VALUES (%s, %s, %s, %s, %s, %s)",(name_product,price,desc,category,productid,id))       
        mysql.connection.commit()
        cur.close()
        flash('Product Added Successfully', 'success')
        return redirect(url_for('add_fashion',id=supplierid))
    return render_template('formfashion.html',id=supplierid)

@app.route('/formhome', methods = ['GET','POST'])
def add_home():
    supplierid=request.args.get('id')
    if request.method == 'POST':
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("show databases")
        name_product = request.form.get('name_product')
        price = request.form.get('price')
        desc = request.form.get('desc')
        category = "homeandkitchen"
        now = datetime.now()
        productid = now.strftime("%Y%m%d%H%M%S")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO homeandkitchen (productname,unit_price,description,productid,supplierid) VALUES (%s, %s, %s, %s, %s)",(name_product,price,desc,id))
        cur.execute("INSERT INTO products (productname,unit_price,description,category,productid,supplierid) VALUES (%s, %s, %s, %s, %s, %s)",(name_product,price,desc,category,id))       
        mysql.connection.commit()
        cur.close()
        flash('Product Added Successfully', 'success')
        return redirect(url_for('add_home',id=supplierid))
    return render_template('formhome.html',id=supplierid)

@app.route('/formsports', methods = ['GET','POST'])
def add_sports():
    supplierid=request.args.get('id')
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("show databases")
        name_product = request.form.get('name_product')
        price = request.form.get('price')
        desc = request.form.get('desc')
        category = "sports"
        now = datetime.now()
        productid = now.strftime("%Y%m%d%H%M%S")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO sports (productname,unit_price,description,productid,supplierid) VALUES (%s, %s, %s, %s , %s)",(name_product,price,desc,productid,id))
        cur.execute("INSERT INTO products (productname,unit_price,description,category,productid,supplierid) VALUES (%s, %s, %s, %s, %s, %s)",(name_product,price,desc,category,productid,id))       
        mysql.connection.commit()
        cur.close()
        flash('Product Added Successfully', 'success')
        return redirect(url_for('add_sports',id=supplierid))
    return render_template('formsports.html',id=supplierid)

@app.route('/formbooks', methods = ['GET','POST'])
def add_books():
    supplierid=request.args.get('id')
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("show databases")
        name_product = request.form.get('name_product')
        price = request.form.get('price')
        desc = request.form.get('desc')
        category = "books"
        now = datetime.now()
        productid = now.strftime("%Y%m%d%H%M%S")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO books (productname,unit_price,description,productid,supplierid) VALUES (%s, %s, %s, %s, %s)",(name_product,price,desc,productid,id))
        cur.execute("INSERT INTO products (productname,unit_price,description,category,productid,supplierid) VALUES (%s, %s, %s, %s, %s, %s)",(name_product,price,desc,category,productid,id))       
        mysql.connection.commit()
        cur.close()
        flash('Product Added Successfully', 'success')
        return redirect(url_for('add_books',id=supplierid))
    return render_template('formbooks.html',id=supplierid)

# @app.route('/product')
# def product():
#     userid = request.args.get('userid')
#     productid = request.args.get('productid')
#     cur = mysql.connection.cursor()
#     cur.execute("use salesquaredb")
#     cur.execute(f"SELECT * FROM products WHERE productid = {productid}")
#     product = cur.fetchone()
#     cur.close
#     render_template("product.html",product=product, userid = userid)

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/myOrders')
def myOrders():
    return render_template('myOrders.html')

@app.route('/mySupplies')
def mySupplies():
    return render_template('mySupplies.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("show databases")
        email = request.form.get('email')
        password = request.form.get('password')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        mysql.connection.commit()
        cur.close()
        if user[1]!=None:
            if user[2]!=password:
                flash("wrong password", 'error')
                return redirect(url_for('login'))
            else:
                mysql.connection.commit()
                cur.close()
                k = email.split("@")
                id = k[0]
                return redirect(url_for('home',id=id))
        else:
            flash("email doesn't exist, please signup.", 'error')
    return render_template('login.html')


@app.route('/checkout')
def checkout():
    productid = request.args.get('productid')
    email = request.args.get('email')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.execute("SELECT * FROM products WHERE productid = %s",(productid,))
    prod = cur.fetchone()
    return render_template("checkout.html",user=user,prod=prod)
    
@app.route('/cart')
def cart():
    id = request.args.get('id')
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("USE CART")
    cur.execute(f"SELECT * FROM {id}")
    car = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template("cart.html",car=car)


# @app.route('/orders')
# def orders():
#     id = request.args.get('id')
#     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cur.execute("USE orders")
#     cur.execute(f"SELECT * FROM {id}")
#     ord = cur.fetchall()
#     mysql.connection.commit()
#     cur.close()
#     return render_template("orders.html",ord=ord)
# @app.route('/supplies')
# def supplies():
#     id = request.args.get('id')
#     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cur.execute("USE supplies")
#     cur.execute(f"SELECT * FROM {id}")
#     sup = cur.fetchall()
#     mysql.connection.commit()
#     cur.close()
#     return render_template("supplies.html",sup=sup)

@app.route('/products')
def products():
    id=request.args.get('id')
    cat=request.args.get('category')
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("USE salesquaredb")
    cur.execute(f"SELECT * FROM {cat}")
    prod = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template("products.html",cat=cat,prod=prod,id=id)

if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/electronics', methods = ['GET', 'POST'])
# def product(id=productid):

#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("select * from electronics")
#     data = cursor.fetchall()
#     return render_template("product.html")

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         cur = mysql.connection.cursor()
#         result = cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
#         if result > 0:
#             data = cur.fetchone()
#             session['username'] = data['username']
#             return redirect(url_for('homepage'))
#         else:
#             return render_template('login.html', error='Invalid email or password')
#     return render_template('login.html')

#
# @app.route("/")
# def home():
#
#     return render_template("index.html")
#
# @app.route("/orders")
# def orders():
#     return render_template("order.html")
#
# @app.route("/cart")
# def cart():
#     return render_template("cart.html")
#
# @app.route("/account")
# def account()
#     return render_template("account.html")
#
# @app.route("/categories")
# def categories()
#     return render_template("categories.html")
