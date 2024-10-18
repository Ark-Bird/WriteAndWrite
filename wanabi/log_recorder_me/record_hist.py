class RecordHist:
    def __init__(self, filename: str):
        self.filename: str = filename

    def write_log(self, message: str) -> None:
        with open(self.filename, mode="a+", encoding="utf-8") as f:
            f.write(message + "\n")

