import os
from datetime import datetime
import time
import convertapi
import urllib.request
from twilio.rest import Client
import firebase_admin
from firebase_admin import credentials, firestore, storage
from tools import  wolfram
from tools import definitions
from tools import translator
# from storage import uploadImage

# setting up twilio connection
ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
ACCOUNT_SECRET = os.environ.get('ACCOUNT_SECRET')
FROM = os.environ.get('FROM')

client = Client(ACCOUNT_SID, ACCOUNT_SECRET)

#setting up firebase connection
cred = credentials.Certificate("./highschoolchatbot-firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': os.environ.get('STORAGE_URL'),
    'databaseUrl': os.environ.get('DATABASE_URL'),
})

secret = "4osBMYYgFECYCBVM"
api_key = "785325902"

convertapi.api_secret = secret

fDb = firestore.client()

bucket = storage.bucket()

def convertToPng(filename):

    result = convertapi.convert('png', { 'File': filename+".gif" })

    # save to file
    result.file.save(filename + ".png")


def uploadImage(filename):
    try:
        print("inside upload file")

        print(filename)

        sfile = str( round(datetime.now().timestamp()) )


        r = urllib.request.urlopen(filename)


        with open(f'./{sfile}.gif', "wb") as file:
            file.write(r.read())

            file.close()

        convertToPng(f'./{sfile}')


        blob = bucket.blob('graphs/'+sfile + ".png")

        blob.upload_from_filename("./"+sfile+".png")

        blob.make_public()

        if os.path.exists("./"+sfile+".png"):
            os.remove("./"+sfile+".png")
        
        if os.path.exists("./"+sfile+".gif"):
            os.remove("./"+sfile+".gif")
            

        return True, blob.public_url
    except Exception as e:
        print(e)
        return False, "Error sending image"

def userExists(senderId):
    users = fDb.collection("users")

    user = users.document(senderId)

    user = user.get()

    exists = user.exists

    return exists, None if not exists else user.to_dict()  

def getUser(senderId):
    users = fDb.collection("users")

    user = users.document(senderId)

    return user.get().to_dict()

def addUser(senderId):

    users = fDb.collection("users")

    users.document(senderId).set({
        "DateCreated": datetime.now(),
        "lastText": "",
        "name": "not-set",
    })

def updateUser(senderId, data):
    users = fDb.collection("users")

    users.document(senderId).update(data)

def showMenu(senderId, message):

    message = message.strip()

    exists, data = userExists(senderId)

    if not exists:
        addUser(senderId)
        data = getUser(senderId)

    if (data["name"]=="not-set" and not data["lastText"] == "set-name"):
        client.messages.create(
            body="Hey, I'm Winnie. Your friendly Assistant from PocketSchool. What is your name ?", 
            from_=FROM,
            to=f'whatsapp:+{senderId}'
        )

        updateUser(senderId, {"lastText":"set-name"})

    elif (data["name"]=="not-set" and data["lastText"] == "set-name"):
        
        if (len(message)>0 and not message.lower() == "not-set"):
            updateUser(senderId, {"name": message, "DateNameSet": datetime.now(), "lastText":""})

            client.messages.create(
                body=f'Hey {message}, It\'s a pleasure to meet you! Type "menu!" to see our menu.', 
                from_=FROM,
                to=f'whatsapp:+{senderId}'
            )

    else:    

        if message.lower()=="menu!":
            client.messages.create(
                        body=
                        f'Hey {data["name"]}, Welcome to PocketSchool!\n'+
                        "This is a service where matric students can get access to resources which can help them study."+
                        "\n"+
                        "\n"+
                        "What can we help you with ?:\n"+
                        "1. Exams (papers, dates)\n"+
                        "2. Universities (dates, bursaries, prospectus)\n"+
                        "3. Learn\n"+
                        "4. Quiz\n"+
                        "5. Smart Tools\n"+
                        "6. Help\n"+
                        
                        
                        "\n"+
                        "\n"+
                        "Send your response below (either 1,2,3 or 4)",
                        from_=FROM,
                        to=f'whatsapp:+{senderId}'
                    )
            updateUser(senderId, {"lastText":""})

        elif message=="1" and data["lastText"]=="":
            client.messages.create(
                        body=
                        "Exams Menu\n"+
                        "a. Past papers(papers, dates)\n"+
                        "b. Timetable\n"+
                        "c. Study tips\n"+
                        
                        "\n"+
                        "\n"+
                        "Send your response below (either a,b or c). Send menu! to go back to the Main Menu.",
                        from_=FROM,
                        to=f'whatsapp:+{senderId}'
                    )

            updateUser(senderId, {"lastText":"1"})
        

        elif (message.lower()=="a" and data["lastText"]=="1") or data["lastText"]=="1a":
            # user has chosen option 1a
            if (data["lastText"]=="1a"):
                
                if (message.count(" ") == 1):
                    paper, year = message.split(" ")

                    client.messages.create(
                        body=
                        # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                        f'Here is your {paper} paper, for year {year}\n'+
                        "Send menu! to return to the Main Menu.",
                        from_=FROM,
                        to=f'whatsapp:+{senderId}'
                    )
                else:
                    client.messages.create(
                        body=
                        # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                        "Your request is in of an incorrect format... correct format is : Maths 2021\n"+
                        "Send menu! to return to the Main Menu.",
                        from_=FROM,
                        to=f'whatsapp:+{senderId}'
                    )
            else:
                # 
                client.messages.create(
                            body=
                            # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                            "Type the name of the subject and year to get a specific past paper\n"+
                            "for example: Maths 2021"
                            "\n"+
                            "\n"+
                            "Send menu! to go back to the Main Menu.",
                            from_=FROM,
                            to=f'whatsapp:+{senderId}'
                        )
                updateUser(senderId, {"lastText":"1a"})
                # allow user to go back, not to main menu but sub menu...

        elif message=="2" and data["lastText"]=="":
            client.messages.create(
                        body=
                        "University Menu\n"+
                        "a. Applications (open/closing dates)\n"+
                        "b. Prospectus\n"+
                        "c. Bursaries\n"+
                        
                        "\n"+
                        "\n"+
                        "Send your response below (either a,b or c). Send menu! to go back to the Main Menu.",
                        from_=FROM,
                        to=f'whatsapp:+{senderId}'
                    )

            updateUser(senderId, {"lastText":"2"})

        elif message=="3" and data["lastText"]=="":
            client.messages.create(
                        body=
                        "Learn Something ...\n"+
                        "a. Mathematics\n"+
                        "b. Physics\n"+
                        "c. Life Science\n"+
                        
                        "\n"+
                        "\n"+
                        "Send your response below (either a,b or c). Send menu! to go back to the Main Menu.",
                        from_=FROM,
                        to=f'whatsapp:+{senderId}'
                    )

            updateUser(senderId, {"lastText":"3"})

        elif message=="4" and data["lastText"]=="":
            client.messages.create(
                        body=
                        "Take a Quiz\n"+
                        "a. Life Science\n"+
                        "b. Mathematics\n"+
                        "c. Physical Science - Physics\n"+
                        "d. Physical Science - Chemistry\n"+
                        
                        "\n"+
                        "\n"+
                        "Send your response below (either a,b,c or d). Send menu! to go back to the Main Menu.",
                        from_=FROM,
                        to=f'whatsapp:+{senderId}'
                    )

            updateUser(senderId, {"lastText":"4"})

        elif message=="5" and data["lastText"]=="":
            client.messages.create(
                        body=
                        "Smart tools you can use :D \n"+
                        "a. Plot 3D graph\n"+
                        "b. Plot 2D graph\n"+
                        "c. Solve equation\n"+
                        "d. Solve equation (with steps)\n"+
                        "e. QnA Bot\n"+
                        "f. Wikipedia Search\n"+
                        "g. Translator\n"+
                        
                        "\n"+
                        "\n"+
                        "Send your response below (either a,b,c,d,e,f or g). Send menu! to go back to the Main Menu.",
                        from_=FROM,
                        to=f'whatsapp:+{senderId}'
                    )

            updateUser(senderId, {"lastText":"5"})

        elif (message.lower()=="a" and data["lastText"]=="5") or data["lastText"]=="5a":
            # user has chosen option 1a
            if (data["lastText"]=="5a"):
                res, src = wolfram.plot3D(message)
                if res:

                    res, src = uploadImage(src)

                    if res:
                
                        client.messages.create(
                            body=
                            # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                            f'Here is your graph {src}\n'+
                            "Send another equation or Send menu! to return to the Main Menu.",
                            from_=FROM,
                            to=f'whatsapp:+{senderId}'
                        )
                        client.messages.create(
                            media_url=[src],
                            from_=FROM,
                            to=f'whatsapp:+{senderId}'
                        )
                    else:
                        client.messages.create(
                            body=
                            # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                            f'Error: {src}\n',
                            from_=FROM,
                            to=f'whatsapp:+{senderId}'
                        )
                else:
                    client.messages.create(
                        body=
                        # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                        f"Error: {src}. \nSend another equation or Send menu! to return to the Main Menu.",
                        from_=FROM,
                        to=f'whatsapp:+{senderId}'
                    )

            else:
                # 
                client.messages.create(
                            body=
                            # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                            "Type the equation of 3d graph you'd like to plot ...\n"+
                            "ie. sin x cos x"
                            "\n"+
                            "\n"+
                            "Send menu! to go back to the Main Menu.",
                            from_=FROM,
                            to=f'whatsapp:+{senderId}'
                        )
                updateUser(senderId, {"lastText":"5a"})

        elif (message.lower()=="b" and data["lastText"]=="5") or data["lastText"]=="5b":
            # user has chosen option 1a
            if (data["lastText"]=="5b"):
                
                res, src = wolfram.plot2D(message)
                if res:
                    
                    res, src = uploadImage(src)
                    print(src)
                    # res, src = False, "testing..."
                    
                    if res:
                        client.messages.create(
                            body=
                            # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                            f'Here is your graph\n'+
                            "Send another equation or Send menu! to return to the Main Menu.",
                            from_=FROM,
                            to=f'whatsapp:+{senderId}'
                        )
                        
                        client.messages.create(
                            media_url=[src],
                            from_=FROM,
                            to=f'whatsapp:+{senderId}'
                        )
                    else:
                        client.messages.create(
                            body=
                            # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                            f'Error: {src}\n',
                            from_=FROM,
                            to=f'whatsapp:+{senderId}'
                        )
                else:
                    client.messages.create(
                        body=
                        # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                        f"Error: {src}. \nSend another equation or Send menu! to return to the Main Menu.",
                        from_=FROM,
                        to=f'whatsapp:+{senderId}'
                    )

            else:
                # 
                client.messages.create(
                            body=
                            # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                            "Type the equation of 2d graph you'd like to plot ...\n"+
                            "ie. y=3x"
                            "\n"+
                            "\n"+
                            "Send menu! to go back to the Main Menu.",
                            from_=FROM,
                            to=f'whatsapp:+{senderId}'
                        )
                updateUser(senderId, {"lastText":"5b"})

        elif (message.lower()=="c" and data["lastText"]=="5") or data["lastText"]=="5c":
            # user has chosen option 1a
            if (data["lastText"]=="5c"):

                res, ans = wolfram.solveEquation(message)
                
                client.messages.create(
                    body=
                    # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                    f'{ans}\n'+
                    "Send another equation or Send menu! to return to the Main Menu.",
                    from_=FROM,
                    to=f'whatsapp:+{senderId}'
                )

            else:
                # 
                client.messages.create(
                            body=
                            # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                            "Type the equation you'd like us to solve ...\n"+
                            "ie. sin x = cos x"
                            "\n"+
                            "\n"+
                            "Send menu! to go back to the Main Menu.",
                            from_=FROM,
                            to=f'whatsapp:+{senderId}'
                        )
                updateUser(senderId, {"lastText":"5c"})

        elif (message.lower()=="d" and data["lastText"]=="5") or data["lastText"]=="5d":
            # user has chosen option 1a
            if (data["lastText"]=="5d"):
                res, ans = wolfram.solveEquationWithSteps(message)
                client.messages.create(
                    body=
                    # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                    f'{ans}\n'+
                    "Send another equation or Send menu! to return to the Main Menu.",
                    from_=FROM,
                    to=f'whatsapp:+{senderId}'
                )

            else:
                # 
                client.messages.create(
                            body=
                            # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                            "Type the equation you'd like us to solve ...\n"+
                            "ie. sin x cos x"
                            "\n"+
                            "\n"+
                            "Send menu! to go back to the Main Menu.",
                            from_=FROM,
                            to=f'whatsapp:+{senderId}'
                        )
                updateUser(senderId, {"lastText":"5d"})


        elif (message.lower()=="e" and data["lastText"]=="5") or data["lastText"]=="5e":
            # user has chosen option 1a
            if (data["lastText"]=="5e"):
                res, ans = wolfram.qnaBot(message)
                client.messages.create(
                    body=
                    # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                    f'{ans}\n'+
                    "Send another question for Winnie to answer or Send menu! to return to the Main Menu.",
                    from_=FROM,
                    to=f'whatsapp:+{senderId}'
                )

            else:
                # 
                client.messages.create(
                            body=
                            # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                            "Ask Winnie any question ...\n"+
                            "ie. What is newton's 1st law ? "
                            "\n"+
                            "\n"+
                            "Send menu! to go back to the Main Menu.",
                            from_=FROM,
                            to=f'whatsapp:+{senderId}'
                        )
                updateUser(senderId, {"lastText":"5e"})

        elif (message.lower()=="f" and data["lastText"]=="5") or data["lastText"]=="5f":
            # user has chosen option 1a
            if (data["lastText"]=="5f"):

                # res, ans = definitions.search(message)

                img, ans = definitions.search(message)

                print(img)
                # print("images done being printed")

                
                client.messages.create(
                    body=
                    # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                    f'{ans}\n'+
                    "Type in what else you want to research or Send menu! to return to the Main Menu.",
                    from_=FROM,
                    media_url=img,
                    to=f'whatsapp:+{senderId}'
                )

            else:
                # 
                client.messages.create(
                            body=
                            # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                            "Type in whatever you want to search on wikipedia ...\n"+
                            "ie. Nelson Mandela"
                            "\n"+
                            "\n"+
                            "Send menu! to go back to the Main Menu.",
                            from_=FROM,
                            to=f'whatsapp:+{senderId}'
                        )
                updateUser(senderId, {"lastText":"5f"})

        elif (message.lower()=="g" and data["lastText"]=="5") or data["lastText"]=="5g":
            # user has chosen option 1a
            if (data["lastText"]=="5g"):

                if (message.count("-")==1 and message.count(":")==1):

                    message = message.lower()
                    spl1 = message.split(":")
                    text = spl1[1].strip()
                    tz = spl1[0].split("-")
                    t1 = tz[0],t2 = tz[1]
                    t1 = t1.strip()
                    t2 = t2.strip()

                    translated = translator.translate(t2, t1, text)
                
                    client.messages.create(
                        body=
                        # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                        f'{translated}\n'+
                        "Type the text and languages to translate between or Send menu! to return to the Main Menu.",
                        from_=FROM,
                        to=f'whatsapp:+{senderId}'
                    )
                else:
                    client.messages.create(
                        body=
                        "Enter correct format, ie. [from] - [to] : [text] or Send menu! to return to the Main Menu.",
                        from_=FROM,
                        to=f'whatsapp:+{senderId}'
                    )  

            else:
                # 
                client.messages.create(
                            body=
                            # "Type the name of the subject, year, term and province to get a specific past paper\n"+
                            "Type the text and languages to translate between ...\n"+
                            "ie. [from] - [to] : [text]"
                            "\n"+
                            "\n"+
                            "Send menu! to go back to the Main Menu.",
                            from_=FROM,
                            to=f'whatsapp:+{senderId}'
                        )
                updateUser(senderId, {"lastText":"5g"})






        elif message=="6" and data["lastText"]=="":
            client.messages.create(
                        body=
                        "Help Page\n\n"+

                        "Different languages:\n"+
                        "Afrikaans - af\n"+
                        "Zulu - zu\n"+
                        "English - en\n"+
                        "French - fr\n"+
                        "Swahili - sw\n"+

                        "\n"+
                        "\n"+

                        "Different Subjects:\n"+
                        "Mathematics - Maths\n"+
                        "Maths Lits - MathsLit\n"+
                        "Life Orientation - LOrientation\n"+
                        "Life Science - LScience\n"+
                        "Physical Science - Physics\n"
                        
                        ,


                        from_=FROM,
                        to=f'whatsapp:+{senderId}'
                    )

        else:
            client.messages.create(
                        body=
                        "Invalid option ... Send menu! to go back to the Main Menu.",
                        from_=FROM,
                        to=f'whatsapp:+{senderId}'
                    )

