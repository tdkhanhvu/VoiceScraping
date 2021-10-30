from service import ServiceScraper, ServiceSoundDetector

if __name__ == "__main__":
    services = [ServiceScraper, ServiceSoundDetector]

    for service in services:
        s = service()
        s.process()