from adafruit_platformdetect import Detector


def is_on_raspberry_pi():
    """Returns true if evaluated on a Raspberry Pi, else False."""
    if Detector().get_device_model() is not None:
        return True
    else:
        return False
