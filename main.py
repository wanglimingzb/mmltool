# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

import ui
from functools import partial
import pandas as pd
import datetime
import copy

now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

tt = -6
# '没有查到相应的结果' in a or '命令无效或资源未就绪' in a or 'RETCODE = 855703635  系统正处于安全退出状态' in a or '网元响应超时' in a:


def convert(ui1):
    in_text = ui1.lineEdit.text()
    result = float(in_text) * 6.7
    ui1.lineEdit_2.setText(str(result))


def get_file(u):
    t = QFileDialog.getOpenFileNames()
    if len(t[0]) < 1:
        u.textBrowser.append('未选择文件')
    else:
        u.textBrowser.append('已选择：')
        for i in t[0]:
            u.textBrowser.append(i)


def run(u):
    t = u.textBrowser.toPlainText()
    t = t.split('已选择：\n')[1]
    for tt in t.split('\n'):
        jiexi(tt)
    u.textBrowser.append('Done')


def jiexi(t):
    with open(t) as f:
        writer = pd.ExcelWriter('MML任务结果_%s_%s.xlsx' % (t.split('/')[-1], now))
        f = f.read().split('\n===========================\n\n')
        zy = f[0].split('\n')
        zy.pop(1)
        data = pd.DataFrame(zy)
        data.columns = ['解析摘要']
        data.to_excel(writer, index=False, sheet_name='解析摘要')
        ff = f[1].split('\n\n======================================\n\n')
        f2 = ff[0]
        r = []
        d = dict()
        for f3 in f2.replace('==========失败命令==========\n', '').replace('\n\n\n---    END', '').split('\n\n'):
            l1 = f3.replace('-----', ' : ').split('\n')
            for i in l1:
                ii = i.split(' : ')
                d[ii[0]] = ii[1]
            r.append(d.copy())
            d.copy()
        data2 = pd.DataFrame(r)
        data2.to_excel(writer, index=False, sheet_name='失败命令')
        # writer.close()
        l2 = []
        for i in ff[1].replace('==========成功命令==========\n', '').split('\n\n\n---    END\n\n\n\n'):
            com = i.split('------------\n')
            cc = com[0].split('\n')
            c = cc[0]
            rl = []
            enbname = cc[1].replace('网元 : ', '')
            print(c, enbname)
            if c not in l2:
                l2.append(l2)
                sheet = c.replace('命令-----', '')[:-2]
            if '结果个数 = 1)' in c and '个报告' not in c:
                a = com[1].split('\n(')
                if len(a) < 2:
                    pass
                else:
                    b = a[0]
                    dd = dict()
                    for nn in b.split('\n'):
                        bb = nn.strip().split('  =  ')
                        if len(bb) < 2:
                            bb = bb[0].replace('=  ', '').split(':')
                        dd['基站名称'] = enbname
                        dd['命令结果'] = '执行成功'
                        dd[bb[0]] = bb[1]
                    rl.append(dd)
                print(rl)



if __name__ == '__main__':
    jiexi('tt2.txt')
    # app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    # mml_ui = ui.Ui_Dialog()
    # mml_ui.setupUi(MainWindow)
    # MainWindow.show()
    # mml_ui.pushButton.clicked.connect(partial(get_file, mml_ui))
    # mml_ui.pushButton_2.clicked.connect(partial(jeixi, mml_ui))
    # sys.exit(app.exec_())
