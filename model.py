# coding=utf-8
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase('proxy.db')
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Proxy(BaseModel):
    PROTOCOL_HTTP = 'http'
    PROTOCOL_SOCKS5 = 'socks5'
    # 透明代理
    TYPE_TRANSPARENT = 'transparent'
    # 匿名代理
    TYPE_ANONYMOUS = 'anonymous'
    # 高匿代理
    TYPE_ELITE = 'elite'
    ip = CharField()
    port = IntegerField()
    protocol = CharField()
    type = CharField()
    # 最后验证时间
    check_time = DateTimeField()

    class Meta:
        indexes = (
            (('ip', 'port'), True),
        )


def create():
    db.create_tables([Proxy])
