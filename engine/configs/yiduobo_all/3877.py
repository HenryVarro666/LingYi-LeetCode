def _fmt(v):
    return '-1' if v == -1 else str(v)


def _cell_f(S, j, v):
    if S.get('_line') in (15, 16) and 'nxt' in S and j == S['nxt']:
        return 'yellow'
    return None


def _cell_g(S, j, v):
    if S.get('_line') in (14, 15, 16) and 'pre' in S and j == S['pre']:
        return 'green'
    return None


def _formula(S):
    if S.get('_line') in (15, 16) and 'nxt' in S:
        return (f'用 `v={S["v"]}`：旧 `g[{S["pre"]}] = {S["g"][S["pre"]]}` → 异或后到 `{S["pre"]} ^ {S["v"]} = {S["nxt"]}`，'
                f'`f[{S["nxt"]}] = {S["f"][S["nxt"]]}`')
    return '`f[x]` = 异或值恰好为 `x` 时最多选几个；`-1` = 凑不出'


CONFIG = dict(
    num=3877, title='达到目标异或值的最少删除次数', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='滚动数组的异或背包 DP',
    tags=['灵神核心路线', '灵神题单·图论算法', '难度分 1745'],
    code='''
class Solution(object):
    def minRemovals(self, nums, target):
        
        ma = max(max(nums), target)
        p2 = 1
        while p2 <= ma:
            p2 += p2
        
        f = [-1] * (p2 + 1)
        f[0] = 0
        for v in nums:
            g = f[:]
            for pre in range(p2 + 1):
                if g[pre] != -1:
                    nxt = pre ^ v
                    f[nxt] = max(f[nxt], g[pre] + 1)

        if f[target] == -1:
            return -1
        return len(nums) - f[target]
''',
    call='Solution().minRemovals([1, 2, 3], 1)',
    expect=1,
    skip=['for pre in range'],
    views=[
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='array', var=lambda S: [_fmt(v) for v in S['g']] if 'g' in S else None,
             label='g：这一轮开始前的 f 副本（绿 = 当前 pre）', h=220, cell=90, pointers={'pre': 'blue'}, color=_cell_g),
        dict(type='array', var=lambda S: [_fmt(v) for v in S['f']] if 'f' in S else None,
             label='f：边用边更新（黄 = f[nxt]）', h=220, cell=90, pointers={'nxt': 'pink'}, color=_cell_f),
        dict(type='array', var='nums', label='nums', h=190, cell=90, pointers={'v': 'pink'}),
    ],
    watch=[('p2', 'p2', 'cyan'), ('v', 'v', 'pink'), ('pre', 'pre', 'blue'), ('nxt', 'nxt', 'yellow')],
    captions={
        'ma = max': '`ma = max(max(nums), target) = {ma}`：异或值最多和它一样长（二进制位数）',
        'p2 = 1': '`p2` 从 1 开始，每次翻倍',
        'while p2 <= ma': lambda S, B, r: ('`p2 = %d`' % S.p2 + (' ≤ `ma`，继续翻倍' if S.p2 <= S.ma else ' > `ma = %d`，停止' % S.ma)),
        'p2 += p2': '`p2` 翻倍 → `{p2}`：找第一个比 `ma` 大的 2 的幂，所有异或结果都小于它',
        'f = [-1]': '`f` 的长度 `p2 + 1 = {p2 + 1}`：==不止到 target==，中间的异或值可能更大',
        'f[0] = 0': '`f[0] = 0`：什么都不选，异或值 0，选了 0 个；其余 `-1` = 凑不出',
        'g = f[:]': '处理 `v = {v}`：先拷贝一份旧的 `g`，==只用旧状态转移==，保证 `v` 不会被选两次',
        'if g[pre]': lambda S, B, r: ('`g[%d] = %d` ≠ -1：旧状态里能凑出异或值 %d' % (S.pre, S.g[S.pre], S.pre) if S.g[S.pre] != -1
                                      else '`g[%d] = -1`：凑不出，跳过' % S.pre),
        'nxt = pre ^ v': '选上 `v={v}`：`{pre} ^ {v}` = ==nxt {nxt}==，异或值从 `{pre}` 变成 `{nxt}`',
        'f[nxt] = max': '`f[{nxt}] = max(旧 {B.f[nxt]}, g[{pre}] + 1 = {g[pre] + 1})` → 新值 =={f[nxt]}==',
        'if f[target] == -1': lambda S, B, r: ('`f[%d] = %d`：凑不出 → 返回 -1' % (S.target, S.f[S.target]) if S.f[S.target] == -1
                                               else '`f[%d] = %d`：能凑出，最多选这么多个' % (S.target, S.f[S.target])),
        'return len(nums)': '最少移除 = `{len(nums)} - {f[target]}` = =={ret}==',
    },
    cards=dict(
        one_liner='移除最少 = 选择最多，f[异或值] 记最多选几个',
        complexity='时间 `O(n·p2)`，空间 `O(p2)`',
        problem=['从 `nums` 里移除任意个元素，使剩余元素按位异或和==恰好等于 `target`==',
                 '求最少移除几个，做不到返回 `-1`',
                 '示例：`nums=[1,2,3], target=1`（演示用）→ `1`（只删 1，留 `2^3=1`）'],
        quote='题目移除尽量少的元素，使得剩下的元素异或值等于target，就相当于从中选取尽量多的元素，使得这些元素的异或值等于target。',
        quote_src='—— yiduobo 题解',
        idea=['`f[pre]`：选若干个数，异或值恰好为 `pre` 时最多选几个',
              '放弃 `v`：`f` 不变；使用 `v`：`nxt = pre ^ v`，`f[nxt] = max(f[nxt], f[pre] + 1)`',
              '每个 `v` 只依赖上一轮，所以用滚动数组省掉 `index` 这一维；答案 `len(nums) - f[target]`'],
        summary=['时间 `O(n·p2)`，空间 `O(p2)`（`p2` 是大于最大值的 2 的幂）',
                 '易错：数组要开到 `p2 + 1`，不能只开到 `target`',
                 '易错：转移要读旧的 `g`、写新的 `f`，否则同一个数会被用两次',
                 '无法凑出时 `f[target] == -1`，要返回 -1 而不是 `n + 1`'],
    ),
)
