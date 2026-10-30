def _g(S):
    return ['-' if v is None else v for v in S['g']]


def _gc(S, k, v):
    ln = S.get('_line', 0)
    if 'x' in S and ln in (11, 12, 13, 16, 17) and k == S['x'] and 'r_time' in S:
        return 'yellow'
    if 'i' in S and 'k' in S and ln >= 21:
        if k == S['i']:
            return 'yellow'
        if k in (S['k'], S['i'] - S['k']):
            return 'blue'
    return None


def _h(S):
    return S['h'] if 'h' in S else []


def _fx(S):
    ln = S.get('_line', 0)
    if 'x' in S and 5 <= ln <= 18 and 'r_time' in S:
        x = S['x']
        a, b = S['h'][x // 2], S['h'][(x + 1) // 2]
        return f'连续跑 {x} 圈 `r_time` = `{S["r_time"]}`；中途换一次胎 `c_time` = `{a} + {b} + {S["changeTime"]}` = =={a + b + S["changeTime"]}=='
    if 'i' in S and 'k' in S and ln >= 21:
        return f'`g[{S["i"]}]` 候选：`g[{S["k"]}] + g[{S["i"] - S["k"]}] + changeTime`'
    return '`g[i]` = 跑完 `i` 圈的最少时间；`h` = 当前轮胎连续跑的累计耗时'


CONFIG = dict(
    num=2188, title='完成比赛的最少时间', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='背包式 DP · 预处理单胎连续圈数',
    tags=['其他线性 DP', '难度分 2315'],
    code='''
class Solution(object):
    def minimumFinishTime(self, tires, changeTime, numLaps):

        g = [None] * (numLaps + 1)
        for f, r in tires:
            h = [0, f]
            if g[1] is None or g[1] > f:
                g[1] = f
            x = 2
            while x <= numLaps:
                r_time = (h[-1] - h[-2]) * r + h[-1]
                c_time = h[x // 2] + h[(x + 1) // 2] + changeTime
                if r_time >= c_time:
                    break
                h.append(r_time)
                if g[x] is None or g[x] > r_time:
                    g[x] = r_time
                x += 1

        for i in range(2, numLaps + 1):
            for k in range(1, i):
                if g[i] is None or g[i] > g[k] + g[i - k] + changeTime:
                    g[i] = g[k] + g[i - k] + changeTime
        
        return g[-1]
''',
    call='Solution().minimumFinishTime([[1,10],[2,2],[3,4]], 6, 5)',
    expect=25,
    skip=['x = 2', 'x += 1', 'if g[1] is None', 'h.append'],
    max_steps=90,
    views=[
        dict(type='array', var=_g, label='g[i]（跑完 i 圈的最少时间，- = 还没有值；黄 = 当前，蓝 = 拆成的两段）', h=230, cell=96, color=_gc),
        dict(type='text', fn=_fx, size=26, h=90),
        dict(type='array', var=_h, label='h[x]（当前轮胎不换胎跑 x 圈的累计耗时）', h=200, cell=96),
    ],
    watch=[('f', 'f', 'blue'), ('r', 'r', 'pink'), ('x', 'x', 'green'), ('i', 'i', 'orange'), ('k', 'k', 'purple')],
    captions={
        'g = [None] * (numLaps + 1)': '`g[i]` = 跑完 `i` 圈的最少时间，==None 表示还没有方案==',
        'for f, r in tires': '看轮胎 `f = {f}`，`r = {r}`',
        'h = [0, f]': '`h[x]` 是这条胎不换胎跑 `x` 圈的累计耗时：`h[1] = {f}`',
        'g[1] = f': '`g[1]` 更新为 `{f}`：一圈的最小耗时',
        'x = 2': '从第 2 圈开始往后试',
        'while x <= numLaps': '`x = {x}`，圈数没超过 `numLaps`',
        'r_time = (h[-1]': '连续跑 {x} 圈：第 {x} 圈耗时 `{h[-1] - h[-2]} × {r}`，累计 `r_time` = =={r_time}==',
        'c_time = h[x // 2]': '换一次胎的最优：==在正中间换==，`c_time` = `{h[x // 2]} + {h[(x + 1) // 2]} + {changeTime}` = =={c_time}==',
        'if r_time >= c_time': lambda S, B, r: (f'`r_time = {S.r_time}` ≥ `c_time = {S.c_time}`：==换胎更划算==，这条胎不用再往后跑' if S.r_time >= S.c_time
                                               else f'`r_time = {S.r_time}` < `c_time = {S.c_time}`：不换胎还是更快，继续'),
        'break': '停止：这条轮胎最多连续跑 `{x - 1}` 圈',
        'h.append(r_time)': '记下 `h[{x}] = {r_time}`',
        'g[x] = r_time': '`g[{x}]` 更新为 =={r_time}==',
        'x += 1': '`x` → {x}',
        'for i in range(2': '`i = {i}`：算跑完 {i} 圈的最少时间',
        'for k in range(1, i)': '枚举换胎前跑了 `k = {k}` 圈',
        'if g[i] is None or g[i] > g[k]': lambda S, B, r: (lambda c: f'拆成 `g[{S.k}] + g[{S.i - S.k}] + changeTime` = `{c}`，' + ('当前 `g[i]` 还是 None → 用它' if S.g[S.i] is None else (f'比 `g[{S.i}] = {S.g[S.i]}` 更小 → 更新' if c < S.g[S.i] else f'不比 `g[{S.i}] = {S.g[S.i]}` 小 → 不更新')))(S.g[S.k] + S.g[S.i - S.k] + S.changeTime),
        'g[i] = g[k] + g[i - k] + changeTime': '`g[{i}]` = `g[{k}] + g[{i - k}] + {changeTime}` = =={g[i]}==',
        'return g[-1]': '跑完 {numLaps} 圈最少 =={ret}== 秒',
    },
    cards=dict(
        one_liner='换胎前后各是一个子问题：g[i] = g[k] + g[i−k] + changeTime',
        complexity='时间 `O(numLaps^2 + n·log)`，空间 `O(numLaps)`',
        problem=['每条轮胎连续用，第 `x` 圈耗时 `f × r^(x-1)`，换胎花 `changeTime`',
                 '轮胎无限多条，求跑完 `numLaps` 圈的最少时间',
                 '示例：`[[1,10],[2,2],[3,4]]`，`changeTime = 6`，`5` 圈 → `25`'],
        quote='中途换胎，可以枚举换胎前跑了多少圈，那么就有g[i] = min(g[k] + g[i - k] + changeTime)，其中k的取值范围在1到i - 1之间，表示换胎前跑了k圈。',
        quote_src='—— yiduobo 题解原文',
        idea=['`g[i]` = 跑 `i` 圈的最少时间；换胎时间固定，所以不用管「用哪条胎」',
              '中途换胎就拆成 `k` 圈和 `i−k` 圈，各自独立',
              '单胎连续跑的耗时指数增长：只要「中间换一次胎」不比不换更好就停，圈数很小'],
        summary=['预处理每条胎连续跑的圈数，再做 `O(numLaps^2)` 的拆分 DP',
                 '判断何时停：不换胎耗时 `r_time ≥` 正中间换一次的 `c_time`',
                 '`g` 里 `None` 表示暂无方案，比较前先判空',
                 '原文为 Python 2 写法，`h[x / 2]`、`h[(x + 1) / 2]` 已改为 `//`',
                 '对比灵神：灵神把单胎圈数上界定为 17 并直接做 `f[i-j]` 转移；yiduobo 用拆分转移'],
    ),
)
