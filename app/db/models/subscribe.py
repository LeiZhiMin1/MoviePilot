import time
from typing import Optional

from sqlalchemy import Column, Integer, String, Sequence, Float, JSON
from sqlalchemy.orm import Session

from app.db import db_query, db_update, Base


class Subscribe(Base):
    """
    订阅表
    """
    id = Column(Integer, Sequence('id'), primary_key=True, index=True)
    # 标题
    name = Column(String, nullable=False, index=True)
    # 年份
    year = Column(String)
    # 类型
    type = Column(String)
    # 搜索关键字
    keyword = Column(String)
    tmdbid = Column(Integer, index=True)
    imdbid = Column(String)
    tvdbid = Column(Integer)
    doubanid = Column(String, index=True)
    bangumiid = Column(Integer, index=True)
    mediaid = Column(String, index=True)
    # 季号
    season = Column(Integer)
    # 海报
    poster = Column(String)
    # 背景图
    backdrop = Column(String)
    # 评分，float
    vote = Column(Float)
    # 简介
    description = Column(String)
    # 过滤规则
    filter = Column(String)
    # 包含
    include = Column(String)
    # 排除
    exclude = Column(String)
    # 质量
    quality = Column(String)
    # 分辨率
    resolution = Column(String)
    # 特效
    effect = Column(String)
    # 总集数
    total_episode = Column(Integer)
    # 开始集数
    start_episode = Column(Integer)
    # 缺失集数
    lack_episode = Column(Integer)
    # 附加信息
    note = Column(JSON)
    # 状态：N-新建 R-订阅中 P-待定 S-暂停
    state = Column(String, nullable=False, index=True, default='N')
    # 最后更新时间
    last_update = Column(String)
    # 创建时间
    date = Column(String)
    # 订阅用户
    username = Column(String)
    # 订阅站点
    sites = Column(JSON, default=list)
    # 下载器
    downloader = Column(String)
    # 是否洗版
    best_version = Column(Integer, default=0)
    # 当前优先级
    current_priority = Column(Integer)
    # 保存路径
    save_path = Column(String)
    # 是否使用 imdbid 搜索
    search_imdbid = Column(Integer, default=0)
    # 是否手动修改过总集数 0否 1是
    manual_total_episode = Column(Integer, default=0)
    # 自定义识别词
    custom_words = Column(String)
    # 自定义媒体类别
    media_category = Column(String)
    # 过滤规则组
    filter_groups = Column(JSON, default=list)
    # 选择的剧集组
    episode_group = Column(String)

    @staticmethod
    @db_query
    def exists(db: Session, tmdbid: Optional[int] = None, doubanid: Optional[str] = None, season: Optional[int] = None):
        if tmdbid:
            if season:
                return db.query(Subscribe).filter(Subscribe.tmdbid == tmdbid,
                                                  Subscribe.season == season).first()
            return db.query(Subscribe).filter(Subscribe.tmdbid == tmdbid).first()
        elif doubanid:
            return db.query(Subscribe).filter(Subscribe.doubanid == doubanid).first()
        return None

    @staticmethod
    @db_query
    def get_by_state(db: Session, state: str):
        # 如果 state 为空或 None，返回所有订阅
        if not state:
            return db.query(Subscribe).all()
        else:
            # 如果传入的状态不为空，拆分成多个状态
            return db.query(Subscribe).filter(Subscribe.state.in_(state.split(','))).all()

    @staticmethod
    @db_query
    def get_by_title(db: Session, title: str, season: Optional[int] = None):
        if season:
            return db.query(Subscribe).filter(Subscribe.name == title,
                                              Subscribe.season == season).first()
        return db.query(Subscribe).filter(Subscribe.name == title).first()

    @staticmethod
    @db_query
    def get_by_tmdbid(db: Session, tmdbid: int, season: Optional[int] = None):
        if season:
            return db.query(Subscribe).filter(Subscribe.tmdbid == tmdbid,
                                              Subscribe.season == season).all()
        else:
            return db.query(Subscribe).filter(Subscribe.tmdbid == tmdbid).all()

    @staticmethod
    @db_query
    def get_by_doubanid(db: Session, doubanid: str):
        return db.query(Subscribe).filter(Subscribe.doubanid == doubanid).first()

    @staticmethod
    @db_query
    def get_by_bangumiid(db: Session, bangumiid: int):
        return db.query(Subscribe).filter(Subscribe.bangumiid == bangumiid).first()

    @staticmethod
    @db_query
    def get_by_mediaid(db: Session, mediaid: str):
        return db.query(Subscribe).filter(Subscribe.mediaid == mediaid).first()

    @db_update
    def delete_by_tmdbid(self, db: Session, tmdbid: int, season: int):
        subscrbies = self.get_by_tmdbid(db, tmdbid, season)
        for subscrbie in subscrbies:
            subscrbie.delete(db, subscrbie.id)
        return True

    @db_update
    def delete_by_doubanid(self, db: Session, doubanid: str):
        subscribe = self.get_by_doubanid(db, doubanid)
        if subscribe:
            subscribe.delete(db, subscribe.id)
        return True

    @db_update
    def delete_by_mediaid(self, db: Session, mediaid: str):
        subscribe = self.get_by_mediaid(db, mediaid)
        if subscribe:
            subscribe.delete(db, subscribe.id)
        return True

    @staticmethod
    @db_query
    def list_by_username(db: Session, username: str, state: Optional[str] = None, mtype: Optional[str] = None):
        if mtype:
            if state:
                return db.query(Subscribe).filter(Subscribe.state == state,
                                                  Subscribe.username == username,
                                                  Subscribe.type == mtype).all()
            else:
                return db.query(Subscribe).filter(Subscribe.username == username,
                                                  Subscribe.type == mtype).all()
        else:
            if state:
                return db.query(Subscribe).filter(Subscribe.state == state,
                                                  Subscribe.username == username).all()
            else:
                return db.query(Subscribe).filter(Subscribe.username == username).all()

    @staticmethod
    @db_query
    def list_by_type(db: Session, mtype: str, days: int):
        return db.query(Subscribe) \
            .filter(Subscribe.type == mtype,
                    Subscribe.date >= time.strftime("%Y-%m-%d %H:%M:%S",
                                                    time.localtime(time.time() - 86400 * int(days)))
                    ).all()
