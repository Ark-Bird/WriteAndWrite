from shutil import make_archive

import extend_exception
import independent_method

if __name__ == '__main__':
    try:
        make_archive('aqua', format='zip', root_dir='dist')
    except Exception:
        print('zipファイルの作成に失敗しました')
        raise extend_exception.FatalError
