NUMS = [2, 3, 6]
N = len(NUMS)


def _live(S):
    return S.get('_line', 0) in range(10, 18) and S.get('state') is not None and S.get('last') is not None


def _cell(S, r, c, v):
    if not _live(S):
        return None
    state, last = S['state'], S['last']
    if r == state and c == last:
        return 'yellow'
    pl = S.get('pre_last')
    if S.get('_line', 0) in (16, 17) and pl is not None and (r, c) == (S.get('pre_state'), pl):
        return 'green'
    return None


def _formula(S):
    if not _live(S) or S.get('pre_state') is None:
        return '`f[state][last]` = 用 state 中的点、最后一个点是 last 的哈密顿路径数'
    st, la, ps = S['state'], S['last'], S['pre_state']
    if ps == 0:
        return f'`state={st:0{N}b}` 只有 `last={la}` 一个点 → 路径只有 1 条'
    return f'`pre_state = {st:0{N}b} ^ (1<<{la}) = {ps:0{N}b}`：去掉末尾点 {NUMS[la]}，前面是 `pre_state` 的路径'


def _cap_cond(S, B, ret):
    la, pl = S.last, S.pre_last
    if not (S.pre_state >> pl & 1):
        return f'点 {pl} 不在 `pre_state` 里，不能当倒数第二个点'
    a, b = NUMS[la], NUMS[pl]
    if a % b == 0 or b % a == 0:
        return f'`{a}` 与 `{b}` 互为倍数 → 图里有边，路径可以接上'
    return f'`{a}` 与 `{b}` 互不整除 → 没有边，不能接'


CONFIG = dict(
    num=2741, title='特别的排列', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='哈密顿路径计数（状压 DP）',
    tags=['灵神题单·动态规划', '难度分 2021'],
    code='''
class Solution(object):
    def specialPerm(self, nums):

        n = len(nums)
        max_state = 1 << n
        f = [[0] * n for _ in range(max_state)]
        mod = 10 ** 9 + 7
        for state in range(1, max_state):
            for last in range(n):
                if state & (1 << last) == (1 << last):
                    pre_state = state ^ (1 << last)
                    if pre_state == 0:
                        f[state][last] = 1
                    else:
                        for pre_last in range(n):
                            if pre_state & (1 << pre_last) == (1 << pre_last) and (nums[last] % nums[pre_last] == 0 or nums[pre_last] % nums[last] == 0):
                                f[state][last] += f[pre_state][pre_last]
                                if f[state][last] >= mod:
                                    f[state][last] -= mod

        return sum(f[-1]) % mod
''',
    call=f'Solution().specialPerm({NUMS})',
    expect=2,
    skip=['for pre_last in range', 'for last in range', 'mod = 10', 'pre_state = state ^', 'max_state = 1', 'f = [[0] * n', 'if f[state][last] >= mod', 'f[state][last] -= mod'],
    max_steps=62,
    views=[
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='array', var='nums', label='nums（点 = 下标，倍数关系 = 边）', h=280, cell=90,
             pointers={'last': 'blue', 'pre_last': 'pink'}),
        dict(type='table', var='f', label='f[state][last]（黄 = 正在算，绿 = 从它转移过来）', h=400, cell=70,
             rows=lambda S: [f'{k:0{N}b}' for k in range(2 ** N)], cols=lambda S: [f'{k}' for k in range(N)],
             color=_cell),
    ],
    watch=[('state', 'state', 'yellow'), ('last', 'last', 'blue'), ('pre_state', 'pre_state', 'purple'), ('pre_last', 'pre_last', 'pink')],
    captions={
        'n = len(nums)': '`n = {n}`，点的个数',
        'for state in range': lambda S, B, r: (f'枚举点集 `state = {S.state:0{S.n}b}`（1 表示这个点在路径里）'
                                               if S.get('state') != B.get('state') else '所有点集都算完了'),
        'if state & (1 << last)': lambda S, B, r: (f'`last = {S.last}` 在 `state` 中 → 它可以做路径的最后一个点' if S.state >> S.last & 1
                                                   else f'`last = {S.last}` 不在 `state` 中，不能当末尾，跳过'),
        'if pre_state == 0': lambda S, B, r: (f'`pre_state = {S.state:0{S.n}b} ^ (1<<{S.last}) = {S.pre_state:0{S.n}b}` 是去掉末尾点后的点集；'
                                              + ('为空 → 路径只有 `last` 一个点' if S.pre_state == 0 else '非空 → 枚举倒数第二个点 `pre_last`')),
        'f[state][last] = 1': '单点路径只有 1 条：`f[{state:0{n}b}][{last}] = 1`',
        'pre_state & (1 << pre_last)': _cap_cond,
        'f[state][last] += f[pre_state][pre_last]': '把 `f[{pre_state:0{n}b}][{pre_last}]` 加进来：`f[{state:0{n}b}][{last}]` = =={f[state][last]}==',
        'return sum(f[-1])': '全集那一行 `f[111]` 累加：每个终点的路径数之和 = =={ret}==',
    },
    cards=dict(
        one_liner='倍数关系建图，数哈密顿路径',
        complexity='时间 `O(n^2 · 2^n)`，空间 `O(n · 2^n)`',
        problem=['`nums` 里 `n` 个互不相同的正整数，排列相邻两数要==一个整除另一个==',
                 '返回满足条件的排列个数，对 `10^9 + 7` 取模',
                 '示例：`nums = [2,3,6]` → `2`'],
        quote='如果将数组中的数视为图中的点，那么对于互为倍数关系的两个点，就可以在图中建立一条无向边，此时问题就变成了问图中哈密顿路径的数目。',
        quote_src='—— yiduobo 题解',
        idea=['`f[state][last]`：路径恰好经过 `state` 里的点，终点是 `last`',
              '先算 `pre_state = state ^ (1<<last)`；为空就只有 1 条路径',
              '否则枚举倒数第二个点 `pre_last`，满足倍数关系就累加 `f[pre_state][pre_last]`'],
        summary=['时间 `O(n^2 2^n)`：`2^n` 个点集 × `n` 个终点 × `n` 个前驱',
                 '这里是==往前看==：由「去掉末尾」的旧状态推出当前状态',
                 '易错：`pre_last` 必须在 `pre_state` 中；累加时随时取模',
                 '最后 `sum(f[-1])` 是全集那一行的所有终点之和'],
    ),
)
