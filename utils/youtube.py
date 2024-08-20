import datetime

def month_before_rfc3339():
    return (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30)).isoformat("T")