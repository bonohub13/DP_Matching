#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import os

from extract_data import extract_data

DATA_011 = extract_data('datas/city011')
DATA_012 = extract_data('datas/city012')
DATA_021 = extract_data('datas/city021')
DATA_022 = extract_data('datas/city022')

keys_list = sorted(list(DATA_011.keys()))

class DP_matching:
    def __init__(self, datas=(DATA_011, DATA_012, DATA_021, DATA_022), keys=keys_list):
        self.data_011, self.data_012, self.data_021, self.data_022 = datas
        self.keys = keys
        self.d = self.local_dist
    
    def local_dist(self, data_1, data_2):
        d = []
        for i in range(len(data_1)):
            d.append([])
            for j in range(len(data_2)):
                d[i].append(np.sqrt(sum([(data_1[i][k]-data_2[j][k])**2 for k in range(15)])))
        return d

    def cumulative_dist(self, data_1, data_2):
        g = []
        d = self.d(data_1, data_2)
        
        # 初期条件
        g.append([d[0][0]])

        # 境界条件
        for j in range(1, len(data_2)):
            g[0].append(g[0][j-1] + d[0][j])
        for i in range(1, len(data_1)):
            g.append([])
            g[-1].append(g[i-1][0] + d[i][0])
            for j in range(1, len(data_2)):
                minimum = g[i-1][j] + d[i][j]
                if (g[i-1][j-1] + 2*d[i][j]) < minimum:
                    g[-1].append(g[i-1][j-1] + 2*d[i][j])
                elif (g[i][j-1] + d[i][j]) < minimum:
                    g[-1].append(g[i][j-1] + d[i][j])
                else:
                    g[-1].append(minimum)

        cumulative_dist = g[len(data_1)-1][len(data_2)-1]/(len(data_1)+len(data_2))
        
        return cumulative_dist

if __name__ == "__main__":
    count_11, count_12, count_21, count_22 = 0, 0, 0, 0
    dp = DP_matching()
    for key_1 in range(len(keys_list)):
        match = []
        for key_2 in range(len(keys_list)):
            cumulative_dist = dp.cumulative_dist(dp.data_011[dp.keys[key_1]], dp.data_011[dp.keys[key_2]])
            match.append(cumulative_dist)
        # print(match)
        if min(match) == match[key_1]:
            print('##### SUCCESS! #####')
            count_12 += 1
        else:
            print('##### UNKO MORETA #####')
    for key_1 in range(len(keys_list)):
        match = []
        for key_2 in range(len(keys_list)):
            cumulative_dist = dp.cumulative_dist(dp.data_011[dp.keys[key_1]], dp.data_012[dp.keys[key_2]])
            match.append(cumulative_dist)
        # print(match)
        if min(match) == match[key_1]:
            print('##### SUCCESS! #####')
            count_11 += 1
        else:
            print('##### UNKO MORETA #####')
    for key_1 in range(len(keys_list)):
        match = []
        for key_2 in range(len(keys_list)):
            cumulative_dist = dp.cumulative_dist(dp.data_011[dp.keys[key_1]], dp.data_021[dp.keys[key_2]])
            match.append(cumulative_dist)
        # print(match)
        if min(match) == match[key_1]:
            print('##### SUCCESS! #####')
            count_21 += 1
        else:
            print('##### UNKO MORETA #####')
    for key_1 in range(len(keys_list)):
        match = []
        for key_2 in range(len(keys_list)):
            cumulative_dist = dp.cumulative_dist(dp.data_011[dp.keys[key_1]], dp.data_022[dp.keys[key_2]])
            match.append(cumulative_dist)
        # print(match)
        if min(match) == match[key_1]:
            print('##### SUCCESS! #####')
            count_22 += 1
        else:
            print('##### UNKO MORETA #####')
    print('--------------------------------------------------------\n\
        comparison between CITY011 and CITY011: %d%% successful!\n\
        comparison between CITY011 and CITY012: %d%% successful!\n\
        comparison between CITY011 and CITY021: %d%% successful!\n\
        comparison between CITY011 and CITY022: %d%% successful!\n\
        -------------------------------------------------------\n' % (count_11, count_12, count_21, count_22))