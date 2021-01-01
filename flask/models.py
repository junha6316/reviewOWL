from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func, Boolean
from sqlalchemy.orm import backref, relationship

from database import Base


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True)
    name = Column(String)


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # Use default=func.now() to set the default hiring time
    # of an Employee to be the current time when an
    # Employee record was created
    hired_on = Column(DateTime, default=func.now())
    department_id = Column(Integer, ForeignKey('department.id'))
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    # Use cascade='delete,all' to propagate the deletion of a Department onto its Employees
    department = relationship(
        Department,
        backref=backref('employees',
                        uselist=True,
                        cascade='delete,all'))
    role = relationship(
        Role,
        backref=backref('roles',
                        uselist=True,
                        cascade='delete,all'))

class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True)

    youtubeId = Column(String)
    title = Column(String)
    publishedAt = Column(DateTime)
    description = Column(String)
    thumbnails = Column(String)
    viewCount = Column(String)
    commentCount = Column(Integer)
    subscriberCount = Column(Integer)
    hiddenSubscriberCount = Column(Boolean)
    videoCount = Column(Integer)


class Playlist(Base):
    __tablename__ = "playlists"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    youtubeId = Column(String)
    publishedAt = Column(DateTime)
    description = Column(String)
    thumbnails = Column(String)


class PlaylistItem(Base):
    __tablename__ = "playlistItems"
    
    id = Column(Integer, primary_key=True)
    youtubeId = Column(String)
    youtubeVideoId= Column(String)

    title= Column(String)
    publishedAt = Column(DateTime)
    description= Column(String)
    thumbnails= Column(String)
    likeCount = Column(Integer)
    dislikeCount = Column(Integer)
    favoriteCount = Column(Integer)
    commentCount = Column(Integer)



'''
{'kind': 'youtube#searchResult', 'etag': 'QmnTR4XkFLH2JdNjTSGntyL13Os', 
'id': {'kind': 'youtube#channel', 'channelId': 'UCUj6rrhMTR9pipbAWBAMvUQ'}, 'snippet': {'publishedAt': '2014-09-30T07:40:14Z', 'channelId': 'UCUj6rrhMTR9pipbAWBAMvUQ', 'title': '침착맨', 'description': '반갑습니다. 오늘도 즐거운 날입니다.', 'thumbnails': {'default': {'url': 'https://yt3.ggpht.com/ytc/AAUvwnip3m0vrondZ7foBbpk-voKKm7coZkTEqWkWmz8nw=s88-c-k-c0xffffffff-no-rj-mo'}, 'medium': {'url': 'https://yt3.ggpht.com/ytc/AAUvwnip3m0vrondZ7foBbpk-voKKm7coZkTEqWkWmz8nw=s240-c-k-c0xffffffff-no-rj-mo'}, 'high': {'url': 'https://yt3.ggpht.com/ytc/AAUvwnip3m0vrondZ7foBbpk-voKKm7coZkTEqWkWmz8nw=s800-c-k-c0xffffffff-no-rj-mo'}}, 'channelTitle': '침착맨', 'liveBroadcastContent': 'upcoming', 'publishTime': '2014-09-30T07:40:14Z'}}

'snippet': 
{'publishedAt': '2020-12-27T11:23:20Z', 
'channelId': 'UCUj6rrhMTR9pipbAWBAMvUQ', '
title': '봉구스 밥버거, 컵밥인가 버거인가?', 
'description': '오타가 많아서 수정 후 재업합니다. 불편을 드려 죄송합니다. 
봉구스 밥버거 -봉구킹: 5000원 -봉구퀸: 5000원 -칠성사이다 500ml 2개: 3400원 -배달비: 3400원 ...', 
'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/QpFD2X703-0/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/QpFD2X703-0/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/QpFD2X703-0/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': '침착맨', 'liveBroadcastContent': 'none', 'publishTime': '2020-12-27T11:23:20Z'}}
'''
