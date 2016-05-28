from flask import Flask, request, make_response, jsonify
from africastalking.AfricasTalkingGateway import AfricasTalkingGateway
import json

from houndify import houndify

clientId = 'KS3xVzZ3e1LYKPYpje8BVA=='
clientKey = 'unUgmQ4ZFvjk4LeJVs5oa16H7V-O4DTbDpJ1-KCSnKpVPu6lP59Y4gyTufdn7_EkGHj8EZGzMIAcLd4F8l-GdA=='

client = houndify.TextHoundClient(clientId, clientKey, "at-shortcode")

app     = Flask('smart-text')
gateway = AfricasTalkingGateway('aT_username', 'at_api_key')


@app.route('/sms', methods=['POST'])
def incoming_sms():
    to      = request.values.get('from', None)
    message = request.values.get('text', None)

    print to, message

    # integrate houndify
    resp     = client.query(message)
    json_obj = json.loads(resp)

    toSend = json_obj['AllResults'][0]['SpokenResponse']
    print toSend

    gateway.sendMessage(to, message)
    # gateway.call('+254711082306', to)
    return make_response(jsonify({'OK': 'Success'}), 200)


@app.route('/call', methods=['POST'])
def process_call():
    callerNumber = request.values.get('callerNumber', None)
    print callerNumber

    response = '<Response> <Say>Thank you for testing my demo </Say> </Response>'

    return make_response(response, 200)


if __name__ == '__main__':
    app.debug = True
    app.run()
