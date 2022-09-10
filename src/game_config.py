import datetime
import json
import random
from types import SimpleNamespace
from constants import HEARTS_COUNT


class GameConfig:
    id: int
    seed: int
    revealed_poses: list[int]
    heart_finders: list[str]
    heart_finders_history: list[list[str]]

    def __init__(self):
        # wow python3 has no limit for int lol, but guess i will leave it here
        self.id = 1  # datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.seed = random.randint(-2147483648, 2147483647)
        self.revealed_poses = []
        self.heart_finders = ['' for x in range(HEARTS_COUNT + 1)]
        self.heart_finders_history = []

    @staticmethod
    def to_json(data):
        return json.dumps(data, default=lambda o: o.__dict__, sort_keys=True)

    @staticmethod
    def from_json(data):
        return json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
