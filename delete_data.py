import datetime
from db import trading_service


def delete_data():
    trading_service.remove({'열기': '7509.25', '고가': '7511.00', '저가': '7509.00', '종': '7511.00'})
    for data in trading_service.find({'열기': '7509.25', '고가': '7511.00', '저가': '7509.00', '종': '7511.00'}):
        print(data)


def search_data(from_date=None, to_date=None):
    if from_date is None:
        from_date = "2001-01-01 00:00"
    if to_date is None:
        to_date = format(datetime.datetime.now(), "%Y-%m-%d %H:%M")
    query = {"time": {"$gte": from_date, "$lte": to_date}}
    cursor = trading_service.find(query, {"_id": False})
    print(list(cursor))
    # for data in cursor:
    #     print(data)


if __name__ == '__main__':
    # delete_data()
    search_data()
    # search_data("2019-06-13 14:10", "2019-06-14 06:55")