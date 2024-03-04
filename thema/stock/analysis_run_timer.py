import os
import pandas as pd
import time
import datetime
import schedule

import analysis_run


class Timer():

    def __init__(self):
        self.ar = analysis_run

    def schedule_run(self):
        # 15時
        schedule.every().day.at('15:20').do(analysis_run.run)

        # # debug
        # for mm in range(0,60):
        #     t = '00:' + str(mm).zfill(2)
        #     # print(t)
        #     schedule.every().day.at(t).do(analysis_run.run)


def main():
    # スケジュール
    Timer().schedule_run()

    # スケジュール実行
    while True:
        schedule.run_pending()
        time.sleep(1)  # 待ち


if __name__ == '__main__':
    main()

