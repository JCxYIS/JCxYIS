from constants import BLOCK_STRS, NUM_STRS, HEART_STRS, GITHUB_REPO_USER, GITHUB_REPO_NAME


def board2console(board: list[list[int]], revealed_poses: list[int]):
    """
    directly print in console
    :param board:
    :param revealed_poses:
    """
    # TODO: support board size other than 10x10
    for i in range(len(board) + 1):
        for j in range(len(board[i - 1]) + 1):
            # table header
            if i == 0:
                print('    0  1  2   3  4  5  6  7   8  9', end=' ')
                break
            if j == 0:
                print(i - 1, end='0 ')
                continue

            # real board
            n = board[i - 1][j - 1]
            # print(n, end=' ')
            # continue
            from game import GameBase
            if GameBase.board_to_pos(i - 1, j - 1) not in revealed_poses:  # not guessed
                print(BLOCK_STRS[0], end=' ')
            elif n > 0:  # distance
                print(NUM_STRS[n], end=' ')
            elif n < 0:  # heart
                print(HEART_STRS[-n], end=' ')
        print()


def render_interface_md(board, revealed_poses, heart_finders, heart_finders_history, current_id):
    result = ''
    with open('Template.md', 'r') as f:
        result = f.read()

    # make a new tmp
    tmp = list[list[str]](heart_finders_history)
    tmp.insert(0, heart_finders)

    # Plug in stuffs :)
    result = result\
        .replace('{ BOARD }', board2md(board, revealed_poses, True))\
        .replace('{ STATS }', heart_finders_to_md(tmp, current_id))
    return result


#
# -------------------------------------------------------
#

def board2md(board: list[list[int]], revealed_poses: list[int], with_links: bool) -> str:
    """
   :param board:
   :param revealed_poses:
   :returns markdown str
   """
    # TODO: support board size other than 10x10
    result = ''
    for i in range(len(board) + 1):
        for j in range(len(board[i - 1]) + 1):
            # table header
            if i == 0:
                result += '|     |  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |\n'
                result += '|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|'
                break
            if j == 0:
                result += '| **' + str(i-1) + '0** | '
                continue

            # real board
            n = board[i - 1][j - 1]
            from game import GameBase
            pos = GameBase.board_to_pos(i - 1, j - 1)
            if pos not in revealed_poses:  # not guessed
                if with_links:
                    result += f'[{BLOCK_STRS[0]}](https://github.com/{GITHUB_REPO_USER}/{GITHUB_REPO_NAME}/issues/new' \
                              f'?title=💓💓💓{pos}&labels=game&body=Press%20**Submit%20new%20issue**%20below%20and%20wait%20for%20a%20little%20moment~) | '
                else:
                    result += f'{BLOCK_STRS[0]} | '
            elif n > 0:  # distance
                result += NUM_STRS[n] + ' | '
            elif n < 0:  # heart
                result += HEART_STRS[-n] + ' | '
        result += '\n'
    return result + '\n'


def heart_finders_to_md(heart_finders_all: list[list[str]], id_end_at=-1) -> str:
    """
    :param heart_finders_all: 2d array: if len==1 will print only 1 row
    :param id_end_at: == -1: dont print #; else will print id, e.g. ==3, than will print #3, #2, #1, etc.)
    :return: md str
    """
    # TODO: support heart count other than 7
    result = ''
    if id_end_at == -1:
        result += '|  ❤   |  🧡   | 💛  | 💚  | 💙  | 💜  | 🤎  |\n'
        result += '|:----:|:-----:|:---:|:---:|:---:|:---:|:---:|\n'
    else:
        result += '|     Game#    |  ❤   |  🧡   | 💛  | 💚  | 💙  | 💜  | 🤎  |\n'
        result += '| ------------ |:----:|:-----:|:---:|:---:|:---:|:---:|:---:|\n'

    heart_finders_all.reverse()
    id = id_end_at
    for heart_finders in heart_finders_all:
        if id_end_at == -1:
            result += '| '
        elif id_end_at == id:
            result += f'| [{str(id)} **(now)**](https://github.com/{GITHUB_REPO_USER}/{GITHUB_REPO_NAME}/blob/main/logs/logs_{str(id)}.md) | '
        else:
            result += f'| [{str(id)}](https://github.com/{GITHUB_REPO_USER}/{GITHUB_REPO_NAME}/blob/main/logs/logs_{str(id)}.md) | '
        for heart_finder in heart_finders[1:]:
            result += f'[{heart_finder}](https://github.com/@{heart_finder}) | '
        result += '\n'
        id -= 1

    return result + '\n'
