from twilio.rest import Client
def send_sms():
    account_sid = "Twillio account_sid"
    auth_token = "Twillio auth_token"
    client = Client(account_sid, auth_token)
    to_number = "receiver's number"
    from_number = "Twillio phone number"
    message_body = "ALert!!! someone needs your help at Location:- 22.7081955, 75.8824422"
    message = client.messages.create(
    body=message_body,
    from_=from_number,
    to=to_number
    )
    print(f"Message sent with SID: {message.sid}")
