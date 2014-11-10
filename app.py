from flask import Flask, request, Response
from twilio.rest import TwilioRestClient
import config

from datetime import datetime

app = Flask(__name__)
client = TwilioRestClient(config.ACCOUNT_SID, config.AUTH_TOKEN)

@app.route('/door', methods=['POST'])
def access():
    key = request.form.get('KEY', '')
    code = request.form.get('CODE', '')
    if code not in config.CODES:
        return Response(status=200)
    if key != config.KEY:
        return Response(status=501)
    client.messages.create(
        to=config.TO_PHONE, 
        from_=config.FROM_PHONE, 
        body=config.MESSAGE % (config.CODES.get(code, 'Unknown (%s)' % code), datetime.now(config.DOOR_TZ).strftime('%I:%M %p %m/%d/%y'))
    )
    return Response(status=200)

if __name__ == '__main__':
    app.run(debug=True)