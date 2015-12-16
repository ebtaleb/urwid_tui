#!/usr/bin/python

import urwid.curses_display
import urwid.raw_display
import urwid.web_display
import urwid

import sys

if urwid.web_display.is_web_request():
    Screen = urwid.web_display.Screen
else:
    if len(sys.argv)>1 and sys.argv[1][:1] == "r":
        Screen = urwid.raw_display.Screen
    else:
        Screen = urwid.curses_display.Screen

def key_test():
    screen = Screen()
    header = urwid.Text("Values from get_input(). Q exits.")
    header = urwid.AttrWrap(header,'header')
    lw = urwid.SimpleListWalker([])
    listbox = urwid.ListBox(lw)
    listbox = urwid.AttrWrap(listbox, 'listbox')
    top = urwid.Frame(listbox, header)

    def input_filter(keys, raw):
        if 'q' in keys or 'Q' in keys:
            raise urwid.ExitMainLoop

        t = []
        a = []
        for k in keys:
            if type(k) == tuple:
                out = []
                for v in k:
                    if out:
                        out += [', ']
                    out += [('key',repr(v))]
                t += ["("] + out + [")"]
            else:
                t += ["'",('key',k),"' "]

        rawt = urwid.Text(", ".join(["%d"%r for r in raw]))

        if t:
            lw.append(
                urwid.Columns([
                    ('weight',2,urwid.Text(t)),
                    rawt])
                )
            listbox.set_focus(len(lw)-1,'above')
        return keys

    loop = urwid.MainLoop(top, [
        ('header', 'black', 'dark cyan', 'standout'),
        ('key', 'yellow', 'dark blue', 'bold'),
        ('listbox', 'light gray', 'black' ),
        ], screen, input_filter=input_filter)

    try:
        old = screen.tty_signal_keys('undefined','undefined',
            'undefined','undefined','undefined')
        loop.run()
    finally:
        screen.tty_signal_keys(*old)

def main():
    urwid.web_display.set_preferences('Input Test')
    if urwid.web_display.handle_short_request():
        return
    key_test()


if '__main__'==__name__ or urwid.web_display.is_web_request():
    main()
