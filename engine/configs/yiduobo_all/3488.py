NUMS = [1, 3, 1, 4, 1, 3, 2]
QS = [0, 3, 5]


def _color(S, i, v):
    ln = S['_line']
    if 'p' in S and 16 <= ln <= 18 and 'index' in S and S['_inner'].get('p') is not None:
        if i == S['p']:
            return 'yellow'
    if ln >= 21 and 'q' in S:
        if i == S['q']:
            return 'yellow'
        if S['pre'][S['q']] == i or S['nxt'][S['q']] == i:
            return 'blue'
    return None


def _fmt_arr(a):
    return ['·' if x is None else x for x in a]


def _top(S):
    ln = S['_line']
    if ln >= 21 and 'q' in S:
        q, n = S['q'], len(NUMS)
        a, b = S['pre'][q], S['nxt'][q]
        if a == q:
            return f'查询 `q = {q}`：`pre[{q}] = {q}`，自己就是自己的上一个 → ==只出现一次=='
        return f'查询 `q = {q}`：往左到 `pre = {a}` 距离 `{(q + n - a) % n}`，往右到 `nxt = {b}` 距离 `{(b + n - q) % n}`'
    if 16 <= ln <= 18 and 'v' in S and S['_inner'].get('m') is not None:
        return f'值 `{S["v"]}` 的下标列表 `{S["pos_dict"][S["v"]]}`：==循环==地取前一个和后一个'
    return '`pos_dict[v]`：值 `v` 出现过的所有下标（遍历得到，天然递增）'


def _if(S, B, ret):
    q = S.q
    if S.pre[q] == q:
        return f'`pre[{q}] == {q}`：数组里只有这一个 `nums[{q}] = {S.nums[q]}` → 结果 -1'
    return f'`pre[{q}] = {S.pre[q]} ≠ {q}`：还有别的相同值 → 算两边距离'


CONFIG = dict(
    num=3488, title='距离最小相等元素查询', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='哈希表收集下标 · 预处理前驱后继',
    tags=['灵神核心路线', '灵神题单·二分算法'],
    code='''
class Solution(object):
    def solveQueries(self, nums, queries):
        
        pos_dict = {}
        for index, v in enumerate(nums):
            if v not in pos_dict:
                pos_dict[v] = []
            pos_dict[v].append(index)
        
        n = len(nums)
        pre = [None] * n
        nxt = [None] * n

        for v in pos_dict:
            m = len(pos_dict[v])
            for index, p in enumerate(pos_dict[v]):
                pre[p] = pos_dict[v][(index - 1 + m) % m]
                nxt[p] = pos_dict[v][(index + 1) % m]

        res = []
        for q in queries:
            if pre[q] == q:
                res.append(-1)
            else:
                res.append(min((q + n - pre[q]) % n, (nxt[q] + n - q) % n))
        
        return res
''',
    call=f'Solution().solveQueries({NUMS}, {QS})',
    expect=[2, -1, 3],
    views=[
        dict(type='text', fn=_top, size=26, h=70),
        dict(type='array', var='nums', label='nums（环形；黄 = 当前位置，蓝 = 它的上一个 / 下一个相同值）', cell=72,
             color=_color, h=160),
        dict(type='map', var='pos_dict', label='pos_dict：值 → 出现的下标列表',
             fmt=lambda k, v: f'{k}: {v}', h=140, font=28),
        dict(type='array', var=lambda S: _fmt_arr(S['pre']) if 'pre' in S else None, label='pre[p]：上一次出现的下标（循环）',
             cell=72, h=150),
        dict(type='array', var=lambda S: _fmt_arr(S['nxt']) if 'nxt' in S else None, label='nxt[p]：下一次出现的下标（循环）',
             cell=72, h=150),
        dict(type='array', var='res', label='res', cell=72, index=False, h=120),
    ],
    watch=['n', ('v', 'v', 'cyan'), 'm', ('p', 'p', 'yellow'), ('q', 'q', 'yellow')],
    skip=['if v not in pos_dict', 'pos_dict[v] = []', 'res = []'],
    max_steps=60,
    captions={
        'pos_dict = {}': '用哈希表把每个值出现的所有下标收集起来',
        'pos_dict[v].append(index)': '`nums[{index}] = {v}` → `pos_dict[{v}] = {pos_dict[v]}`',
        'n = len': '`n = {n}`',
        'pre = [None]': '`pre`、`nxt`：每个位置的相同值上一次 / 下一次出现在哪',
        'for v in pos_dict:': lambda S, B, r: (f'处理值 `{S.v}`：下标列表 `{S.pos_dict[S.v]}`' if S._line == 14 and 'v' in S and S.get('v') != B.get('v') else '所有值处理完毕'),
        'm = len': '`m = {m}` 个位置',
        'pre[p] = pos_dict': lambda S, B, r: (f'`pre[{S.p}]`：列表里前一个，下标 `({S.index} − 1 + {S.m}) % {S.m}` → =={S.pre[S.p]}==' + ('（只有一个，前一个就是自己）' if S.m == 1 else '（第一个就绕到最后一个）' if S.index == 0 else '')),
        'nxt[p] = pos_dict': lambda S, B, r: (f'`nxt[{S.p}]`：列表里后一个，下标 `({S.index} + 1) % {S.m}` → =={S.nxt[S.p]}==' + ('' if S.m == 1 else '（最后一个就绕回第一个）' if S.index == S.m - 1 else '')),
        'if pre[q] == q': _if,
        'res.append(-1)': '`res` 加入 -1',
        'res.append(min': lambda S, B, r: f'距离取 `min(({S.q}+{S.n}−{S.pre[S.q]})%{S.n}, ({S.nxt[S.q]}+{S.n}−{S.q})%{S.n})` = =={S.res[-1]}==',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='最近的相同值，只可能是它上一次或下一次出现的位置',
        complexity='时间 `O(n + q)`，空间 `O(n)`',
        problem=['环形数组 `nums`，每个查询给一个下标 `q`',
                 '求与 `nums[q]` 相等的==其他==下标到 `q` 的最小环形距离，没有则 -1',
                 '示例：`nums = [1,3,1,4,1,3,2], queries = [0,3,5]` → `[2,-1,3]`'],
        quote='与其相等且距离index最近的p的必然是nums[index]这个数值在nums中==上一次出现或者下一次出现的位置==这二者之一',
        quote_src='—— yiduobo 题解原文',
        idea=['先用 `pos_dict` 收集每个值的下标列表，天然单调递增',
              '列表里第 `index` 个的前驱 / 后继：`(index − 1 + m) % m`、`(index + 1) % m`',
              '查询时 `pre[q] == q` 说明只出现一次；否则距离用 `% n` 处理绕圈'],
        summary=['时间 `O(n + q)`，空间 `O(n)`：没有用到二分，直接预处理前驱后继',
                 '取模让列表首尾相接，`m = 1` 时前驱后继都是自己，正好用来判 -1',
                 '距离 `(q + n − pre[q]) % n` 和 `(nxt[q] + n − q) % n` 统一处理了绕圈',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行'],
    ),
)
