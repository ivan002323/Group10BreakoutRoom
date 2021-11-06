import urllib.parse
import requests
from flask import Flask, render_template, url_for, request
app = Flask(__name__)
main_api = "https://www.mapquestapi.com/directions/v2/route?" 
key = "PIJUdlV69l1oAPGEAxL75j6uXQVmGhnN" #Replace with your MapQuest key"

@app.route('/')
@app.route('/home',methods=['GET'])
def home():
    return render_template("indexmap.html")

@app.route('/result',methods=['POST'])
def result():
    output = request.form.to_dict()
    print(output)
    orig = output["orig"]
    dest = output["dest"]
    url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest})
    print("URL: " + (url))
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]
    if json_status == 0:
        success_call = str("API Status: " + str(json_status) + " = A successful route call.")
        Destination = str((orig) + " to " + (dest))
        Duration = str(json_data["route"]["formattedTime"])
        Kilometers = str("{:.2f}".format((json_data["route"]["distance"])*1.61))
        Fuel = str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78))
        maneu = []
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            maneu.append((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))

    elif json_status == 402:
        j402 = str("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        return render_template('output.html', j402 = j402)
    elif json_status == 611:
        j611 = str("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        return render_template('output.html', j611 = j611)
    else:
        unknown = str("For Staus Code: " + str(json_status) + "; Refer to:")
        unknown1 = str("https://developer.mapquest.com/documentation/directions-api/status-codes")
        return render_template('output.html', unknown = unknown, unknown1 = unknown1)

    return render_template('output.html', json_status = json_status, Destination = Destination, Duration = Duration, Kilometers = Kilometers, Fuel = Fuel, success_call = success_call, maneu = maneu)

if __name__ == "__main__":
    app.run(debug=True)