import os

from pathlib import Path


def _get_trader_dir(temp_name: str):
    """
    Get path where trader is running in.
    """
    cwd = Path.cwd()
    temp_path = cwd.joinpath(temp_name)
    if temp_path.exists():
        return cwd, temp_path
    # Otherwise use home path of system.
    home_path = Path.home()

    temp_path = home_path.joinpath(temp_name)
    if not temp_path.exists():
        temp_path.mkdir()
    return home_path, temp_path


def get_folder_path(folder_name: str):
    """
    Get path for temp folder with folder name.
    """
    TRADER_DIR, TEMP_DIR = _get_trader_dir(".ctpbee")
    folder_path = TEMP_DIR.joinpath(folder_name)
    if not folder_path.exists():
        os.makedirs(folder_path)
    return folder_path


class LoginRequired:
    def __init__(self):
        self.connect_required = False
        self.login_required = False
        self.position_required = False
        self.account_required = False
        self.contract_required = False
        self.init_local = False

    @property
    def ready(self):
        return (
            self.connect_required
            and self.login_required
            and self.position_required
            and self.account_required
            and self.contract_required
        )

    def connect(self):
        raise NotImplemented
