import aiohttp
from yandex_music import ClientAsync
from typing import Optional, Tuple
import json
import random
import string
from config import config

from DB.files.admin_song import read_admin_song, upd_admin_song

__client = ClientAsync(config.yandex_music.token)


def __create_request_payload(web_socket_proto: dict) -> dict:
    return {
        "update_full_state": {
            "player_state": {
                "player_queue": {
                    "current_playable_index": -1,
                    "entity_id": "",
                    "entity_type": "VARIOUS",
                    "playable_list": [],
                    "options": {"repeat_mode": "NONE"},
                    "entity_context": "BASED_ON_ENTITY_BY_DEFAULT",
                    "version": {
                        "device_id": web_socket_proto["Ynison-Device-Id"],
                        "version": 9021243204784341000,
                        "timestamp_ms": 0
                    },
                    "from_optional": ""
                },
                "status": {
                    "duration_ms": 0,
                    "paused": True,
                    "playback_speed": 1,
                    "progress_ms": 0,
                    "version": {
                        "device_id": web_socket_proto["Ynison-Device-Id"],
                        "version": 8321822175199937000,
                        "timestamp_ms": 0
                    }
                }
            },
            "device": {
                "capabilities": {
                    "can_be_player": True,
                    "can_be_remote_controller": False,
                    "volume_granularity": 16
                },
                "info": {
                    "device_id": web_socket_proto["Ynison-Device-Id"],
                    "type": "WEB",
                    "title": "Chrome Browser",
                    "app_name": "Chrome"
                },
                "volume_info": {"volume": 0},
                "is_shadow": True
            },
            "is_currently_active": False
        },
        "rid": "ac281c26-a047-4419-ad00-e4fbfda1cba3",
        "player_action_timestamp_ms": 0,
        "activity_interception_type": "DO_NOT_INTERCEPT_BY_DEFAULT"}


def __create_request_headers(web_socket_proto: dict) -> dict:
    return {
        "Sec-WebSocket-Protocol": f"Bearer, v2, {json.dumps(web_socket_proto)}",
        "Origin": "http://music.yandex.ru",
        "Authorization": f"OAuth {config.yandex_music.token}",
    }


async def __get_pre_ynison(session):
    web_socket_proto = {
        "Ynison-Device-Id": "".join([random.choice(string.ascii_lowercase) for _ in range(16)]),
        "Ynison-Device-Info": json.dumps(config.yandex_music.ynison_device_info)
    }

    async with session.ws_connect(url=config.yandex_music.ynison_gry_main_url,
                                  headers=__create_request_headers(web_socket_proto)) as ws:

        recv = await ws.receive()
        data = json.loads(recv.data)

        new_web_socket_proto = web_socket_proto.copy()
        new_web_socket_proto["Ynison-Redirect-Ticket"] = data["redirect_ticket"]

        return __create_request_payload(web_socket_proto), data['host'], new_web_socket_proto


async def __fetch_ynison(session):
    request_payload, host, proto = await __get_pre_ynison(session)
    async with session.ws_connect(
            url=config.yandex_music.ynison_pys_main_url.replace('%%', str(host)),
            headers=__create_request_headers(proto),
            method="GET"
    ) as ws:

        await ws.send_str(json.dumps(request_payload))
        recv = await ws.receive()
        return json.loads(recv.data)


async def __song_from_ynison() -> Optional[Tuple[str, str, str]]:
    try:
        async with aiohttp.ClientSession() as session:
            ynison = await __fetch_ynison(session)
            track = ynison['player_state']['player_queue']['playable_list'][ynison['player_state']['player_queue']['current_playable_index']]
            song = (await __client.tracks(track['playable_id']))[0]
            artists_title = ', '.join(artist.name for artist in song.artists)
            return song.title, artists_title, str(song.id)
    except Exception as e:
        print(e)
        return


async def __get_song_lyrics(song_id) -> Optional[str]:
    song = (await __client.tracks(song_id))[0]
    if song.lyrics_info.has_available_text_lyrics:
        lyrics = await song.get_lyrics_async()
        return await lyrics.fetch_lyrics_async()
    else:
        return


# async def download_song(artist_title: str, album_id: str, song_id: str, x_factor) -> str:
#     song = (await __client.tracks(song_id))[0]
#     save_path = TEMP_DIR + f'/{artist_title}-{album_id}-{song_id}-{x_factor}.mp3'
#     await song.download_async(save_path)
#     return save_path


async def get_admin_song() -> Tuple[str, str, str]:
    song = await __song_from_ynison()

    if song:
        upd_admin_song(song)
        return song

    return read_admin_song()


async def get_random_song_lines(song_id: str) -> Optional[str]:
    lyrics = await __get_song_lyrics(song_id)
    if not lyrics:
        return

    lines = [l.strip() for l in lyrics.split('\n') if l != '']

    start_idx = random.randint(0, len(lines) - 1)
    max_length = min(4, len(lines) - start_idx)
    num_lines = random.randint(1, max_length)

    return '\n'.join(lines[start_idx:start_idx + num_lines])


async def get_song_artist_title_by_song_id(song_id: str) -> Tuple[str, str]:
    song = (await __client.tracks(song_id))[0]
    return song.title, ', '.join([artist.name for artist in song.artists])
