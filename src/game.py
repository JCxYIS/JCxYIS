import abc
import os
import random

import logger
import renderer
from constants import BOARD_WIDTH, BOARD_HEIGHT, HEARTS_COUNT, BASE_PATH, LOG_DIR_PATH
from game_config import GameConfig


class GameBase(abc.ABC):  # ABC: Abstraction Base Classes
    """
    Abstract base of the game, need to inherit this.
    """
    # Game config
    config: GameConfig
    user: str  = ''  # player data

    # Runtime variables
    board = [[999 for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGHT)]  # 8x8 game
    """
    Negative int: heart
    Positive int: Min distance to heart 
    """

    def __init__(self, config: GameConfig, seed: int):
        """
        load seed and generate board
        """
        self.config = config
        random.seed(seed)

        # init folder
        os.makedirs(BASE_PATH, exist_ok=True)

        # determine hearts pos
        poses = []
        for i in range(HEARTS_COUNT):
            pos_num = -1
            while pos_num == -1 or pos_num in poses:
                pos_num = random.randint(0, BOARD_WIDTH * BOARD_HEIGHT - 1)
            poses.append(pos_num)
            self.board[int(pos_num / BOARD_WIDTH)][int(pos_num % BOARD_HEIGHT)] = -len(poses)

        # determine each "heartless" pos: min distance to heart
        for iterate in range(len(poses)):
            queue = [{'pos': poses[iterate], 'dist': 0}]
            # BFS
            while len(queue) > 0:
                item = queue.pop(0)
                pos = item['pos']
                dist = item['dist']
                # print(pos)
                current_dist = self.get_pos(pos)
                if current_dist < 0:  # hearts
                    if dist == 1:  # heart is aside
                        continue
                    dist = 0
                elif dist >= current_dist:  # no need to update
                    continue
                else:  # update!
                    self.set_pos(pos, dist)
                if int(pos % 10) != 0: queue.append({'pos': pos - 1, 'dist': dist + 1})
                if int(pos % 10) != 9: queue.append({'pos': pos + 1, 'dist': dist + 1})
                if int(pos / 10) != 0: queue.append({'pos': pos - 10, 'dist': dist + 1})
                if int(pos / 10) != 9: queue.append({'pos': pos + 10, 'dist': dist + 1})

    def play(self, play_recursive: bool):
        """
        Main Game Logic
        :param play_recursive: Play multiple rounds in one execution?
        :return:
        """
        play_round = 0
        self.game_inited()
        while play_round == 0 or play_recursive:
            play_round += 1
            self.set_user()
            self.round_started()
            cmd = self.handle_cmd()
            self.eval_cmd(cmd)
            self.render_board()
            self.write_save()
            self.write_log()
            self.round_finished()

    def game_inited(self):
        """
        Called when game is inited
        """
        pass

    def round_started(self):
        """
        Called when a round has started
        :return:
        """
        pass

    @abc.abstractmethod
    def set_user(self):
        pass

    @abc.abstractmethod
    def render_board(self):
        pass

    @abc.abstractmethod
    def handle_cmd(self) -> int:
        pass

    def eval_cmd(self, cmd: int):
        """
        Evaluate user input
        :param cmd: >=0: guess, -1: invalid
        """
        if cmd >= 0:  # guess a pos
            # check range
            if cmd >= BOARD_WIDTH * BOARD_HEIGHT:
                print('Out of range!!')
                return

            # check existed
            if cmd in self.config.revealed_poses:
                print('Pos ' + str(cmd) + " has already been guessed!")
                return

            # append into revealed_poses list
            self.config.revealed_poses.append(cmd)

            # check if hit the heart
            heart = self.get_pos(cmd)
            if heart < 0:
                # oh yeah, record the hitter
                self.config.heart_finders[-heart] = self.user
                logger.write_found_result(self.user, -heart)

            # Log
            logger.write_round_result(
                len(self.config.revealed_poses),
                self.user,
                renderer.board2md(self.board, self.config.revealed_poses, False))

            # check if game completed
            if '' not in self.config.heart_finders[1:]:
                print('Game Completed!')

                # flush the current logger before we update
                self.config.heart_finders_history.append(self.config.heart_finders)
                logger.write_final_result(
                    renderer.heart_finders_to_md(self.config.heart_finders_history, self.config.id))
                self.write_log()

                # new game!
                new_config = GameConfig()
                new_config.heart_finders_history = self.config.heart_finders_history
                new_config.id = self.config.id + 1
                if len(new_config.heart_finders_history) > 3:
                    new_config.heart_finders_history.pop(0)
                self.config = new_config
        else:
            pass  # TODO: extra cmds?

    @abc.abstractmethod
    def write_save(self):
        """
        save the game (config)
        """
        pass

    def write_log(self):
        logger.flush(str(self.config.id))

    def round_finished(self):
        """
        Called when a round is finished
        """
        pass

    # ---

    def get_pos(self, pos: int):
        """
        Helper function for getting certain pos on the board by num
        :param pos:
        :return:
        """
        return self.board[int(pos / BOARD_WIDTH)][int(pos % BOARD_HEIGHT)]

    def set_pos(self, pos: int, value: int):
        """
        Helper function for setting certain pos on the board by num
        :param value:
        :param pos:
        :return:
        """
        self.board[int(pos / BOARD_WIDTH)][int(pos % BOARD_HEIGHT)] = value

    @staticmethod
    def board_to_pos(i: int, j: int):
        """
        Helper function that converts [i][j] to pos form
        :param i:
        :param j:
        :return:
        """
        return i * BOARD_WIDTH + j
