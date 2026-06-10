import data_loader

# guns: all weapons that consume ammo, sorted alphabetically
guns = data_loader.get_guns_list()

# guns2: all weapons sorted by npc_priority (lower = NPCs prefer it more)
guns2 = data_loader.get_guns2_list()
