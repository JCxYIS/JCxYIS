import os

from constants import LOG_DIR_PATH, HEART_STRS

buffer: list[str] = [' ']


def write_log(data: str):
    buffer.append(data)


def write_found_result(user, heart_index):
    buffer.append(f'## [{user}](https://github.com/@{user}) find a {HEART_STRS[heart_index]}!\n')


def write_round_result(guess_count: int, user, table: str):
    buffer.append(
        '\n<details> \n' +
        f'<summary> Guess #{guess_count} by\n\n[{user}](https://github.com/@{user}) \n\n</summary>\n' +
        '<br>\n\n' +
        table + '\n' +
        '</details>\n'
    )

def write_final_result(table:str):
    buffer.append('---')
    buffer.append('\n' + table)

def flush(id: str):
    """
    write the buffer into log file
    """
    os.makedirs(LOG_DIR_PATH, exist_ok=True)
    path = LOG_DIR_PATH + 'logs_' + id + '.md'
    if not os.path.exists(path):
        buffer.insert(0, '# Game ' + id + '\n')

    with open(path, 'a') as f:
        f.writelines(buffer)
        buffer.clear()
