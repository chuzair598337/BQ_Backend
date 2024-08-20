import os

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Set the database path relative to the current file location
database = os.path.join(os.path.dirname(__file__), '..', 'Data', 'BQ_Database.db')

# Function to connect to the database
def connect_db():
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row 
    return conn

# Function to convert row to dictionary
def row_to_dict(row):
    return {key: row[key] for key in row.keys()}

# ------------------- Surah Routes -------------------

# Select All Surahs
@app.route('/api/surahs', methods=['GET'])
def get_surahs():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Surahs")
    surahs = cursor.fetchall()
    conn.close()
    return jsonify([row_to_dict(row) for row in surahs])

# Select Surah by ID
@app.route('/api/surahs/<int:surah_id>', methods=['GET'])
def get_surah(surah_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Surah WHERE surahID=?", (surah_id,))
    surah = cursor.fetchone()
    conn.close()
    if surah:
        return jsonify(row_to_dict(surah))
    else:
        return jsonify({"error": "Surah not found"}), 404

# Create a new Surah
@app.route('/api/surahs', methods=['POST'])
def create_surah():
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Surah (surahEnglishName, surahArabicName, surahEnglishMeaning, surahVerses)
        VALUES (?, ?, ?, ?)""",
        (data['surahEnglishName'], data['surahArabicName'], data['surahEnglishMeaning'], data['surahVerses']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Surah created successfully"}), 201

# Update Surah by ID
@app.route('/api/surahs/<int:surah_id>', methods=['PUT'])
def update_surah(surah_id):
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Surah
        SET surahEnglishName=?, surahArabicName=?, surahEnglishMeaning=?, surahVerses=?
        WHERE surahID=?""",
        (data['surahEnglishName'], data['surahArabicName'], data['surahEnglishMeaning'], data['surahVerses'], surah_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Surah updated successfully"})

# Delete Surah by ID
@app.route('/api/surahs/<int:surah_id>', methods=['DELETE'])
def delete_surah(surah_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Surah WHERE surahID=?", (surah_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Surah deleted successfully"})

# ------------------- QuranEPak Routes -------------------

# Select All QuranEPak entries
@app.route('/api/quranepak', methods=['GET'])
def get_quranepak():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM QuranEPak")
    quranepak = cursor.fetchall()
    conn.close()
    return jsonify([row_to_dict(row) for row in quranepak])

# Select QuranEPak by ID
@app.route('/api/quranepak/<int:quranepak_id>', methods=['GET'])
def get_quranepak_by_id(quranepak_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM QuranEPak WHERE quranEPakID=?", (quranepak_id,))
    quranepak = cursor.fetchone()
    conn.close()
    if quranepak:
        return jsonify(row_to_dict(quranepak))
    else:
        return jsonify({"error": "QuranEPak entry not found"}), 404

# Create a new QuranEPak entry
@app.route('/api/quranepak', methods=['POST'])
def create_quranepak():
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO QuranEPak (surahID, verseID, verseFileName, verseArabicText, verseUrduText)
        VALUES (?, ?, ?, ?, ?)""",
        (data['surahID'], data['verseID'], data['verseFileName'], data['verseArabicText'], data['verseUrduText']))
    conn.commit()
    conn.close()
    return jsonify({"message": "QuranEPak entry created successfully"}), 201

# Update QuranEPak by ID
@app.route('/api/quranepak/<int:quranepak_id>', methods=['PUT'])
def update_quranepak(quranepak_id):
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE QuranEPak
        SET surahID=?, verseID=?, verseFileName=?, verseArabicText=?, verseUrduText=?
        WHERE quranEPakID=?""",
        (data['surahID'], data['verseID'], data['verseFileName'], data['verseArabicText'], data['verseUrduText'], quranepak_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "QuranEPak entry updated successfully"})

# Delete QuranEPak by ID
@app.route('/api/quranepak/<int:quranepak_id>', methods=['DELETE'])
def delete_quranepak(quranepak_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM QuranEPak WHERE quranEPakID=?", (quranepak_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "QuranEPak entry deleted successfully"})

# ------------------- Bayans Routes -------------------

# Select All Bayans
@app.route('/api/bayans', methods=['GET'])
def get_bayans():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Bayans")
    bayans = cursor.fetchall()
    conn.close()
    return jsonify([row_to_dict(row) for row in bayans])

# Select Bayans by ID
@app.route('/api/bayans/<int:bayan_id>', methods=['GET'])
def get_bayan(bayan_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Bayans WHERE bayanID=?", (bayan_id,))
    bayan = cursor.fetchone()
    conn.close()
    if (bayan):
        return jsonify(row_to_dict(bayan))
    else:
        return jsonify({"error": "Bayan not found"}), 404

# Create a new Bayan
@app.route('/api/bayans', methods=['POST'])
def create_bayan():
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Bayans (surahID, verseFrom, verseTo, bayanFileName)
        VALUES (?, ?, ?, ?)""",
        (data['surahID'], data['verseFrom'], data['verseTo'], data['bayanFileName']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Bayan created successfully"}), 201

# Update Bayan by ID
@app.route('/api/bayans/<int:bayan_id>', methods=['PUT'])
def update_bayan(bayan_id):
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Bayans
        SET surahID=?, verseFrom=?, verseTo=?, bayanFileName=?
        WHERE bayanID=?""",
        (data['surahID'], data['verseFrom'], data['verseTo'], data['bayanFileName'], bayan_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Bayan updated successfully"})

# Delete Bayan by ID
@app.route('/api/bayans/<int:bayan_id>', methods=['DELETE'])
def delete_bayan(bayan_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Bayans WHERE bayanID=?", (bayan_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Bayan deleted successfully"})

# ------------------- Bookmarks Routes -------------------

# Select All Bookmarks
@app.route('/api/bookmarks', methods=['GET'])
def get_bookmarks():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Bookmarks")
    bookmarks = cursor.fetchall()
    conn.close()
    return jsonify([row_to_dict(row) for row in bookmarks])

# Select Bookmarks by ID
@app.route('/api/bookmarks/<int:bookmark_id>', methods=['GET'])
def get_bookmark(bookmark_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Bookmarks WHERE bookmarkID=?", (bookmark_id,))
    bookmark = cursor.fetchone()
    conn.close()
    if bookmark:
        return jsonify(row_to_dict(bookmark))
    else:
        return jsonify({"error": "Bookmark not found"}), 404

# Create a new Bookmark
@app.route('/api/bookmarks', methods=['POST'])
def create_bookmark():
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Bookmarks (surahID, verseID, bookmarkDescription)
        VALUES (?, ?, ?)""",
        (data['surahID'], data['verseID'], data['bookmarkDescription']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Bookmark created successfully"}), 201

# Update Bookmark by ID
@app.route('/api/bookmarks/<int:bookmark_id>', methods=['PUT'])
def update_bookmark(bookmark_id):
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Bookmarks
        SET surahID=?, verseID=?, bookmarkDescription=?
        WHERE bookmarkID=?""",
        (data['surahID'], data['verseID'], data['bookmarkDescription'], bookmark_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Bookmark updated successfully"})

# Delete Bookmark by ID
@app.route('/api/bookmarks/<int:bookmark_id>', methods=['DELETE'])
def delete_bookmark(bookmark_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Bookmarks WHERE bookmarkID=?", (bookmark_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Bookmark deleted successfully"})


# ------------------- Chain Routes -------------------

# Select All Chains
@app.route('/api/chains', methods=['GET'])
def get_chains():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Chains")
    chains = cursor.fetchall()
    conn.close()
    return jsonify([row_to_dict(row) for row in chains])

# Select Chain by ID
@app.route('/api/chains/<int:chain_id>', methods=['GET'])
def get_chain(chain_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Chains WHERE chainID=?", (chain_id,))
    chain = cursor.fetchone()
    conn.close()
    if chain:
        return jsonify(row_to_dict(chain))
    else:
        return jsonify({"error": "Chains not found"}), 404

# Create a new Chain
@app.route('/api/chains', methods=['POST'])
def create_chain():
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Chains (chainTitle) VALUES (?)", (data['chainTitle'],))
    conn.commit()
    conn.close()
    return jsonify({"message": "Chains created successfully"}), 201

# Update Chain by ID
@app.route('/api/chains/<int:chain_id>', methods=['PUT'])
def update_chain(chain_id):
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Chain SET chainTitle=? WHERE chainID=?", (data['chainTitle'], chain_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Chain updated successfully"})

# Delete Chain by ID
@app.route('/api/chains/<int:chain_id>', methods=['DELETE'])
def delete_chain(chain_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Chain WHERE chainID=?", (chain_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Chain deleted successfully"})

# ------------------- ChainDetail Routes -------------------

# Select All ChainDetails
@app.route('/api/chaindetails', methods=['GET'])
def get_chaindetails():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chainDetail")
    chaindetails = cursor.fetchall()
    conn.close()
    return jsonify([row_to_dict(row) for row in chaindetails])

# Select ChainDetail by ID
@app.route('/api/chaindetails/<int:chaindetail_id>', methods=['GET'])
def get_chaindetail(chaindetail_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chainDetail WHERE chainDetailID=?", (chaindetail_id,))
    chaindetail = cursor.fetchone()
    conn.close()
    if chaindetail:
        return jsonify(row_to_dict(chaindetail))
    else:
        return jsonify({"error": "ChainDetail not found"}), 404

# Create a new ChainDetail
@app.route('/api/chaindetails', methods=['POST'])
def create_chaindetail():
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chainDetail (chainID, verseFrom, verseTo, repeatCount, sequenceNo)
        VALUES (?, ?, ?, ?, ?)""",
        (data['chainID'], data['verseFrom'], data['verseTo'], data['repeatCount'], data['sequenceNo']))
    conn.commit()
    conn.close()
    return jsonify({"message": "ChainDetail created successfully"}), 201

# Update ChainDetail by ID
@app.route('/api/chaindetails/<int:chaindetail_id>', methods=['PUT'])
def update_chaindetail(chaindetail_id):
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE chainDetail
        SET chainID=?, verseFrom=?, verseTo=?, repeatCount=?, sequenceNo=?
        WHERE chainDetailID=?""",
        (data['chainID'], data['verseFrom'], data['verseTo'], data['repeatCount'], data['sequenceNo'], chaindetail_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "ChainDetail updated successfully"})

# Delete ChainDetail by ID
@app.route('/api/chaindetails/<int:chaindetail_id>', methods=['DELETE'])
def delete_chaindetail(chaindetail_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chainDetail WHERE chainDetailID=?", (chaindetail_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "ChainDetail deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)
