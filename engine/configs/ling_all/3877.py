from math import inf as _inf


def _fmt(v):
    return '-∞' if v == _inf * -1 or v == float('-inf') else str(v)


def _cell_f(S, j, v):
    if S.get('_line') != 13 or 'j' not in S or 'x' not in S:
        return None
    if j in (S['j'], S['j'] ^ S['x']):
        return 'green'
    return None


def _cell_nf(S, j, v):
    if S.get('_line') == 13 and 'j' in S and j == S['j']:
        return 'yellow'
    return None


def _formula(S):
    if S.get('_line') == 13 and 'j' in S and 'x' in S:
        j, x, f, nf = S['j'], S['x'], S['f'], S['nf']
        return (f'`nf[{j}] = max(f[{j}], f[{j}^{x}] + 1) = max({_fmt(f[j])}, {_fmt(f[j ^ x])} + 1)` = =={_fmt(nf[j])}==')
    return '`f[j]` = 异或和恰好为 `j` 时最多能留几个数；`-∞` = 凑不出'


CONFIG = dict(
    num=3877, title='达到目标异或值的最少删除次数', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='0-1 背包（恰好装满，异或版）',
    tags=['灵神核心路线', '灵神题单·图论算法', '难度分 1745'],
    code='''
class Solution:
    def minRemovals(self, nums: List[int], target: int) -> int:
        m = max(nums).bit_length()
        if (1 << m) <= target:
            return -1

        f = [-inf] * (1 << m)
        f[0] = 0

        nf = [0] * (1 << m)
        for x in nums:
            for j in range(1 << m):
                nf[j] = max(f[j], f[j ^ x] + 1)  # x 不选 or 选
            f, nf = nf, f

        if f[target] < 0:
            return -1
        return len(nums) - f[target]
''',
    call='Solution().minRemovals([1, 2, 3], 2)',
    expect=1,
    skip=['for j in range'],
    views=[
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='array', var=lambda S: [_fmt(v) for v in S['f']] if 'f' in S else None,
             label='f[j]：上一轮（绿 = 不选 x 的 f[j] 和选 x 的 f[j^x]）', h=220, cell=100,
             pointers={'j': 'blue'}, color=_cell_f),
        dict(type='array', var=lambda S: [_fmt(v) for v in S['nf']] if 'nf' in S else None,
             label='nf[j]：这一轮正在填（黄 = nf[j]）', h=220, cell=100, pointers={'j': 'blue'}, color=_cell_nf),
        dict(type='array', var='nums', label='nums', h=190, cell=100, pointers={'x': 'pink'}),
    ],
    watch=[('m', 'm', 'cyan'), ('x', 'x', 'pink'), ('j', 'j', 'blue'), ('target', 'target', 'yellow')],
    captions={
        'm = max': '`m = {m}`：最大数有 `{m}` 位二进制，异或结果不会超过 `2^m - 1 = {(1 << m) - 1}`',
        'if (1 << m) <= target': lambda S, B, r: ('`2^m = %d` %s `target = %d`：%s' % (
            1 << S.m, '≤' if (1 << S.m) <= S.target else '>', S.target,
            'target 比任何异或结果都长 → ==无解==' if (1 << S.m) <= S.target else 'target 的位数不超过 m，可能有解，继续 DP')),
        'f = [-inf]': '`f` 大小是 `2^m = {1 << m}`，==不是 target+1==：中途异或和可能比 target 大，最后再降下来',
        'f[0] = 0': '`f[0] = 0`：一个数都不选，异或和为 0，留下 0 个；其余 `-∞` 表示凑不出',
        'nf = [0]': '`nf` 保存新一轮的结果，和 `f` 来回交换，空间只要 `O(U)`',
        'nf[j] = max': lambda S, B, r: ('`x = %d`：不选 → `f[%d] = %s`；选 → 前面异或和要是 `j^x = %d`，`f[%d] + 1 = %s`；取大 → `nf[%d]` = ==%s==' % (
            S.x, S.j, _fmt(S.f[S.j]), S.j ^ S.x, S.j ^ S.x, _fmt(S.f[S.j ^ S.x] + 1), S.j, _fmt(S.nf[S.j]))),
        'f, nf = nf, f': '`nums` 里这个数处理完：`nf` 变成新的 `f`（滚动数组）',
        'if f[target] < 0': lambda S, B, r: ('`f[%d] = %s`：%s' % (S.target, _fmt(S.f[S.target]), '凑不出 target → 返回 -1' if S.f[S.target] < 0 else '能凑出，最多保留这么多个'))
        if S.f[S.target] >= 0 else '`f[%d] = -∞`：凑不出 target → 返回 -1' % S.target,
        'return len(nums)': '最少删除 = 总个数 `{len(nums)}` − 最多保留 `{f[target]}` = =={ret}==',
    },
    cards=dict(
        one_liner='删得最少 = 留得最多：异或版恰好装满背包',
        complexity='时间 `O(nU)`，空间 `O(U)`',
        problem=['给整数数组 `nums` 和 `target`，可以删掉任意个元素，使剩余元素的==异或和等于 `target`==',
                 '求最少删几个；做不到返回 `-1`（空数组异或和为 0）',
                 '示例：`nums=[1,2,3], target=2` → `1`（删掉 2，`1^3=2`）'],
        quote='移除次数尽量小，等价于保留的元素个数尽量多。……这是恰好装满型 0-1 背包。……只需把 2915 转移方程中的 j - nums[i] 改成 j ⊕ nums[i] 即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i+1][j] = max(f[i][j], f[i][j ^ nums[i]] + 1)`：不选 x，或者选 x（原来异或和是 `j^x`）',
              '初始 `f[0][0] = 0`，其余 `-∞`；答案是 `n - f[n][target]`',
              '数组大小取 `2^m`（异或最大值加一），不能只开 `target+1`；异或是自己的逆运算，所以能「查表」'],
        summary=['时间 `O(nU)`，空间 `O(U)`（滚动数组）',
                 '易错：`f` 要开到 `2^m`；`(1<<m) <= target` 直接返回 -1',
                 '`-inf + 1` 仍是 `-inf`，不用特判；最后 `f[target] < 0` 说明凑不出',
                 '原文还有二维数组写法、刷表法（改成 AND/OR 时用）和 BFS 最短路写法（异或和当节点）'],
    ),
)
