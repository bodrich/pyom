import handler_room
import interp
import merc


def do_up(ch, argument):
    handler_ch.move_char(ch, merc.DIR_UP, False)
    return


interp.cmd_type('up', do_up, merc.POS_STANDING, 0, merc.LOG_NEVER, 0)
