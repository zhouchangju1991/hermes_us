This project fetches the near real time stock information from Hermes US website and send notifications when some products are published/unpublished.

main.py contains the logic for the whole process. main() in main.py is scheduled to be called every minute. database.py is for read / write to firestore database. crawler.py is for crawling Hermes US website. mailer.py is for sending notifications. log.py is for logging.
