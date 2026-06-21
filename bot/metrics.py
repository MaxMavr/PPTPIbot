import logging
import os

from prometheus_client import Counter, Gauge

from db.repositories.users import UsersRepository

logger = logging.getLogger(__name__)

BOT_NAME = os.getenv('BOT_NAME', 'pptpibot')

POSTS = Counter(
    'bot_posts_total',
    'Post suggestion lifecycle events',
    ['bot', 'action'],  # suggested | published | rejected | cancelled
)

SONG_REQUESTS = Counter(
    'bot_song_requests_total',
    'Now-playing song requests by users',
    ['bot', 'kind'],  # admin_song | mood_song | mrr
)

SONG_LINES_FORMATTED = Counter(
    'bot_song_lines_formatted_total',
    'Song lines formatted for users',
    ['bot', 'source'],  # private | inline
)

INLINE_QUERIES = Counter(
    'bot_inline_queries_total',
    'Inline queries handled',
    ['bot'],
)

USERS_REGISTERED = Counter(
    'bot_users_registered_total',
    'New users seen for the first time',
    ['bot'],
)

ADMIN_SONG_UPDATED = Counter(
    'bot_admin_song_updated_total',
    'Admin/mood song updated by an admin',
    ['bot', 'kind'],  # admin | mood
)

USERS_TOTAL = Gauge(
    'bot_users_total',
    'Total known users',
    ['bot'],
)

ADMINS_TOTAL = Gauge(
    'bot_admins_total',
    'Total admins',
    ['bot'],
)


def record_post(action: str) -> None:
    POSTS.labels(bot=BOT_NAME, action=action).inc()


def record_song_request(kind: str) -> None:
    SONG_REQUESTS.labels(bot=BOT_NAME, kind=kind).inc()


def record_song_line(source: str) -> None:
    SONG_LINES_FORMATTED.labels(bot=BOT_NAME, source=source).inc()


def record_inline_query() -> None:
    INLINE_QUERIES.labels(bot=BOT_NAME).inc()


def record_user_registered() -> None:
    USERS_REGISTERED.labels(bot=BOT_NAME).inc()


def record_admin_song_updated(kind: str) -> None:
    ADMIN_SONG_UPDATED.labels(bot=BOT_NAME, kind=kind).inc()


def refresh_business_gauges(users_repo: UsersRepository) -> None:
    try:
        _, pagination = users_repo.get_all_users(1, 1)
        USERS_TOTAL.labels(bot=BOT_NAME).set(pagination.total_items)
        ADMINS_TOTAL.labels(bot=BOT_NAME).set(len(users_repo.get_admins()))
    except Exception:
        logger.exception('Failed to refresh business gauges')
