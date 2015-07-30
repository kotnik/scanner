
from yapsy.IPlugin import IPlugin

from scanner.ssltest import is_vulnerable


class Heartbleed(IPlugin):
    def description(self):
        return "Heartbleed"

    def check(self, url, host_info):
        host_info[self.description()] = None
        if host_info["ssl checked"].get():
            return None
        else:
            vulnerable = is_vulnerable(url)
            host_info[self.description()] = vulnerable
            return vulnerable
