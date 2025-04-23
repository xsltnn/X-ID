from config import get_db

def search_all_collections(fields, keyword):
    db = get_db()
    results = []

    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        found_any = False

        for field in fields:
            query = {field: {"$regex": keyword, "$options": "i"}}
            found = list(collection.find(query))
            if found:
                for doc in found:
                    doc["_collection"] = collection_name
                    doc["_matched_field"] = field
                results.extend(found)
                found_any = True
                break  # Stop at the first matching field

    return results

# 🔍 Nama: fallback dari "Nama Lengkap" ke "Nama"
def search_by_name(name):
    return search_all_collections(["Nama Lengkap", "Nama"], name)

def search_by_phone(phone):
    return search_all_collections(["Nomor Telepon"], phone)

def search_by_email(email):
    return search_all_collections(["Email"], email)
