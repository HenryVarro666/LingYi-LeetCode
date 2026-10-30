CONFIG = dict(
    num=3279, title='活塞占据的最大总面积', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='高度变化量差分',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def maxArea(self, height, positions, directions):

        f = [0] * (height * 2 + 1)
        for p, d in zip(positions, directions):
            if p == 0 or (d == 'U' and p != height):
                f[1] += 1
                f[height - p + 1] -= 2
                if p != 0:
                    f[height * 2 - p + 1] += 2
            else:
                f[1] -= 1
                f[p + 1] += 2
                if p != height:
                    f[height + p + 1] -= 2
        
        now = sum(positions)
        res = now
        delta = 0
        for t in range(1, height * 2):
            delta += f[t]
            now += delta
            res = max(res, now)
        
        return res
''',
    call="Solution().maxArea(4, [2, 4, 1], 'UDD')",
    expect=7,
    views=[
        dict(type='text', fn=lambda S: (f"活塞：高 `p={S['p']}`，方向 `{S['d']}`（周期 `2×height = {S['height']*2}` 秒）" if 'p' in S and 'delta' not in S else '')),
        dict(type='array', var='f', label='f[t]：第 t 秒速度变化量（差分）', pointers={'t': 'blue'}, h=200, cell=70,
             color=lambda S, i, v: 'yellow' if v != 0 else None),
        dict(type='text', fn=lambda S: (f"第 `{S['t']}` 秒：速度总和 `delta = {S['delta']}`，高度总和 `now = {S['now']}`" if 't' in S and 'now' in S and 'delta' in S else (f"初始高度和 `now = {S['now']}`" if 'now' in S else ''))),
    ],
    watch=['now', 'delta', 't', ('res', 'res', 'green')],
    captions={
        'f = [0]': '`f[t]` 记录第 `t` 秒速度总和相对上一秒的变化；只看一个周期 `0 ~ {height*2-1}` 秒',
        'if p == 0 or': lambda S, B, r: (f'活塞 `p={S.p}`，方向 `{S.d}`：接下来==先向上==（在底部或向上且没到顶）' if (S.p == 0 or (S.d == 'U' and S.p != S.height)) else f'活塞 `p={S.p}`，方向 `{S.d}`：接下来==先向下=='),
        'f[1] += 1': '第 1 秒起速度 `+1`（向上）',
        'f[height - p + 1] -= 2': '第 `height − p = {height - p}` 秒到顶，下一秒起变成向下 → 速度 +1 变 −1，差 `-2`',
        'f[height * 2 - p + 1] += 2': '再过 `height` 秒到底，下一秒起又向上 → `+2`',
        'f[1] -= 1': '第 1 秒起速度 `−1`（向下）',
        'f[p + 1] += 2': '第 `p = {p}` 秒到底，下一秒起转向上 → `+2`',
        'f[height + p + 1] -= 2': '再过 `height` 秒到顶，下一秒起转向下 → `-2`',
        'now = sum(positions)': '第 0 秒总高度 `now = {now}`',
        'res = now': '先把第 0 秒当作答案',
        'delta += f[t]': '用 `f[{t}] = {f[t]}` 更新速度总和 `delta = {delta}`',
        'now += delta': '总高度 `now = {B.now} + {delta} = {now}`',
        'res = max': '`res = max({B.res}, {now}) = {res}`',
        'return res': '最大总高度（面积）为 `{res}`',
    },
    cards=dict(
        one_liner='活塞每 2×height 秒一个周期，用差分记录“速度总和”的变化',
        complexity='时间 `O(n + height)`，空间 `O(height)`',
        problem=['活塞在高度 `0 ~ height` 之间每秒移动 1，到顶/到底后反向',
                 '给出初始高度 `positions` 和方向 `directions`（U / D）',
                 '求某一时刻所有活塞下方面积（高度之和）的==最大值=='],
        quote='每经过 height * 2 秒，每个活塞都将会恢复到初始状态，只需要考察 0 到 height * 2 - 1 秒。……高度的变化情况将形成最多三段全部由 1 或者 -1 的区间。',
        quote_src='—— yiduobo 题解原文',
        idea=['周期为 `2×height`，只模拟一个周期',
              '每个活塞每秒 ±1，一个周期内最多转向两次 → 每个活塞只改 3 个差分位置',
              '`f` 累加得总速度 `delta`，`delta` 累加得总高度 `now`，取最大'],
        summary=['时间 `O(n + height)`，空间 `O(height)`，不用逐活塞逐秒模拟',
                 '转向处速度从 +1 变 −1，差分是 `∓2`，不是 `∓1`',
                 '`p == 0` 的活塞按“向上”处理；`p == height` 且 `U` 的按“向下”处理',
                 '原文为 Python 2 风格，代码无需改动',
                 '同类题：1094 拼车、1109 航班预订统计'],
    ),
)
