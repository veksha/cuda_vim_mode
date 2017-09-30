from cudatext import *
import cudatext_cmd as cc
import cudatext_keys as ck
from .word_proc import *

def msg(s):
    msg_status('[Vim] '+s)


class Command:
    active = False
    ins = False
    replace = False
    replace_char = False


    def toggle_active(self):
        self.ins = False
        self.active = not self.active
        if self.active:
            msg('plugin activated')
        else:
            msg('plugin deactivated')


    def on_key(self, ed_self, key, state):
        if not self.active: return

        if key==ck.VK_ESCAPE:
            if self.ins:
                self.ins = False
                msg('command mode')
                return False
            else:
                return

        if key in [ck.VK_LEFT, ck.VK_RIGHT, ck.VK_UP, ck.VK_DOWN,
                    ck.VK_PAGEUP, ck.VK_PAGEDOWN]:
            msg('arrow key')
            return

        if self.ins:
            msg('insertion mode')
            return

        if state in ['', 's']:
            if self.replace_char:
                return

            if key==ord('H') and state=='':
                ed.cmd(cc.cCommand_KeyLeft)
                msg('left')
                return False

            if key==ord('J') and state=='':
                ed.cmd(cc.cCommand_KeyDown)
                msg('down')
                return False

            if key==ord('K') and state=='':
                ed.cmd(cc.cCommand_KeyUp)
                msg('up')
                return False

            if key==ord('L') and state=='':
                ed.cmd(cc.cCommand_KeyRight)
                msg('right')
                return False

            if key==ord('B') and state=='':
                ed.cmd(cc.cCommand_GotoWordPrev)
                msg('go to prev word')
                return False

            if key==ord('W') and state=='':
                ed.cmd(cc.cCommand_GotoWordNext)
                msg('go to next word')
                return False

            if key==ord('E') and state=='':
                goto_word_end()
                msg('go to word end')
                return False

            if key==ord('A') and state=='':
                ed.cmd(cc.cCommand_KeyRight)
                self.ins = True
                msg('insertion mode, after current char')
                return False

            if key==ord('I') and state=='':
                self.ins = True
                msg('insertion mode, at current char')
                return False

            if key==ord('X') and state=='':
                ed.cmd(cc.cCommand_KeyDelete)
                msg('delete char')
                return False

            if key==ord('X') and state=='s':
                ed.cmd(cc.cCommand_KeyBackspace)
                msg('delete char left')
                return False

            if key==ord('R') and state=='':
                self.replace_char = True
                msg('replace char to')
                return False


    def on_key_up(self, ed_self, key, state):
        if not self.active: return


    def on_insert(self, ed_self, text):
        if not self.active:
            return

        if not self.replace_char:
            msg('key not handled')
            return False

        if self.replace_char:
            self.replace_char = False

            x0, y0, x1, y1 = ed.get_carets()[0]
            ed.replace(x0, y0, x0+len(text), y0, text)

            msg('replace char to: '+text)
            return False
