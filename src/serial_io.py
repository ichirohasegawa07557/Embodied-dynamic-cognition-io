from dataclasses import dataclass
import time

@dataclass
class HardwareReading:
    step: int
    distance_cm: float
    raw_line: str

class SerialHardwareInterface:
    '''
    Serial protocol.

    Python sends:
        A,<servo_angle>,<led_intensity>

    Arduino returns:
        S,<distance_cm>
    '''

    def __init__(self, port: str, baud_rate: int = 115200, timeout: float = 2.0):
        import serial
        self.serial = serial.Serial(port, baud_rate, timeout=timeout)
        time.sleep(2.0)
        self.step = 0

    def send_action(self, servo_angle: int, led_intensity: int):
        msg = f"A,{int(servo_angle)},{int(led_intensity)}\n"
        self.serial.write(msg.encode("utf-8"))

    def read_sensor(self) -> HardwareReading:
        line = self.serial.readline().decode("utf-8", errors="ignore").strip()
        self.step += 1
        if not line:
            raise RuntimeError("No serial response received.")
        parts = line.split(",")
        if len(parts) < 2 or parts[0] != "S":
            raise ValueError(f"Invalid serial line: {line}")
        return HardwareReading(self.step, float(parts[1]), line)

    def close(self):
        self.serial.close()
