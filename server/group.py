from file_directories import file_exists
import globals as g
from variable_management import string_contains, string_split
from timer import timer
from file_directories import file_delete

class group:
    def __init__(self, name, owner):
        self.members = []
        self.freedomhit=1
        self.name = name
        self.actions = ""
        self.owner = owner
        self.kills = 0
        self.deaths = 0
        self.admins = []
        self.join_requests = []
        self.donations = ""
        self.zhtoken = 0
        self.announcement = ""
    def send(self, mess, channel):
        for m in self.members:
            ind = g.get_player_index_from(m)
            if ind > -1:
                g.n.send_reliable(g.players[ind].peer_id, mess, channel)

    def add_kill(self):
        """Add a kill to the group and check if rewards should be given every 100 kills."""
        self.kills += 1

        # Check if the group's kills are a multiple of 100
        if self.kills % 100 == 0:
            self.give_rewards(2)  # Give 2 tokens for every 100 kills

    def give_rewards(self, num):
        """Give tokens to all members of the group."""
        for member in self.members:
            index = g.get_player_index_from(member)
            if index > -1:
                g.players[index].zhtoken += num  # Give specified amount of tokens (2 in this case)

def create_group(name, owner):
    gp = group(name, owner)
    gp.members.append(owner)
    g.groups.append(gp)

def rename_group(old, new):
    g.get_group(old).name = new
