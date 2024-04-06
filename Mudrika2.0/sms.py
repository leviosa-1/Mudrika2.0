from twilio.rest import Client
def send_sms():
    account_sid = "AC091ddcdbd3f3a86db5c7ab71145435fe"
    auth_token = "6c9750c149dbe1580668098e140f319a"
    client = Client(account_sid, auth_token)
    to_number = "+917024896018"
    from_number = "+16592518494"
    message_body = "ALert!!! someone needs your help at Location:- 22.7081955, 75.8824422"
    message = client.messages.create(
    body=message_body,
    from_=from_number,
    to=to_number
    )
    print(f"Message sent with SID: {message.sid}")
