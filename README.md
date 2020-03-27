# 360机试题

## 需求描述
观察github的feeds流，编写用户获取其关注用户的最新更新动态API

## 数据库表设计

- gh_action表记录用户的更新行为

| 字段名 | 字段含义 |
| -- | -- |
| action_type | 1-star 2-create 3-fork 4-follow |
| object_type | 1-project 2-repository 3-user |
| object_id | 相应行为的对象id |
| user_id | 用户id |

- gh_follow表记录用户相互关注关系
  
| 字段名 | 字段含义 |
| -- | -- |
| user_id | 被关注者id |
| follower_id | 粉丝id |

- gh_user, gh_project, gh_repository分别记录相应的用户、项目、仓库的具体信息

## API接口实现
主要使用python的flask框架实现

