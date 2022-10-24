from speechkit import Session, SpeechSynthesis
from data import config


class YandexVoiceGen:
    def __init__(self):
        self.oauth_token = config.yandex_token
        self.catalog_id = config.yandex_folder_id

    def gen_voice(self, text):
        session = Session.from_yandex_passport_oauth_token(self.oauth_token, self.catalog_id)
        synthesizeAudio = SpeechSynthesis(session)
        synthesizeAudio.synthesize(
            'voice/temp/out.ogg', text=text,
            voice='filipp', format='oggopus', sampleRateHertz='48000', speed='0.7'
        )
