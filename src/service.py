class Service():
    def __init__(self):
        pass

    def process(self):
        pass

    def process_audio(self, items):
        if self.AudioClass.is_valid(items):
            audio_item = self.AudioClass(items)
            self.meta_manager.update(audio_item)
            audio_item.process()
