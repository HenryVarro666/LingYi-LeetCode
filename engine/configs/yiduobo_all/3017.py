def _top(S):
    ln = S.get('_line') or 0
    if ln < 20:
        return '先让 `x < y`；`y − x ≤ 1` 时没有有效近路，答案是 `[(n−1)×2, …, 2, 0]`' if ln < 10 else f'==第一部分==：x 到 y 形成长 `{S.get("circle_len", "?")}` 的环，环内距离用差分一次写好'
    if ln < 27:
        return '==第二部分==：1→x→y→n 的链，x~y 一段在环里算过，最后要减去重复的'
    if ln < 45:
        return f'==第三部分==：链外的房子 `{S["index"]}` 先走到 x（或 y），再套用环的结论，去掉到 x、y 的重复'
    return '==汇总==：对差分数组做前缀和，得到每个距离的房屋对数'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n, x, y = S.get('n'), S.get('x'), S.get('y')
    if n is None or x is None or y is None or x >= y:
        return
    cv.text((x0 + 18, y0 + 4), '三部分：环（x~y）、主链、链外的房子', 24, T['muted'], bold=True)
    L, R = x0 + 60, x1 - 60
    cy = y0 + 150
    step = (R - L) / max(1, n - 1)

    def X(h):
        return L + (h - 1) * step
    cv.line([(X(1), cy), (X(n), cy)], T['border'], 3)
    cv.line([(X(x), cy), (X(x), cy - 60), (X(y), cy - 60), (X(y), cy)], T['purple'], 4)
    cv.text(((X(x) + X(y)) / 2, cy - 66), f'环长 {y - x + 1}', 20, T['purple'], anchor='mb', bold=True)
    idx = S.get('index') if 27 <= (S.get('_line') or 0) < 45 else None
    for h in range(1, n + 1):
        c = (125, 133, 145)
        if x <= h <= y:
            c = T['purple']
        if h == idx:
            c = T['yellow']
        cv.rect((X(h) - 22, cy - 22, X(h) + 22, cy + 22), fill=c, r=22)
        cv.text((X(h), cy), h, 24, T['bg'], anchor='mm', bold=True)


CONFIG = dict(
    num=3017, title='按距离统计房屋对数目 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='拆成环与链 · 差分数组',
    tags=['常用数据结构', '贪心与思维', '难度分 2709'],
    code='''
class Solution(object):
    def countOfPairs(self, n, x, y):

        if x > y:
            x, y = y, x
        
        if y - x <= 1:
            return [(index - 1) * 2 for index in range(n, 0, -1)]
        
        delta = [0] * (n + 1)
        circle_len = y - x + 1
        circle_dis_max = circle_len // 2
        delta[1] += circle_len * 2
        delta[circle_dis_max + 1] -= circle_len
        if circle_len % 2 == 0:
            delta[circle_dis_max] -= circle_len
        else:
            delta[circle_dis_max + 1] -= circle_len
        
        chain_len = x - 1 + n - y + 2
        for index in range(1, chain_len):
            delta[1] += 2
            delta[chain_len - index + 1] -= 2
        delta[1] -= 2
        delta[2] += 2

        for index in range(x - 1, 0, -1):
            delta[x - index + 1] += 2
            delta[x - index + circle_dis_max + 1] -= 2
            delta[x - index + 2] += 2
            if circle_len % 2 == 0:
                delta[x - index + circle_dis_max] -= 2
            else:
                delta[x - index + circle_dis_max + 1] -= 2

        for index in range(y + 1, n + 1):
            delta[index - y + 1] += 2
            delta[index - y + circle_dis_max + 1] -= 2
            delta[index - y + 2] += 2
            if circle_len % 2 == 0:
                delta[index - y + circle_dis_max] -= 2
            else:
                delta[index - y + circle_dis_max + 1] -= 2

        v = 0
        res = []
        for index in range(1, n + 1):
            v += delta[index]
            res.append(v)
        
        return res
''',
    call='Solution().countOfPairs(7, 2, 6)',
    expect=[14, 18, 10, 0, 0, 0, 0],
    views=[
        dict(type='text', fn=_top, size=23, h=80),
        dict(type='custom', draw=_draw, h=230),
        dict(type='array', var='delta', label='delta（差分数组，下标 = 距离）',
             color=lambda S, i, v: 'yellow' if (S.get('_line') or 0) >= 45 and i == S.get('index') else None, h=170),
        dict(type='array', var='res', label='res（每个距离的房屋对数）', h=140),
    ],
    watch=[('circle_len', 'circle_len', 'purple'), ('circle_dis_max', 'circle_dis_max', 'cyan'), ('chain_len', 'chain_len', 'blue'), ('index', 'index', 'yellow'), ('v', 'v', 'green')],
    captions={
        'if x > y': '约定 `x < y`，交换不影响结果',
        'if y - x <= 1': lambda S, B, r: (f'`y − x = {S.y - S.x} <= 1`：近路等于没有，走特殊情况' if S.y - S.x <= 1 else f'`y − x = {S.y - S.x} > 1`：近路有效，继续'),
        'delta = [0]': '`delta` 是答案的差分数组：区间 `[l, r]` 加一 = `delta[l] += 1`，`delta[r+1] -= 1`（这里每次加 2，因为 (a,b)、(b,a) 都算）',
        'circle_len =': '环长 `circle_len = y − x + 1 = {circle_len}`',
        'circle_dis_max =': '环内最大距离 `circle_dis_max = {circle_len} // 2 = {circle_dis_max}`',
        'delta[1] += circle_len * 2': '环里每个点向两个方向走：距离 1 起每档先写 `{circle_len*2}` 对',
        14: '距离不会超过 `{circle_dis_max}`：在 `{circle_dis_max+1}` 处先扣掉 `{circle_len}`',
        18: '奇数环：再扣 `{circle_len}`，距离 `1..{circle_dis_max}` 每档恰好 `{circle_len*2}` 对',
        'if circle_len % 2 == 0': lambda S, B, r: ('环长为偶数：每点有唯一的“对角点”，最大距离那一档只有一半的对数' if S.circle_len % 2 == 0 else '环长为奇数：两个方向走到的最远点不同，每档都是整对'),
        'delta[circle_dis_max] -= circle_len': '偶数环：距离 `{circle_dis_max}` 这一档只剩 `circle_len` 对，再扣一份',
        'chain_len =': '主链 1→x→y→n 的长度（x~y 的捷径算一步）：`chain_len = {chain_len}`',
        'delta[1] += 2': lambda S, B, r: ('链上每个点到右边点的距离是 `1..`：区间 `[1, chain_len−index]` 加一' if 'index' in S and 'chain_len' in S and S.get('_line') != 0 else '先写入 1 号距离'),
        'delta[chain_len - index + 1] -= 2': '区间在 `chain_len − index` 处结束，下一格抵消',
        'delta[1] -= 2': '距离 1：x~y 这条边在环和链里各算了一次，扣掉 2 个有序对',
        'delta[2] += 2': '`+2` 放在 2 号位，让上一步的扣减只影响距离 1 这一档',
        'for index in range(x - 1, 0, -1)': '处理链外左侧的房子 `index = {index}`：先走 `x − index = {x-index}` 步到 x',
        'for index in range(y + 1, n + 1)': '处理链外右侧的房子 `index = {index}`：先走 `index − y = {index-y}` 步到 y',
        'delta[x - index + 1] += 2': '距离区间从 `x − index + 1 = {x-index+1}` 开始（走到 x 后再走 1 步）',
        'delta[x - index + circle_dis_max + 1] -= 2': '区间到 `x − index + circle_dis_max = {x-index+circle_dis_max}` 为止',
        'delta[x - index + 2] += 2': '另一个方向绕环的区间，从 `{x-index+2}` 开始（去掉了到 y 的重复）',
        'delta[index - y + 1] += 2': '距离区间从 `index − y + 1 = {index-y+1}` 开始（走到 y 后再走 1 步）',
        'delta[index - y + circle_dis_max + 1] -= 2': '区间到 `index − y + circle_dis_max = {index-y+circle_dis_max}` 为止',
        'delta[index - y + 2] += 2': '另一个方向绕环的区间，从 `{index-y+2}` 开始（去掉了到 x 的重复）',
        'delta[x - index + circle_dis_max] -= 2': '偶数环：另一个方向少一档，在 `{x-index+circle_dis_max-1}` 结束',
        'delta[index - y + circle_dis_max] -= 2': '偶数环：另一个方向少一档，在 `{index-y+circle_dis_max-1}` 结束',
        'v += delta[index]': '前缀和：距离 `{index}` 的房屋对数 `v = {v}`',
        'res.append(v)': '写入 `res`：距离 {index} 有 =={v}== 对',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='把图拆成环、主链和链外点三块，全部写进差分数组',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['房屋 `1..n` 相邻相连，另有一条街连接 `x` 和 `y`',
                 '统计最短距离为 `k` 的有序房屋对个数，`k = 1..n`',
                 '本视频：`n=7, x=2, y=6` → `[14,18,10,0,0,0,0]`'],
        quote='从每个节点出发的距离都必然是连续的，那么对于从某个点出发的距离为1到k的结果，可以视为在答案数组中的1到k中每个数都加上1，这是一个非常典型的静态区间修改，最后单点求值的情况，是非常适合用差分数组的。',
        quote_src='—— yiduobo 题解原文',
        idea=['`x~y` 形成环：环内距离奇偶分情况，一次性写出',
              '`1→x→y→n` 是一条链，链上距离 `1..n−1`，但 x~y 一段与环重复，要扣掉',
              '链外的房子先走到 x（或 y），再套环的结论；去掉到 x、y 的重复，仍是连续区间 → 差分'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`y − x ≤ 1` 时近路无效，直接返回 `[(n−1)×2, …, 2, 0]`',
                 '易错点：环长奇偶不同，最大距离那一档的数量不同；链和环重复计了一次距离 1',
                 '对比灵神：灵神按 i 枚举并分三段区间；yiduobo 按环、链、链外三块分别写差分',
                 '原文已是 Python 3 可运行的写法（整数除法本来就是 `//`），未作修改'],
    ),
)
