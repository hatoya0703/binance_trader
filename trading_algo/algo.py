import numpy as np
def min_max(in_real):
    min_val = in_real[0]
    max_val = in_real[0]

    for price in in_real:
        if price < min_val:
            min_val = price
        if price > max_val:
            max_val = price

    return min_val, max_val

# 一目均衡表を求める処理
def ichimoku_cloud(in_real):
    length = len(in_real)
    tenkan = [0] * min(9, length)
    kijun = [0] * min(26, length)
    senkou_a = [0] * min(26, length)
    senkou_b = [0] * min(52, length)
    chikou = [0] * min(26, length)

    for i in range(len(in_real)):
        if i >= 9: # 9日間のデータが溜まったら転換線を求める
            min_val, max_val = min_max(in_real[i-9:i]) # 9日間の最小値と最大値を取得
            tenkan.append((min_val + max_val) / 2) # 9日間の最小値と最大値の平均値を転換線とする
        if i >= 26: # 26日間のデータが溜まったら基準線を求める
            min_val, max_val = min_max(in_real[i-26:i]) # 26日間の最小値と最大値を取得
            kijun.append((min_val + max_val) / 2) # 26日間の最小値と最大値の平均値を基準線とする

            senkou_a.append((tenkan[i] + kijun[i]) / 2) # 転換線と基準線の平均値を先行スパンAとする

            chikou.append(in_real[i-26]) # 26日前の終値を遅行スパンとする

        if i >= 52: # 52日間のデータが溜まったら先行スパンBを求める
            min_val, max_val = min_max(in_real[i-52:i]) # 52日間の最小値と最大値を取得
            senkou_b.append((min_val + max_val) / 2) # 52日間の最小値と最大値の平均値を先行スパンBとする

        senkou_a = ([0] * 26) + senkou_a[:length-26] # 先行スパンAを26日分ずらす
        senkou_b = ([0] * 26) + senkou_b[:length-26] # 先行スパンBを26日分ずらす

    return tenkan, kijun, senkou_a, senkou_b, chikou