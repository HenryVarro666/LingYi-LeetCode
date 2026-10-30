def _m(x, m=2):
    return format(x, f'0{m}b')


def _fv(v):
    return '无' if v is None else str(v)


def _info(S):
    if 'sub_state' in S and S.get('sub_state') and 'state' in S and 'v' in S and 'cost' in S:
        st, ss = S['state'], S['sub_state']
        return (f"state=`{st:02b}`：让 `{S['v']}` 负责 `{ss:02b}`（变成 `{S['lcm'][ss]}` 的倍数，要 `{S['cost'] if S['_line'] >= 0 else ''}` 次），"
                f"余下 `{st ^ ss:02b}` 靠前面的数：`g[{st ^ ss:02b}]` = {_fv(S['g'][st ^ ss])}")
    return '`f[state]`：覆盖 state 里的 target 元素最少要几次操作（位 i = target[i]，「无」= 做不到）'


CONFIG = dict(
    num=3444, title='使数组包含目标值倍数的最少增量', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状压 DP · 滚动数组',
    tags=['灵神题单·动态规划', '难度分 2337'],
    code='''
class Solution(object):
    def minimumIncrements(self, nums, target):
        
        n = len(nums)
        m = len(target)
        max_state = (1 << m)
        lcm = [0] * max_state
        lcm[0] = 1

        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        for state in range(1, max_state):
            for index, v in enumerate(target):
                if state & (1 << index) == (1 << index):
                    pre_state = state ^ (1 << index)
                    lcm[state] = lcm[pre_state] * v // gcd(lcm[pre_state], v)
                    break

        f = [None] * max_state
        f[0] = 0
        for v in nums:
            g = f[:]
            f = [None] * max_state
            f[0] = 0
            for state in range(max_state):
                if g[state] is not None:
                    f[state] = g[state]
                sub_state = state
                while sub_state:
                    cost = v % lcm[sub_state]
                    if cost != 0:
                        cost = lcm[sub_state] - cost

                    if g[state ^ sub_state] is not None:
                        cost += g[state ^ sub_state]
                        if f[state] is None or f[state] > cost:
                            f[state] = cost

                    sub_state = (sub_state - 1) & state

        return f[-1]
''',
    call='Solution().minimumIncrements([7,5], [4,6])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums', h=140, cell=70,
             color=lambda S, i, v: 'yellow' if 'v' in S and v == S['v'] and i == S['nums'].index(S['v']) else None),
        dict(type='array', var='lcm', label='lcm[state]：target 子集的最小公倍数', h=160, cell=80,
             color=lambda S, i, v: 'yellow' if i == S.get('sub_state') and S.get('sub_state') else None),
        dict(type='array', var='g', label='g：上一轮的 f（• = None 做不到）', h=160, cell=80,
             fmt=lambda v: '无' if v is None else str(v)),
        dict(type='array', var='f', label='f[state]：最少操作次数（• = None 做不到）', h=160, cell=80,
             fmt=lambda v: '无' if v is None else str(v),
             color=lambda S, i, v: 'yellow' if i == S.get('state') and 'g' in S else None),
        dict(type='text', size=27, fn=_info, h=100),
    ],
    watch=[('v', 'v', 'pink'), ('state', "format(state, '02b')", 'yellow'), ('sub_state', "format(sub_state, '02b')", 'cyan'), ('cost', 'cost', 'orange')],
    captions={
        'n = len(nums)': '`target` 很短（`m ≤ 4`），用二进制 `state` 表示「已经覆盖了 target 的哪些元素」',
        'm = len(target)': '`m = {m}`，所以 `state` 有 `{1 << m}` 种',
        'max_state = ': '`max_state = {max_state}`，状态 `0 ~ {max_state - 1}`',
        'lcm = [0]': '`lcm[state]`：把 `state` 里所有 target 元素的最小公倍数存起来',
        'lcm[0] = 1': '空集的最小公倍数记为 1',
        'def gcd': '自己写一个辗转相除求最大公约数',
        'if state & (1 << index)': '取 `state` 里的一位 `target[{index}] = {v}`',
        'lcm[state] = lcm[pre_state]': lambda S, B, r: f'`lcm[{S.state:02b}]` = `lcm[{S.pre_state:02b}] × {S.v} ÷ gcd` = =={S.lcm[S.pre_state] * S.v // gcd(S.lcm[S.pre_state], S.v)}==',
        'f = [None] * max_state': lambda S, B, r: ('`f` 重新开始（`f[0]` 仍是 0），之后分两种情况：`v` 不起作用 / `v` 起作用' if 'g' in S else '`f[state] = None` 表示这个 state 目前做不到；只有 `f[0] = 0`'),
        'f[0] = 0': '什么都不覆盖：0 次操作',
        'for v in nums': lambda S, B, r: (f'轮到 `v = {S.v}`：只有上一轮的 `g` 和它有关，所以用滚动数组；先备份 `g = f`，`f` 重新开始' if B.get('v') != S.v else '所有数都处理完了，`f` 就是最终结果'),
        'g = f[:]': '先把上一轮的结果备份给 `g`',
        'f[state] = g[state]': '`f[{state:02b}] = {g[state]}`（继承）',
        'if g[state] is not None': lambda S, B, r: (f'情况一：`v` 不起作用，`f[{S.state:02b}]` 直接继承上一轮 `g` = {S.g[S.state]}' if S.g[S.state] is not None else f'情况一：上一轮 `g[{S.state:02b}]` 是 None，没有可继承的，只能靠情况二'),
        'sub_state = state': '情况二：枚举 `state={state:02b}` 的所有子状态，让 `v` 负责其中一个',
        'cost = v % lcm': '把 `v = {v}` 变成 `lcm[{sub_state:02b}] = {lcm[sub_state]}` 的倍数：当前余数 `{cost}`',
        'cost = lcm[sub_state] - cost': '余数不为 0，还差 `lcm - 余数` = =={cost}== 次操作',
        'if g[state ^ sub_state] is not None': lambda S, B, r: (f'让 `v = {S.v}` 变成 `lcm[{S.sub_state:02b}] = {S.lcm[S.sub_state]}` 的倍数要 `{S.cost}` 次。余下 `{S.state ^ S.sub_state:02b}` 要靠前面的数：`g` = {_fv(S.g[S.state ^ S.sub_state])}' + ('，有解' if S.g[S.state ^ S.sub_state] is not None else '，前面做不到 → 这个子状态不能用')),
        'if f[state] is None or f[state] > cost': lambda S, B, r: (f'总代价 = `v` 的代价 + 前面的数的代价 = `{S.cost}`。`f[{S.state:02b}]` = {_fv(S.f[S.state])}：' + ('还没有方案或更小 → 更新' if S.f[S.state] is None or S.f[S.state] > S.cost else '不比现有的好 → 不更新')),
        'f[state] = cost': '`f[{state:02b}] = {cost}`（`v = {v}` 负责 `{sub_state:02b}`）',
        'sub_state = (sub_state - 1) & state': '`(sub_state - 1) & state`：下一个子状态 `{sub_state:02b}`',
        'return f[-1]': '`f[-1]` 就是 target 全部覆盖：最少 =={ret}== 次',
    },
    skip=[26, 38, 4, 6, 8, 10, 11, 12, 13, 15, 16, 17, 18, 20, 23, 25, 27, 28, 31, 32, 33, 34, 35, 42],
    max_steps=110,
    cards=dict(
        one_liner='用二进制记录「已经覆盖 target 的哪些元素」，滚动数组逐个加入 nums',
        complexity='时间 `O(n·3^m)`，空间 `O(2^m)`',
        problem=['`nums` 每次可把一个数 `+1`，要让 `target` 的每个数在 `nums` 里都至少有一个倍数',
                 '求最少操作次数，`target` 长度不超过 4',
                 '本视频：`nums=[7,5]`，`target=[4,6]` → `2`（7→8，5→6）'],
        quote='由于target的长度很小，那么在这里就可以尝试使用状态压缩来表示当前已经覆盖住的target中的元素，接下来就可以使用动态规划求解了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[index][state]`：用 `nums[0..index]` 覆盖 `state` 的最少操作次数',
              '最后一个数 ==没用==：直接继承；==有用==：它要变成 `sub_state` 里所有数的最小公倍数的倍数',
              '`lcm[sub_state]` 提前预处理，`cost = lcm − v % lcm`（已是倍数则 0）',
              '`f` 每轮只依赖上一轮 → 用 `g = f[:]` 当滚动数组'],
        summary=['时间 `O(n·3^m)`，空间 `O(2^m)`',
                 '`None` 表示做不到，更新前要先判断 `g[state ^ sub_state]` 存在',
                 '`cost = v % lcm`，非 0 时才用 `lcm − cost`，否则不需要操作',
                 '对比灵神：yiduobo 对每个数都做 DP；灵神先筛出前 m 小的候选再 DP',
                 '代码本身是 Python 3 兼容的，未做修改'],
    ),
)
