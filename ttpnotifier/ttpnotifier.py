import logging
import subprocess
import time
from abc import ABC, abstractmethod
from datetime import datetime
from threading import Thread
from typing import List

import requests

API_URL = 'https://ttp.cbp.dhs.gov/schedulerapi'


class TTPNotifier:
    def __init__(self, location_id: int, current_appointment: str, num_appointments=10, poll_interval=60) -> None:
        self.location_id = location_id
        self.current_appointment = datetime.strptime(current_appointment, '%B %d, %Y')
        self.num_appointments = num_appointments
        self.poll_interval = poll_interval

        self._observers = set()
        self._available_appointments = []

        self.ttp_notifier_thread = Thread(target=self.poll, daemon=True)
        self.ttp_notifier_thread.start()
        logging.info('TTPNotifier initialized!')

    def get_soonest_appointments(self, limit=10):
        available_appointments = []
        try:
            data = requests.get(
                f"{API_URL}/slots?orderBy=soonest&limit={limit}&locationId={self.location_id}&minimum=1").json()
            for d in data:
                if d['active']:
                    if self.current_appointment > datetime.strptime(d['startTimestamp'], '%Y-%m-%dT%H:%M'):
                        available_appointments.append(d['startTimestamp'])
        except Exception as e:
            logging.error('Something went wrong retrieving appointments...')
            logging.exception(e)

        return available_appointments

    def subscribe(self, observer):
        self._observers.add(observer)

    def unsubscribe(self, observer):
        self._observers.remove(observer)

    def _notify(self):
        if len(self.available_appointments) > 0:
            for observer in self._observers:
                observer.update(self.available_appointments)
        else:
            logging.info(f'No appointments found... Trying again in {self.poll_interval} seconds.')

    @property
    def available_appointments(self):
        return self._available_appointments

    @available_appointments.setter
    def available_appointments(self, arg):
        self._available_appointments = arg
        self._notify()

    def poll(self):
        while self.ttp_notifier_thread.is_alive():
            self.available_appointments = self.get_soonest_appointments(limit=self.num_appointments)
            time.sleep(self.poll_interval)


class Observer(ABC):
    @abstractmethod
    def update(self, available_appointments):
        pass


class ConsoleObserver(Observer):
    def update(self, available_appointments):
        logging.info(f'Found {len(available_appointments)} appointment(s): {", ".join(available_appointments)}')


class NotificationsObserver(Observer):
    def update(self, available_appointments):
        title = f'{len(available_appointments)} appointment(s) available'
        message = '\n'.join(available_appointments)
        subprocess.call(['osascript', '-e',
                         f'display notification "{message}" with title "{title}"'])


class MessagesObserver(Observer):
    def __init__(self, phone_numbers: List[str]):
        self.phone_numbers = phone_numbers

    def update(self, available_appointments):
        title = f'{len(available_appointments)} appointment(s) available'
        message = '\n'.join(available_appointments)
        for phone_number in self.phone_numbers:
            subprocess.call(['osascript', '-e',
                             f'tell application "Messages" to send "{title}:\n{message}" to buddy "{phone_number}"'])
