#coding=utf-8

import json

from app import app
from flask import g, request


def get_user_info(user_ids):
    sql = """select id, name, pic_url, ropo_num, follower_num from gh_user where id in (%s)""" % ','.join(str(user_id) for user_id in user_ids)
    rows = g.db.execute(sql).fetchall()
    user_info_dict = {}
    for r in rows:
        user_id, name, pic_url, repo_num, follower_num = r
        user_info_dict[str(user_id)] = {
            "name": name,
            "pic_url": pic_url,
            "repo_num": repo_num,
            "follower_num": follower_num
        }
    return user_info_dict

def get_proj_info(proj_ids):
    sql = """select id, name, description from gh_project where id in (%s)""" % ','.join(str(proj_id) for proj_id in proj_ids)
    rows = g.db.execute(sql).fetchall()
    proj_info_dict = {}
    for r in rows:
        proj_id, name, description = r
        proj_info_dict[str(proj_id)] = {
            "name": name,
            "description": description,
        }
    return proj_info_dict

def get_repo_info(repo_ids):
    sql = """select id, name, description, language, star_num from gh_repository where id in (%s)""" % ','.join(str(repo_id) for repo_id in repo_ids)
    rows = g.db.execute(sql).fetchall()
    repo_info_dict = {}
    for r in rows:
        repo_id, name, description, language, star_num = r
        repo_info_dict[str(repo_id)] = {
            "name": name,
            "description": description,
            "language": language,
            "star_num": star_num
        }
    return repo_info_dict

@app.route("/feeds/<int:user_id>", methods=["GET"])
def get_feeds(user_id):
    # get offset and limit parameters.
    cursor = int(request.args.get("after"))
    limit = request.args.get("limit") or 10

    sql_args = {"limit": limit, "user_id": user_id}

    # get following latest actions.
    sql = """select b.id, b.user_id, b.action_type, b.object_id, b.object_type, b.create_time from 
            (select user_id from gh_follow where follower_id = :user_id and is_deleted = 0) a 
            join gh_action b on a.user_id = b.user_id"""

    if cursor:
        sql = sql + " where b.id < :curosr and b.is_deleted = 0"
        sql_args["cursor"] = cursor
    else:
        sql = sql + " where b.is_deleted = 0"

    sql = sql + " order by b.create_time desc limit :limit"

    rows = g.db.execute(sql, sql_args).fetchall()
    data = []
    user_ids = [user_id]
    repo_ids = []
    proj_ids = []
    for r in rows:
        action_id, user_id, action_type, object_id, object_type, create_time = r
        user_ids.append(user_id)
        if object_type == 1:
            proj_ids.append(object_id)
        elif object_type == 2:
            repo_ids.append(object_id)
        elif object_type == 3:
            user_ids.append(user_id)
        d = {
            "id": action_id,
            "action_type": action_type,
            "create_time": create_time,
            "object_type": object_type,
            "user_id": user_id,
            "user_info": {},
            "object_id": object_id,
            "object_info": {}
        }
        data.append(d)

    # get user_info.
    user_info_dict = get_user_info(user_ids)

    # get proj_info.
    proj_info_dict = get_proj_info(proj_ids)

    # get repo_info.
    repo_info_dict = get_repo_info(repo_ids)

    for d in data:
        d["user_info"] = user_info_dict[str(d["user_id"])]
        object_type = d["object_type"]
        if object_type == 1:
            object_info = proj_info_dict[str(d["object_id"])]
        elif object_type == 2:
            object_info = repo_info_dict[str(d["object_id"])]
        elif object_type == 3:
            object_info = user_info_dict[str(d["object_id"])]
        else:
            object_info = {}
        d["object_info"] = object_info

    ret = {"error_code": 0, "msg": "success", "data": data}
    return json.dumps(ret)
