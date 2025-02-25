from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(name)

# Koneksi ke MongoDB (ganti URL jika pakai server lain)
client = MongoClient("mongodb://localhost:27017/")  # MongoDB lokal
db = client["farid_databes"]  # Nama database
collection = db["farid_collection"]  # Nama koleksi (tabel)

# Endpoint untuk menyimpan data
@app.route('/send_data', methods=['POST'])
def receive_data():
    data = request.json  # Menerima data dalam format JSON
    
    if data:
        collection.insert_one(data)  # Menyimpan data ke MongoDB
        return jsonify({"message": "Data saved successfully", "status": "success"}), 200
    
    return jsonify({"message": "No data received", "status": "failed"}), 400

if name == 'main':
    app.run(host='0.0.0.0', port=5000, debug=True)
