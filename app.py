from flask import Flask, request, Response
from flask_cors import CORS
import json
import traceback
import dbconnect
app = Flask(__name__)
CORS(app)


@app.get("/candy")
def get_candy():
    candies = None
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    cursor.execute(
        "SELECT name, description, price, image_url, id FROM candy ORDER BY id DESC")
    candies = cursor.fetchall(
    )
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    if candies == None:
        return Response("There was an error getting the candies", mimetype='text/plain', status=500)
    else:
        candies_json = json.dumps(candies, default=str)
        return Response(candies_json, mimetype='application/json', status=200)


@app.post("/candy")
def new_candy():
    try:
        # this comes from user input
        name = request.json['name']
        desc = request.json['desc']
        price = float(request.json['price'])
        img = request.json['img']
    except:
        traceback.print_exc()
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    new_id = -1
    try:
        cursor.execute(
            "INSERT INTO candy(name, description, price, image_url) VALUES(?, ?, ?, ?)", [name, desc, price, img])
        conn.commit()
        new_id = cursor.lastrowid
    except:
        traceback.print_exc()
        print("Sonething went wrong, please try again")
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    if new_id == -1:
        return Response("New candy addition failed", mimetype='text/plain   ', status=500)
    else:
        candy_json = json.dumps([name, desc, price, img, new_id], default=str)
        return Response(candy_json, mimetype='application/json', status=200)


@app.patch("/candy")
def update_candy():
    candy_id = None
    try:
        # .get here returns none if the input is empty
        candy_id = int(request.json['candyId'])
        name = request.json.get('name')
        desc = request.json.get('desc')
        price = request.json.get('price')
        if price != None and price != "":
            price = float(price)
        img = request.json.get('img')
    except:
        traceback.print_exc()
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    # set empty array that we can append/push to it
    candies_args = []
    if candy_id != None and candy_id != "":
        try:
            if name != None and name != "":
                cursor.execute("UPDATE candy SET name = ? WHERE id = ?",
                               [name, candy_id])
                conn.commit()
                # adds this argument to candy_args = [] if it exists
                candies_args.append(name)
        except:
            traceback.print_exc()
        # try to put these all into one cursor.execute
        try:
            if desc != None and desc != "":
                cursor.execute("UPDATE candy SET description = ? WHERE id = ?",
                               [desc, candy_id])
                conn.commit()
                # adds this argument to candy_args = [] if it exists
                candies_args.append(desc)
        except:
            traceback.print_exc()
        try:
            if price != None and price != "":
                cursor.execute("UPDATE candy SET price = ? WHERE id = ?",
                               [price, candy_id])
                conn.commit()
                # adds this argument to candy_args = [] if it exists
                candies_args.append(price)
        except:
            traceback.print_exc()
        try:
            if img != None and img != "":
                cursor.execute("UPDATE candy SET image_url = ? WHERE id = ?",
                               [img, candy_id])
                conn.commit()
                # adds this argument to candy_args = [] if it exists
                candies_args.append(img)
        except:
            traceback.print_exc()
    else:
        return Response("Something went wrong", mimetype='text/plain', status=400)
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    candy_json = json.dumps(candies_args, default=str)
    return Response("Candy name updated", mimetype='text/plain', status=200)


@app.delete("/candy")
def delete_candy():
    try:
        candy_id = int(request.json['candyId'])
    except:
        traceback.print_exc()
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    try:
        cursor.execute("DELETE FROM candy WHERE id = ?", [candy_id, ])
        conn.commit()
    except:
        traceback.print_exc()
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)

    return Response("Candy deleted!", mimetype='text/plain', status=200)


app.run(debug=True)
