
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType, utils

from models import Department as DepartmentModel
from models import Employee as EmployeeModel
from models import Role as RoleModel
from models import Channel as ChannelModel
from models import Playlist as PlaylistModel
from models import PlaylistItem as PlaylistItemModel

from youtube.youtube import searchChannel, searchPlaylist, searchPlaylistItems

class Channel(SQLAlchemyObjectType):
    class Meta:
        model = ChannelModel

class Playlist(SQLAlchemyObjectType):
    class Meta:
        model = PlaylistModel

class PlaylistItem(SQLAlchemyObjectType):
    class Meta:
        model = PlaylistItemModel
        

class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )


class DepartmentCon(relay.Connection):
    class Meta:
        node = Department

class Role(SQLAlchemyObjectType):
    class Meta:
        model = RoleModel
        interfaces = (relay.Node, )

class RoleCon(relay.Connection):
    class Meta:
        node = Role



class Query(graphene.ObjectType):
    node = relay.Node.Field()
    role = graphene.List(Role, role_id=graphene.Int(required=True))

    def resolve_role(self, info, **kwargs): 
        role_query = Role.get_query(info)
        result =role_query.filter(RoleModel.role_id.contains(kwargs.get('role_id')))
        return role_query.filter(RoleModel.role_id.contains(kwargs.get('role_id')))
    
    search = graphene.List(Channel, keyword=graphene.String(required=True))

    def resolve_search(self, info, **kwargs):
        keyword = kwargs.get('keyword')
        search_result = searchChannel(keyword)
        return search_result

    playlists = graphene.List(Playlist, channelId=graphene.String(required=True))
    
    def resolve_playlists(self, info, **kwargs):
        channelId = kwargs.get('channelId')
        search_result = searchPlaylist(channelId)
        return search_result

    playlistItems = graphene.List(PlaylistItem, playlistId=graphene.String(required=True))
    
    def resolve_playlistItems(self, info, **kwargs):
        playlistId = kwargs.get('playlistId')
        search_result = searchPlaylistItems(playlistId)
        return search_result




    # Allows sorting over multiple columns, by default over the primary key
    all_roles = SQLAlchemyConnectionField(RoleCon)
    # Disable sorting over this field
    all_departments = SQLAlchemyConnectionField(DepartmentCon, sort=None)


schema = graphene.Schema(query=Query, types=[Department, Role])
