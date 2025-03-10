from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
import uuid
import json
import time
import numpy as np

# Connect to Milvus
connections.connect("default", host="localhost", port="19530")

# Define Schema
fields = [
    FieldSchema(name="_id", dtype=DataType.VARCHAR, max_length=36,
                is_primary=True),  # Use VARCHAR for UUID
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=128),
    FieldSchema(name="metadata", dtype=DataType.VARCHAR, max_length=2048),
    FieldSchema(name="time_create", dtype=DataType.VARCHAR, max_length=50),
    FieldSchema(name="time_update", dtype=DataType.VARCHAR, max_length=50),
]

schema = CollectionSchema(fields, description="FaceID Storage")

# Create Collection
collection_name = "face_ids_v2"
if not utility.has_collection(collection_name):
    collection = Collection(collection_name, schema)
    collection.create_index("embedding", {
        "metric_type": "L2",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 1024}
    })
    print("Collection created successfully.")
else:
    collection = Collection(collection_name)
    print("Collection found successfully.")

collection.load()


def insert_face_embedding(metadata, embeddings):
    """
    Insert multiple face embeddings into the Milvus collection.
    :param metadata: List of metadata dictionaries.
    :param embeddings: List of 512D face embeddings (List of lists).
    """
    time_now = str(int(time.time()))
    _ids = str(uuid.uuid4())
    data = [
        [_ids],
        [embeddings],
        [metadata],
        [time_now],
        [time_now]
    ]
    collection.insert(data)
    collection.flush()
    return _ids


def upsert_face_embedding(_id, metadata, embedding):
    """
    Upsert (Insert or Update) a face embedding in Milvus.
    :param _id: Unique identifier (UUID).
    :param metadata: Metadata dictionary.
    :param embedding: 512D face embedding.
    """
    time_now = str(int(time.time()))  # Current timestamp

    # Check if ID exists
    expr = f"_id == '{_id}'"
    results = collection.query(expr, output_fields=["_id"])

    if results:
        # If exists, delete first
        delete_face_embedding(_id)

    # Insert new entry
    data = [[_id], [embedding], [metadata], [time_now], [time_now]]
    collection.insert(data)
    collection.flush()
    return _id


def delete_face_embedding(_id):
    """
    Delete a face embedding from Milvus.
    :param _id: Unique identifier (UUID).
    """
    expr = f"_id == '{_id}'"
    collection.delete(expr)
    collection.flush()
    print(f"Deleted embedding with ID: {_id}")


def search_face_embedding(embedding, threshold=0.38, top_k=5, pick=['_id', 'metadata']):
    """
    Search for the top_k most similar embeddings in Milvus.
    :param embedding: 512D face embedding.
    :param top_k: Number of nearest matches to retrieve.
    :return: List of matches with metadata and distances.
    """
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

    results = collection.search(
        data=[embedding],
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        output_fields=pick
    )
    matches = []
    for hits in results:
        for hit in hits:
            if hit.distance <= threshold:
                mgs = {
                    "id": hit.id,
                    "metadata": hit.entity.get("metadata"),
                    "distance": hit.distance,
                }
                if "embedding" in pick:
                    mgs["embedding"] = hit.entity.get("embedding")
                matches.append(mgs)
    return matches
