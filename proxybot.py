from aiotg import Bot
import aiohttp
from aiosocksy.connector import ProxyConnector, ProxyClientRequest

try:
    import certifi
    import ssl
except ImportError:
    certifi = None


class ProxyBot(Bot):
    @property
    def session(self):
        if not self._session or self._session.closed:
            if certifi:
                context = ssl.create_default_context(cafile=certifi.where())
                connector = ProxyConnector(remote_resolve=True)
            else:
                connector = None

            self._session = aiohttp.ClientSession(
                connector=connector,
                request_class=ProxyClientRequest,
                json_serialize=self.json_serialize
            )
        return self._session

    async def loop(self, db_connection):
        self._db_conn = db_connection
        await super().loop()
