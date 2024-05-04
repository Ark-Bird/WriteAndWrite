import const


class AppName:
    def __init__(self):
        """
        アプリ名を定数として設定
        """
        self._APP_CODE_NAME: const.Const = const.Const("""Lycoris""")

    def return_app_name_for_now(self) -> str:
        """
        暫定アプリ名を返す
        :return: app_name
        """
        return self._APP_CODE_NAME.get_const()
