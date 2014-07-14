import os
import sys
import logging

import const
import object_creator
import game_utils
import handler_game
import handler_item
import npc_handler
import world_classes
import handler_room
import merc
import settings
import state_checks
import tables


logger = logging.getLogger()

__author__ = 'venom'


def load_areas():
    logger.info('Loading Areas...')
    narea_list = os.path.join(settings.AREA_DIR, settings.AREA_LIST)
    fp = open(narea_list, 'r')
    area = fp.readline().strip()
    while area != "$":
        afp = open(os.path.join(settings.AREA_DIR, area), 'r')
        load_area(afp.read())
        area = fp.readline().strip()
        afp.close()
    fp.close()

    logger.info('Done. (loading areas)')


def load_area(area):
    if not area.strip():
        return

    area, w = game_utils.read_word(area, False)
    pArea = None
    while area:
        if w == "#AREA":
            pArea = world_classes.Area(None)
            area, pArea.file_name = game_utils.read_string(area)
            area, pArea.name = game_utils.read_string(area)
            area, pArea.credits = game_utils.read_string(area)
            area, pArea.min_vnum = game_utils.read_int(area)
            area, pArea.max_vnum = game_utils.read_int(area)
            merc.areaTemplate[pArea.name] = pArea
            area_instance = world_classes.Area(pArea)
            logger.info("    Loading %s", area_instance)

        elif w == "#HELPS":
            area = load_helps(area)
        elif w == "#MOBILES":
            area = load_mobiles(area, area_instance)
        elif w == "#OBJECTS":
            area = load_objects(area, area_instance)
        elif w == "#RESETS":
            area = load_resets(area, area_instance)
        elif w == "#ROOMS":
            area = load_rooms(area, area_instance)
        elif w == "#SHOPS":
            area = load_shops(area)
        elif w == "#SOCIALS":
            area = load_socials(area)
        elif w == "#SPECIALS":
            area = load_specials(area)
        elif w == '#$':
            break
        else:
            logger.error('Bad section name: %s', w)

        area, w = game_utils.read_word(area, False)


def load_helps(area):
    while True:
        nhelp = handler_game.HELP_DATA()
        area, nhelp.level = game_utils.read_int(area)
        area, nhelp.keyword = game_utils.read_string(area)
        merc.helps[nhelp.keyword] = nhelp

        if nhelp.keyword == '$':
            del nhelp
            break

        area, nhelp.text = game_utils.read_string(area)

        if nhelp.keyword == "GREETING":
            merc.greeting_list.append(nhelp)

        merc.help_list.append(nhelp)
    return area


def load_mobiles(area, pArea):
    area, w = game_utils.read_word(area, False)
    w = w[1:]  # strip the pound

    while w != '0':
        mob = npc_handler.Npc(None, None)
        mob.vnum = int(w)
        merc.characterTemplate[mob.vnum] = mob
        mob.area = pArea.name
        area, mob.name = game_utils.read_string(area)
        area, mob.short_descr = game_utils.read_string(area)
        area, mob.long_descr = game_utils.read_string(area)
        area, mob.description = game_utils.read_string(area)
        area, race_name = game_utils.read_string(area)
        mob.race = race_name
        area, mob.act = game_utils.read_flags(area)
        mob.act = mob.act | merc.ACT_IS_NPC | mob.race.act
        area, mob.affected_by = game_utils.read_flags(area)
        mob.affected_by = mob.affected_by | mob.race.aff
        area, mob.alignment = game_utils.read_int(area)
        area, mob.group = game_utils.read_int(area)
        area, mob.level = game_utils.read_int(area)
        area, mob.hitroll = game_utils.read_int(area)
        area, mob.hit_dice[0] = game_utils.read_int(area)
        area = game_utils.read_forward(area)
        area, mob.hit_dice[1] = game_utils.read_int(area)
        area = game_utils.read_forward(area)
        area, mob.hit_dice[2] = game_utils.read_int(area)
        area, mob.mana_dice[0] = game_utils.read_int(area)
        area = game_utils.read_forward(area)
        area, mob.mana_dice[1] = game_utils.read_int(area)
        area = game_utils.read_forward(area)
        area, mob.mana_dice[2] = game_utils.read_int(area)
        area, mob.dam_dice[0] = game_utils.read_int(area)
        area = game_utils.read_forward(area)
        area, mob.dam_dice[1] = game_utils.read_int(area)
        area = game_utils.read_forward(area)
        area, mob.dam_dice[2] = game_utils.read_int(area)
        area, mob.dam_type = game_utils.read_word(area, False)
        mob.dam_type = state_checks.name_lookup(const.attack_table, mob.dam_type)
        area, mob.armor[0] = game_utils.read_int(area)
        area, mob.armor[1] = game_utils.read_int(area)
        area, mob.armor[2] = game_utils.read_int(area)
        area, mob.armor[3] = game_utils.read_int(area)
        area, mob.off_flags = game_utils.read_flags(area)
        mob.off_flags = mob.off_flags | mob.race.off
        area, mob.imm_flags = game_utils.read_flags(area)
        mob.imm_flags = mob.imm_flags | mob.race.imm
        area, mob.res_flags = game_utils.read_flags(area)
        mob.res_flags = mob.res_flags | mob.race.res
        area, mob.vuln_flags = game_utils.read_flags(area)
        mob.vuln_flags = mob.vuln_flags | mob.race.vuln
        area, mob.start_pos = game_utils.read_word(area, False)
        area, mob.default_pos = game_utils.read_word(area, False)
        mob.start_pos = state_checks.name_lookup(tables.position_table, mob.start_pos, 'short_name')
        mob.default_pos = state_checks.name_lookup(tables.position_table, mob.default_pos, 'short_name')
        area, sex = game_utils.read_word(area, False)
        mob.sex = state_checks.value_lookup(tables.sex_table, sex)
        area, mob.wealth = game_utils.read_int(area)
        area, mob.form = game_utils.read_flags(area)
        mob.form = mob.form | mob.race.form
        area, mob.parts = game_utils.read_flags(area)
        mob.parts = mob.parts | mob.race.parts
        area, mob.size = game_utils.read_word(area, False)
        area, mob.material = game_utils.read_word(area, False)
        area, w = game_utils.read_word(area, False)
        mob.size = tables.size_table.index(mob.size)
        while w == 'F':
            area, word = game_utils.read_word(area, False)
            area, vector = game_utils.read_flags(area)
            area, w = game_utils.read_word(area, False)
        w = w[1:]  # strip the pound
    return area


def load_objects(area, pArea):
    area, w = game_utils.read_word(area, False)
    w = w[1:]  # strip the pound
    while w != '0':
        obj = handler_item.Items(None)
        obj.vnum = int(w)
        merc.itemTemplate[obj.vnum] = obj
        obj.area = pArea.name
        area, obj.name = game_utils.read_string(area)
        area, obj.short_descr = game_utils.read_string(area)

        area, obj.description = game_utils.read_string(area)
        area, obj.material = game_utils.read_string(area)
        area, obj.item_type = game_utils.read_word(area, False)
        area, obj.extra_flags = game_utils.read_flags(area)
        area, obj.wear_flags = game_utils.read_flags(area)

        if obj.item_type == merc.ITEM_WEAPON:
            area, obj.value[0] = game_utils.read_word(area, False)
            area, obj.value[1] = game_utils.read_int(area)
            area, obj.value[2] = game_utils.read_int(area)
            area, obj.value[3] = game_utils.read_word(area, False)
            obj.value[3] = state_checks.name_lookup(const.attack_table, obj.value[3])
            area, obj.value[4] = game_utils.read_flags(area)
        elif obj.item_type == merc.ITEM_CONTAINER:
            area, obj.value[0] = game_utils.read_int(area)
            area, obj.value[1] = game_utils.read_flags(area)
            area, obj.value[2] = game_utils.read_int(area)
            area, obj.value[3] = game_utils.read_int(area)
            area, obj.value[4] = game_utils.read_int(area)
        elif obj.item_type == merc.ITEM_DRINK_CON or obj.item_type == merc.ITEM_FOUNTAIN:
            area, obj.value[0] = game_utils.read_int(area)
            area, obj.value[1] = game_utils.read_int(area)
            area, obj.value[2] = game_utils.read_word(area, False)
            area, obj.value[3] = game_utils.read_int(area)
            area, obj.value[4] = game_utils.read_int(area)
        elif obj.item_type == merc.ITEM_WAND or obj.item_type == merc.ITEM_STAFF:
            area, obj.value[0] = game_utils.read_int(area)
            area, obj.value[1] = game_utils.read_int(area)
            area, obj.value[2] = game_utils.read_int(area)
            area, obj.value[3] = game_utils.read_word(area, False)
            area, obj.value[4] = game_utils.read_int(area)
        elif obj.item_type == merc.ITEM_POTION or obj.item_type == merc.ITEM_SCROLL or obj.item_type == merc.ITEM_PILL:
            area, obj.value[0] = game_utils.read_int(area)
            area, obj.value[1] = game_utils.read_word(area, False)
            area, obj.value[2] = game_utils.read_word(area, False)
            area, obj.value[3] = game_utils.read_word(area, False)
            area, obj.value[4] = game_utils.read_word(area, False)
        else:
            area, obj.value[0] = game_utils.read_flags(area)
            area, obj.value[1] = game_utils.read_flags(area)
            area, obj.value[2] = game_utils.read_flags(area)
            area, obj.value[3] = game_utils.read_flags(area)
            area, obj.value[4] = game_utils.read_flags(area)

        area, obj.level = game_utils.read_int(area)
        area, obj.weight = game_utils.read_int(area)
        area, obj.cost = game_utils.read_int(area)
        area, obj.condition = game_utils.read_word(area, False)
        if obj.condition == 'P':
            obj.condition = 100
        elif obj.condition == 'G':
            obj.condition = 90
        elif obj.condition == 'A':
            obj.condition = 75
        elif obj.condition == 'W':
            obj.condition = 50
        elif obj.condition == 'D':
            obj.condition = 25
        elif obj.condition == 'B':
            obj.condition = 10
        elif obj.condition == 'R':
            obj.condition = 0
        else:
            obj.condition = 100

        area, w = game_utils.read_word(area, False)

        while w == 'F' or w == 'A' or w == 'E':
            if w == 'F':
                area, word = game_utils.read_word(area, False)
                area, number = game_utils.read_int(area)
                area, number = game_utils.read_int(area)
                area, flags = game_utils.read_flags(area)
            elif w == 'A':
                area, number = game_utils.read_int(area)
                area, number = game_utils.read_int(area)
            elif w == 'E':
                ed = world_classes.ExtraDescrData()
                area, ed.keyword = game_utils.read_string(area)
                area, ed.description = game_utils.read_string(area)
                obj.extra_descr.append(ed)

            area, w = game_utils.read_word(area, False)
        w = w[1:]  # strip the pound
    return area


def load_resets(area, pArea):
    count = 0
    while True:
        count += 1
        area, letter = game_utils.read_letter(area)
        if letter == 'S':
            break

        if letter == '*':
            area, t = game_utils.read_to_eol(area)
            continue

        reset = world_classes.Reset(None)
        reset.command = letter
        reset.template_area = pArea.name
        reset.template_name = pArea.name + " Reset " + str(count)
        area, number = game_utils.read_int(area)  # if_flag
        area, reset.arg1 = game_utils.read_int(area)
        area, reset.arg2 = game_utils.read_int(area)
        area, reset.arg3 = (area, 0) if letter == 'G' or letter == 'R' else game_utils.read_int(area)
        area, reset.arg4 = game_utils.read_int(area) if letter == 'P' or letter == 'M' else (area, 0)
        area, t = game_utils.read_to_eol(area)
        pArea.reset_list.append(reset)
    return area


def load_rooms(area, pArea):
    area, w = game_utils.read_word(area, False)
    w = w[1:]  # strip the pound
    while w != '0':
        room = handler_room.Room(None)
        room.vnum = int(w)
        if room.vnum in merc.roomTemplate:
            logger.critical('Dupicate room Vnum: %d', room.vnum)
            sys.exit(1)
        merc.roomTemplate[room.vnum] = room
        room.area = pArea.name
        area, room.name = game_utils.read_string(area)
        area, room.description = game_utils.read_string(area)
        area, number = game_utils.read_int(area)  # area number
        area, room.room_flags = game_utils.read_flags(area)
        area, room.sector_type = game_utils.read_int(area)
        while True:
            area, letter = game_utils.read_letter(area)

            if letter == 'S':
                break
            elif letter == 'H':  # Healing Room
                area, room.heal_rate = game_utils.read_int(area)
            elif letter == 'M':  # Mana Room
                area, room.mana_rate = game_utils.read_int(area)
            elif letter == 'C':  # Clan
                area, room.clan = game_utils.read_string(area)
            elif letter == 'D':  # exit
                nexit = world_classes.Exit(None)
                area, door = game_utils.read_int(area)
                area, nexit.description = game_utils.read_string(area)
                area, nexit.keyword = game_utils.read_string(area)
                area, locks = game_utils.read_int(area)
                area, nexit.key = game_utils.read_int(area)
                area, nexit.to_room_vnum = game_utils.read_int(area)
                nexit.name = "Exit %s %d to %d" % \
                             (nexit.keyword,
                              room.vnum,
                              nexit.to_room_vnum)
                room.exit[door] = nexit
            elif letter == 'E':
                ed = world_classes.ExtraDescrData()
                area, ed.keyword = game_utils.read_string(area)
                area, ed.description = game_utils.read_string(area)
                room.extra_descr.append(ed)
            elif letter == 'O':
                area, room.owner = game_utils.read_string(area)
            else:
                logger.critical("RoomIndexData(%d) has flag other than SHMCDEO: %s", (room.vnum, letter))
                sys.exit(1)
        area, w = game_utils.read_word(area, False)
        w = w[1:]  # strip the pound
        # Create our instances
        object_creator.create_room(room)
    return area


def load_shops(area):
    while True:
        area, keeper = game_utils.read_int(area)

        if keeper == 0:
            break
        shop = world_classes.Shop(None)
        shop.keeper = keeper
        merc.shopTemplate[shop.keeper] = shop
        merc.characterTemplate[shop.keeper].pShop = merc.shopTemplate[shop.keeper]
        for r in range(merc.MAX_TRADE):
            area, shop.buy_type[r] = game_utils.read_int(area)
        area, shop.profit_buy = game_utils.read_int(area)
        area, shop.profit_sell = game_utils.read_int(area)
        area, shop.open_hour = game_utils.read_int(area)
        area, shop.close_hour = game_utils.read_int(area)
        area, t = game_utils.read_to_eol(area)
    return area


def load_socials(area):
    while True:
        area, word = game_utils.read_word(area, False)

        if word == '#0':
            return
        social = handler_game.SOCIAL_DATA()
        social.name = word
        merc.social[social.name] = social
        area, throwaway = game_utils.read_to_eol(area)
        area, line = game_utils.read_to_eol(area)
        if line == '$':
            social.char_no_arg = None
        elif line == '#':
            if social not in merc.social_list:
                merc.social_list.append(social)
            continue
        else:
            social.char_no_arg = line

        area, line = game_utils.read_to_eol(area)

        if line == '$':
            social.others_no_arg = None
        elif line == '#':
            if social not in merc.social_list:
                merc.social_list.append(social)
            continue
        else:
            social.others_no_arg = line
        area, line = game_utils.read_to_eol(area)

        if line == '$':
            social.char_found = None
        elif line == '#':
            if social not in merc.social_list:
                merc.social_list.append(social)
            continue
        else:
            social.char_found = line
        area, line = game_utils.read_to_eol(area)

        if line == '$':
            social.others_found = None
        elif line == '#':
            if social not in merc.social_list:
                merc.social_list.append(social)
            continue
        else:
            social.others_found = line
        area, line = game_utils.read_to_eol(area)

        if line == '$':
            social.vict_found = None
        elif line == '#':
            if social not in merc.social_list:
                merc.social_list.append(social)
            continue
        else:
            social.vict_found = line
        area, line = game_utils.read_to_eol(area)

        if line == '$':
            social.char_not_found = None
        elif line == '#':
            if social not in merc.social_list:
                merc.social_list.append(social)
            continue
        else:
            social.char_not_found = line
        area, line = game_utils.read_to_eol(area)

        if line == '$':
            social.char_auto = None
        elif line == '#':
            if social not in merc.social_list:
                merc.social_list.append(social)
            continue
        else:
            social.char_auto = line
        area, line = game_utils.read_to_eol(area)

        if line == '$':
            social.others_auto = None
        elif line == '#':
            if social not in merc.social_list:
                merc.social_list.append(social)
            continue
        else:
            social.others_auto = line

        if social not in merc.social_list:
            merc.social_list.append(social)
    return area


def load_specials(area):
    while True:
        area, letter = game_utils.read_letter(area)

        if letter == '*':
            area, t = game_utils.read_to_eol(area)
            continue
        elif letter == 'S':
            return area
        elif letter == 'M':
            area, vnum = game_utils.read_int(area)
            area, merc.characterTemplate[vnum].spec_fun = game_utils.read_word(area, False)
        else:
            logger.error("Load_specials: letter noth *SM: %s", letter)

    return area