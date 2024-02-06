import argparse
import http.client, urllib
def create_parser():
    parser = argparse.ArgumentParser(
        description="Downnload, and filter the PDB fiiles from the RCBS PDB database"
        )
    parser.add_argument(
        "--message",
        type=str,
        required=False,
        default="Hello World!",
        help="The message to send to the user.",
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
    keys = read_keys_from_file("../pushover.keys")

    api_token = keys.get("api_token")
    user_key = keys.get("user_key")

    message = args.message
    send_pushover_notification(api_token, user_key, message)

