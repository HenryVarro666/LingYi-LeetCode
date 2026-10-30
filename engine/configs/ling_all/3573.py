P0 = [1, 7, 6, 2]
K0 = 2
NEG = float('-inf')


def _idx(S):
    return S['prices'].index(S['p']) if 'p' in S and S.get('p') in S['prices'] else -1


def _cell(S, r, c, v):
    j = S.get('j')
    if j is None or S.get('_line') not in (8, 9, 10):
        return None
    cur = {8: 0, 9: 1, 10: 2}[S['_line']]
    if (r, c) == (j, cur):
        return 'yellow'
    src = {8: [(j, 1), (j, 2)], 9: [(j - 1, 0)], 10: [(j - 1, 0)]}[S['_line']]
    if (r, c) in src or (S['_line'] == 8 and (r, c) == (j, 0)):
        return 'blue'
    return None


def _txt(S):
    j = S.get('j')
    ln = S.get('_line')
    if j is None or ln not in (8, 9, 10):
        return '`f[j][0]` 未持有　`f[j][1]` 持有（普通交易中）　`f[j][2]` 做空中；`j` = 已用交易笔数 + 1'
    p = S['p']
    f = S['f']
    if ln == 8:
        return f'未持有：不动 / 卖出 `f[{j}][1]+{p}` / 买回 `f[{j}][2]-{p}` → =={f[j][0]}=='
    if ln == 9:
        return f'持有：不动 / 买入 `f[{j-1}][0]-{p}` → =={f[j][1]}=='
    return f'做空中：不动 / 开空 `f[{j-1}][0]+{p}` → =={f[j][2]}=='


CONFIG = dict(
    num=3573, title='买卖股票的最佳时机 V', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='状态机 DP（三状态，空间优化）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1777'],
    code='''
class Solution:
    def maximumProfit(self, prices: List[int], k: int) -> int:
        f = [[-inf] * 3 for _ in range(k + 2)]
        for j in range(1, k + 2):
            f[j][0] = 0
        for p in prices:
            for j in range(k + 1, 0, -1):
                f[j][0] = max(f[j][0], f[j][1] + p, f[j][2] - p)
                f[j][1] = max(f[j][1], f[j - 1][0] - p)
                f[j][2] = max(f[j][2], f[j - 1][0] + p)
        return f[-1][0]
''',
    call=f'Solution().maximumProfit({P0}, {K0})',
    expect=10,
    skip=['range(k + 1'],
    max_steps=80,
    views=[
        dict(type='array', var='prices', label='prices（蓝 = 今天）', h=170, cell=80,
             color=lambda S, i, v: 'blue' if i == _idx(S) else None,
             dim=lambda S, i, v: _idx(S) >= 0 and i < _idx(S)),
        dict(type='text', fn=_txt, size=24, h=80),
        dict(type='table', var='f', label='f[j][状态]', h=340, cell=64,
             rows=lambda S: [f'j={r}' for r in range(len(S['f']))], cols=['未持有', '持有', '做空'],
             color=_cell),
    ],
    watch=[('j', 'j', 'blue'), 'p', ('f[-1][0]', 'f[-1][0]', 'green')],
    captions={
        'f = [[-inf]': '`f[j][s]`：至多 `j-1` 笔交易、当天结束处于状态 `s`（0 未持有 / 1 持有 / 2 做空）；一开始全是 ==-∞==',
        'f[j][0] = 0': '`f[{j}][0] = 0`：还没开始交易，未持有收益 0',
        'for p in prices': lambda S, B, r: ('所有天都处理完了' if 'p' in B and B['p'] == S['p'] else f"第 `{S['prices'].index(S['p'])}` 天，价格 `p = {S['p']}`；`j` 从大到小，保证用到的是昨天的 `f[j-1]`"),
        'f[j][0] = max': '==未持有==：保持 `{B.f[j][0]}`，卖出多头 `{f[j][1]} + {p}`，或买回空头 `{f[j][2]} - {p}`（平仓完成一笔）→ =={f[j][0]}==',
        'f[j][1] = max': '==持有==：保持 `{B.f[j][1]}`，或用 `f[{j-1}][0] = {f[j-1][0]}` 买入 `-{p}`（开多）→ =={f[j][1]}==',
        'f[j][2] = max': '==做空中==：保持 `{B.f[j][2]}`，或用 `f[{j-1}][0] = {f[j-1][0]}` 卖出 `+{p}`（开空）→ =={f[j][2]}==',
        'return f[-1][0]': '最后必须平仓，答案 `f[-1][0]` = =={ret}==',
    },
    cards=dict(
        one_liner='在 188 题的基础上，加一个「做空中」状态',
        complexity='时间 `O(nk)`，空间 `O(k)`',
        problem=['`prices[i]` 是第 `i` 天股价，最多做 `k` 笔交易',
                 '普通交易：先买后卖；做空交易：先卖后买回',
                 '每笔交易结束前不能开始下一笔，同一天不能买卖两次',
                 '示例：`prices=[1,7,6,2], k=2` → `10`'],
        quote='本题可以做空交易，也就是可以先加再减（普通交易是先减再加）。我们需要额外增加一类状态：dfs(i,j,2) 表示……第 i 天结束时处于做空中（空头状态）的最大利润。',
        quote_src='—— 灵茶山艾府题解',
        idea=['三个状态：未持有 / 持有 / 做空中',
              '开多 `f[j-1][0] - p`，开空 `f[j-1][0] + p`；平仓（卖出或买回）回到未持有',
              '一笔交易在「开仓」时就算一笔，所以用 `j-1` 转移；`j` 倒序遍历省掉天数这一维'],
        after=[dict(heading='另外两种写法', lines=['题解先写 `@cache` 记忆化搜索 `dfs(i, j, end_state)`',
                                                   '再 1:1 翻译成三维递推，最后滚动成现在的二维数组'])],
        summary=['时间 `O(nk)`，空间 `O(k)`',
                 '易错：`j` 必须倒序，否则 `f[j-1][0]` 已经是今天的值',
                 '易错：中间收益可能为负，初值要用 `-inf`，不能用 0 或 -1',
                 '同类：188 买卖股票 IV、123 买卖股票 III'],
    ),
)
