from yaml import safe_load


class Data:
    def __init__(self, path):
        # Load tokens from config.yml
        with open(path) as f:
            cfg = safe_load(f)
        telegram_tokens = cfg['Telegram']
        yandex_tokens = cfg['Yandex']
        self.yandex_token = yandex_tokens['OAuth']
        self.yandex_folder_id = yandex_tokens['FolderId']
        self.telegram_app_hash = telegram_tokens['TelegramAppHash']
        self.telegram_app_id = telegram_tokens['TelegramAppId']

        # Load commands from commands.yml
        with open('commands.yml') as f:
            cfg = safe_load(f)
        triggers = cfg['Triggers']
        self.command_trigger = '\\' + triggers['Command']
        self.debug_trigger = '\\' + triggers['Debug']


config = Data('config.yml')
