# USB MIDI to DIN MIDI

Installation - Hardware:
 - Connect a DIN MIDI socket to the TX pin of the raspberry
 - Connect a an LED to pin 5 (or other pin, and modify `start.py`)
 - boot the raspberry

Installation - Software:
 - `cp 33-usbmidi.rules /etc/udev/rules.d/`
 - `cp usbmidi.service /etc/systemd/system`

Then, each time you plug in a USB midi device, its messages should be forwarded via the DIN jack.
Currently only supports one USB device, since I'm using a Raspi Zero W.
