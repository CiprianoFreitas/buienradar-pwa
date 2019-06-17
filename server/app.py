from flask import Flask, jsonify, request
from buienradar.buienradar import (get_data, parse_data)
from buienradar.constants import (CONTENT, RAINCONTENT, SUCCESS)

app = Flask(__name__)


@app.route('/')
def forecast():
    timeframe = 45

    # gps-coordinates for the weather data
    latitude = int(request.args.get('latitude'))
    longitude = int(request.args.get('longitude'))

    result = get_data(latitude=latitude,
                    longitude=longitude,
                    )

    if result.get(SUCCESS):
        data = result[CONTENT]
        raindata = result[RAINCONTENT]

        result = parse_data(data, raindata, latitude, longitude, timeframe)

    return jsonify(result)

if __name__ == '__main__':
    app.run()