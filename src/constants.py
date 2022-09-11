# ❤️ 🧡 💛 💚 💙 💜 🖤 🤍 🤎 💔 ❣️ 💕 💞 💓 💗 💖 💘 💝
import os

BOARD_WIDTH = 10  # max: 16
BOARD_HEIGHT = 10  # max: 16
HEARTS_COUNT = 7  # max: 9

HEART_STRS = ['', '❤', '🧡', '💛', '💚', '💙', '💜', '🤎', '🖤', '🤍']  # index 0 is null
NUM_STRS = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣, '7️⃣', '8️⃣', '9️⃣', '🔟']
DIR_STRS = ['➡', '⬅', '⬆', '⬇', '↗', '↘', '↙', '↖']
BLOCK_STRS = ['🔳', '🔲']

BASE_PATH = os.environ.get('BASE_PATH', '.runtime/')  # should be '../' on remote, but not to be added to VCS at local
LOG_DIR_PATH = BASE_PATH + 'logs/'
SAVE_PATH = BASE_PATH + '.save.txt'

GITHUB_REPO_USER = os.environ.get('GITHUB_REPO_USER', 'JCxYIS')
GITHUB_REPO_NAME = os.environ.get('GITHUB_REPO_NAME', 'gh-profile-game')

GITHUB_APP_KEY = os.environ.get('GITHUB_APP_KEY')  # should be a very long RSA key
GITHUB_APP_ID = os.environ.get('GITHUB_APP_ID')  # int, e.g. "236777"

DEPLOY_SALT = os.environ.get('GITHUB_APP_ID', 'LOLI_GOOD')  # I believe there's no one that boring to crack ma game



