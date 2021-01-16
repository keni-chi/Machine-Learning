from ipywidgets import interact, Select


class MyError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'エラーメッセージ'



class InnerClass:
    def run(self, dfa):
        print('run')
        df_select =dfa

        # dfから先頭末尾の年を取得し、list化
        # year_list = ['2002', '2004', '2006']
        year_list = [str(n) for n in list(range(2002,2006+1))]

        y1 = year_list
        y2 = year_list

        @interact(y1=Select(options=y1, rows=1, value=year_list[0]), m1=Select(options=['04', '10'], rows=1), 
                  y2=Select(options=y2, rows=1, value=year_list[-1]), m2=Select(options=['03', '09'], rows=1))
        def function(y1, m1, y2, m2):
            print('function')
            

            start = y1 + '-' + m1 + '-01'
            if m2 == '03':
                end = y2 + '-' + m2 + '-31'
            elif m2 == '09':
                end = y2 + '-' + m2 + '-30'
            else:
                pass

            print(start)
            print(end)

            df_show = df_select[start:end]

            if len(df_show)==0:
                print('エラーメッセージ')
                raise MyError()

            print(df_show)
            df_show.plot()
            df_show.plot()


def run(dfa):
    instance = InnerClass()
    instance.run(dfa)
