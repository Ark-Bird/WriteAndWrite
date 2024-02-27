class RamMemo:
    def __init__(self):
        """
        フィールドの初期化
        """
        self.memo: str = "I am amnesia"

    def new_memo(self, memo: str) -> None:
        """
        実行中に変数memoに文字列を保持
        スクリプト終了時に変数は破棄される
        :param memo:
        :return:
        """
        self.memo = memo
        return

    def remember(self) -> str:
        """
        変数memoを返す関数
        :return:self.memoはstr型
        """
        return self.memo
