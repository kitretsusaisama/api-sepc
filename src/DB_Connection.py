#from pymongo.mongo_client import MongoClient
#from pymongo.server_api import ServerApi
#
#class DB_Connection:
#        def __init__(self):   
#            uri = "mongodb+srv://adminSeed:process.env.DB_PASS@productstable.5h6sox3.mongodb.net/?retryWrites=true&w=majority&appName=ProductsTable"
#            
            # Create a new client and connect to the server
            #client = MongoClient(uri, server_api=ServerApi('1'))
#            client = MongoClient(uri)
            # Send a ping to confirm a successful connection
#            try:
#                client.admin.command('ping')
#                print("Pinged your deployment. You successfully connected to MongoDB!")
#            except Exception as e:
#                print(e)