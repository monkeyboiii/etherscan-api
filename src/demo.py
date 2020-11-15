import json
import time
import random
import logging
import asyncio
import requests


FIN = 'D:\\SUSTech\\3-1\\blockchain\\data\\etherscan\\export-verified-contractaddress-opensource-license.csv'
FOUT = 'D:\\SUSTech\\3-1\\blockchain\\out\\demo\\{}.json'
LOGOUT = 'D:\\SUSTech\\3-1\\blockchain\\out\\log\\demo.log'
API = 'https://api.etherscan.io/api?module=contract&action=getsourcecode&address={}&apikey={}'
TOKEN = ['CJ941NT1GNPF4VP4MUZNWG17X3ZXGWUKI9',
         '5PCZ72DR4WS1CF5IA2UERNP6252G9916H4',
         '86MHMDAV5VZIQH9M38Q6SJHFGGBUMVVT2M']


class Job:
    def __init__(self, fin, fout, api, token, logout):
        self.fin = fin
        self.fout = fout
        self.api = api
        self.token = list(token)
        self.limit = 5  # per ip
        logging.basicConfig(
            filename=logout,
            filemode='w',
            level=logging.DEBUG
        )

        self.contracts = []  # (address, name)
        self.name = {}

        # works with csv version
        with open(self.fin, 'r') as f:
            for row in f:
                line = f.readline().split(',')
                line[2] = line[2].rstrip('\n')
                if line[2] in self.name:
                    self.name[line[2]] += 1
                    line[2] += '-{}'.format(str(self.name[line[2]]))
                else:
                    self.name[line[2]] = 1
                self.contracts.append((line[1], line[2]))

    async def _task(self, offset):
        cur = offset - 1
        while cur < len(self.contracts):
            address = self.contracts[cur][0]
            name = self.contracts[cur][1]
            token = self.token[random.randint(0, 2)]
            fout = self.fout.format(self.contracts[cur][1])

            api = self.api.format(address, token)
            future = self.loop.run_in_executor(None, requests.get, api)
            response = await future

            msg = 'cur/off = {}/{}; text length = {}'.format(
                cur, offset, len(response.text))
            # print(response.text)
            print(msg)
            logging.info(msg)

            with open(fout, 'w') as fp:
                try:
                    data = json.loads(response.text)
                    json.dump(data, fp)
                except Exception:
                    logging.error('ERROR! in dump\n' + msg)

            await asyncio.sleep(1)
            cur += self.limit
        # exit while

        print('_task({}) finished'.format(offset))

    def begin(self):
        self.loop = asyncio.get_event_loop()
        try:
            for i in range(self.limit):
                self.loop.create_task(self._task(i + 1))
            self.loop.run_forever()

        except KeyboardInterrupt:
            print('Crtl + C, exit, ', end='')

        finally:
            print('loop closed')
            self.loop.close()


if __name__ == "__main__":
    job = Job(FIN, FOUT, API, TOKEN, LOGOUT)
    job.begin()
