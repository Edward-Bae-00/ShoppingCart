from flask import Flask, session, render_template, redirect, url_for, request
import datetime
import sqlite3

app = Flask('app')

app.debug = True
app.secret_key = "thingy mabob"

productId = -1
counter = -1

# gets the number of items currently in the cart
def getLoginDetails():
  #checks if items is in session and 
  if 'items' not in session:  
    noOfItems = 0
  else:
    noOfItems = 0
    for i in session['num']:
      noOfItems += int(i)
  return (noOfItems)

# the login page
@app.route('/login', methods=['GET','POST'])
def login():
  # connect the database
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  
  if request.method == 'POST':
    if 'login' in request.form:
      username = request.form['username']
      cursor.execute("SELECT username, password FROM users WHERE username = ?", (username,))
      data = cursor.fetchall()
      cursor.execute('SELECT DISTINCT(type) FROM items')
      categoryData = cursor.fetchall()
      connection.close()

      if len(data) == 0 or data[0]['password'] != request.form['password']:
        return render_template('login.html', success=False)
      else:
        session['username'] = request.form['username']
        return redirect('/')
    elif "logout" in request.form:
     return redirect('/logout')
    elif "adduser" in request.form:
      return redirect('/adduser')
  else:
    cursor.execute('SELECT DISTINCT(type) FROM items')
    categoryData = cursor.fetchall()
    connection.close()
    return render_template('login.html', categoryData=categoryData)


@app.route('/adduser', methods = ['GET', 'POST'])
def add_user():
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    if (request.method == 'POST'):
          username = request.form['username']
          password = request.form['password']
          fname = request.form['fname']
          lname = request.form['lname']

          cursor.execute("INSERT INTO users VALUES(?,?,?,?)", (username, password, fname, lname))
          connection.commit()
          cursor.execute('SELECT DISTINCT(type) FROM items')
          categoryData = cursor.fetchall()
          connection.close()

          return render_template("login.html", categoryData=categoryData)
    cursor.execute('SELECT DISTINCT(type) FROM items')
    categoryData = cursor.fetchall()
    connection.close()
    return render_template("form.html", categoryData=categoryData)


@app.route('/', methods=['GET', 'POST'])
def store():
  # gets the number of items
  noOfItems = getLoginDetails()  
  # connect the database
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  # get the products info to display on the page
  cursor.execute('SELECT DISTINCT(type) FROM items')
  categoryData = cursor.fetchall()
  cursor.execute('SELECT id, name, image, price, type FROM items')
  productData = cursor.fetchall()
  # gets the value of search
  thing = request.args.get('searchQuery')
  # print(thing)

  # if the search is empty then show all the products
  # if the search is not empty then get the info of the product and show that product
  if thing is None:
    return render_template('store.html', categoryData=categoryData, productData = productData, noOfItems = noOfItems)
  else:
    cursor.execute("SELECT id, name, image, price, type, inventory FROM items WHERE name = ?", (thing,))
    productData = cursor.fetchone()
    # print(productData)
    # print(productData[0])
    # print(productData[1])
    # print(productData[3])
    return render_template("productDescription.html", data=productData, noOfItems = noOfItems, categoryData=categoryData) 


@app.route("/productDescription")
def productDescription():
  # gets the number of items
  noOfItems = getLoginDetails()  
  # connect the database
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()

  global productId
  productId = request.args.get('productId')
  cursor.execute('SELECT id, name, image, price, type, inventory FROM items WHERE id = ?', (productId, ))
  productData = cursor.fetchone()
  # print(productData[2])
  cursor.execute('SELECT DISTINCT(type) FROM items')
  categoryData = cursor.fetchall()
  cursor.close()
  return render_template("productDescription.html", data=productData, noOfItems = noOfItems, categoryData=categoryData)
    
@app.route("/displayCategory")
def displayCategory():
  noOfItems = getLoginDetails()
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  type = request.args.get('categoryId')
  print(type)
  cursor = connection.cursor()
  cursor.execute("SELECT id, name, image, price, type FROM items WHERE items.type = ?", (type, ))
  data = cursor.fetchall()
  cursor.execute('SELECT DISTINCT(type) FROM items')
  categoryData = cursor.fetchall()
  return render_template('category.html', data=data, noOfItems=noOfItems, categoryData=categoryData)



@app.route("/addToCart", methods=['POST'])
def addToCart():
  # checks if the request is a post
  if (request.method == 'POST'):
    # checks if the user is signed in and if they are not go to the login page
    # also check if items are already in the cart. If they are not then initial the variable
    if 'username' not in session:
      return redirect(url_for('login'))
    else:
      if 'items' not in session:
        session['items'] = []
        session['num'] = []
      

      if productId in session['items']:
        for i in range(len(session['items'])):
          if (session['items'][i] == productId):
            temp = session['num']
            temp[i] = int(temp[i]) + int(request.form['counter'])
            connection = sqlite3.connect("myDatabase.db")
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, image, price, type, inventory FROM items WHERE id = ?", (session['items'][i], ))
            data = cursor.fetchall()
            print(data[0][5])
            if (temp[i] > int(data[0][5])):
              temp[i] = int(data[0][5])
            session['num'] = temp
      else:
        temp = session['items']
        temp.append(productId)
        session['items'] = temp

        print(productId)
        print(session['items'])


        temp = session['num']
        temp.append(int(request.form['counter']))
        session['num'] = temp
    return redirect(url_for('store'))
  



@app.route("/cart", methods=['GET', 'POST'])
def cart():
    if 'username' not in session:
      return redirect(url_for('login'))
    noOfItems = getLoginDetails()
    # username = session['username']
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    products = []
    if request.method == 'POST':
      # print("goes here")
      return redirect(url_for('checkout'))
    if 'items' not in session:
        session['items'] = []
        session['num'] = []
    for i in session['items']:
      productId = int(i)
      cursor.execute("SELECT id, name, image, price, type FROM items WHERE items.id = ?", (productId, ))
      products.append(cursor.fetchall())

    totalPrice = 0.00
    for i in range(len(products)):
      totalPrice += products[i][0][3] * int(session['num'][i])
    print(totalPrice)

    cursor.execute('SELECT DISTINCT(type) FROM items')
    categoryData = cursor.fetchall()
    connection.close()
    return render_template("cart.html", products = products, totalPrice=totalPrice, noOfItems=noOfItems, categoryData=categoryData, amount = session['num'])




@app.route("/removeFromCart")
def removeFromCart():
    if 'username' not in session:
      return redirect(url_for('login'))
    username = session['username']
    productId = request.args.get('productId')
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    print(productId)
    for i in range(len(session['items'])):
      if (session['items'][i] == productId):
        print('hits')
        temp1 = session['items']
        temp1.pop(i)
        session['items'] = temp1

        temp2 = session['num']
        temp2.pop(i)
        session['num'] = temp2
        break
    connection.close()
    return redirect('/')




@app.route('/logout', methods=['GET', 'POST'])
def logout():
  session.clear()
  return redirect('/')



@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
  if 'username' not in session:
    return redirect(url_for('login'))
  else:
    noOfItems = getLoginDetails()
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if noOfItems == 0:
      return redirect('/')
    else:
      products = []
      for i in session['items']:
        cursor.execute("SELECT id, name, image, price, type FROM items WHERE items.id = ?", (i[0], ))
        products.append(cursor.fetchall())

      totalPrice = 0.00
      for i in range(len(products)):
        totalPrice += products[i][0][3] * int(session['num'][i])


      items = session.pop('items', None)
      num = session.pop('num', None)
      global counter
      if (counter == -1):
        counter = 1
      else:
        counter = counter + 1
      cursor.execute("INSERT INTO orders VALUES(?,?,?,?)", (int(counter), session['username'], totalPrice, datetime.datetime.now()))
      connection.commit()

      for i in range(len(items)):
        thingy = cursor.lastrowid
        productId = int(items[i])
        cursor.execute("SELECT id, name, image, price, type FROM items WHERE items.id = ?", (productId, ))
        thing = cursor.fetchone()
        print('thing')
        print(thing)
        print(thing[0])
        cursor.execute("INSERT INTO order_items VALUES(?,?,?,?,?)", (thingy, int(counter), items[i], num[i], thing[3] ))
        connection.commit()
      return redirect('/')
    


@app.route('/order')
def orders():
  noOfItems = getLoginDetails()
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  if 'username' not in session:
    return redirect(url_for('login'))
  cursor.execute("SELECT order_id, username, total_price, order_date FROM orders WHERE username = ? ", (session['username'], ))
  thing = cursor.fetchall()
  print(thing)
  print(thing[0])
  print(thing[0][0])
  cursor.execute('SELECT DISTINCT(type) FROM items')
  categoryData = cursor.fetchall()
  connection.close()
  return render_template("order.html", noOfItems=noOfItems, orderinfo = thing, categoryData=categoryData)




app.run(host='0.0.0.0', port=8080)