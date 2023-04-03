import argparse
import logging
import time

from ttpnotifier.ttpnotifier import MessagesObserver, NotificationsObserver, TTPNotifier, ConsoleObserver

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--location_id', type=int, required=True)
parser.add_argument('-c', '--current_appointment', type=str, required=True)
parser.add_argument('-i', '--poll_interval', default=5 * 60, type=int)
parser.add_argument('-p', '--phone_number', action='append', default=[], dest='phone_numbers', type=str)
args = parser.parse_args()

notifier = TTPNotifier(location_id=args.location_id, current_appointment=args.current_appointment,
                       poll_interval=args.poll_interval)

messages_observer = MessagesObserver(phone_numbers=args.phone_numbers)
notifications_observer = NotificationsObserver()
console_observer = ConsoleObserver()

notifier.subscribe(messages_observer)
notifier.subscribe(notifications_observer)
notifier.subscribe(console_observer)

while True:
    time.sleep(1)
