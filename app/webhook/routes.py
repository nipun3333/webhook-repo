from flask import Blueprint, json, request, redirect, url_for, render_template
from ..extensions import mongo
import datetime
import time

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

#Route for the logs
@webhook.route('/')
def home():
    # getting all the data in collection
    collection = mongo.db.logs.find()
    # rendering html template
    return render_template("home.html", logs=collection, result=time.time())

# route for reveiving data in json format
@webhook.route('/receiver', methods=["POST"])
def receiver():
    if request.headers['Content-Type'] == 'application/json':
        info = json.dumps(request.json)
        # converting json to python dictionary
        payload_dict = json.loads(info)

        # Checking if request is for pulling or pushing 
        if "ref" in payload_dict:
            # getting data in variables
            branch = payload_dict["ref"].split("/")[-1]
            author = payload_dict["sender"]["login"]

            # current date and time
            d1 = datetime.datetime.utcnow()
            time = str(d1.year)+"-"+str(d1.month)+"-"+str(d1.day)+"T"+str(d1.hour)+":"+str(d1.minute)+":"+str(d1.second)+"Z"
            d1 = datetime.datetime.strptime(time,"%Y-%m-%dT%H:%M:%SZ")
            
            _date = d1.date()
            _time = list(datetime.datetime.strptime(time,"%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%dT%I:%M:%S %p').split('T'))[-1]
            
            # formatting time
            if _date.day==1:
                time =  _date.strftime("%dst %b %Y")+" - "  +_time
            elif _date.day==2:
                time =  _date.strftime("%dnd %b %Y")+" - "  +_time
            elif _date.day==3:
                time =  _date.strftime("%drd %b %Y")+" - "  +_time
            else:
                time =  _date.strftime("%dth %b %Y")+" - "  +_time

            # inserting into database
            collection = mongo.db.logs.insert({"request":"PUSH", "author":author, "branch":branch, "time":time})

        
        else:
            # getting data in variables
            author = payload_dict["sender"]["login"]
            request_from = payload_dict["pull_request"]["head"]["label"]
            request_to = payload_dict["pull_request"]["base"]["label"]

            # current date and time
            d1 = datetime.datetime.utcnow()
            time = str(d1.year)+"-"+str(d1.month)+"-"+str(d1.day)+"T"+str(d1.hour)+":"+str(d1.minute)+":"+str(d1.second)+"Z"

            
            d1 = datetime.datetime.strptime(time,"%Y-%m-%dT%H:%M:%SZ")
            _date = d1.date()
            _time = list(datetime.datetime.strptime(time,"%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%dT%I:%M:%S %p').split('T'))[-1]

            # formatting time
            if _date.day==1:
                time =  _date.strftime("%dst %b %Y")+" - "  +_time
            elif _date.day==2:
                time =  _date.strftime("%dnd %b %Y")+" - "  +_time
            elif _date.day==3:
                time =  _date.strftime("%drd %b %Y")+" - "  +_time
            else:
                time =  _date.strftime("%dth %b %Y")+" - "  +_time

            # inserting into database
            collection = mongo.db.logs.insert({"request":"PULL", "author":author, "from_branch":request_from, "to_branch":request_to, "time":time})

    # redirecting to home page
    return redirect(url_for('Webhook.home'))
