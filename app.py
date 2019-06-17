from flask import Flask, jsonify, request
from buienradar.buienradar import (get_data, parse_data)
from buienradar.constants import (CONTENT, RAINCONTENT, SUCCESS)

app = Flask(__name__)


def parse_rainfall(data):
    lines = data.splitlines()
    index = 1
    nrlines = len(lines)
    result = []

    while index < nrlines:
        line = lines[index]
        # pylint: disable=unused-variable
        (val, key) = line.split("|")
        result.append({"time": key, "value": val})
        index += 1

    return result


@app.route('/')
def forecast():
    timeframe = 60

    # gps-coordinates for the weather data
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))

    result = get_data(latitude=latitude,
                      longitude=longitude,
                      )

    if result.get(SUCCESS):
        data = result[CONTENT]
        raindata = result[RAINCONTENT]

        result = parse_data(data, raindata, latitude, longitude, timeframe)

    return jsonify({"forecast": result, "rainfall": parse_rainfall(raindata)})


if __name__ == '__main__':
    app.run()
