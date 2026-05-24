from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# GANTI dengan connection string MongoDB Atlas kamu
MONGO_URI = "mongodb+srv://DB_Umum:admin123@cluster0.6rwbojg.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)

db = client["blog_db"]
collection = db["artikel"]


# =========================
# Home
# =========================
@app.route("/")
def home():
    return {
        "message": "API Artikel Blog"
    }


# =========================
# Tambah Artikel
# =========================
@app.route("/artikel", methods=["POST"])
def tambah_artikel():

    data = request.json

    artikel = {
        "judul": data["judul"],
        "penulis": data["penulis"],
        "isi": data["isi"]
    }

    collection.insert_one(artikel)

    return jsonify({
        "message": "Artikel berhasil ditambahkan"
    })


# =========================
# Lihat Semua Artikel
# =========================
@app.route("/artikel", methods=["GET"])
def lihat_artikel():

    data = []

    for artikel in collection.find({}, {"_id": 0}):
        data.append(artikel)

    return jsonify(data)


# =========================
# Cari Artikel
# =========================
@app.route("/cari/<judul>", methods=["GET"])
def cari_artikel(judul):

    artikel = collection.find_one(
        {"judul": judul},
        {"_id": 0}
    )

    if artikel:
        return jsonify(artikel)

    return jsonify({
        "message": "Artikel tidak ditemukan"
    })


# =========================
# Run
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)