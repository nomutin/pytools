# -*- coding: utf-8 -*-
import rumps
import time


class MenuTimer(rumps.App):
    def __init__(self):
        super(MenuTimer, self).__init__(name=' ', title=None, icon='glasses.png')
        self.quit_button = rumps.MenuItem('Quit', key='q')
        self.menu = ['StopWatch', ('Timer', ('1min', '3min', '5min', '10min'))]
        self.stopwatch_active, self.timer_active = False, False
        self.timer_base_time = 0

    @rumps.clicked('StopWatch')
    def stopwatch_on_off(self, sender):
        if self.stopwatch_active:
            self.icon, self.title = 'glasses.png', None
            sender.title = 'StopWatch'
            self.stopwatch_active = False
        else:
            self.icon = None
            sender.title = 'Stop'
            self.stopwatch_active = True

    def stopwatch(self):
        pass



    @rumps.clicked('Timer', '1min')
    @rumps.clicked('Timer', '3min')
    @rumps.clicked('Timer', '5min')
    @rumps.clicked('Timer', '10min')
    def a(self):
        pass


if __name__ == "__main__":
    mtimer = MenuTimer()
    MenuTimer().run()

# todo 自由時間の時の処理(tkinter??)
# todo タイマーとストップウォッチがかぶったときの処理をどうにかする
# todo タイマーがゼロになった時の処理を考える
# todo 押した瞬間からタイマースタートするようにしたい

# todo アイコン作る
