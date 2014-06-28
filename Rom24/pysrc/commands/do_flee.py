import random
import logging
import handler_room

logger = logging.getLogger()


import handler_ch
import state_checks
import merc
import interp
import fight
import update
import handler_game


def do_flee( ch, argument ):
    victim = ch.fighting
    if not victim:
        if ch.position == merc.POS_FIGHTING:
            ch.position = merc.POS_STANDING
        ch.send("You aren't fighting anyone.\n")
        return

    was_in = ch.in_room
    for attempt in range(6):
        door = handler_room.number_door()
        pexit = was_in.exit[door]
        if not pexit \
                or not pexit.to_room \
                or state_checks.IS_SET(pexit.exit_info, merc.EX_CLOSED) \
                or random.randint(0, ch.daze) != 0 \
                or (state_checks.IS_NPC(ch)
                    and state_checks.IS_SET(pexit.u1.to_room.room_flags, merc.ROOM_NO_MOB)):
            continue

        handler_ch.move_char(ch, door, False)
        now_in = ch.in_room
        if now_in == was_in:
            continue
        ch.in_room = was_in
        handler_game.act("$n has fled!", ch, None, None, merc.TO_ROOM)
        ch.in_room = now_in
        if not state_checks.IS_NPC(ch):
            ch.send("You flee from combat!\n")
            if ch.guild.name == 'thief' and (random.randint(1, 99) < 3 * (ch.level // 2) ):
                ch.send("You snuck away safely.\n")
            else:
                ch.send("You lost 10 exp.\n")
                update.gain_exp(ch, -10)

        fight.stop_fighting(ch, True)
        return
    ch.send("PANIC! You couldn't escape!\n")
    return


interp.register_command(interp.cmd_type('flee', do_flee, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 1))
