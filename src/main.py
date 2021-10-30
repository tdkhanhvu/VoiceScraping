from service import ServiceScraper, ServiceSoundDetector, ServiceLanguageDetector

if __name__ == "__main__":
    services = [ServiceScraper, ServiceSoundDetector, ServiceLanguageDetector]

    for service in services:
        s = service()
        s.process()