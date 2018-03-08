# -*- coding: utf-8 -*-

import asyncio
from aiohttp import web
import aiohttp
import json
import logging
from sh import rpi_kt0803k

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(levelname)s][%(funcName)-2s]-> %(message)s',
                    datefmt='%m-%d %H:%M:%S')
aiohttp_listen_addr = '127.0.0.1'
aiohttp_listen_port = 8088
appkey = '0e6283d3-52b4-4a2b-883b-d07cc2d820b6'

kt0803k_func = {
    'channel': 77000,  # channel     | 0~204750 | kHz
    'fdev': 2,         # bandwidth   | 0~3      | 75k 112.5k 150k 187.5k
    'rfgain': 15,      # rf_gain     | 0~15
    'limitlevel': 1,   # aux_limiter | 0~3      | 0.6875 0.75 0.875 0.9625
    'mono': False,
    'pabias': True,
    'softwaregain': 0, # -15~12
    'mute': False
}

def query_status():
    ret_body = {'result':'unexcepted error', 'status': kt0803k_func}
    try:
        k = rpi_kt0803k('--query').strip().replace(' ','').split('\n')
        ret_body['status']['mute'] = True if k[0][4:]=='true' else False
        ret_body['status']['mono'] = True if k[1][4:]=='true' else False
        ret_body['status']['rfgain'] = int(k[2][6:])
        ret_body['status']['softwaregain'] = int(k[3][12:])
        ret_body['status']['pabias'] = True if k[4][6:]=='true' else False
        ret_body['status']['limitlevel'] = int(k[5][10:])
        ret_body['status']['fdev'] = int(k[6][4:])
        ret_body['status']['channel'] = int(k[7][7:])
        ret_body['result'] = 'ok'
    except Exception as e:
        logging.error(f'Unexcepted error: {e}')
    finally:
        return ret_body

def update_setting(setting_json):
    if not 'setting' in setting_json:
        return {'result':'missing parameters'}
    logging.info(setting_json['setting'])
    for k, v in setting_json['setting'].items():
        if k in kt0803k_func:
            rpi_kt0803k(f'--{k}',v)
    return query_status()

async def ktapi(request):
    ret_body = {'result':'unexcepted error'}
    try:
        r = json.loads(await request.text())
        if r.get('appkey', '') != appkey:
            ret_body['result'] = 'unavailable key'
            raise ValueError("Unauthorized access")
        if r.get('mode', '') == 'query':
            ret_body = query_status()
        elif r.get('mode', '') == 'set':
            ret_body = update_setting(r)
        else:
            ret_body['result'] = 'unsupport method'
            raise ValueError("Undefined method")
    except json.decoder.JSONDecodeError:
        logging.error('Json decode error.')
    except Exception as e:
        logging.error(f'Unexcepted error: {e}')
    finally:
        return web.Response(body=json.dumps(ret_body))

async def server_loop(mloop):
    app = web.Application(loop=mloop)
    app.router.add_route('POST', '/api', ktapi)
    srv = await mloop.create_server(app.make_handler(access_log=None), aiohttp_listen_addr, aiohttp_listen_port)
    logging.info(f'KTAPI Server started at http://{aiohttp_listen_addr}:{aiohttp_listen_port}...')
    return srv

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server_loop(loop))
    loop.run_forever()