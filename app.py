from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    print(request.form)
    msg = request.form.get('Body')
    sender = request.form.get('From')

    # Create reply
    resp = MessagingResponse()
    msg_reply,img=fetch_reply(msg,sender)
    
    if img!=' ':
        final_img="https://image.tmdb.org/t/p/w600_and_h900_bestv2"+img
        resp.message(msg_reply).media(final_img)
    else :
        resp.message(msg_reply)
        #return str(msg_reply)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)