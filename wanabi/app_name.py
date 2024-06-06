from wanabi import const


class AppName:
    def __init__(self):
        """
        アプリ名を定数として設定
        タイトルバーに表示されるアプリ名（仮）
        """
        self._APP_CODE_NAME: const.Const = const.Const("""水無月""")

    def return_app_name_for_now(self) -> str:
        """
        暫定アプリ名を返す
        :return: アプリ名
        """
        return self._APP_CODE_NAME.get_const()
