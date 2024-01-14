import redis
import json
from flask import current_app


def get_repos() -> list:
    conn = redis.StrictRedis(
        host=current_app.config["REDIS_HOST"],
        port=int(current_app.config["REDIS_PORT"])
    )

    repos = []
    for key in conn.scan_iter("miniwebsite:*"):
        repos.append(json.loads(conn.get(key)))

    return repos
