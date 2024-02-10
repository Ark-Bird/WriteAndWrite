class RamMemo:
    def __init__(self):
        self.memo: str = "I am amnesia"

    def new_memo(self, memo: str) -> None:
        self.memo = memo
        return

    def remember(self) -> str:
        return self.memo
