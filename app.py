import datetime
import flask_excel as excel
from flask import Flask, request
from db import trading_service


app = Flask(__name__)


@app.route("/download", methods=['GET'])
def download_file():
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    output = search_data(from_date, to_date)
    return excel.make_response_from_array(output, "xlsx",
                                          file_name="trading_view")


@app.route("/export", methods=['GET'])
def export_records():
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    output = search_data(from_date, to_date)
    return excel.make_response_from_array(output, "xlsx",
                                          file_name="trading_view")


def search_data(from_date=None, to_date=None):
    if from_date is None:
        from_date = "2001-01-01 00:00"
    if to_date is None:
        to_date = format(datetime.datetime.now(), "%Y-%m-%d %H:%M")
    query = {"time": {"$gte": from_date, "$lte": to_date}}
    cursor = trading_service.find(query, {"_id": False})

    output = []

    output.append(['time', '열기', '고가', '저가', '종'])

    for data in cursor:
        output.append([data['time'], data['열기'], data['고가'], data['저가'], data['종']])

    return output


# insert database related code here
if __name__ == "__main__":
    excel.init_excel(app)
    app.run(host="0.0.0.0")