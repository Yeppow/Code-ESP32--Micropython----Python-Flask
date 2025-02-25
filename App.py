from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(name)

# Koneksi ke MongoDB 
client = MongoClient("mongodb://localhost:27017/")  # MongoDB lokal
db = client["farid_databes"]  
collection = db["farid_collection"]  

# Endpoint untuk menyimpan data
@app.route('/send_data', methods=['POST'])
def receive_data():
    data = request.json  
    
    if data:
        collection.insert_one(data)  # Menyimpan data ke MongoDB
        return jsonify({"message": "Data saved successfully", "status": "success"}), 200
    
    return jsonify({"message": "No data received", "status": "failed"}), 400

if name == 'main':
    app.run(host='0.0.0.0', port=5000, debug=True)
