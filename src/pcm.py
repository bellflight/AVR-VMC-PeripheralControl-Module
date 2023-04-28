import os

from bell.avr.mqtt.module import MQTTModule
from bell.avr.serial.client import SerialLoop
from bell.avr.serial.pcc import PeripheralControlComputer
from bell.avr.utils.env import get_env_int

PCM_SERIAL_DEVICE = os.getenv("PCM_SERIAL_DEVICE", "/dev/ttyACM0")
PCM_SERIAL_BAUD_RATE = get_env_int("PCM_SERIAL_BAUD_RATE", 115200)


class PeripheralControlModule(MQTTModule):
    def __init__(self, port: str, baud_rate: int):
        super().__init__()

        # PCC connection
        self.serial = SerialLoop()
        self.serial.port = port
        self.serial.baudrate = baud_rate
        self.serial.open()

        self.pcc = PeripheralControlComputer(self.serial)

        # MQTT topics
        self.topic_callbacks = {
            "avr/pcm/color/set": lambda payload: self.pcc.set_base_color(
                wrgb=payload.wrgb
            ),
            "avr/pcm/color/timed": lambda payload: self.pcc.set_temp_color(
                wrgb=payload.wrgb, time=payload.time
            ),
            "avr/pcm/laser/fire": self.pcc.fire_laser,
            "avr/pcm/laser/on": self.pcc.set_laser_on,
            "avr/pcm/laser/off": self.pcc.set_laser_off,
            "avr/pcm/servo/open": lambda payload: self.pcc.set_servo_open_close(
                payload.servo, "open"
            ),
            "avr/pcm/servo/close": lambda payload: self.pcc.set_servo_open_close(
                payload.servo, "close"
            ),
            "avr/pcm/servo/pwm/min": lambda payload: self.pcc.set_servo_min(
                payload.servo, payload.pulse
            ),
            "avr/pcm/servo/pwm/max": lambda payload: self.pcc.set_servo_max(
                payload.servo, payload.pulse
            ),
            "avr/pcm/servo/percent": lambda payload: self.pcc.set_servo_pct(
                payload.servo, payload.percent
            ),
            "avr/pcm/servo/absolute": lambda payload: self.pcc.set_servo_abs(
                payload.servo, payload.position
            ),
        }

    def run(self) -> None:
        super().run_non_blocking()
        self.serial.run()


if __name__ == "__main__":
    pcm = PeripheralControlModule(PCM_SERIAL_DEVICE, PCM_SERIAL_BAUD_RATE)
    pcm.run()
