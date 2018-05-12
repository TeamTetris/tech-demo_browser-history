from enum import Enum
import platform


class OperatingSystem(Enum):
    Windows = "Windows"
    Linux = "Linux"
    Mac = "Darwin"
    Not_Supported = ""

    @classmethod
    def detect(cls):
        os_name = platform.system()

        for name, member in OperatingSystem.__members__.items():
            if name == OperatingSystem.Not_Supported.name:
                continue

            if member.value == os_name:
                return member

        return OperatingSystem.Not_Supported
