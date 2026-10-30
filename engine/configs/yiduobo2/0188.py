K = 2
PRICES = [3, 2, 6, 5, 0, 3]


def _name(j):
    return f"{'买' if j % 2 == 0 else '卖'}{j // 2 + 1}"


def _states(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    f = S.get('f')
    if f is None:
        cv.text((x0 + 18, y0 + 4), 'f[j]：刚完成第 j 个动作时的最大收益（买1, 卖1, 买2, 卖2, …）', 22, T['muted'], bold=True)
        return
    ln = S.get('_line')
    j = S.get('j')
    i = S.get('i')
    cv.text((x0 + 18, y0 + 4), 'f[j]：刚完成第 j 个动作时的最大收益（· = None，还到达不了）', 22, T['muted'], bold=True)
    m = len(f)
    bw, gap = 150, 80
    total = m * bw + (m - 1) * gap
    sx = x0 + 20 + (x1 - x0 - 40 - total) / 2
    Y = y0 + 70
    tgt = src = None
    if ln in (22, 23, 24) and j is not None and i is not None:
        tgt, src = j, j - 1
    if ln == 26 or ln == 14:
        tgt = 0
    if ln in (30, 31):
        tgt = (S['i'] * 2 - 1) % m
    bf = B.get('f')
    for k in range(m):
        X = sx + k * (bw + gap)
        c = T['green'] if k == tgt else (T['blue'] if k == src else T['panel2'])
        changed = bf is not None and len(bf) == m and bf[k] != f[k]
        cv.rect((X, Y, X + bw, Y + 110), fill=c, r=12, outline=T['yellow'] if changed else T['border'], width=3 if changed else 1)
        on = k in (tgt, src)
        cv.text((X + bw / 2, Y + 28), f'f[{k}] {_name(k)}', 24, T['bg'] if on else T['muted'], anchor='mm', bold=True)
        v = f[k]
        cv.text((X + bw / 2, Y + 76), '·' if v is None else v, 40, T['bg'] if on else T['text'], anchor='mm', bold=True)
        if k > 0:
            xa = X - gap + 6
            sign = '+p' if k % 2 == 1 else '−p'
            cv.arrow((xa, Y + 55), (X - 6, Y + 55), T['blue'] if k == tgt else T['dim'], 3, 12)
            cv.text((X - gap / 2, Y + 44), sign, 20, T['blue'] if k == tgt else T['dim'], anchor='mb', bold=True)
    if ln in (22, 23, 24) and j is not None and i is not None:
        p = S['prices'][i]
        flag = S['flag']
        cand = None if f[j - 1] is None else (B['f'][j - 1] + flag * p if ln == 24 else f[j - 1] + flag * p)
        msg = (f"`f[{j}]` ← `f[{j - 1}] {'+' if flag > 0 else '−'} prices[{i}]`"
               + (f" = `{f[j - 1]} {'+' if flag > 0 else '−'} {p}` = =={cand}==" if cand is not None else '：`f[{0}]` 还是 None，不能转移'.format(j - 1)))
        cv.rich(x0 + 30, Y + 140, msg, x1 - x0 - 60, size=28, accent=T['orange'])


def _prices(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    p = S.get('prices') or PRICES
    ln = S.get('_line')
    i = S.get('i') if ln is not None and 15 <= ln <= 26 else None
    idx = S.get('index')
    cv.text((x0 + 18, y0 + 4), f'prices（n = {len(p)}，k = {K}；k < n // 2 → 动态规划）', 22, T['muted'], bold=True)
    cell = min(120, (x1 - x0 - 40) / len(p))
    sx = x0 + 20 + (x1 - x0 - 40 - cell * len(p)) / 2
    for k, v in enumerate(p):
        X = sx + k * cell
        on = k == i or k == idx
        cv.rect((X + 6, y0 + 40, X + cell - 6, y0 + 96), fill=T['orange'] if on else T['panel2'], r=10, outline=T['border'])
        cv.text((X + cell / 2, y0 + 68), v, 28, T['bg'] if on else (T['dim'] if i is not None and k > i else T['text']),
                anchor='mm', bold=True)
        cv.text((X + cell / 2, y0 + 102), f'第 {k} 天', 18, T['dim'], anchor='mt')


def _note(S):
    ln = S.get('_line')
    if ln is not None and 15 <= ln <= 26 and S.get('j') is not None:
        j = S['j']
        if j == 1 and S['k'] > 1:
            return '`j = 1` 用到的 `f[0]` 已在本轮被更新过：相当于今天买今天卖，收益 0，不影响答案'
        return (f"==倒序==：处理 `j = {j}` 时 `f[{j - 1}]` 还是==昨天==的值（转移要用它），"
                f"`f[{j + 1}..]` 已经是今天的")
    if ln is not None and ln >= 28:
        return '答案 = `max(0, f[1], f[3], …)`：最后一个动作必须是「卖」才有意义'
    return ''


def _cap_fj1(S, B, ret):
    j, f = S.j, S.f
    if f[j - 1] is None:
        return f'`f[{j - 1}]`（{_name(j - 1)}）还是 None → 跳过'
    return f'`j = {j}`：`f[{j - 1}]`（{_name(j - 1)}）= `{f[j - 1]}` 可以转移'




def _cap_f0(S, B, ret):
    if S.i == 1 and S.j == 2 * S.k - 1:
        return f'边界「买1」= 前 i 天最低价的相反数：`max({B.f[0]}, -{S.prices[S.i]})` = `{S.f[0]}`'
    if S.i == 1 and S.j == 2 * S.k - 2:
        return '这行缩进在内层循环里，每个 `j` 都执行一次，但结果不变'
    if B.f[0] != S.f[0]:
        return f'「买1」更新：`max({B.f[0]}, -{S.prices[S.i]})` = `{S.f[0]}`'
    return f'`f[0]` 仍是 `{S.f[0]}`'


def _cap_better(S, B, ret):
    j, f, p, flag = S.j, S.f, S.prices[S.i], S.flag
    cand = f[j - 1] + flag * p
    op = '卖出' if flag > 0 else '买入'
    if f[j] is None:
        return f'`f[{j}]` 是 None → 第一次到达（今天{op}）'
    if f[j] < cand:
        return f'今天{op}：`{f[j - 1]} {"+" if flag > 0 else "−"} {p} = {cand}` > `{f[j]}` → ==更新=='
    return f'今天{op}：`{cand}` ≤ `{f[j]}` → 不更新'


CONFIG = dict(
    num=188, title='买卖股票的最佳时机 IV', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='2k 个状态串成链 · 滚动数组倒序更新',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def maxProfit(self, k, prices):
        if len(prices) < 2 or not k:
            return 0

        if k >= len(prices) // 2:
            res = 0
            for index in range(1, len(prices)):
                if prices[index] > prices[index - 1]:
                    res += prices[index] - prices[index - 1]
            return res

        f = [None] * (k * 2)
        f[0] = -prices[0]
        for i in range(1, len(prices)):
            for j in range(k + k - 1, 0, -1):
                if j % 2 == 1:
                    flag = 1
                else:
                    flag = -1

                if f[j - 1] is not None:
                    if f[j] is None or f[j] < f[j - 1] + flag * prices[i]:
                        f[j] = f[j - 1] + flag * prices[i]

                f[0] = max(f[0], -prices[i])

        res = 0
        for i in range(k):
            if f[i * 2 - 1] is not None:
                res = max(res, f[i * 2 - 1])

        return res
''',
    call=f'Solution().maxProfit({K}, {PRICES})',
    expect=7,
    views=[
        dict(type='custom', draw=_prices, h=140),
        dict(type='custom', draw=_states, h=300),
        dict(type='text', fn=_note, h=110, lines=2, size=26),
    ],
    skip=['if j % 2 == 1', 'flag = 1', 'flag = -1', 'for j in range'],
    max_steps=72,
    watch=[('i', 'i', 'orange'), ('j', 'j', 'cyan'), ('flag', 'flag'), ('res', 'res', 'green')],
    captions={
        'if len(prices) < 2 or not k': '天数 ≥ 2 且 `k > 0`，继续',
        'if k >= len(prices) // 2': '`k = {k} < n // 2 = {len(prices) // 2}`：次数==真的受限== → 只能老老实实动态规划',
        'f = [None] * (k * 2)': '`2k = {len(f)}` 个状态：买1、卖1、买2、卖2；`None` 表示还到达不了',
        'f[0] = -prices[0]': '第 0 天就能「买1」：`f[0] = -{prices[0]}`',
        'for i in range(1, len(prices))': lambda S, B, ret: ('所有天数处理完毕' if B.get('i') == S.i else
                                                             f'第 `{S.i}` 天，股价 `{S.prices[S.i]}`：`j` 从 `{2 * S.k - 1}` 倒着更新到 1'),
        'if f[j - 1] is not None': _cap_fj1,
        'if f[j] is None or': _cap_better,
        'f[j] = f[j - 1] + flag': '`f[{j}]` → =={f[j]}==',
        'f[0] = max(f[0], -prices[i])': _cap_f0,
        'res = 0': '答案 = `max(0, 所有「卖」状态)`',
        'for i in range(k)': lambda S, B, ret: (f'`i = {S.i}`：看 `f[{S.i * 2 - 1}]`' + ('（下标 -1 就是最后一个「卖」）' if S.i == 0 else '')
                                                if S.get('i') != B.get('i') or B.get('_line') != 29 else '检查完毕'),
        'if f[i * 2 - 1] is not None': lambda S, B, ret: f'`f[{S.i * 2 - 1}] = {S.f[S.i * 2 - 1]}`',
        'res = max(res, f[i * 2 - 1])': '`res = max({B.res}, {f[i * 2 - 1]})` = =={res}==',
        'return res': '最大利润 =={ret}==',
    },
    cards=dict(
        one_liner='把 k 次买卖拆成 2k 个状态，每个状态只从前一个状态转移',
        complexity='时间 `O(nk)`，空间 `O(k)`',
        problem=['`prices[i]` 是第 `i` 天的股价，==至多==完成 `k` 笔交易（买 + 卖 = 一笔）',
                 '手里最多持有一股，求最大利润',
                 f'本视频：`k = {K}`，`{PRICES}` → `7`（2 买 6 卖 + 0 买 3 卖）'],
        quote='若k满足k >= n/2，那么可以看做是不限次数的买入卖出股票，于是问题就退化到了122题……如果k < n/2，那么就只能老老实实用动态规划来做了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[j]`：j = 0 买1，1 卖1，2 买2，3 卖2……==所有 j 都从 j − 1 转移==',
              '卖（j 奇数）`+prices[i]`，买（j 偶数）`−prices[i]`，这就是 `flag`',
              '滚动数组要从 `2k − 1` 往 0 倒着更新：今天的 `f[j]` 需要昨天的 `f[j−1]`',
              '答案 `max(0, f[1], f[3], …, f[2k−1])`'],
        summary=['时间 `O(nk)`，空间 `O(k)`；`k ≥ n // 2` 时退化成 122 的贪心，`O(n)`',
                 '原文为 Python 2 写法：`len(prices) / 2` 是整除，已改为 `//`；并删去了类型说明文档字符串',
                 '`f[0] = max(...)` 缩进在内层循环里，每个 j 都会执行一次，但结果不变',
                 '最后的循环用 `f[i*2-1]`：`i = 0` 时取 `f[-1]`，正好是最后一个「卖」',
                 '对比灵神：灵神用 `f[i][j][hold]` 三维状态（至多 j 次 + 是否持有）'],
    ),
)
