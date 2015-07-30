
from yapsy.IPlugin import IPlugin

from scanner.util import check_call


class FallbackScsv(IPlugin):
    def description(self):
        return "TLS_FALLBACK_SCSV"

    def check(self, url, host_info):
        host_info[self.description()] = None
        if host_info["ssl checked"].get():
            return None
        else:
            output = check_call([
                "openssl", "s_client", "-connect", "{}:443".format(url),
                "-fallback_scsv", "-no_tls1_2",
            ])
            if "alert inappropriate fallback" in output:
                host_info[self.description()] = True
                return True

            host_info[self.description()] = False
            return False
