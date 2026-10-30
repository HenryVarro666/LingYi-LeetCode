GAS, COST = [3, 1, 1, 4, 1], [1, 2, 4, 1, 2]
N = len(GAS)


def _color(S, i, v):
    if 'p' not in S or 'index' not in S or not isinstance(S.get('index'), int):
        return None
    if i < S['p']:
        return None
    if S['p'] <= i <= S['index']:
        return 'red' if S.get('sum', 0) < 0 else 'cyan'
    return None


def _dim(S, i, v):
    if 'p' not in S:
        return False
    return i < S['p']


def _win_text(S):
    if 'p' not in S or 'index' not in S or 'sum' not in S:
        return ''
    p, idx, sm = S['p'], S['index'], S['sum']
    if p > idx:
        return f'起点重新假设为 `p = {p}`，油箱清零'
    seg = ' + '.join(f'({x})' if x < 0 else str(x) for x in S['rest'][p:idx + 1])
    return f'`rest[{p}..{idx}]` = {seg} = =={sm}==，已走 `{idx - p + 1}` 站（目标 `{N}` 站）'


def _if(S, B, ret):
    if S.sum < 0:
        if S.index > S.p:
            mids = '、'.join(str(k) for k in range(S.p + 1, S.index + 1))
            return (f'`sum = {S.sum} < 0`：从 `{S.p}` 出发跨不过 `{S.index}`；'
                    f'从 {mids} 出发==只会更差==，也都排除')
        return f'`sum = {S.sum} < 0`：从 `{S.p}` 出发连这一站都过不去 → 排除'
    if S.index == S.p:
        return f'`sum = {S.sum} ≥ 0`：从 `p = {S.p}` 出发，第一站没问题'
    return f'`sum = {S.sum} ≥ 0`：从 `p = {S.p}` 出发目前还符合条件'


def _elif(S, B, ret):
    k = S.index - S.p + 1
    if k == N:
        return f'`index − p + 1 = {k} == len(gas)`：已经连续走完一整圈'
    return f'`index − p + 1 = {k}`，还没到 `{N}` 站，继续验证'


CONFIG = dict(
    num=134, title='加油站', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='复制一遍拆环 · 子段和 < 0 就跳过整段',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def canCompleteCircuit(self, gas, cost):
        if not gas:
            return -1

        rest = [gas[index] - cost[index] for index in range(len(gas))]
        rest.extend(rest)

        p = 0
        sum = 0
        for index, r in enumerate(rest):
            sum += r
            if sum < 0:
                p = index + 1
                sum = 0
            elif index - p + 1 == len(gas):
                return p

        return -1
''',
    call=f'Solution().canCompleteCircuit({GAS}, {COST})',
    expect=3,
    skip=['if not gas'],
    views=[
        dict(type='text', fn=_win_text, h=60),
        dict(type='array', var='rest', h=300, cell=90, window=('p', 'index'),
             pointers={'p': 'pink', 'index': 'blue'}, color=_color, dim=_dim,
             label='rest（青 = 正在验证的子段，红 = 子段和 < 0，暗 = 已排除的起点）'),
        dict(type='custom', h=90, draw=lambda cv, S, B, box, T: (
            cv.text((box[0] + 18, box[1] + 10), f'下标 {N}..{2 * N - 1} 是复制出来的：下标 i 就是 i mod {N} 号站（绕回环的开头）', 22, T['muted'])
            if 'rest' in S and len(S['rest']) == 2 * N else None)),
    ],
    watch=[('p', 'p', 'pink'), ('index', 'index', 'blue'), 'r', ('sum', 'sum', 'yellow')],
    captions={
        'rest = [': '`rest[i] = gas[i] − cost[i]`：经过 `i` 号站之后油量的变化 `{rest}`',
        'rest.extend(rest)': '处理环状问题的经典做法：==原样复制一遍接在后面==，变成线性问题',
        'p = 0': '先假设起点 `p = 0`，逐个往后验证',
        10: '`sum`：从 `p` 出发、到当前站为止的子段和（油箱里的油）',
        'for index, r in': lambda S, B, r: (f'验证到 `index = {S.index}`：`r = rest[{S.index}] = {S.r}`'
                                             if 'index' not in B or B.index != S.index else '扫描结束'),
        'sum += r': '`sum += {r}` → `{sum}`',
        'if sum < 0': _if,
        'p = index + 1': '所以重新假设起点 `p = index + 1 = {p}`',
        15: '油箱清零：`sum = 0`',
        'elif index - p + 1': _elif,
        'return p': '从 `p = {p}` 出发长度 1 到 `len(gas)` 的子段和都 ≥ 0 → 返回 =={ret}==',
        'return -1': '一趟扫描都没找到 `p` → 无解，返回 `-1`',
    },
    cards=dict(
        one_liner='环接成两倍长的链；子段和一旦 < 0，整段都不能当起点',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['环路上 `n` 个加油站：在 `i` 站加油 `gas[i]`，开到 `i+1` 站耗油 `cost[i]`',
                 '油箱起始为空；能绕一圈就返回出发站编号（唯一），否则返回 `-1`',
                 '示例：`gas = [1,2,3,4,5], cost = [3,4,5,1,2]` → `3`',
                 '本视频：`gas = [3,1,1,4,1], cost = [1,2,4,1,2]` → `3`'],
        quote='从k开始的子段和一定也跨不过index这个点，这说明==从p开始到index在内的所有点都不能成为起始点==，于是重新假设p = index + 1。',
        quote_src='—— yiduobo 题解',
        idea=['`rest = gas − cost` 复制一遍；找 `p`：从 `p` 起长度 1..n 的子段和都 ≥ 0',
              '中间点 `k` 的前缀 `rest[p..k-1]` ≥ 0，去掉它只会让 `rest[k..index]` ==更小==',
              '所以 `p..index` 全部排除，直接从 `index + 1` 重新开始，一趟扫描'],
        result='返回 `3`：从 3 号站出发能绕一圈 ✓',
        summary=['时间 `O(n)`：复制后长度 `2n`，`p` 和 `index` 都只往前走；空间 `O(n)` 存 `rest`',
                 '易错：排除时 `p` 跳到 `index + 1`，不是 `p + 1`',
                 '变量名 `sum` 遮住了内置函数，自己写时建议换个名字',
                 '对比灵神：灵神找油量折线的最低点，`O(1)` 空间、不用复制数组',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
