def addtocart():
    id = request.args.get('id')
    prodid = request.args.get("productid")
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("USE CART")
    cur.execute(f"SELECT * FROM {id} WHERE product_id = {prodid}")
    item = cur.fetchone()
    quant = item[1]+1
    if item!=None:
        cur.execute(f"INSERT INTO {id} (productid,quantity) VALUES (%s, %s)", (prodid,1))
    else:
        cur.execute(f"UPDATE {id} SET productid = {prodid}, quantity = {quant}")
    return render_template("cart.html",id=id)
         


;



    return render_template()
