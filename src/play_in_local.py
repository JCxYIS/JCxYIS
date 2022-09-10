from os import path

from game import GameBase
import renderer
from constants import BLOCK_STRS, NUM_STRS, HEART_STRS, SAVE_PATH, BASE_PATH
from game_config import GameConfig


class Game(GameBase):
    def __init__(self):
        # load game setups
        config: GameConfig
        if path.exists(SAVE_PATH):
            with open(SAVE_PATH) as f:
                s = f.read()
                config = GameConfig.from_json(s)
        else:
            print('Create new game...')
            config = GameConfig()  # new
        super().__init__(config, config.seed)

    def game_inited(self):
        # print board on start
        self.render_board()

    def set_user(self):
        # input username if not inited
        if not self.user:
            print('Input your name: @', end='')
            self.user = input()

    def handle_cmd(self) -> int:
        print('Input a number to make your guess (1-99): ', end=' ')
        cmd = input()
        if not cmd.isdigit():
            print("Not A Number!")
            cmd = 0
        return int(cmd)

    def render_board(self):
        renderer.board2console(self.board, self.config.revealed_poses)
        # test: write a production md
        with open(BASE_PATH + 'README.md', 'w') as f:
            f.write(renderer.render_interface_md(
                self.board,
                self.config.revealed_poses,
                self.config.heart_finders,
                self.config.heart_finders_history,
                self.config.id
            ))

    def write_save(self):
        js = GameConfig.to_json(self.config)
        with open(SAVE_PATH, 'w') as f:
            f.write(js)


if __name__ == '__main__':
    # init game
    game = Game()
    game.play(play_recursive=True)

