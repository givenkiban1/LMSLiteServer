from firebase_admin import credentials, firestore, storage
import firebase_admin
import urllib.request
import os
import datetime
# from dotenv import load_dotenv
# load_dotenv()

# cred=credentials.Certificate("./highschoolchatbot-firebase-adminsdk.json")

# firebase_admin.initialize_app(cred, {
#     'storageBucket': os.environ.get('STORAGE_URL')
# })

bucket = storage.bucket()


def uploadImage(filename):
    try:
        print("inside upload file")

        sfile = str( round(datetime.datetime.now().timestamp()) )


        r = urllib.request.urlopen(filename)

        blob = bucket.blob('graphs/'+sfile)

        blob.upload(r.read())

        blob.make_public()

        return True, blob.public_url
    except Exception as e:
        print(e)
        return False, "Error sending image"



# {
#   "type": "service_account",
#   "project_id": os.environ.get("project_id"),
#   "private_key_id": os.environ.get("private_key_id"),
#   "private_key": os.environ.get("private_key"),
#   "client_email": os.environ.get("client_email"),
#   "client_id": os.environ.get("client_id"),
#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#   "token_uri": "https://oauth2.googleapis.com/token",
#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#   "client_x509_cert_url": os.environ.get("client_x509_cert_url")
# }
