from pymongo import MongoClient
import certifi

uri = ""

client = MongoClient(
    uri,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000,
)

print(client.admin.command("ping"))