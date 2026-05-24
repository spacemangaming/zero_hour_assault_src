from timer import timer
from random import randint as random
from network import network
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
dontlose=["MosinNagant","maverick88","KelTecP318"]
rebootputtime=0
rebootreason=""
timeditemlist=["MosinNagant","maverick88","KelTecP318"]
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
invlimits = {
    'revival_nectar': 20,
    'vitality_potion': 40,
    'small_potion': 60,
    'hand_grenade': 20,
    'molotov_cocktail': 50,
    'snowflake_shard': 50,
    'timebomb': 20,
    'tm62': 30,
    'metal_shield': 15,
    'steel_helmet': 2,
    'invisibility_shield': 2,
    'ladder': 4,
    'barricade': 2,
    '7.62x51mm': 500,
    '5.56x45mm': 1500,
    '9mm': 500,
    '45_ACP': 700,
    '12_gauge': 400,
    '40S&W': 800,
    '22_LR_Long_Rifle': 600,
    'm4_ammo_cartrigges': 20,
    'colt1911_ammo_cartrigges': 20,
    'fnhfnp40_ammo_cartrigges': 20,
    'silencer': 2
}
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
last_random_player_chosen=""
playertimer=timer()
weaponlaslslaltimer=timer()

chestlolololtimer=timer()
bikes=[]
molotofs=[]
ttchecktimer=timer()
mailbans=[]