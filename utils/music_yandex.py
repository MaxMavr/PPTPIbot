import json
import logging
import random
import string
from dataclasses import dataclass

import aiohttp
from yandex_music import ClientAsync

from config import load_config
from db.files.admin_song import read_admin_song, upd_admin_song

logger = logging.getLogger(__name__)

_config = load_config()


@dataclass
class Ynison:
    song_title: str
    artists_title: str
    song_id: str
    player_type: str
    repeat_mode: str
    progress_s: int
    duration_s: int
    paused: bool
    is_offline: bool
    timestamp_s: int
    volume: float
    cover_url: str


__client = ClientAsync(_config.yandex_music.token)


def __create_request_payload(web_socket_proto: dict) -> dict:
    return {
        'update_full_state': {
            'player_state': {
                'player_queue': {
                    'current_playable_index': -1,
                    'entity_id': '',
                    'entity_type': 'VARIOUS',
                    'playable_list': [],
                    'options': {'repeat_mode': 'NONE'},
                    'entity_context': 'BASED_ON_ENTITY_BY_DEFAULT',
                    'version': {
                        'device_id': web_socket_proto['Ynison-Device-Id'],
                        'version': 9021243204784341000,
                        'timestamp_ms': 0,
                    },
                    'from_optional': '',
                },
                'status': {
                    'duration_ms': 0,
                    'paused': True,
                    'playback_speed': 1,
                    'progress_ms': 0,
                    'version': {
                        'device_id': web_socket_proto['Ynison-Device-Id'],
                        'version': 8321822175199937000,
                        'timestamp_ms': 0,
                    },
                },
            },
            'device': {
                'capabilities': {
                    'can_be_player': True,
                    'can_be_remote_controller': False,
                    'volume_granularity': 16,
                },
                'info': {
                    'device_id': web_socket_proto['Ynison-Device-Id'],
                    'type': 'WEB',
                    'title': 'Chrome Browser',
                    'app_name': 'Chrome',
                },
                'volume_info': {'volume': 0},
                'is_shadow': True,
            },
            'is_currently_active': False,
        },
        'rid': 'ac281c26-a047-4419-ad00-e4fbfda1cba3',
        'player_action_timestamp_ms': 0,
        'activity_interception_type': 'DO_NOT_INTERCEPT_BY_DEFAULT',
    }


def __create_request_headers(web_socket_proto: dict) -> dict:
    return {
        'Sec-WebSocket-Protocol': f'Bearer, v2, {json.dumps(web_socket_proto)}',
        'Origin': 'http://music.yandex.ru',
        'Authorization': f'OAuth {_config.yandex_music.token}',
    }


async def __get_pre_ynison(session):
    web_socket_proto = {
        'Ynison-Device-Id': ''.join([random.choice(string.ascii_lowercase) for _ in range(16)]),
        'Ynison-Device-Info': json.dumps(_config.yandex_music.ynison_device_info),
    }

    async with session.ws_connect(
        url=_config.yandex_music.ynison_gry_main_url,
        headers=__create_request_headers(web_socket_proto),
    ) as ws:
        recv = await ws.receive()
        data = json.loads(recv.data)

        new_web_socket_proto = web_socket_proto.copy()
        new_web_socket_proto['Ynison-Redirect-Ticket'] = data['redirect_ticket']

        return __create_request_payload(web_socket_proto), data['host'], new_web_socket_proto


async def __fetch_ynison(session):
    request_payload, host, proto = await __get_pre_ynison(session)
    async with session.ws_connect(
        url=_config.yandex_music.ynison_pys_main_url.replace('%%', str(host)),
        headers=__create_request_headers(proto),
        method='GET',
    ) as ws:
        await ws.send_str(json.dumps(request_payload))
        recv = await ws.receive()
        return json.loads(recv.data)


async def __song_from_ynison() -> tuple[str, str, str] | None:
    try:
        async with aiohttp.ClientSession() as session:
            ynison = await __fetch_ynison(session)
            queue = ynison['player_state']['player_queue']
            track = queue['playable_list'][queue['current_playable_index']]
            song = (await __client.tracks(track['playable_id']))[0]
            artists_title = ', '.join(artist.name for artist in song.artists)
            return song.title, artists_title, str(song.id)
    except Exception as e:
        logger.error(f'Failed to fetch song from Ynison: {e!s}')
        return None


async def __song_from_ynison_expanded() -> 'Ynison | None':
    try:
        async with aiohttp.ClientSession() as session:
            ynison = await __fetch_ynison(session)

            player_state = ynison['player_state']
            device = ynison['devices'][0]
            timestamp_ms = ynison['timestamp_ms']
            del ynison

            volume = device['volume']
            is_offline = device['is_offline']
            del device

            status = player_state['status']
            player_queue = player_state['player_queue']
            del player_state

            progress_ms = int(status['progress_ms'])
            duration_ms = int(status['duration_ms'])
            paused = status['paused']
            del status

            current_playable_index = player_queue['current_playable_index']
            playable_list = player_queue['playable_list']
            player_type = player_queue['entity_type']
            repeat_mode = player_queue['options']['repeat_mode']
            del player_queue

            current_song = playable_list[current_playable_index]
            current_song_title = current_song['title']
            current_song_cover_url = current_song['cover_url_optional'].replace('%%', '1000x1000')
            song_id = current_song['playable_id']
            del current_song

            song = (await __client.tracks(song_id))[0]
            artists_title = ', '.join(artist.name for artist in song.artists)

            return Ynison(
                song_title=current_song_title,
                artists_title=artists_title,
                song_id=str(song_id),
                player_type=player_type,
                repeat_mode=repeat_mode,
                progress_s=int(progress_ms) // 1000,
                duration_s=int(duration_ms) // 1000,
                paused=paused == 'True',
                is_offline=is_offline == 'True',
                timestamp_s=int(timestamp_ms) // 1000,
                volume=volume,
                cover_url=current_song_cover_url,
            )
    except Exception as e:
        logger.error(f'Failed to fetch expanded song from Ynison: {e!s}')
        return None


async def __get_song_lyrics(song_id) -> str | None:
    song = (await __client.tracks(song_id))[0]
    if song.lyrics_info.has_available_text_lyrics:
        lyrics = await song.get_lyrics_async()
        return await lyrics.fetch_lyrics_async()
    return None


async def get_admin_song_expanded() -> 'tuple[str, str, str] | Ynison':
    song = await __song_from_ynison_expanded()

    if song:
        return song

    return await get_admin_song()


async def get_admin_song() -> tuple[str, str, str]:
    song = await __song_from_ynison()

    if song:
        upd_admin_song(song)
        return song

    return read_admin_song()


async def get_random_song_lines(song_id: str) -> str | None:
    lyrics = await __get_song_lyrics(song_id)
    if not lyrics:
        return None

    lines = [line.strip() for line in lyrics.split('\n') if line != '']

    start_idx = random.randint(0, len(lines) - 1)
    max_length = min(4, len(lines) - start_idx)
    num_lines = random.randint(1, max_length)

    return '\n'.join(lines[start_idx : start_idx + num_lines])


async def get_song_artist_title_by_song_id(song_id: str) -> tuple[str, str]:
    song = (await __client.tracks(song_id))[0]
    return song.title, ', '.join([artist.name for artist in song.artists])
