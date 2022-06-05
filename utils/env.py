import asyncio
import sys
from json import dumps
from os import listdir, makedirs

from colorama import init, Fore
from faker import Faker

from utils import terminal
from utils.custom_logger import Log
from utils.root import get_project_root
from utils.terminal import update_title

init()
terminal.clear()
makedirs(f'{get_project_root()}/user_data/', exist_ok=True)


def line_not_empty(each): return len(each.strip()) > 0


def split_by_comma(each): return [line.strip() for line in each.strip().split(',')]


def strip_each(line): return [item.strip() for item in line.strip().split(',')][:2]


class Env:
    proxies: list = []
    accs_q: asyncio.Queue = asyncio.Queue()  # for sequential acc returning
    log: Log = Log('[ENV]', do_update_title=False)
    fake = Faker()
    update_title('Setting Up Env')

    def __init__(self):
        self.key, self.requests_per_second = (None for _ in range(2))
        self.increase_limits()
        self.make_files()
        self.load_config()
        self.is_running_on_server = True

        # proxies
        self.load_proxies(f'{get_project_root()}/user_data/proxies.txt')
        self.load_accs()

    def __str__(self):
        out = ''
        for key in dir(Env):
            if '__' in key:  # don't process python base stuff
                continue

            val = getattr(self, key)  # get the val in self
            if callable(val):  # don't process any functions
                continue
            if key in ('log', 'counter', 'fake'):
                continue
            if '_q' in key:
                this_val: asyncio.Queue = val
                val = this_val.qsize()
            if key in ('proxies', 'emails', 'accs'):
                val = len(val)
            val = '\n'.join(dumps(val, indent=4).split("\n"))
            out += f'[{key.upper()}]: {val}\n'
        return f"{Fore.BLUE}\n" \
               f"[ENV SUMMARY]\n\n" \
               f"{out}"

    def make_files(self):
        # make required files
        base_folders = {
            f'{get_project_root()}/user_data': [
                'proxies.txt',
                'config.csv',
                'accs_to_check.txt',
                'good_accs.txt',
                'webhooks.txt'
            ]
        }
        for folder, files in base_folders.items():
            makedirs(folder, exist_ok=True)  # make the folder if not exists
            current_files = listdir(folder)  # get current files in folder
            for file in files:
                if file not in current_files:
                    self.make_default_file(folder, file)

    @staticmethod
    def make_default_file(folder, file_name):
        with open(f'{folder}/{file_name}', 'w') as file:
            if file_name == 'config.csv':
                out = "SETTING, VALUE\n"
                to_write = [
                    ('KEY', 'WINX4-E67X-3O49-2QR1-A9PZ'),
                    ('REQUESTS PER SECOND', '50')
                ]
                for setting, value in to_write:
                    out += f'{setting}, {value}\n'
                file.write(out)
                return True
            return False

    """Loading ENV object."""

    def load_config(self):
        # grab config
        with open(f'{get_project_root()}/user_data/config.csv') as file:
            settings = {
                split_by_comma(line)[0].strip(): split_by_comma(line)[1].strip()
                for line in file.readlines()
                if line_not_empty(line)
            }

            self.key = settings['KEY']
            self.requests_per_second = int(settings['REQUESTS PER SECOND'])

        out = ''
        for key, val in settings.items():
            out += f'\t{key}: {val}\n'

    def load_proxies(self, proxies_file):
        with open(proxies_file) as file:
            self.proxies = [line.strip().split(':') for line in file.readlines() if line_not_empty(line)]
            self.proxies = [
                f'http://{line[0]}:{line[1]}'
                if len(line) == 2
                else
                f'http://{line[2]}:{line[3]}@{line[0]}:{line[1]}'
                for line in self.proxies
            ]
        Env.proxies = self.proxies

    def load_accs(self):
        with open(f'{get_project_root()}/user_data/accs_to_check.txt') as file:
            accs_to_check = set(line for line in file.readlines() if line_not_empty(line))
            accs_to_check = (tuple(line.strip().split(':')) for line in accs_to_check)

        with open(f'{get_project_root()}/user_data/good_accs.txt') as file:
            good_accs = set(line for line in file.readlines() if line_not_empty(line))
            good_accs = {tuple(acc.strip().split(':')): 1 for acc in good_accs}

        for acc in accs_to_check:
            if good_accs.get(acc):
                continue
            self.accs_q.put_nowait(acc)

    @staticmethod
    def increase_limits():
        if sys.platform == 'win32':
            import win32file

            # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            win32file._setmaxstdio(8192)

        if sys.platform == 'linux':
            import resource

            before, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
            try:
                resource.setrlimit(resource.RLIMIT_NOFILE, (1048576, hard))
            except ValueError:
                Env.log.debug(f'Already at max limit - {before}')


ENV: Env = Env()
if __name__ == "__main__":
    pass
