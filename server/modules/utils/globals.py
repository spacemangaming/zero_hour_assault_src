from timer import timer
from random import randint as random
from network import network
import data_loader
players=[]
bodyfalls=[]
weapons=[]
maps=[]
n=network()
wdata={}
npcs=[]
rebooting=False
gamestop=0
reboottimer=timer()
items=[]
itemspawntimer=timer()
reboot2=False
reboot2timer=timer()
compbans={}
ipbans={}
comphandles=[]
teams=[]
lolsavetimer=timer()
matches=[]
flags=[]
zombies=[]
loots=[]
msounds=[]
tickets=[]
dontlose=["MosinNagant","maverick88","KelTecP318","weapon_spawner"]
rebootputtime=0
rebootreason=""
timeditemlist=["MosinNagant","maverick88","KelTecP318","weapon_spawner"]
timeditems=[]
motors=[]
pathfinding=False
chests=[]
corpses=[]
groups=[]
communitys=[]

grenades=[]
molotofs=[]

servertime=timer()
group_bases=[]
timebombs=[]
zks=[]

mwalls=[]
mines=[]
invlimits = data_loader.get_inventory_limits()
barricades=[]
ladders=[]
rain=False
rainstarttimer=timer()
rainstarttime=random(2000000, 4000000)
raintime=random(200000, 300000)
nomudtiles=["clay","debris","deepsand","dirt","dirt2","dirt3","dirt4","dirt5","dirt6","dirt7","dirt8","dirt9","grass","grass2","grass3","grass4","gravel","gravel2","gravel3","gravel4","gravel5","gravel6","sand","wetdirt"]
rainvoltimer=timer()
rainvoltime=random(15000, 30000)
rainvolume=-20
raintimer=timer()
electrics=[]
timed_electrics=[]
rainfinish=False
rainfinishtimer=timer()
freedomsurvivor=""
task=-1
mega_boss=None
mega_boss_alive=False
last_random_player_chosen=""
playertimer=timer()
weaponlaslslaltimer=timer()

chestlolololtimer=timer()
bikes=[]
molotofs=[]
ttchecktimer=timer()
mailbans=[]
transits=[]
waypoints=[]