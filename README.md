# ttp-notifier
Simple library that notifies of appointments for the Trusted Traveler Program

## Getting Started

### Prerequisites
This library was tested against Python 3.7+.

### Installation

Clone the repo:
```shell
git clone https://github.com/thesilvad/ttp-notifier
```

Install the dependencies:
```shell
cd ttp-notifier
pip install -r requirements.txt
```

If you'd like to use it as a python module, you can install it with the following:
```shell
pip install .
```

Find your `location_id` from one of the following:

- [Global Entry](https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName=Global%20Entry)
- [NEXUS](https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName=NEXUS)
- [SENTRI](https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName=SENTRI)
- [US/Mexico FAST](https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName=U.S.%20%2F%20Mexico%20FAST)
- [US/Canada FAST](https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName=U.S.%20%2F%20Canada%20FAST)

## Usage
There is an example `main.py` script that contains three example notifications. Two of which only work on macOS. The `main.py` script can be modified to not include the macOS notifications.

You can run the script with the following:
```shell
python main.py --location_id 5002 \
               --current_appointment "May 20, 2024" \
               --poll_interval 10 \
               --phone_number 1-555-555-1234
```


### ConsoleObserver
The `ConsoleObserver` class will simply log the appointments to the console log.

### NotificationsObserver
The `NotificationsObserver` class will only work on macOS. It depends `osascript` to create display notifications. 

### MessagesObserver
The `MessagesObserver` class will only work on macOS. It depends on `osascript` to send an iMessage to a phone number.

### Writing a Custom Observer
If instead you'd like to write your own custom observers, simply subclass the `Observer` and implement its `update` method. Here is a very simple example of how to log the available appointments to the console:

```python
import logging
import time

from ttpnotifier.ttpnotifier import Observer, TTPNotifier


class ConsoleObserver(Observer):
    def update(self, available_appointments):
        logging.info(f'Found {len(available_appointments)} appointment(s): {", ".join(available_appointments)}')


console_observer = ConsoleObserver()
notifier = TTPNotifier(
    location_id=5002,
    current_appointment='January 19, 2038',
    num_appointments=10,
    poll_interval=60)
notifier.subscribe(console_observer)

while True:
    time.sleep(1)
```