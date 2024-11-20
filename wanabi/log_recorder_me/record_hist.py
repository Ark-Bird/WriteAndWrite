import datetime
import wanabi.encoding

class RecordHist:
    def __init__(self, filename: str):
        self.filename: str = filename
        self.codepoint = wanabi.encoding.Encoding()
        self.code = self.codepoint.code

    def write_log(self, message: str) -> None:
        now_time = datetime.datetime.now()
        err_message = f"{now_time.year}/{now_time.month}/{now_time.day}-:{now_time.hour}:{now_time.minute}:{now_time.second}:{message}"
        with open(self.filename, mode="a+", encoding=self.code) as f:
            f.write(err_message + "\n")

