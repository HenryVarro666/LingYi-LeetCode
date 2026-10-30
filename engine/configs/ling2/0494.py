NUMS = [1, 2, 1, 3]
TARGET = 1

# 代码是 `for x in nums`，没有下标；字幕按顺序生成时数一数第几个物品，给视图标出当前的 x
_cnt = [-1]
_POS = {}


def _rec(fn):
    def g(S, B, ret):
        if S._line == 9:
            _cnt[0] += 1
        if 'f' in S:
            _POS[id(S.f)] = _cnt[0]
        return fn(S, B, ret)
    return g


def _item(S):
    k = _POS.get(id(S.get('f')))
    return k if k is not None and 0 <= k < len(NUMS) else None


def _fcolor(S, i, v):
    if 'c' not in S or _item(S) is None or S.get('_line') != 11:
        return None
    c, x = S['c'], S['x']
    if i == c:
        return 'yellow'
    if i == c - x:
        return 'purple'
    return None


def _fdim(S, i, v):
    if 'c' not in S or _item(S) is None or S.get('_line') != 11:
        return False
    return i < S['x'] and i != S['c'] - S['x']


def _ncolor(S, i, v):
    k = _item(S)
    if k is None:
        return None
    if i == k:
        return 'yellow'
    return 'green' if i < k else None


def _pc(S):
    return S['c'] if S.get('_line') == 11 and 'c' in S else None


def _pcx(S):
    return S['c'] - S['x'] if S.get('_line') == 11 and 'c' in S else None


def _text(S):
    if 'c' in S and S.get('_line') == 11 and _item(S) is not None:
        c, x, f = S['c'], S['x'], S['f']
        return f'`f[{c}] += f[{c - x}]`：不选 `{x}` 的 `{f[c] - f[c - x]}` 种 + 选 `{x}` 的 `{f[c - x]}` 种 = =={f[c]}=='
    if 'm' in S:
        return f"`f[c]`：从已遍历的数中选一些，和==恰好==为 `c` 的方案数（容量 `m = {S['m']}`）"
    return '取负号的数之和 `q = (S − |target|) / 2`，问题变成：选数凑出 `q` 的方案数'


def _cap_for_x(S, B, ret):
    k = _cnt[0]
    if k >= len(NUMS):
        return '所有数都考虑完了'
    if S.x == S.m:
        return f'考虑第 {k} 个数 `x = {S.x}`：只有 `f[{S.m}]` 能选它'
    return f'考虑第 {k} 个数 `x = {S.x}`：从大到小更新 `f[{S.m}]`…`f[{S.x}]`（`c < x` 选不了，保持不变）'


def _cap_upd(S, B, ret):
    c, x, f = S.c, S.x, S.f
    if c == S.m and _cnt[0] == 0:
        return (f'`f[{c}] += f[{c - x}]`：`f[{c - x}]` 还是==旧画==（上一轮的值），'
                f'所以必须==从大到小==更新 → `{f[c]}`')
    return f'`f[{c}]` = 不选 `{B.f[c]}` + 选 `f[{c - x}] = {B.f[c - x]}` → `{f[c]}`'


CONFIG = dict(
    num=494, title='目标和', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='转化成 0-1 背包 · 一个数组',
    tags=['热题173'],
    code='''
class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        s = sum(nums) - abs(target)
        if s < 0 or s % 2:
            return 0

        m = s // 2  # 背包容量
        f = [1] + [0] * m
        for x in nums:
            for c in range(m, x - 1, -1):
                f[c] += f[c - x]
        return f[m]
''',
    call=f'Solution().findTargetSumWays({NUMS}, {TARGET})',
    expect=3,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='array', var='nums', label='nums（黄 = 当前物品 x，绿 = 已考虑）', cell=90, color=_ncolor, h=150),
        dict(type='array', var='f', label='f（黄 = 正在更新 f[c]，紫 = 用到的 f[c−x]，灰 = c < x 不用动）', cell=120,
             pointers={_pc: 'yellow', _pcx: 'purple'}, pointer_labels={_pc: 'c', _pcx: 'c - x'},
             color=_fcolor, dim=_fdim, h=260),
    ],
    watch=[('x', 'x', 'yellow'), ('c', 'c', 'yellow'), ('m', 'm', 'green'), ('f[m]', 'f[m]', 'green')],
    skip=['for c in range'],
    captions={
        's = sum': _rec(lambda S, B, ret: f'元素和 `{sum(S.nums)}` − `|target| = {abs(S.target)}` → `s = {S.s}`'),
        'if s < 0': _rec(lambda S, B, ret: f'`s = {S.s}` 非负且是偶数 → 有解的可能'),
        'm = s // 2': _rec(lambda S, B, ret: f'背包容量 `m = s / 2 = {S.m}`：选一些数取负号，和恰好为 `{S.m}`'),
        'f = [1]': _rec(lambda S, B, ret: '`f[0] = 1`：什么都不选，和为 0，==1 种方案==；其余为 0'),
        'for x in nums': _rec(_cap_for_x),
        'f[c] += f[c - x]': _rec(_cap_upd),
        'return f[m]': _rec(lambda S, B, ret: f'`f[{S.m}]` 就是答案：=={ret}== 种添加符号的方法'),
    },
    cards=dict(
        one_liner='p − q = target，p + q = S → 选数凑出 (S − |target|) / 2',
        complexity='时间 `O(nm)`，空间 `O(m)`（`m = (S − |target|) / 2`）',
        problem=['给每个数前面添 `+` 或 `-`，串起来得到表达式',
                 '求运算结果等于 `target` 的==不同表达式数目==',
                 '示例：`[1,1,1,1,1]`，`target = 3` → `5`',
                 '演示：`[1,2,1,3]`，`target = 1` → `3`'],
        before=[dict(heading='一、转化', lines=[
            '设元素和为 `S`，正号元素之和为 `p`，负号元素（绝对值）之和为 `q`',
            '`p + q = S`，`p − q = target` → `q = (S − target) / 2`',
            '取 `(S − |target|) / 2` 作为容量最优；它为负数或奇数时答案为 0',
        ])],
        quote='只要我们选出的取正号的元素和恰好等于 p，或者取负号的元素和恰好等于 q，就==等价于==表达式的结果恰好等于 target。',
        quote_src='—— 灵茶山艾府题解',
        idea=['问题变成：从 `nums` 中选一些数，和==恰好等于==容量的方案数（0-1 背包）',
              '`f[c] = 不选 + 选 = f[c] + f[c − x]`',
              '空间优化：像在墙上画新画，==必须从大到小画==，旧画 `f[c − x]` 才还在'],
        after=[dict(heading='灵神的完整推导链', lines=[
            '记忆化搜索 `dfs(i, c) = dfs(i−1, c) + dfs(i−1, c − nums[i])`',
            '1:1 翻译成递推 `f[i+1][c]` → 两个数组滚动 → ==一个数组==（本视频）',
            '另一种方法：折半枚举，`nums[i]` 很大时用，`O(n · 2^(n/2))`',
        ])],
        summary=['时间 `O(nm)`，空间 `O(m)`',
                 '易错：内层循环必须==倒序==，正序会把同一个数用多次（变成完全背包）',
                 '易错：`nums` 里有 0 时不能在 `c = 0` 提前返回 1（0 选不选都行）',
                 '`target` 可以是负数，所以用 `abs(target)`'],
    ),
)
