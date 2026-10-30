NUMS = [1, 2, 5, 4]


def _txt(S):
    if 'x' not in S or 'f' not in S or 'max_state' not in S:
        return '`f[state]`：state 的所有子状态中数值最大的那个（必须在 nums 里）'
    x, ms = S['x'], S['max_state']
    w = ms.bit_length()
    if S.get('_line', 0) >= 20 and 'res' in S:
        return f'`x={x:0{w}b}`，剩下的位 `max_state ^ x = {ms ^ x:0{w}b}`，其中最大的数 `f[{ms ^ x}] = {S["f"][ms ^ x]}`'
    if 'v' in S and S.get('_line', 0) >= 15 and x not in S['num_set'] and 'b' in S:
        return f'`x={x:0{w}b}` 不在 nums 里：去掉一个 1（`b={S["b"]:0{w}b}`）得 `{x ^ S["b"]:0{w}b}`，它的 f 是候选'
    return f'`state = {x:0{w}b}`：自己在 nums 里就是自己；否则看「去掉一个 1」的子状态'


def _col(S, i, v):
    x, b = S.get('x'), S.get('b')
    if x is None or S.get('_line', 0) > 22:
        return None
    if i == x:
        return 'blue'
    if b is not None and i == x ^ b and S.get('_line', 0) >= 15:
        return 'pink'
    return None


CONFIG = dict(
    num=3670, title='没有公共位的整数最大乘积', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='子状态最大值 · lowbit 逐位去 1',
    tags=['灵神题单·动态规划', '难度分 2234'],
    code='''
class Solution(object):
    def maxProduct(self, nums):
        
        ma = max(nums)
        max_state = 1
        while max_state <= ma:
            max_state <<= 1
        max_state -= 1
        
        f = [0] * (max_state + 1)
        num_set = set(nums)
        for x in range(1, max_state + 1):
            if x in num_set:
                f[x] = x
            else:
                v = x
                while v:
                    b = v & -v
                    pre = f[x ^ b]
                    if pre > f[x]:
                        f[x] = pre
                    v ^= b
        
        res = 0
        for x in num_set:
            res = max(res, f[max_state ^ x] * x)
        return res
''',
    call=f'Solution().maxProduct({NUMS})',
    expect=10,
    skip=['while max_state <= ma', 'max_state <<= 1', 'while v:', 'v ^= b', 'num_set = set', 'ma = max'],
    max_steps=60,
    views=[
        dict(type='array', var='nums', label='nums', h=170, cell=90),
        dict(type='text', fn=_txt, size=24, h=80),
        dict(type='array', var='f', label='f[state]：state 的子状态里最大的数（蓝 = 当前 x，粉 = 去掉一个 1 之后）', h=300, cell=80,
             color=_col, pointers={'x': 'blue'}),
    ],
    watch=[('x', 'x', 'blue'), ('b', 'b', 'orange'), ('pre', 'pre', 'pink'), ('res', 'res', 'green')],
    captions={
        'max_state -= 1': '`max_state = {max_state}`：最大值 `{ma}` 的二进制有 `{max_state.bit_length()}` 位，全是 1 的数就是全集',
        'f = [0] * (max_state + 1)': '`f` 下标 `0 ~ {max_state}`，每个下标是一个状态（集合）',
        'for x in range(1, max_state + 1)': lambda S, B, r: ('每个状态都算完了，`f` 填好' if B.get('x') == S.x else
                                                             f'依次处理状态 `x = {S.x}`（二进制 `{S.x:0{S.max_state.bit_length()}b}`）'),
        'if x in num_set': lambda S, B, r: (f'`{S.x}` 在 nums 里 → 子状态里最大的就是它自己' if S.x in S.num_set
                                            else f'`{S.x}` 不在 nums 里 → 要从它去掉某些 1 得到的子状态里选'),
        'f[x] = x': '`f[{x}] = {x}`',
        'v = x': '`v = x`：用 `v` 记录还没处理的 1',
        'b = v & -v': '`b = v & -v` = `{b}`：lowbit，取出 `v` 里最低的一个 1',
        'pre = f[x ^ b]': '去掉这个 1：`x ^ b = {x ^ b}`，它的最大子状态 `f[{x ^ b}] = {pre}`。去掉多个 1 的情况，已经包含在这一个里面',
        'if pre > f[x]': lambda S, B, r: (f'`pre = {S.pre} > f[{S.x}] = {S.f[S.x]}`：更大 → ==更新=='
                                          if S.pre > S.f[S.x] else f'`pre = {S.pre} <= f[{S.x}] = {S.f[S.x]}`：不更新'),
        'f[x] = pre': '`f[{x}] = {pre}`',
        'res = 0': '`res` 记录最大乘积',
        'for x in num_set': lambda S, B, r: ('nums 里的数枚举完了' if B.get('x') == S.x else f'枚举 nums 里的每个 `x = {S.x}`（二进制 `{S.x:0{S.max_state.bit_length()}b}`）'),
        'res = max(res': lambda S, B, r: (f'`x` 用掉的位，剩下 `max_state ^ x = {S.max_state ^ S.x}`，其中最大的数 `f[{S.max_state ^ S.x}] = {S.f[S.max_state ^ S.x]}`；'
                                          f'乘积 `{S.f[S.max_state ^ S.x]} × {S.x}` = {S.f[S.max_state ^ S.x] * S.x}，`res` → =={S.res}=='),
        'return res': '最大乘积 =={res}==（不存在合法数对时 `f` 为 0，乘积也是 0）',
    },
    cards=dict(
        one_liner='x 用掉的位之外，剩下的位里挑最大的数配对',
        complexity='时间 `O(U log U)`（U 为状态数），空间 `O(U)`',
        problem=['给整数数组 `nums`，找两个不同下标，二进制==没有公共置位==，使乘积最大；没有则返回 `0`',
                 '`n` 可达 `10^5`，数值 `≤ 10^6`，暴力 `O(n²)` 会超时',
                 '示例：`[1,2,3,4,5,6,7]` → `12`；本视频：`[1,2,5,4]` → `10`'],
        quote='对于nums[i]，其消耗掉了nums[i]的这些位，剩下的位为max_state ^ nums[i]，而nums[j]就是max_state ^ nums[i]的所有子状态中数值最大的那一个。',
        quote_src='—— yiduobo 题解原文',
        idea=['`max_state` = 最大值的二进制长度对应的全 1 数，当作全集',
              '`f[state]`：state 所有子状态里最大的数；自己在 nums 里就是自己',
              '否则用 lowbit 逐个去掉一个 1：`f[state ^ b]` 的最大者；去掉多个 1 的情况已包含在内',
              '最后枚举 `x`：`f[max_state ^ x] * x` 取最大'],
        summary=['时间 `O(U log U)`，空间 `O(U)`；原文已是 Python 3 可运行，没有改动',
                 '`pre > f[x]` 只需看「去掉一个 1」的子状态，不用枚举所有子集',
                 '`f[...]` 为 0 表示补集里没有 nums 的数，乘积为 0',
                 '和灵神相比：yiduobo 先判断 x 是否在 nums 里，灵神先初始化 `f[x] = x` 再逐位合并'],
    ),
)
