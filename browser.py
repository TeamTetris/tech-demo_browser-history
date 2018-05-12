import re
from operating_system import OperatingSystem

C_URL_REGEX = re.compile("^https?\:\/\/((?P<sub_domain>([a-z0-9][a-z0-9_-]+?)+)\.)?(?P<domain>[a-z0-9][a-z0-9_-]+?)\.(?P<tld>[a-z]{2,3})(\/|$)?.+?$", re.IGNORECASE)


class Browser:

    @classmethod
    def match_url(cls, url):
        match = C_URL_REGEX.match(url)
        sub_domain = ""
        domain = ""
        tld = ""

        if not match:
            return False, sub_domain, domain, tld

        if match.group("sub_domain"):
            sub_domain = match.group("sub_domain")

        if match.group("domain"):
            domain = match.group("domain")

        if match.group("tld"):
            tld = match.group("tld")

        return True, sub_domain, domain, tld

    def __init__(self):
        my_os = OperatingSystem.detect()

        if my_os == OperatingSystem.Not_Supported:
            return

        elif my_os == OperatingSystem.Windows:
            self.__history_file__ = self.__history_file_windows__()

        elif my_os == OperatingSystem.Linux:
            self.__history_file__ = self.__history_file_linux__()

        elif my_os == OperatingSystem.Mac:
            self.__history_file__ = self.__history_file_mac__()

        else:
            raise Exception("unknown operating system: " + my_os.name)

    def is_installed(self):
        return self.__history_file__.is_file() and self.__history_file__.exists()

    def history_raw(self):
        raise NotImplementedError("abstract browser called")

    def history(self):
        history = dict()

        for row in self.history_raw():
            if len(row) < 2:
                continue

            matched, sub_domain, domain, tld = self.match_url(row[0])

            if not matched:
                print("unmatched url: " + row[0])
                continue

            if row[1] <= 0:
                continue

            if domain not in history.keys():
                history[domain] = 0

            history[domain] += row[1]

        return [(domain, history[domain]) for domain in sorted(history, key=history.get, reverse=True)]

    def __history_file_windows__(self):
        raise NotImplementedError("abstract browser called")

    def __history_file_linux__(self):
        raise NotImplementedError("abstract browser called")

    def __history_file_mac__(self):
        raise NotImplementedError("abstract browser called")
