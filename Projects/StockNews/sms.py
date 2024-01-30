from twilio.rest import Client


def send_sms(from_, to, body, account_sid, auth_token):
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_=from_,
        to=to,
    )

    print(message.sid)
