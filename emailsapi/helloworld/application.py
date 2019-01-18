#!flask/bin/python
import json, sys
from flask import request
from flask import Flask, Response
from helloworld.flaskrun import flaskrun
import boto3
from apscheduler.scheduler import Scheduler
from flask_cors import CORS
import datetime, os
import requests


client = boto3.client(
    'sqs', region_name='us-east-2',
    aws_access_key_id="AKIAIK3VOQV5REHT5AMQ",
    aws_secret_access_key="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",
)
queue_url = "https://sqs.us-east-2.amazonaws.com/279786682270/EmailQueue"


def pushQueue(Msgbody):
    # send message to queue
    enqueue_response = client.send_message(QueueUrl=queue_url, MessageBody=Msgbody)
    return enqueue_response['MessageId']
    # print('Message ID : ',enqueue_response['MessageId'])

def popQueue():
    try:
        messages = client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)
        if 'Messages' in messages:  # when the queue is exhausted, the response dict contains no 'Messages' key
            for message in messages['Messages']:  # 'Messages' is a list
                # process the messages
                # print(message['Body'])
                # next, we delete the message from the queue so no one else will process it again
                client.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])
                # output data to file
                ip = requests.get('https://api.ipify.org').text
                res = ip + " : " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
                # print(res)
                file = open("append.txt", "a")
                file.write(res)
                file.close()
                break
        else:
            res = 'Queue is now empty' + " : " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
    except:
        pass



application = Flask(__name__)
CORS(application)

""""Schedular"""
sched = Scheduler()  # Scheduler object
sched.start()

"""
@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World' + str(sys.version_info)}), mimetype='application/json', status=200)

@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
"""

@application.route('/', methods=['GET'])
def get():
    res = ""
    if os.path.isfile("append.txt"):
        file = open("append.txt", "r")
        data = file.readlines()
        res = ""
        for row in data:
            res += "<p>" + row + "</p>"
    return Response(res, mimetype='text/html', status=200)


@application.route('/', methods=['POST'])
def post():
    file = open("append.txt", "w")
    file.write("")
    file.close()
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)


@application.route('/push', methods=['POST'])
def push():
    if request.method == 'POST':
        if 'msg' in request.form:
            msg = request.form['msg']
            if msg != '':
                # pushQueue(msg)
                return Response(json.dumps({'Output': pushQueue(msg)}), mimetype='application/json', status=200)
            else:
                return Response(json.dumps({'Output': 'No message'}), mimetype='application/json', status=400)
        else:
            return Response(json.dumps({'Output': 'No message'}), mimetype='application/json', status=400)
    else:
        return Response(json.dumps({'Output': 'Method not allowed'}), mimetype='application/json', status=405)


@application.route('/pop', methods=['GET'])
def pop():
    popQueue()




# add your job here
sched.add_interval_job(popQueue, seconds=20)

if __name__ == '__main__':
    flaskrun(application)
