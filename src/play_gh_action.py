from os import path

from github import Github, GithubIntegration
from github.Issue import Issue
from github.PaginatedList import PaginatedList
from github.Repository import Repository

from game import GameBase
import renderer
from constants import SAVE_PATH, BASE_PATH, GITHUB_REPO_USER, GITHUB_REPO_NAME, GITHUB_APP_ID, GITHUB_APP_KEY, DEPLOY_SALT
from game_config import GameConfig


class Game(GameBase):
    gh: Github
    repo: Repository
    issues: list[Issue]
    current_issue: Issue

    def __init__(self):
        # setup GitHub
        gh_app = GithubIntegration(GITHUB_APP_ID, GITHUB_APP_KEY)
        self.gh = Github(gh_app.get_access_token(gh_app.get_installation(GITHUB_REPO_USER, GITHUB_REPO_NAME).id).token)
        self.repo = self.gh.get_repo(f'{GITHUB_REPO_USER}/{GITHUB_REPO_NAME}')
        print('Get github repo', self.repo.name)

        # load game setups
        config: GameConfig
        if path.exists(SAVE_PATH):
            with open(SAVE_PATH) as f:
                s = f.read()
                config = GameConfig.from_json(s)
        else:
            print('Create new game...')
            config = GameConfig()
        super().__init__(config, hash(DEPLOY_SALT+str(config.seed)))

    def game_inited(self):
        # print board on start
        self.render_board()

    def set_user(self):
        # Find all issues
        self.issues = list(self.repo.get_issues(state='open'))
        if len(self.issues) == 0:
            print('All issues are cleared!')
            exit(0)
        self.current_issue = self.issues.pop()
        # Check Invalid
        if not self.current_issue.title.startswith('💓💓💓'):
#             self.current_issue.create_comment('I don\'t know what you mean...')
#             self.current_issue.edit(state='closed', labels=['game', 'invalid'])
            self.set_user()  # skip to next issue
            return
        self.user = self.current_issue.user.name
        self.current_issue.edit(state='closed', labels=['game'])  # close it first to avoid sync issue (gh-action may trigger multiple times)
        print('user: ', self.user)

    def handle_cmd(self) -> int:
        cmd = self.current_issue.title.replace('💓💓💓', '').replace(' ', '')
        if not cmd.isdigit():
            print("Not A Number!")
            cmd = -1
        print('cmd: ', cmd)
        return int(cmd)

    def render_board(self):
        # write board to console
        renderer.board2console(self.board, self.config.revealed_poses)
        # write a production md
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
        self.current_issue.create_comment(
            f'Done! You may now visit https://github.com/{GITHUB_REPO_USER}')


if __name__ == '__main__':
    # init game
    game = Game()
    game.play(play_recursive=True)

