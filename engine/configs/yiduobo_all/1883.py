def _txt(S):
    if 'i' not in S:
        return '`f[j]` ÷ `speed` = 走完前几条路、跳过 `j` 次休息的最少小时数（分子统一存成 `×speed` 的整数）'
    sp = S['speed']
    i = S['i']
    return f'第 `{i}` 条路：用上一轮 `g`（走完前 `{i}` 条路）推出新一轮 `f`'


CONFIG = dict(
    num=1883, title='准时抵达会议现场的最小跳过休息次数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='二维 DP · 每种跳过次数的最早到达时间',
    tags=['其他线性 DP', '多维 DP', '难度分 2588'],
    code='''
class Solution(object):
    def minSkips(self, dist, speed, hoursBefore):

        f = [dist[0]]

        for i in range(1, len(dist)):
            g = f[:]
            f = []
            for j in range(i):
                if g[j] % speed == 0:
                    t = g[j]
                else:
                    t = (g[j] // speed + 1) * speed
                
                f.append(t + dist[i])
                
                if j > 0:
                    f[-1] = min(f[-1], g[j - 1] + dist[i])
            
            f.append(g[-1] + dist[i])
        
        if f[-1] > speed * hoursBefore:
            return -1
        
        res = 0
        while f[res] > speed * hoursBefore:
            res += 1
        return res
''',
    call='Solution().minSkips([7, 3, 5, 5], 2, 10)',
    expect=2,
    views=[
        dict(type='array', var='dist', label='dist（蓝 = 正在加入的第 i 条路）', cell=84, h=210,
             pointers={'i': 'blue'}, color=lambda S, k, v: 'blue' if k == S.get('i') else None),
        dict(type='array', var='g', label='g[j]：走完前 i 条路、跳过 j 次的最短用时 × speed', cell=96, h=210,
             pointers={'j': 'cyan'}, color=lambda S, k, v: 'cyan' if k == S.get('j') else None),
        dict(type='array', var='f', label='f[j]：走完前 i+1 条路（正在生成，粉 = 刚写入）', cell=96, h=210,
             color=lambda S, k, v: 'pink' if S.get('_line') in (15, 18, 20) and k == len(S['f']) - 1 else None),
        dict(type='text', fn=_txt, size=24, h=70),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'cyan'), ('t', 't', 'yellow'), ('speed', 'speed', 'orange'), ('res', 'res', 'green')],
    skip=['g = f[:]', 'f = []', 'for j in range', 'else:'],
    captions={
        'f = [dist[0]]': '只走第 0 条路：不存在“跳过”，`f[0] = dist[0] = {dist[0]}`（单位是 ==距离==，除以 `speed` 才是小时）',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：加入第 `{S.i}` 条路，由上一轮 `g` 推出 `f`' if S.get('i') != B.get('i') else '所有路都加入完了：`f[j]` = 走完全程、跳过 `j` 次的最短用时'),
        'if g[j] % speed == 0': '`g[j] = {g[j]}`，`speed = {speed}`：{"恰好是整数小时 → 不用等" if g[j] % speed == 0 else "不是整点 → 休息时要向上取整到下一个整点"}',
        't = g[j]': '`t = g[j] = {t}`：已在整点，休息不耗时',
        't = (g[j] //': '向上取整到整点：`({g[j]}//{speed}+1)×{speed}` = =={t}==',
        'f.append(t + dist[i])': '==不跳过==这次休息：`f[{j}] = t + dist[i] = {t}+{dist[i]}` = =={f[-1]}==',
        'if j > 0': '`j = {j}`：{"还可以考虑跳过最后一次休息（用上一轮 j-1 次的结果）" if j > 0 else "j = 0 表示一次都没跳，没有“跳过”可选"}',
        'f[-1] = min': '==跳过==最后一次休息：`g[{j-1}] + dist[i] = {g[j-1]}+{dist[i]}` = {g[j-1]+dist[i]}，与不跳过取小 → =={f[-1]}==',
        'f.append(g[-1]': '`f[{i}]`（恰好把前 `{i}` 次休息全跳掉）：不需要取整，`g[-1] + dist[i]` = =={f[-1]}==',
        'if f[-1] > speed': '全跳也要 `{f[-1]}`，而时限是 `speed × hoursBefore = {speed*hoursBefore}`：{"超时 → 返回 -1" if f[-1] > speed*hoursBefore else "来得及，一定有解"}',
        'res = 0': '从跳过 0 次开始，往后找第一个来得及的跳过次数',
        'while f[res] >': lambda S, B, r: (f'`f[{S.res}] = {S.f[S.res]}` {">" if S.f[S.res] > S.speed*S.hoursBefore else "≤"} `{S.speed*S.hoursBefore}`：'
                                           f'{"来不及 → 多跳一次" if S.f[S.res] > S.speed*S.hoursBefore else "来得及 → 停"}'),
        'res += 1': '`res` → {res}',
        'return res': '最少跳过 ==`{res}`== 次',
    },
    max_steps=100,
    cards=dict(
        one_liner='换个问法：跳过 j 次，最早什么时候到？再找最小的 j',
        complexity='时间 `O(n^2)`，空间 `O(n)`（滚动数组）',
        problem=['依次走 `n` 条路，每走完一条要休息到下一个整点；可以跳过某些休息，求准时（`hoursBefore` 小时内）到达的最少跳过次数',
                 '最后一条路后不用休息；到不了返回 -1',
                 '示例：`dist=[7,3,5,5], speed=2, hoursBefore=10` → `2`'],
        quote='直接求解起来比较困难……不妨转换思路，考虑跳过若干次之后最早什么时候可以抵达会议现场。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：走完 0..i 条路、跳过 j 次休息的最少用时，要求 `j < i + 1`',
              '不跳过最后一次休息：`ceil(f[i-1][j]) + dist[i]/speed`；跳过：`f[i-1][j-1] + dist[i]/speed`',
              '分母都是 `speed`，用整数（乘 `speed`）代替分数，避免浮点误差'],
        summary=['时间 `O(n^2)`，滚动数组 `g`/`f` 空间 `O(n)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '易错：全跳那一项 `f[i]`单独 `append`，它没有“不跳过”的分支',
                 '易错：最后一段不需要休息，所以 `f` 里不对最后一条路取整',
                 '对比灵神：灵神枚举“最多跳 i 次”并只算到 `dist[:-1]`；yiduobo 逐条路扩展，恰好跳 j 次'],
    ),
)
