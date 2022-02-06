## Poweroff Command.
if HS_Data["poweroff"]["status"] == True:
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    formattedRequestTime = datetime.strptime(HS_Data["poweroff"]["requestTime"], '%Y-%m-%d %H:%M:%S')

    # Check if it has been 60 seconds since the request was made.
    if str(time_now) == str(formattedRequestTime + timedelta(seconds = 60)):

        functions.send_message(recepient_id = HS_Data["alert_channel_id"], message = "The system has now temporarily deactivated. All requests will be suspended until it is reactivated. You will be notified of this event.")

        HS_Data["poweroff"]["status"] = False
        HS_Data["poweroff"]["requestTime"] = ""

        with open('data.json', 'w') as data_file:
            json.dump(HS_Data, data_file, indent = 4)

        os.system('shutdown now -h')

## Restart Command
if HS_Data["restart"]["status"] == True:
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    formattedRequestTime = datetime.strptime(HS_Data["restart"]["requestTime"], '%Y-%m-%d %H:%M:%S')

    # Check if it has been 60 seconds since the request was made.
    if str(time_now) == str(formattedRequestTime + timedelta(seconds = 60)):

        functions.send_message(recepient_id = HS_Data["alert_channel_id"], message = "The system has now restarted. You will be notified when the restart has completed.")

        HS_Data["restart"]["status"] = False
        HS_Data["restart"]["requestTime"] = ""

        with open('data.json', 'w') as data_file:
            json.dump(HS_Data, data_file, indent = 4)

        os.system('shutdown now -r')