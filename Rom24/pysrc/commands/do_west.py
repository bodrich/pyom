import handler_ch
import interp
import merc


def do_west(ch, argument):
    handler_ch.move_char(ch, merc.DIR_WEST, False)
    return


interp.cmd_type('west', do_west, merc.POS_STANDING, 0, merc.LOG_NEVER, 0)
