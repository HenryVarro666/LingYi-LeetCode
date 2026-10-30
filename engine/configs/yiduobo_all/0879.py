def _tgt(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or 'cost' not in S or 'w' not in S:
        return None
    return i + S['cost'], min(j + S['w'], S['minProfit'])


def _col(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    line = S.get('_line')
    if i is None or j is None or line not in (11, 13, 14):
        return None
    t = _tgt(S)
    if (r, c) == t:
        return 'pink'
    if (r, c) == (i, j):
        return 'yellow'
    return None


def _formula(S):
    line = S.get('_line')
    if 'cost' not in S or line not in (11, 13, 14) or S.get('j') is None:
        return '`f[i][j]` = 花费恰好 `i`、利润（封顶 `minProfit`）为 `j` 的方案数'
    i, j, cost, w, mp = S['i'], S['j'], S['cost'], S['w'], S['minProfit']
    t = _tgt(S)
    return f'从 `f[{i}][{j}]` = {S["f"][i][j]} 出发：人数 `{i}+{cost}={i + cost}`，利润 `{j}+{w}={j + w}` → 落在 `f[{t[0]}][{t[1]}]`' + ('（封顶）' if j + w >= mp else '')


CONFIG = dict(
    num=879, title='盈利计划', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='二维费用 0-1 背包 · 利润封顶',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def profitableSchemes(self, n, minProfit, group, profit):

        m = len(group)
        f = [[0] * (minProfit + 1) for _ in range(n + 1)]
        f[0][0] = 1
        mod = 10**9 + 7
        for cost, w in zip(group, profit):
            for i in range(n - cost, -1, -1):
                for j in range(minProfit, -1, -1):
                    if j + w >= minProfit:
                        f[i + cost][minProfit] = (f[i + cost][minProfit] + f[i][j]) % mod
                    else:
                        f[i + cost][j + w] = (f[i + cost][j + w] + f[i][j]) % mod
        
        res = 0
        for i in range(n + 1):
            res = (res + f[i][-1]) % mod
        return res
''',
    call='Solution().profitableSchemes(3, 2, [2, 1], [2, 1])',
    expect=2,
    skip=['m = len', 'mod = ', 'for j in range(minProfit', 'res = 0'],
    max_steps=70,
    views=[
        dict(type='table', var='f', label='f[i][j]：行 = 已用人数 i，列 = 利润 j（封顶）。黄 = 来源，粉 = 加到的目标格', cell=100, h=380,
             rows=lambda S: [f'人数 {i}' for i in range(len(S['f']))] if 'f' in S else None,
             cols=lambda S: [f'利润 {j}' for j in range(len(S['f'][0]))] if 'f' in S else None,
             color=_col),
        dict(type='text', fn=_formula, size=24, h=80),
    ],
    watch=['cost', 'w', 'i', 'j', ('res', 'res', 'green')],
    captions={
        'f = [[0]': '`f[i][j]`：恰好用 `i` 个人、利润达到 `j`（超过 `minProfit` 都算 `minProfit`）的方案数',
        'f[0][0] = 1': '什么工作都不选：`f[0][0] = 1`（一种方案）',
        'for cost, w in zip': '考虑工作 `(人数 {cost}, 利润 {w})`：每个工作选或不选，==二维费用 0-1 背包==',
        'for i in range(n - cost': '`i` 从 `{n - cost}` ==倒序==到 0：保证这个工作只被选一次',
        'if j + w >= minProfit': '`j + w = {j} + {w} = {j + w}`，{"≥" if j + w >= minProfit else "<"} `minProfit = {minProfit}`：{"利润够了，==封顶==记到第 " + str(minProfit) + " 列" if j + w >= minProfit else "利润还不够，记到第 " + str(j + w) + " 列"}',
        'f[i + cost][minProfit] =': '`f[{i + cost}][{minProfit}]` += `f[{i}][{j}]`({B.f[i][j]}) → =={f[i + cost][minProfit]}==（选了这个工作）',
        'f[i + cost][j + w] =': '`f[{i + cost}][{j + w}]` += `f[{i}][{j}]`({B.f[i][j]}) → =={f[i + cost][j + w]}==（选了这个工作）',
        'for i in range(n + 1)': lambda S, B, r: ('`i` 枚举完了，累加结束' if B.get('i') == S.i and S.i == S.n else f'人数恰好 `{S.i}` 的方案：`f[{S.i}][{S.minProfit}]` = {S.f[S.i][-1]}'),
        'res = (res': '`res` += `f[{i}][-1]` → =={res}==',
        'return res': '利润 ≥ {minProfit} 且人数 ≤ {n} 的方案共 `{res}` 种',
    },
    cards=dict(
        one_liner='二维费用背包：人数是容量，利润封顶在 minProfit',
        complexity='时间 `O(len·n·minProfit)`，空间 `O(n·minProfit)`',
        problem=['`n` 个成员，每个工作要 `group[k]` 人、产生 `profit[k]` 利润',
                 '一个成员只能做一个工作；求利润 ==至少 minProfit==、总人数 ≤ n 的方案数（模 1e9+7）',
                 '本视频：`n=3, minProfit=2, group=[2,1], profit=[2,1]` → `2`'],
        quote='这里收益的上限为minProfit，因此状态转移时需要对此进行讨论。注意到这里的状态转移只与上一轮的状态有关，因此可以省去k这一维。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[k][i][j]`：前 `k` 个工作、恰好用 `i` 个人、利润 `j` 的方案数',
              '不选这个工作：沿用上一轮；选：人数 `+group`、利润 `+profit`',
              '利润超过 `minProfit` 就==封顶==记到最后一列；省掉 `k` 维后 `i`、`j` 要倒序'],
        summary=['时间 `O(len·n·minProfit)`，空间 `O(n·minProfit)`',
                 '`i` 必须倒序（0-1 背包）；`j` 也倒序，防止同一状态被连续写入后又读出',
                 '利润要封顶：`j + w >= minProfit` 时统一记到 `minProfit`',
                 '答案累加最后一列 `f[i][-1]`，每次都要取模',
                 '`f[0][0] = 1`：不选任何工作也算利润 0 的一种方案，`minProfit = 0` 时要用到'],
    ),
)
