from service import ServiceScraper, ServiceSoundDetector

if __name__ == "__main__":
    scraper = ServiceScraper()
    scraper.process()

    sound_detector = ServiceSoundDetector()
    sound_detector.process()