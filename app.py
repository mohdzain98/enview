import os

from flask import Flask, render_template, request, redirect, url_for,flash
app = Flask(__name__)
alerts = [
  {
    "id": "6049dbd2-45bc-4e34-9ea2-c82ced0279f1",
    "alert_type": "Unsafe driving",
    "vehicle_id": "cc70a7e5-8397-4914-bbbb-4d6bb521ec67",
    "driver_friendly_name": "Ramesh",
    "vehicle_friendly_name": "KA12A3456",
    "timestamp": "2023-03-01T04:25:45.424Z",
    "status": "active"
  },
  {
    "id": "5149dbd2-45bc-4e34-9ea2-c82ced0279f1",
    "alert_type": "Distracted driver",
    "vehicle_id": "dd70a7e5-8397-4914-bbbb-4d6bb521ec67",
    "driver_friendly_name": "Suresh",
    "vehicle_friendly_name": "MH12A3456",
    "timestamp": "2023-03-01T04:24:45.424Z",
    "status": "active"
  },
]

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

from datetime import datetime
def getTime(time):
    timestamp_datetime = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    date_string = timestamp_datetime.strftime("%d %B %Y")
    time_string = timestamp_datetime.strftime("%H:%M")

    formatted_string = f"{date_string} at {time_string}"
    return formatted_string

@app.route("/alerts", methods=['POST','GET'])
def searchrecord():
    if request.method == "POST":
        
        name = request.form.get("name")
        vehicle=request.form.get("vehicle")
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        filtered_alerts = []
        time =[]

    for alert in alerts:
        if (
            (name.lower() in alert['alert_type'].lower() or
             name.lower() in alert['driver_friendly_name'].lower() or
             name.lower() in alert['vehicle_friendly_name'].lower()) if name else True
        ) and (
            (vehicle.lower() in alert['vehicle_friendly_name'].lower()) if vehicle else True
        )and (
            (start_date <= alert['timestamp'] <= end_date) if start_date and end_date else True
        ):
            filtered_alerts.append(alert)
            time.append(getTime(alert['timestamp']))

    return render_template('index.html', alerts=filtered_alerts, time=time)

@app.route('/mark_false_alarm/<alert_id>')
def mark_false_alarm(alert_id):
    for alert in alerts:
        if alert['id'] == alert_id:
            alert['status'] = 'false_alarm'
            break

    return render_template('index.html', alerts=alerts)


if __name__ == "__main__":
    app.run(debug=True)