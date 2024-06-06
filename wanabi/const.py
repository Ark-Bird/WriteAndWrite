from typing import Any


class Const:
    def __init__(self, const: Any):
        """
        定数として記録する
        :param const: 任意の方の定数
        """
        self._const_: Any = const

    def get_const(self) -> Any:
        """
        定数のgetter、setterは無し
        :return:インスタンスの保持する定数
        """
        return self._const_
