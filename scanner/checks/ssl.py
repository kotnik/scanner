
from gevent import ssl, socket, select
from yapsy.IPlugin import IPlugin


class SSL(IPlugin):
    def description(self):
        return "SSL missing"

    def check(self, url, host_info):
        host_info[self.description()] = None
        host_ip = socket.getaddrinfo(url, 443)[0][4][0]
        try:
            sock = socket.socket()
            sock.connect((host_ip, 443))
        except socket.error:
            host_info["ssl checked"].set(True)
            host_info[self.description()] = True
            return True

        try:
            sock = ssl.wrap_socket(sock,
                ca_certs="/etc/ssl/certs/ca-certificates.crt",
                cert_reqs=ssl.CERT_NONE,
            )
            cert = sock.getpeercert()
        except ssl.SSLError:
            host_info["ssl checked"].set(True)
            host_info[self.description()] = True
            return True

        host_info["ssl checked"].set(False)
        host_info[self.description()] = False
        return False
