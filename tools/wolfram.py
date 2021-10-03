# https://towardsdatascience.com/build-your-next-project-with-wolfram-alpha-api-and-python-51c2c361d8b9
# https://martinheinz.dev/blog/36
# https://jsonformatter.curiousconcept.com/#

from pprint import pprint
import requests
import os
import urllib.request
import urllib.parse

# appid = os.getenv('WA_APPID', '...')
appid = "5K4R26-PJ72TKLK7Q"

# plotting 2D graph function
def plot2D(function):
    try:

        # function = "49=x**2 + y**2"
        query = f"plot {function}"
        query_url = f"http://api.wolframalpha.com/v2/query?" \
                    f"appid={appid}" \
                    f"&input={query}" \
                    f"&output=json" \
                    f"&includepodid=*"

        r = requests.get(query_url).json()

        if (r["queryresult"]["success"]):
            pods = r["queryresult"]["pods"]
            plot_url = pods[1]["subpods"][0]["img"]["src"]
    
            return True, plot_url
        else:
            return False,"Could not perform task"



    except Exception as e:
        return False, "We either could not understand your input or something's broken on our side ..."

# plotting 3D graph function
def plot3D(function):
    try:

        # plotting graphs
        # function = "(sin 10*(x**2+y**2) )/10"
        function = "sin x cos x"
        
        query = f"plot {function}"
        query_url = f"http://api.wolframalpha.com/v2/query?" \
                    f"appid={appid}" \
                    f"&input={query}" \
                    f"&output=json" \
                    f"&includepodid=3DPlot" \
                    f"&includepodid=ContourPlot"

        r = requests.get(query_url).json()

        if (r["queryresult"]["success"]):
            pods = r["queryresult"]["pods"]
            plot_3d_url = pods[0]["subpods"][0]["img"]["src"]
            plot_contour_url = pods[1]["subpods"][0]["img"]["src"]
    
            return True, plot_url
        else:
            return False,"Could not perform task"



    except Exception as e:
        return False, "We either could not understand your input or something's broken on our side ..."


# res, link = plot3D("")

# solving equation without showing steps
def solveEquation(equation):
    try:

        # not showing steps
        # equation = "7 + 2x = 12 - 3x"
        query = urllib.parse.quote_plus(f"solve {equation}")
        query_url = f"http://api.wolframalpha.com/v2/query?" \
                    f"appid={appid}" \
                    f"&input={query}" \
                    f"&includepodid=Result" \
                    f"&output=json"

        r = requests.get(query_url).json()

        # print(data["img"]["src"])
        
        if (r["queryresult"]["success"]):
            data = r["queryresult"]["pods"][0]["subpods"][0]
            
            plaintext = data["plaintext"]
    
            return True, f"Result of {equation} is '{plaintext}'."
        else:
            return False,"Could not perform task"



    except Exception as e:
        return False, "We either could not understand your input or something's broken on our side ..."


# solving equation with showing steps
def solveEquationWithSteps(equation):
    try:

        # showing steps
        # equation = "7 + 2x = 12 - 3x"
        query = urllib.parse.quote_plus(f"solve {equation}")
        query_url = f"http://api.wolframalpha.com/v2/query?" \
                    f"appid={appid}" \
                    f"&input={query}" \
                    f"&scanner=Solve" \
                    f"&podstate=Result__Step-by-step+solution" \
                    "&format=plaintext" \
                    f"&output=json"

        r = requests.get(query_url).json()

        # print(data["img"]["src"])
        
        if (r["queryresult"]["success"]):
            data = r["queryresult"]["pods"][0]["subpods"]
            result = data[0]["plaintext"]
            steps = data[1]["plaintext"]
            plaintext = data["plaintext"]
    
            return True, f"Result of {equation} is '{plaintext}'.\n\n" + f"Possible steps to solution:\n\n{steps}"
        else:
            return False,"Could not perform task"



    except Exception as e:
        return False, "We either could not understand your input or something's broken on our side ..."


def qnaBot(question):
    try:
        # question = "what is the most spoken language in the world?"
        query_url = f"http://api.wolframalpha.com/v1/spoken?" \
                    f"appid={appid}" \
                    f"&i={question}" \
                    

        r = requests.get(query_url)

        return True, r.text
    except:
        return False, "Could not get you an answer ..."

