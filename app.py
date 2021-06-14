from flask import Flask, app, request, Response
from flask_cors import CORS
import json
import traceback
import dbconnect
app = Flask(__name__)
CORS(app)


@app.get("/candy")
def get_candy():
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    cursor.execute(
        "SELECT name, description, price, image_url, id FROM candy ORDER BY id DESC")
    candies = cursor.fetchall(
    )
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)

    candies_json = json.dumps(candies, default=str)
    return Response(candies_json, mimetype='application/json', status=200)


@app.post("/candy")
def new_candy():
    try:
        name = request.json['name']
        desc = request.json['desc']
        price = float(request.json['price'])
        img = request.json['img']
    except:
        traceback.print_exc()
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    try:
        cursor.execute(
            "INSERT INTO candy(name, description, price, image_url) VALUES(?, ?, ?, ?)", [name, desc, price, img])
        conn.commit()
    except:
        traceback.print_exc()
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)

    candy_json = json.dumps([name, desc, price, img], default=str)
    return Response(candy_json, mimetype='application/json', status=200)


@app.patch("/candy")
def update_candy():
    name = ""
    desc = ""
    price = None
    img = ""
    candy_id = None
    try:
        name = request.json['name']
        candy_id = int(request.json['candyId'])
        desc = request.json['desc']
        price = float(request.json['price'])
        img = request.json['img']
    except:
        traceback.print_exc()
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    # there has to be a better way to do this......
    try:
        if name != "":
            cursor.execute("UPDATE candy SET name = ?, description = description, price = price, image_url = image_url WHERE id = ?",
                           [name, candy_id])
            conn.commit()
    except:
        traceback.print_exc()
    try:
        if desc != "":
            cursor.execute("UPDATE candy SET description = ?, name = name, price = price, image_url = image_url WHERE id = ?",
                           [desc, candy_id])
            conn.commit()
    except:
        traceback.print_exc()
    try:
        if price != None:
            cursor.execute("UPDATE candy SET price = ?, name = name, description = description, image_url = image_url WHERE id = ?",
                           [price, candy_id])
            conn.commit()
    except:
        traceback.print_exc()
    try:
        if img != "":
            cursor.execute("UPDATE candy SET image_url = ?, name = name, description = description, price = price WHERE id = ?",
                           [img, candy_id])
            conn.commit()
    except:
        traceback.print_exc()
    # if desc != None:
        # try:
        #     cursor.execute("UPDATE candy SET description = ?, name = name, price = price, image_url = image_url WHERE id = ?",
        #                    [desc, candy_id])
        #     conn.commit()
        # except:
        #     traceback.print_exc()

    # if price != None and candy_id != None:
    # try:
    #     cursor.execute("UPDATE candy SET price = ? WHERE price = ? AND id = ?",
    #                    [price, old_price, candy_id])
    #     conn.commit()
    # except:
    #     traceback.print_exc()
    # # if img != None and candy_id != None:
    # try:
    #     cursor.execute("UPDATE candy SET image_url = ? WHERE image_url = ? AND id = ?",
    #                    [img, old_img, candy_id])
    #     conn.commit()
    # except:
    #     traceback.print_exc()
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    candy_json = json.dumps([name, candy_id, desc, price, img], default=str)
    # candy_dictionary = {}
    # for info in updated_candy:
    #     candy_dictionary = {
    #         "name": info[0],
    #         "desc": info[1],
    #         "price": info[2],
    #         "img": info[3]
    #     }
    candy_json = json.dumps(candy_json, default=str)
    return Response(candy_json, mimetype='application/json', status=200)


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
