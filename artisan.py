from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from typing import List
from pydantic import BaseModel

app = FastAPI()

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from typing import List

app = FastAPI()

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Your existing routes and database setup remain the same


MONGO_USERNAME = "Nithya"
MONGO_PASSWORD = "1999"
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "database_0"
 
# Create a MongoDB client for database_0
client = MongoClient(
    f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}")

MONGO_USERNAME1 = "Shivani"
MONGO_PASSWORD1 = "1999"
MONGO_HOST1 = "localhost"
MONGO_PORT1 = 27017
MONGO_DB1 = "database_1"
 
# Create a MongoDB client for database_1
client1 = MongoClient(
    f"mongodb://{MONGO_USERNAME1}:{MONGO_PASSWORD1}@{MONGO_HOST1}:{MONGO_PORT1}/{MONGO_DB1}")

# Function to hash the artist name
def hash_name(name):
    return sum(map(ord, name)) % 2


# Endpoint for retrieving documents from multiple databases
@app.get("/get_documents")
async def get_documents():
    # List to store all retrieved documents
    document_list = []

    # Fetch documents from database_0
    db_0 = client[MONGO_DB]
    collection_0 = db_0["artworks"]
    documents_0 = collection_0.find()

    # Convert ObjectId to string for each document in database_0
    for doc in documents_0:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        document_list.append(doc)

    # Fetch documents from database_1
    db_1 = client1[MONGO_DB1]
    collection_1 = db_1["artworks"]
    documents_1 = collection_1.find()

    # Convert ObjectId to string for each document in database_1
    for doc in documents_1:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        document_list.append(doc)

    return {"documents": document_list}

class Artwork(BaseModel):
    artist: str
    art_id: int
    art_images: str
    price: str
    location: str
    title: str
    creation_year: str
    signed: str
    condition: str
    category: str
    movement: str

@app.post("/insert_document")
async def insert_document(artwork: Artwork):
    db_index = hash_name(artwork.artist)
    db_name = f"database_{db_index}"
    collection_name = "artworks"
    
    # Construct the document
    document = {
        "Artist": artwork.artist,
        "ArtID": artwork.art_id,
        "ArtImages": artwork.art_images,
        "Price": artwork.price,
        "Location": artwork.location,
        "Title": artwork.title,
        "CreationYear": artwork.creation_year,
        "Signed": artwork.signed,
        "Condition": artwork.condition,
        "Category": artwork.category,
        "Movement": artwork.movement
    }
    
    # Fetch the appropriate database based on the hash value
    db = client[db_name]
    collection = db[collection_name]
    
    # Insert the document into the collection
    collection.insert_one(document)
    
    return {db_name}


class UpdateArtworkRequest(BaseModel):
    art_id: int
    new_price: str
    new_condition: str

# Endpoint to update artwork
@app.put("/update_artwork")
async def update_artwork(request: UpdateArtworkRequest):
    # Update the document in the "artworks" collection in database_0
    result = client[MONGO_DB]["artworks"].update_one(
        {"ArtID": request.art_id},
        {"$set": {"Price": request.new_price, "Condition": request.new_condition}}
    )
    
    # If the document was not found in database_0, try updating in database_1
    if result.matched_count == 0:
        result = client1[MONGO_DB1]["artworks"].update_one(
            {"ArtID": request.art_id},
            {"$set": {"Price": request.new_price, "Condition": request.new_condition}}
        )
    
    # Check if the update was successful
    if result.modified_count == 1:
        return {"message": "Artwork updated successfully"}
    else:
        return {"message": "Artwork not found"}


@app.delete("/delete_artwork")
async def delete_artwork(art_id: int):
    # Delete the document from the "artworks" collection in database_0
    result = client[MONGO_DB]["artworks"].delete_one({"ArtID": art_id})
    
    # If the document was not found in database_0, try deleting in database_1
    if result.deleted_count == 0:
        result = client1[MONGO_DB1]["artworks"].delete_one({"ArtID": art_id})
    
    # Check if the document was found and deleted
    if result.deleted_count > 0:
        return {"message": f"Deleted the record with ArtID {art_id}"}
    else:
        return {"message": "Artwork not found"}



@app.get("/search_by_artist")
async def search_by_artist(artist: str):
    # List to store all retrieved artworks
    artworks = []

    # Fetch artworks from database_0
    db_0 = client[MONGO_DB]
    collection_0 = db_0["artworks"]
    documents_0 = collection_0.find({"Artist": artist})

    # Convert ObjectId to string for each document in database_0
    for doc in documents_0:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        artworks.append(doc)

    # Fetch artworks from database_1
    db_1 = client1[MONGO_DB1]
    collection_1 = db_1["artworks"]
    documents_1 = collection_1.find({"Artist": artist})

    # Convert ObjectId to string for each document in database_1
    for doc in documents_1:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        artworks.append(doc)

    return {"artworks": artworks}


@app.get("/search_by_category")
async def search_by_category(category: str):
    # List to store all retrieved artworks
    artworks = []

    # Fetch artworks from database_0
    db_0 = client[MONGO_DB]
    collection_0 = db_0["artworks"]
    documents_0 = collection_0.find({"Category": category})

    # Convert ObjectId to string for each document in database_0
    for doc in documents_0:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        artworks.append(doc)

    # Fetch artworks from database_1
    db_1 = client1[MONGO_DB1]
    collection_1 = db_1["artworks"]
    documents_1 = collection_1.find({"Category": category})

    # Convert ObjectId to string for each document in database_1
    for doc in documents_1:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        artworks.append(doc)

    return {"artworks": artworks}


@app.get("/list_categories", response_model=List[str])
async def list_categories():
    categories = set()  # Use a set to store unique categories

    # Fetch categories from database_1
    db_1 = client[MONGO_DB]
    collection_1 = db_1["artworks"]
    categories.update(collection_1.distinct("Category"))

    # Fetch categories from database_2
    db_2 = client1[MONGO_DB1]
    collection_2 = db_2["artworks"]
    categories.update(collection_2.distinct("Category"))

    return list(categories)


@app.get("/list_artists", response_model=List[str])
async def list_artists():
    artists = set()  # Use a set to store unique artists

    # Fetch artists from database_1
    db_1 = client[MONGO_DB]
    collection_1 = db_1["artworks"]
    artists.update(collection_1.distinct("Artist"))

    # Fetch artists from database_2
    db_2 = client1[MONGO_DB1]
    collection_2 = db_2["artworks"]
    artists.update(collection_2.distinct("Artist"))

    return list(artists)