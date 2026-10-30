NUMS = [3, 5, 2]
K = 2


def _rows(S):
    n = len(NUMS)
    return [f'{s:0{n}b}' for s in range(1 << n)]


def _color(S, i, j, v):
    st, x = S.get('state'), S.get('x')
    if st is not None and i == st and j == x:
        return 'yellow'
    nst, nx = S.get('nxt_state'), S.get('nxt_x')
    if S.get('_line') in (27, 28, 29) and nst is not None and i == nst and j == nx:
        return 'green'
    return None


def _txt(S):
    if 'state' not in S:
        return '`f[state][x]`：用了 state 里的数、拼接后模 k 余 x，是否可达（1 = 可达）'
    n = len(S['nums'])
    st = S['state']
    used = [S['nums'][j] for j in range(n) if st >> j & 1]
    return f'`state = {st:0{n}b}`（用了 {used}），拼接数长度 `length = {S["length"][st]}`，余数 `x = {S["x"]}`'


CONFIG = dict(
    num=3533, title='判断连接可整除性', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状压 DP · 数字拼在前方 + 倒推构造',
    tags=['灵神题单', '动态规划', '难度分 2257'],
    code='''
class Solution(object):
    def concatenatedDivisibility(self, nums, k):
        
        tot_length = 0
        str_nums = []
        nums.sort()
        for v in nums:
            str_nums.append(str(v))
            tot_length += len(str(v))

        r = [1 % k]
        for index in range(1, tot_length):
            r.append(r[-1] * 10 % k)
        
        n = len(nums)
        tot_state = (1 << n)
        f = [[False] * k for _ in range(tot_state)]
        use = [[None] * k for _ in range(tot_state)]
        pre = [[None] * k for _ in range(tot_state)]

        length = [None] * tot_state
        f[0][0] = True
        length[0] = 0

        for state in range(tot_state):
            for x in range(k):
                if f[state][x]:
                    for index in range(n):
                        if state & (1 << index) == 0:
                            nxt_state = state | (1 << index)
                            if length[nxt_state] is None:
                                length[nxt_state] = length[state] + len(str_nums[index])
                            
                            nxt_x = (x + r[length[state]] * nums[index]) % k
                            f[nxt_state][nxt_x] = True
                            use[nxt_state][nxt_x] = nums[index]
                            pre[nxt_state][nxt_x] = (state, x)
        
        if not f[-1][0]:
            return []
        
        res = []
        state, x = tot_state - 1, 0
        while state:
            res.append(use[state][x])
            state, x = pre[state][x]
        return res
''',
    call=f'Solution().concatenatedDivisibility({NUMS!r}, {K})',
    expect=[3, 5, 2],
    views=[
        dict(type='text', fn=_txt, h=80),
        dict(type='array', var='nums', label='nums（排序后）', cell=70, h=200,
             pointers={'index': 'pink'}),
        dict(type='table', var='[[int(b) for b in row] for row in f]', label='f[state][x]（黄 = 当前，绿 = 新标记）',
             h=470, cell=110, rows=_rows, cols=lambda S: [f'x={c}' for c in range(K)], color=_color),
    ],
    watch=['state', 'x', 'index', 'nxt_state', 'nxt_x', 'res'],
    skip=['tot_length = 0', 'str_nums = []', 'str_nums.append', 'tot_length +=', 'for v in nums', 'for index in range(1', 'r.append',
          'use = ', 'pre = ', 'length = [None]', 'for x in range(k)', 'for index in range(n)',
          'use[nxt_state]', 'nxt_state = state', 'pre[nxt_state]', 'if length[nxt_state]', 'n = len(nums)', 'tot_state = (1', 'length[0] = 0'],
    captions={
        'nums.sort()': '==先排序==：后面更靠前的元素拼在前方，字典序才会更小',
        'r = [1 % k]': '预处理 `r[i] = 10^i mod k`：拼在前方等于加上 `nums[index] × 10^length`，余数用 `r` 查表，`r = {r}`',
        'f = [[False]': '`f[state][x]`：用了 `state` 里的数、拼成的整数模 `k` 余 `x` 能否做到；另有 `use/pre` 记来路',
        'f[0][0] = True': '什么都没拼：余数 0 可达，`f[0][0] = True`',
        'for state in range': '按 `state` 从小到大枚举（`state = {state:0{n}b}`），保证前置状态先算完',
        'if f[state][x]:': lambda S, B, r: (
            f'`f[{S.state}][{S.x}]` 可达 → 尝试在==前方==再拼一个没用过的数' if S.f[S.state][S.x]
            else f'`f[{S.state}][{S.x}]` 不可达，跳过'),
        'if state & (1 << index) == 0': lambda S, B, r: (
            f'`nums[{B.index}] = {B.nums[B.index]}` 还没用（`state` 第 {B.index} 位是 0）→ 拼在前方，新状态 `{B.state | 1 << B.index:0{len(B.nums)}b}`' if not B.state >> B.index & 1
            else f'`nums[{B.index}] = {B.nums[B.index]}` 已在 `state` 里，跳过'),
        'length[nxt_state] = ': '`{nxt_state:0{n}b}` 第一次出现：位数 = 前置位数 + `len(str(nums[{index}]))` = `{length[nxt_state]}`（同一 state 位数固定）',
        'nxt_x = ': '前方拼 `nums[{index}]` = 加 `{nums[index]} × 10^{length[state]}`，查表 `r[{length[state]}] = {r[length[state]]}` → `nxt_x = ({B.x} + {r[length[state]]}×{nums[index]}) % {k}` = =={nxt_x}==',
        'f[nxt_state][nxt_x] = True': '`f[{nxt_state}][{nxt_x}]` 标记可达（后写入的是更大的前置状态，覆盖 `use/pre`）：来路 `state={state}, x={x}`',
        'if not f[-1][0]': lambda S, B, r: ('全部数都用了且余数 0 可达 → 有解，开始倒推' if S.f[-1][0] else '全用完余数 0 不可达 → 返回空列表'),
        'res = []': '倒推：从 `f[全集][0]` 沿 `pre` 走回去，沿途的 `use` 就是答案',
        'state, x = tot_state - 1, 0': '从终点出发：`state = {state:0{n}b}`，`x = 0`',
        'while state': lambda S, B, r: ('`state != 0`，继续回溯' if S.state else '`state = 0` 回到起点，倒推完成'),
        'res.append(use[state][x])': '`use[{state}][{x}]` = ==`{use[state][x]}`==，排列的下一个数（拼在前方，倒推顺序正好是正序）',
        'state, x = pre[state][x]': '跳到前置状态：`state = {state:0{n}b}`，`x = {x}`',
        'return res': '返回字典序最小的可整除排列 `{res}`',
    },
    max_steps=40,
    cards=dict(
        one_liner='状压 DP：数字拼在前方，余数和位数都能查表算出',
        complexity='时间 `O(2^n · k · n)`，空间 `O(2^n · k)`',
        problem=['给正整数数组 `nums`（最多 13 个）和 `k`，重排后依次拼接成整数，要求能被 `k` 整除',
                 '要求这个排列的==字典序==最小，不是拼出的整数最小',
                 '无解返回 `[]`；本视频：`[3,5,2], k=2` → `[3,5,2]`（352 为偶数）'],
        quote='需要特别注意，本题中是排列的字典序最小，而不是按顺序连接后形成的整数字典序最小。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[state][x]`：用了 `state` 里的数，拼出整数模 `k` 余 `x` 是否可达',
              '新数拼在==前方==：`state` 里的数位数固定，加 `nums[index] × 10^length` 即可，`10^i mod k` 预处理成 `r`',
              '`nums` 先排序，`state` 从小到大枚举，后覆盖的前置状态更大 → 前面的数更小，用 `use/pre` 倒推出答案'],
        summary=['时间 `O(2^n · k · n)`，空间 `O(2^n · k)`（`f/use/pre` 三张表）',
                 '拼在前方是为了位数好算：`length[state]` 对每个 `state` 是固定值',
                 '`nums.sort()` 不能少：字典序最小靠「排序 + 取最大前置状态」',
                 '无解时 `f[-1][0]` 为 False，返回 `[]`',
                 '原文为 Python 2 风格写法，Python 3 下可直接运行，未改动'],
    ),
)
