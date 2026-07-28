from pymongo import MongoClient
import certifi

uri = "mongodb+srv://amitrai8602:Ideapad9999@amitdb.k2actmy.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(
    uri,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000,
)

print(client.admin.command("ping"))