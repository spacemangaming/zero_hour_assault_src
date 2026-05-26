from file_directories import file_exists
import globals as g
from variable_management import string_contains, string_split
from timer import timer
from file_directories import file_delete

class community:
    def __init__(self, name, owner):
        self.members = []
        self.name = name
        self.actions = ""
        self.owner = owner
        self.admins = []
        self.join_requests = []
        self.announcement = ""
    def send(self, mess, channel):
        for m in self.members:
            ind = g.get_player_index_from(m)
            if ind > -1:
                g.n.send_reliable(g.players[ind].peer_id, mess, channel)

def create_community(name, owner):
    gp = community(name, owner)
    gp.members.append(owner)
    g.communitys.append(gp)

def rename_community(old, new):
    g.get_community(old).name = new
