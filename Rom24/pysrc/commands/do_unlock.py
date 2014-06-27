import handler_ch
import handler_game
import handler_room
import interp
import game_utils
import state_checks
import merc


def do_unlock(ch, argument):
    argument, arg = game_utils.read_word(argument)

    if not arg:
        ch.send("Unlock what?\n")
        return
    obj = ch.get_obj_here(arg)
    if obj:
        # portal stuff */
        if obj.item_type == merc.ITEM_PORTAL:
            if not state_checks.IS_SET(obj.value[1], merc.EX_ISDOOR):
                ch.send("You can't do that.\n")
                return
            if not state_checks.IS_SET(obj.value[1], merc.EX_CLOSED):
                ch.send("It's not closed.\n")
                return
            if obj.value[4] < 0:
                ch.send("It can't be unlocked.\n")
                return
            if not handler_ch.has_key(ch, obj.value[4]):
                ch.send("You lack the key.\n")
                return
            if not state_checks.IS_SET(obj.value[1], merc.EX_LOCKED):
                ch.send("It's already unlocked.\n")
                return
            state_checks.REMOVE_BIT(obj.value[1], merc.EX_LOCKED)
            handler_game.act("You unlock $p.", ch, obj, None, merc.TO_CHAR)
            handler_game.act("$n unlocks $p.", ch, obj, None, merc.TO_ROOM)
            return
            # 'unlock object' */
        if obj.item_type != merc.ITEM_CONTAINER:
            ch.send("That's not a container.\n")
            return
        if not state_checks.IS_SET(obj.value[1], merc.CONT_CLOSED):
            ch.send("It's not closed.\n")
            return
        if obj.value[2] < 0:
            ch.send("It can't be unlocked.\n")
            return
        if not handler_ch.has_key(ch, obj.value[2]):
            ch.send("You lack the key.\n")
            return
        if not state_checks.IS_SET(obj.value[1], merc.CONT_LOCKED):
            ch.send("It's already unlocked.\n")
            return

        state_checks.REMOVE_BIT(obj.value[1], merc.CONT_LOCKED)
        handler_game.act("You unlock $p.", ch, obj, None, merc.TO_CHAR)
        handler_game.act("$n unlocks $p.", ch, obj, None, merc.TO_ROOM)
        return

    door = handler_room.find_door(ch, arg)
    if door >= 0:
        # 'unlock door'
        pexit = ch.in_room.exit[door]
        if not state_checks.IS_SET(pexit.exit_info, merc.EX_CLOSED):
            ch.send("It's not closed.\n")
            return
        if pexit.key < 0:
            ch.send("It can't be unlocked.\n")
            return
        if not handler_ch.has_key(ch, pexit.key):
            ch.send("You lack the key.\n")
            return
        if not state_checks.IS_SET(pexit.exit_info, merc.EX_LOCKED):
            ch.send("It's already unlocked.\n")
            return
        state_checks.REMOVE_BIT(pexit.exit_info, merc.EX_LOCKED)
        ch.send("*Click*\n")
        handler_game.act("$n unlocks the $d.", ch, None, pexit.keyword, merc.TO_ROOM)

        # unlock the other side */
        to_room = pexit.to_room
        if to_room and to_room.exit[merc.rev_dir[door]] != 0 \
                and to_room.exit[merc.rev_dir[door]].to_room == ch.in_room:
            state_checks.REMOVE_BIT(to_room.exit[merc.rev_dir[door]].exit_info, merc.EX_LOCKED)


interp.cmd_type('unlock', do_unlock, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)
