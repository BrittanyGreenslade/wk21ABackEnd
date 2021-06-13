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
    cursor.execute("SELECT name, description, price, image_url, id FROM candy")
    candies = cursor.fetchall(
    )
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    candies_json = json.dumps(candies, default=str)
    return Response(candies_json, mimetype='application/json', status=200)

# @app.post("/candy")
# @app.patch("/candy")
# @app.delete("/candy")


app.run(debug=True)
