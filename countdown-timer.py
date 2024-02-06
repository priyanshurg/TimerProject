import argparse
import http.client, urllib, re, time
from plyer import notification

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10  # Specify the notification timeout in seconds
    )

def time_argument(value):
    if ':' in value:
        try: 
            hours = int(value.split(':')[0])
            minutes = int(value.split(':')[1])
            return hours*60*60 + minutes*60
        except:
            print("Time format is not HH:MM")

    elif "h" in value and "m" in value:
        try:
            hours = int(value.split('h')[0])
            minutes = int(value.split('h')[1].strip('m'))
            return hours*60*60 + minutes*60
        except:
            print("time format is not XhYm")
    elif "m" in value and "s" in value:
        try:
            minutes = int(value.split('m')[0])
            seconds = int(value.split('m')[1].strip('s'))
            return minutes*60 + seconds
        except:
            print("Time format is not XmYs")
    elif "s" in value and "m" not in value:
        try:
            seconds = int(value.split('s')[0])
            return seconds
        except:
            print("Time not in Xs format")
    elif "h" in value and "m" not in value:
        try:
            hours = int(value.split('h')[0])
            return hours*3600
        except:
            print("Time format is not Xh ")
    elif "m" in value and "h" not in value and "s" not in value:
        try:
            minutes = int(value.split('h')[0])
            return minutes*60
        except:
            print("Time format is not Xh ")

        


def create_parser():
    parser = argparse.ArgumentParser(
        description="Run a countdown timer in following formats ex. 1:30, 1h30m, 1m30s, 1m, 30s, 1h."
        )
    parser.add_argument(
        "--message",
        type=str,
        required=False,
        default="Hello World!",
        help="The message to send to the user.",
        )
    parser.add_argument(
        '--time', 
        type=str, 
        required=False,
        help="Usage: python3 time-notif.py --time 0m2s \n Time formats accepted: [HH:YY] [HhMm] [MmSs] [Ss] [Hh] [Mm]",        
        )

    return parser



def read_keys_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        keys = {}
        for line in lines:
            key, value = line.strip().split(':')
            keys[key] = value
        return keys
def send_pushover_notification(api_token, user_key, message):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": f"{api_token}",
        "user": f"{user_key}",
        "message": f"{message}",
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    if args.time == '':
        print("Usage: python3 time-notif.py --time 0m2s \n Time formats accepted: [HH:YY] [HhMm] [MmSs] [Ss] [Hh] [Mm]")
        exit()

    if args.time:
        time_val = time_argument(args.time)
        print(time_val)
        time.sleep(time_val)

    keys = read_keys_from_file("../pushover.keys")

    api_token = keys.get("api_token")
    user_key = keys.get("user_key")

    message = args.message
    send_pushover_notification(api_token, user_key, message)
    title = "Python notification- Countdown Timer"
    send_notification(title, message)
