"""
from https://qiita.com/61503891/items/4ae3ae64b2531b516321
keylogger.py
"""
import Quartz


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
