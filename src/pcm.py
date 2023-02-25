import os

from bell.avr.mqtt.module import MQTTModule
from bell.avr.mqtt.payloads import (
    AVRPCMColorSet,
    AVRPCMColorTimed,
    AVRPCMServo,
    AVRPCMServoAbsolute,
    AVRPCMServoPercent,
    AVRPCMServoPWM,
)
from bell.avr.serial.client import SerialLoop
from bell.avr.serial.pcc import PeripheralControlComputer
from bell.avr.utils.env import get_env_int

PCM_SERIAL_DEVICE = os.getenv("PCM_DEVICE", "/dev/ttyACM0")
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
            "avr/pcm/color/set": self.color_set,
            "avr/pcm/color/timed": self.color_timed,
            "avr/pcm/laser/fire": self.laser_fire,
            "avr/pcm/laser/on": self.laser_on,
            "avr/pcm/laser/off": self.laser_off,
            "avr/pcm/servo/open": self.servo_open,
            "avr/pcm/servo/close": self.servo_close,
            "avr/pcm/servo/pwm/min": self.servo_pwm_min,
            "avr/pcm/servo/pwm/max": self.servo_pwm_max,
            "avr/pcm/servo/percent": self.servo_percent,
            "avr/pcm/servo/absolute": self.servo_absolute,
        }

    def run(self) -> None:
        super().run_non_blocking()
        self.serial.run()

    def color_set(self, payload: AVRPCMColorSet) -> None:
        self.pcc.set_base_color(wrgb=payload.wrgb)

    def color_timed(self, payload: AVRPCMColorTimed) -> None:
        self.pcc.set_temp_color(wrgb=payload.wrgb, time=payload.time)

    def laser_fire(self) -> None:
        self.pcc.fire_laser()

    def laser_on(self) -> None:
        self.pcc.set_laser_on()

    def laser_off(self) -> None:
        self.pcc.set_laser_off()

    def servo_open(self, payload: AVRPCMServo) -> None:
        self.pcc.set_servo_open_close(payload.servo, "open")

    def servo_close(self, payload: AVRPCMServo) -> None:
        self.pcc.set_servo_open_close(payload.servo, "close")

    def servo_pwm_min(self, payload: AVRPCMServoPWM) -> None:
        self.pcc.set_servo_min(payload.servo, payload.pulse)

    def servo_pwm_max(self, payload: AVRPCMServoPWM) -> None:
        self.pcc.set_servo_max(payload.servo, payload.pulse)

    def servo_percent(self, payload: AVRPCMServoPercent) -> None:
        self.pcc.set_servo_pct(payload.servo, payload.percent)

    def servo_absolute(self, payload: AVRPCMServoAbsolute) -> None:
        self.pcc.set_servo_abs(payload.servo, payload.position)


if __name__ == "__main__":
    pcm = PeripheralControlModule(PCM_SERIAL_DEVICE, PCM_SERIAL_BAUD_RATE)
    pcm.run()
