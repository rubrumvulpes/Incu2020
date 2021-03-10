import datetime
import requests
import json
from pytz import timezone

from flask import Flask, request

"""           BOT DATA           """

bot_name = "timezoneconverter@webex.bot"
roomId = "Y2lzY29zcGFyazovL3VzL1JPT00vMjUyMTNjYjMtYTUwZC0zZWQyLWFjMjItOTY1YmExN2JlZjRm"
token = "YzliZWQxYjgtNzMwMy00YWFmLWFmMTMtZGRiNDYwMGI2YmZkZDQ2ZGNhMzQtMDI4_PF84_consumer"
header = {
    "content-type": "application/json; charset=utf-8",
    "authorization": f"Bearer {token}",
}
help_text = "Helper text\nWrite 'currentcontinent/capital datetime->yyyy:mm:ddThh:mm:ss targetcontinent/capital)'"
info = (
    "This is the TimeZone Converter!\nGot an important meeting across the world?\nNever miss it due to time "
    "difference! "
)

"""      BOT IMPLEMENTATION      """


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def timezone_converter():
    webhook = request.json
    url = "https://webexapis.com/v1/messages"
    payload = {"roomId": webhook["data"]["roomId"]}
    sender = webhook["data"]["personEmail"]
    message = get_message()

    if sender != bot_name:
        if message.lower() == "help":
            payload["markdown"] = help_text
        elif message.lower() == "info":
            payload["markdown"] = info
        else:
            try:
                split_message = message.split()
                formated_time_list = [
                    item.split(":") for item in split_message[1].split("T")
                ]
                requestee_time = datetime.datetime(
                    int(formated_time_list[0][0]),
                    int(formated_time_list[0][1]),
                    int(formated_time_list[0][2]),
                    int(formated_time_list[1][0]),
                    int(formated_time_list[1][1]),
                    int(formated_time_list[1][2]),
                    tzinfo=timezone(split_message[0]),
                )
                format = "%Y-%m-%d %H:%M:%S %Z%z"
                payload["markdown"] = (
                    f"Time in {split_message[2]} : "
                    f"{(requestee_time.astimezone(timezone(split_message[2]))).strftime(format)}"
                )

            except:
                payload["markdown"] = f"Error occured\n{help_text}"

        requests.post(url, data=json.dumps(payload), headers=header, verify=True)


def get_message():
    webhook = request.json
    url = f"https://webexapis.com/v1/messages/{webhook['data']['id']}"
    return (requests.get(url, headers=header, verify=True)).json()["text"]


app.run(debug=True)
