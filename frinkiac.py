import os
import schedule
import requests
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from twilio.base.exceptions import TwilioException

# The first four lines in the code above are simply importing all of the libraries we just installed.

# The three lines after our imports configure and create a TwilioRestClient object that will let us make calls to the
# Twilio REST API.
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
phoneTo = os.environ.get('PHONE_TO')
phoneFrom = os.environ.get('PHONE_FROM')


print("To :", phoneTo, "From :", phoneFrom)
client = Client(account_sid, auth_token)


def get_quote():
    headers = {'content-type': 'application/json'}
    r = requests.get("https://frinkiac.com/api/random", headers=headers)


    print(r)
    if r.status_code == 200:
        json = r.json()
        print(json)
        # Extract the episode number and timestamp from the API response
        # and convert them both to strings.
        frame_id, episode, timestamp = map(str, json["Frame"].values())
        print("Timestamp :", timestamp, "episode :",episode)

        image_url = "https://frinkiac.com/meme/" + episode + "/" + timestamp

        # Combine each line of subtitles into one string.
        print(image_url)
        caption = "\n".join([subtitle["Content"] for subtitle in json["Subtitles"]])
        print(caption)
        return image_url, caption


def send_MMS():
    media, body = get_quote()
    try:
        message = client.messages.create(
            body=body,
            media_url=media,
            to=phoneTo,  # Replace with your phone number
            from_=phoneFrom)  # Replace with your Twilio number
        print("Message sent!")
    # If an error occurs, print it out.
    except TwilioRestException as e:
        print(e)


# schedule.every().day.at("12:00").do(send_MMS)
schedule.every(3).seconds.do(send_MMS)
while True:
    schedule.run_pending()
