class NotOpenPathException(Exception):
    """
    ファイルを開くのに失敗した時の例外
    基本的に握りつぶしてデフォルトを適用して続行する目的
    """

    pass


class FatalError(Exception):
    """
    復旧不能なエラーの発生時に投げる
    """

    pass
