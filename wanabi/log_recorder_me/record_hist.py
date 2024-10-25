import datetime


class RecordHist:
    def __init__(self, filename: str):
        self.filename: str = filename

    def write_log(self, message: str) -> None:
        now_time = datetime.datetime.now()
        err_message = f"{now_time.year}/{now_time.month}/{now_time.day}-:{now_time.hour}:{now_time.minute}:{now_time.second}:{message}"
        with open(self.filename, mode="a+", encoding="utf-8") as f:
            f.write(err_message + "\n")

