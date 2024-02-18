class Const:
    def __init__(self, const):
        """
        定数として記録する
        :param const:
        """
        self._const_ = const

    def get_const(self):
        """
        定数のgetter、setterは無し
        """
        return self._const_
