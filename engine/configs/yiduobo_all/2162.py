def _txt(S, B):
    ln = S['_line']
    if ln < 5 or 'now' not in S:
        return '暴力枚举每一种输入的数字'
    keys = 'abcd' if ln < 20 else 'bcd' if ln < 33 else 'cd' if ln < 43 else 'd'
    digs = [S[k] for k in keys]
    sec = sum(v * m for v, m in zip(reversed(digs), (1, 10, 60, 600)))
    return f"枚举到 `{' '.join(map(str, digs))}`：秒数 ==`{sec}`==，当前最小代价 ==`{S['res']}`=="


CONFIG = dict(
    num=2162, title='设置时间的最少代价', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='暴力枚举 4 位数字', tags=['灵神题单', '难度分 1852'],
    code='''
class Solution(object):
    def minCostSetTime(self, startAt, moveCost, pushCost, targetSeconds):

        res = (moveCost + pushCost) * 4
        for a in range(1, 10):
            for b in range(10):
                for c in range(10):
                    for d in range(10):
                        if a * 600 + b * 60 + c * 10 + d == targetSeconds:
                            now = pushCost * 4
                            if a != startAt:
                                now += moveCost
                            if a != b:
                                now += moveCost
                            if b != c:
                                now += moveCost
                            if c != d:
                                now += moveCost
                            res = min(res, now)
        
        for b in range(1, 10):
            for c in range(10):
                for d in range(10):
                    if b * 60 + c * 10 + d == targetSeconds:
                        now = pushCost * 3
                        if b != startAt:
                            now += moveCost
                        if b != c:
                            now += moveCost
                        if c != d:
                            now += moveCost
                        res = min(res, now)
        
        for c in range(1, 10):
            for d in range(10):
                if c * 10 + d == targetSeconds:
                    now = pushCost * 2
                    if c != startAt:
                        now += moveCost
                    if c != d:
                        now += moveCost
                    res = min(res, now)
        
        for d in range(1, 10):
            if d == targetSeconds:
                now = pushCost
                if d != startAt:
                    now += moveCost
                res = min(res, now)
        
        return res
''',
    call='Solution().minCostSetTime(0, 1, 2, 76)',
    expect=6,
    skip=['for ', '== targetSeconds'],
    max_steps=90, max_events=200000,
    views=[
        dict(type='text', fn=_txt, size=28, h=130),
        dict(type='text', fn=lambda S: f"手指起点 `{S['startAt']}`，移动 `{S['moveCost']}`，按键 `{S['pushCost']}`，目标 `{S['targetSeconds']}` 秒", size=26, h=110),
    ],
    watch=[('now', 'now', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = (moveCost': '先给 `res` 一个上界：4 个数字每个都移动 + 按键 = =={res}==',
        'now = pushCost * 4': '四位数 `{a}{b}{c}{d}` 恰好等于目标秒数：按键 4 次，`now` = =={now}==',
        'now = pushCost * 3': '三位数 `{b}{c}{d}`（前缀 0 自动补）等于目标：按键 3 次，`now` = =={now}==',
        'now = pushCost * 2': '两位数 `{c}{d}` 等于目标：按键 2 次，`now` = =={now}==',
        'now = pushCost\n': '一位数 `{d}` 等于目标：按键 1 次，`now` = =={now}==',
        'if a != startAt': '首位 `{a}` 和起点 `{startAt}` {"不同" if a != startAt else "相同"}',
        'if a != b': '`{a}` 与 `{b}` {"不同" if a != b else "相同"}：相邻数字不同才要移动',
        'if b != c': '`{b}` 与 `{c}` {"不同" if b != c else "相同"}',
        'if c != d': '`{c}` 与 `{d}` {"不同" if c != d else "相同"}',
        'if b != startAt': '首位 `{b}` 和起点 `{startAt}` {"不同" if b != startAt else "相同"}',
        'if c != startAt': '首位 `{c}` 和起点 `{startAt}` {"不同" if c != startAt else "相同"}',
        'if d != startAt': '首位 `{d}` 和起点 `{startAt}` {"不同" if d != startAt else "相同"}',
        'now += moveCost': '需要移动手指：`now` = =={now}==',
        'res = min': '`res = min({B.res}, {now})` = =={res}==',
        'return res': '所有输入方式里最小代价是 =={res}==',
    },
    cards=dict(
        one_liner='最多 4 位数字，一万种输入，直接暴力',
        complexity='时间 `O(10^4)`，空间 `O(1)`',
        problem=['微波炉输入 1 到 4 位数字，补前导 0 后前两位是分钟、后两位是秒',
                 '移动手指花 `moveCost`，每次按键花 `pushCost`',
                 '示例：`startAt=0, moveCost=1, pushCost=2, 目标 76 秒` → `6`'],
        quote='由于最多只有4位数字，那么最多也只有一万种可能的输入，可以直接暴力求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['按输入位数分四组，==强制最高位不为 0== 再枚举，避免前导 0 重复',
              '算出这串数字代表的秒数，等于目标才计算代价',
              '代价 = 按键次数 × `pushCost` + 相邻数字不同的次数 × `moveCost`',
              '为了看得清，动画只展示命中目标的方案'],
        summary=['时间 `O(10^4)`，空间 `O(1)`',
                 '易错：分钟、秒都可以是 99 以内，所以 `0 9 6 0` 这类借分钟也被枚举到',
                 '易错：一组枚举的最高位要从 1 开始，否则同一时间会重复算',
                 '代码逐字照搬原文，无需改动即可在 Python 3 运行',
                 '对比灵神：灵神只构造至多三种写法，yiduobo 直接枚举全部'],
    ),
)
