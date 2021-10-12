from shutil import make_archive


if __name__ == '__main__':
    try:
        make_archive('aqua', format='zip', root_dir='dist')
    except Exception:
        print('zipファイルの作成に失敗しました')

