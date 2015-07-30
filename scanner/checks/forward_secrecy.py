
from yapsy.IPlugin import IPlugin

from scanner.util import check_call


class ForwardSecrecy(IPlugin):
    def description(self):
        return "Forward Secrecy"

    def check(self, url, host_info):
        host_info[self.description()] = None
        if host_info["ssl checked"].get():
            return None
        else:
            output = check_call([
                "openssl", "s_client", "-connect", "{}:443".format(url),
                "-cipher", "EDH,EECDH",
            ])
            if "alert handshake failure" in output:
                host_info[self.description()] = False
                return False

            host_info[self.description()] = True
            return True
