from src.storage import IndexStorage


sample_index = {
    "life": {
        "https://example.com": {
            "frequency": 2,
            "positions": [1, 5]
        }
    }
}

storage = IndexStorage("data/test_index.json")

saved_path = storage.save_index(sample_index)
loaded_index = storage.load_index()

print(f"Saved index to: {saved_path}")
print(loaded_index)