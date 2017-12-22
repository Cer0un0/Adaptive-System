#! /usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from numpy.random import *
import subprocess as sub



def plot(ant_count_l, ant_count_r, C_l_level, C_r_level): # プロット
    fig, (axL, axR) = plt.subplots(ncols=2, figsize=(10,4), sharex=True)
    plt.rcParams['font.family'] = 'AppleGothic'
    l_count = [0]
    r_count = [0]
    l_level = [0]
    r_level = [0]
    x_label = []
    for i in range(0, 61):
        x_label.append(i)

    for l, r in zip(ant_count_l.values(), ant_count_r.values()):
        l_count.append(l)
        r_count.append(r)

    for l, r in zip(C_l_level.values(), C_r_level.values()):
        l_level.append(l/60)
        r_level.append(r/60)

    axL.plot(x_label, l_count, label = 'L', color = 'Red')
    axL.plot(x_label, r_count, label = 'R', color = 'Blue')
    axL.legend()
    axL.set_xlabel(u'時間(分)')
    axL.set_ylabel(u'左または右の道を通るアリの個体数(匹/分)')
    axL.grid(True)


    axR.plot(x_label, l_level, label = 'L', color = 'Red')
    axR.plot(x_label, r_level, label = 'R', color = 'Blue')
    axR.legend()
    axR.set_xlabel(u'時間(分)')
    axR.set_ylabel(u'フェロモンレベル')
    axR.grid(True)
    plt.show()


def simu(): # シュミュレーション
    C_l = 0.0
    C_r = 0.0
    C_l_level = {} # Lのフェロモンレベル 1分毎に管理
    C_r_level = {} # Rのフェロモンレベル 1分毎に管理
    ant = {0:0, 'L':0, 'R':0} # {0:アリが発生すれば1, L: Lに行けば1, R: Rに行けば1}
    ant_count_l = {} # Lにいくアリの数 1分毎に管理
    ant_count_r = {} # Rにいくアリの数 1分毎に管理

    for i in range(60):
        ant_count_l.update({i:0})
        ant_count_r.update({i:0})
        C_l_level.update({i:0})
        C_r_level.update({i:0})

    for i in range(3600): # 講義資料にあったアルゴリズムの実装
        P_l = pow(k+C_l, n)/(pow(k+C_l,n) + pow(k+C_r,n))
        P_r = 1 - P_l
        if rand() <= phi * delta_t:
            ant[0] = 1
        else:
            ant[0] = 0

        if ant[0] == 1:
            if rand() <= P_l:
                ant['L'] = 1
                ant['R'] = 0
                ant_count_l[i/60] += 1
            else:
                ant['L'] = 0
                ant['R'] = 1
                ant_count_r[i/60] += 1


            C_l = C_l + delta_t * (q * ant['L'] - alpha * C_l)
            C_r = C_r + delta_t * (q * ant['R'] - alpha * C_r)
        C_l_level[i/60] += C_l
        C_r_level[i/60] += C_r

        if ant[0] == 0:
            ant['L'] = 0
            ant['R'] = 0


    return ant_count_l, ant_count_r, C_l_level, C_r_level



if __name__ == '__main__': # パラメータの設定
    q = 1.0
    n = 2
    k = 5.0
    phi = 0.2
    delta_t = 1
    alpha = 0.0005

    ant_count_l, ant_count_r, C_l_level, C_r_level = simu()

    plot(ant_count_l, ant_count_r, C_l_level, C_r_level)
