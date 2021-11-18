"""
sensible base module.

This is the principal module of the sensible project.
here you put your main classes and objects.
"""


# Device:
# - One flexible core protocol.
#   - Can extablish details about communication to other devices.

# - The device simply accumulates information of the world by collecting  sensor data from other devices.
# - Other devices can share the sensor data that they have collected from other devices aswell.

# Core functionality:
# - Discover other devices.
# - Establish communication protocol with them.
#   - The resulting communication protocol is set by the user depending on requirements.
#   - The resulting communciation protocol is also dependent on the other device.
# - Recieve, send, and store sensor data.
# - The stored sensor data can be queried and inspected.

class BaseClass:
    def base_method(self) -> str:
        """
        Base method.
        """
        return "hello from BaseClass"

    def __call__(self) -> str:
        return self.base_method()

def base_function() -> str:
    """
    Base function.
    """
    return "hello from base function"
