from twilio.rest import Client

class MessageHandler:
    phone_number = None
    otp = None
    acc_sid = 'AC94b9d02a8cfba3054b71456208def8be'
    auth_token = '349d7c1714e6904e71d8abd5733b7d6d'
    def __init__(self,phone_number,otp):
        self.phone_number = phone_number
        self.otp = otp
    def send_otp(self):
        message = f'Team Drugger\notp for registration of {self.phone_number} is : {self.otp}'
        client = Client(self.acc_sid, self.auth_token)

        message = client.messages.create(
            from_='+19389465628',
            body=message,
            to=f'{self.phone_number}'
        )

        print(message.sid)
