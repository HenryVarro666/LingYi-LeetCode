PR = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def _names(mask):
    ps = [str(PR[j]) for j in range(10) if mask >> j & 1]
    return '×'.join(ps) if ps else '空集'


def _nz(S):
    f = S.get('f')
    if not f:
        return {}
    return {j: v for j, v in enumerate(f) if v}


def _top(S):
    if 'v' not in S:
        return '`f[index]`：用到的质数集合恰好是 `index` 的子集数（只含大于 1 的数）'
    s = f"当前数 `v = {S['v']}`"
    if 'state' in S and S['_line'] >= 20:
        s += f"，质数集合 `state = {S['state']}`（{_names(S['state'])}）"
    return s + f"，已有 `{S['one']}` 个 1"


def _flag(S, B, r):
    if S.flag:
        return f'`{S.v}` 无平方因子：`state = {S.state}`（{_names(S.state)}）→ 往 `f` 里加'
    return f'`{S.v}` 里某个质数的指数 ≥ 2（有平方因子）→ 不能选，直接跳过'


CONFIG = dict(
    num=2572, title='无平方子集计数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='质数状压 DP · 单独处理 1',
    tags=['灵神题单', '难度分 2420'],
    code='''
class Solution(object):
    def squareFreeSubsets(self, nums):

        prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        max_state = 1024

        f = [0] * max_state
        f[0] = 1
        mod = 10 ** 9 + 7
        one = 0

        for v in nums:
            if v == 1:
                one += 1
                continue

            state = 0
            flag = True
            for index, p in enumerate(prime):
                if v % p == 0:
                    if v // p % p == 0:
                        flag = False
                        break
                    
                    state |= (1 << index)
            
            if not flag:
                continue
            
            for index in range(max_state - 1, state - 1, -1):
                if index & state == state:
                    f[index] += f[index ^ state]
                    if f[index] >= mod:
                        f[index] -= mod

        res = 0

        for index in range(1, max_state):
            res += f[index]
            if res >= mod:
                res -= mod
        
        pow2 = 1
        for _ in range(one):
            res += res
            if res >= mod:
                res -= mod

            pow2 += pow2
            if pow2 >= mod:
                pow2 -= mod
        
        res = res + pow2 - 1
        if res < 0:
            res += mod
        if res >= mod:
            res -= mod

        return res
''',
    call='Solution().squareFreeSubsets([1,1,2,3,4,5])',
    expect=31,
    max_events=80000,
    skip=['for index, p in enumerate', 'if v % p == 0', 'if v // p % p', 'flag = False', 'break', 'state |=', 'continue',
          'for index in range(max_state - 1', 'if index & state == state', 'f[index] +=', 'if f[index] >= mod', 'f[index] -= mod',
          'for index in range(1, max_state)', 'res += f[index]', 'if res >= mod', 'res -= mod', 'for _ in range(one)', 'res += res',
          'pow2 += pow2', 'if pow2 >= mod', 'pow2 -= mod', 'if res < 0', 'res += mod', 'state = 0', 'max_state = 1024',
          'f = [0] * max_state', 'mod = 10', 'flag = True', 'prime = ['],
    max_steps=60,
    views=[
        dict(type='text', fn=_top, size=24, h=80),
        dict(type='array', var='nums', label='nums（1 单独计数；4 含平方因子 2^2，不能选）', h=170, cell=70,
             color=lambda S, i, v: ('blue' if 'v' in S and S['v'] == v and (v != 1 or i == (S['one'] - 1 if S['_line'] >= 14 else S['one'])) else None)),
        dict(type='map', var=_nz, label='f[index]：非零项（index = 质数集合位掩码 → 子集数）', h=360, font=26,
             fmt=lambda k, v: f'{k} ({_names(k)}) → {v}'),
    ],
    watch=[('v', 'v', 'blue'), ('state', 'state', 'green'), ('one', 'one', 'yellow'), ('res', 'res', 'pink')],
    captions={
        'f[0] = 1': '`f[0] = 1`：空集（还没选任何大于 1 的数）算 1 种，转移要从它出发',
        'one = 0': '`one` 统计 1 的个数：1 不影响乘积是否无平方，单独处理',
        'for v in nums': lambda S, B, r: ('数字都看完了：大于 1 的数的合法子集都在 `f` 里' if B.get('v') == S.get('v') and 'state' in B else f'看数字 `v = {S.v}`'),
        'if v == 1': lambda S, B, r: (f'`v = 1`：只计数，`one` → {S.one + 1}，不进 DP' if S.v == 1 else f'`v = {S.v} > 1`：要分解质因数'),
        'one += 1': '`one` = {one}',
        'if not flag': _flag,
        'res = 0': '把 `f[1]` 到 `f[1023]` 全部相加 = 大于 1 的数构成的合法子集数（去掉空集 `f[0]`）：`res` 之后 = {sum(f[1:]) % mod}',
        'pow2 = 1': '每个 1 都可以加或不加：`res` 翻倍 `{one}` 次，`pow2 = 2^{one}`（循环略过）',
        'res = res + pow2 - 1': '公式：`res × 2^one + 2^one − 1` = `{res}`（`{one}` 个 1 任选 + 单独由 1 组成的非空子集）',
        'return res': '答案 `{ret}`',
    },
    cards=dict(
        one_liner='1 不影响合法性，其余数用 10 位二进制记录用过哪些质数',
        complexity='时间 `O(n·2^10)`，空间 `O(2^10)`',
        problem=['无平方因子数：不能被 `1` 以外的任何平方数整除',
                 '数一数 `nums` 里乘积无平方因子的==非空子集==，对 `10^9 + 7` 取模',
                 '示例：`[3,4,4,5]` → `3`；本视频：`[1,1,2,3,4,5]` → `31`'],
        quote='首先，1在本题中不会影响平方子集的判定，因此每个1都可以任意选择加入或者不加入某个子集。……一个合法子集要求的是将子集中每个数分解质因数，并按照底数分别累加指数后，最大的指数和不能大于等于2。',
        quote_src='—— yiduobo 题解原文',
        idea=['先拿掉 1：设有 `one` 个 1，其余合法子集 `res` 个 → 共 `res × 2^one + 2^one − 1` 个',
              '30 以内只有 10 个质数 → 10 位二进制 `state` 表示已用质数',
              '`f[index] += f[index ^ state]`：01 背包，`index` 倒序枚举，省去一维'],
        summary=['时间 `O(n·2^10)`，空间 `O(2^10)`',
                 '`index` 必须倒序，否则同一个数会被用多次',
                 '`f[0] = 1` 是空集，求和时从 `index = 1` 开始，排除空集',
                 '原文为 Python 2 写法，`v / p % p` 的整数除法已改为 `v // p % p`',
                 '对比灵神：灵神把相同数字合并、枚举补集的子集；这里逐个数做背包，1 用 `2^one` 公式补上'],
    ),
)
