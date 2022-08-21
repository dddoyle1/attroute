import bs4
from bs4 import BeautifulSoup
import requests
import time
class Router:
    def __init__(self,
        address: str,
        expiration: float = 0):
        """

        :param address: address of router
        :param expiration: last update expiration (minutes)
        """
        self.address = address
        self.expiration = expiration

        # initialize cache
        self.bbipv4 = self._get_broadband_ipv4_address()
        self.cache_last_updated = time.perf_counter()

    def get_broadband_ipv4_address(self) -> str:
        now = time.perf_counter() / 60.# seconds->minutes
        if now - self.cache_last_updated > self.expiration:
            self.bbipv4 = self._get_broadband_ipv4_address()
        return self.bbipv4
    def _get_broadband_ipv4_address(self) -> str:
        """
        Internal method for making request to router
        Parses HTML response for Broadband IPv4 table entry
        :return: broadband ipv4 address
        """
        url = f'http://{self.address}/cgi-bin/broadbandstatistics.ha'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        def search_bbipv4(tag : bs4.Tag):
            if tag.name == 'td':
                if tag.find_previous_sibling('th', string='Broadband IPv4 Address'):
                    return True
            return False
        return soup.find(search_bbipv4).string

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser('router_address')
    parser = argparse.ArgumentParser('--cache_expiration', help='(minutes)', default=0)
    args = parser.parse_args()

    router = Router(args.router_addres, args.cache_expiration)
    print(router.get_broadband_ipv4_address())

