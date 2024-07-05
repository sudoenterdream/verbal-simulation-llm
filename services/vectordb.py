from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, Index

# Initialize Milvus connection
connections.connect("default", host="localhost", port="19530")

# Define a collection schema for Milvus with a primary key
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=512)
]
schema = CollectionSchema(fields, "Long-term memory collection")

# Create a collection
collection = Collection("long_term_memory", schema)

# Create an index on the embedding field
index_params = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 128}
}
index = Index(collection, "embedding", index_params)

# Load the collection to memory
collection.load()

def store_embedding(embedding, text):
    collection.insert([[embedding], [text]])
    print(f"Saved to long-term memory: {text}")

def search_embedding(embedding, limit=3):
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    results = collection.search([embedding], "embedding", search_params, limit=limit)
    
    retrieved_texts = []
    for result in results[0]:
        text = result.entity.get("text")
        if text:
            retrieved_texts.append(text)
        else:
            print(f"Warning: Retrieved text is None for result: {result}")
    
    retrieved_texts_str = " ".join(retrieved_texts)
    print(f"Retrieved from long-term memory: {retrieved_texts_str}")
    return retrieved_texts_str
