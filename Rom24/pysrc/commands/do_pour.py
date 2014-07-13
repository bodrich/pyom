import logging


logger = logging.getLogger()

import merc
import const
import interp
import game_utils


def do_pour(ch, argument):
    argument, arg = game_utils.read_word(argument)

    if not arg or not argument:
        ch.send("Pour what into what?\n")
        return
    out = ch.get_item_carry(arg, ch)
    if not out:
        ch.send("You don't have that item.\n")
        return
    if out.item_type != merc.ITEM_DRINK_CON:
        ch.send("That's not a drink container.\n")
        return
    if argument == "out":
        if out.value[1] == 0:
            ch.send("It's already empty.\n")
            return
        out.value[1] = 0
        out.value[3] = 0
        act("You invert $p, spilling %s all over the ground." % const.liq_table[out.value[2]].liq_name, ch, out,
                 None, merc.TO_CHAR)
        act("$n inverts $p, spilling %s all over the ground." % const.liq_table[out.value[2]].liq_name, ch, out,
                 None, merc.TO_ROOM)
        return
    into = ch.get_item_here(argument)
    vch = None
    if not into:
        vch = ch.get_char_room(argument)

        if vch is None:
            ch.send("Pour into what?\n")
            return
        into = vch.get_eq(merc.WEAR_HOLD)
        if not into:
            ch.send("They aren't holding anything.")

    if into.item_type != merc.ITEM_DRINK_CON:
        ch.send("You can only pour into other drink containers.\n")
        return
    if into == out:
        ch.send("You cannot change the laws of physics!\n")
        return
    if into.value[1] != 0 and into.value[2] != out.value[2]:
        ch.send("They don't hold the same liquid.\n")
        return
    if out.value[1] == 0:
        act("There's nothing in $p to pour.", ch, out, None, merc.TO_CHAR)
        return
    if into.value[1] >= into.value[0]:
        act("$p is already filled to the top.", ch, into, None, merc.TO_CHAR)
        return
    amount = min(out.value[1], into.value[0] - into.value[1])

    into.value[1] += amount
    out.value[1] -= amount
    into.value[2] = out.value[2]

    if not vch:
        act("You pour %s from $p into $P." % const.liq_table[out.value[2]].liq_name, ch, out, into,
                         merc.TO_CHAR)
        act("$n pours %s from $p into $P." % const.liq_table[out.value[2]].liq_name, ch, out, into,
                         merc.TO_ROOM)
    else:
        act("You pour some %s for $N." % const.liq_table[out.value[2]].liq_name, ch, None, vch,
                         merc.TO_CHAR)
        act("$n pours you some %s." % const.liq_table[out.value[2]].liq_name, ch, None, vch, merc.TO_VICT)
        act("$n pours some %s for $N." % const.liq_table[out.value[2]].liq_name, ch, None, vch,
                         merc.TO_NOTVICT)


interp.register_command(interp.cmd_type('pour', do_pour, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
