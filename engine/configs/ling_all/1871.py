def _rng(S):
    j = S.get('j')
    if j is None:
        return None
    return max(j - S['maxJump'], 0), j - S['minJump']


def _fcolor(S, i, v):
    if S.get('_line') not in (9, 10) or 'j' not in S:
        return None
    lo, hi = _rng(S)
    if i == S['j']:
        return 'pink'
    if lo <= i <= hi:
        return 'blue'
    return None


def _show(S):
    j = S.get('j')
    if j is None or S.get('_line') not in (9, 10):
        return '`f[j]`：能否从 0 跳到 j；`sum_` 是 `f` 的前缀和（True 当 1）'
    lo, hi = _rng(S)
    if hi < lo:
        return f'`j = {j}` < `minJump`：==还没人能跳到==这里'
    return f'能跳到 `j = {j}` 的起跳点 `i ∈ [{lo}, {hi}]`：`sum_[{hi + 1}] − sum_[{lo}]` = {S["sum_"][hi + 1] - S["sum_"][lo]}'


CONFIG = dict(
    num=1871, title='跳跃游戏 VII', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='前缀和优化 DP',
    tags=['滑动窗口与双指针', '常用数据结构', '难度分 1896'],
    code='''
class Solution:
    def canReach(self, s: str, minJump: int, maxJump: int) -> bool:
        n = len(s)
        f = [False] * n
        sum_ = [0] * (n + 1)  # f 的前缀和
        f[0] = True
        sum_[1] = 1

        for j in range(1, n):
            f[j] = j >= minJump and s[j] == '0' and sum_[j - minJump + 1] > sum_[max(j - maxJump, 0)]
            sum_[j + 1] = sum_[j] + f[j]

        return f[-1]
''',
    call="Solution().canReach('01101000', 2, 3)",
    expect=True,
    setup='',
    views=[
        dict(type='text', fn=_show, size=26, h=70),
        dict(type='string', var='s', label='s（0 能落脚，1 不能）', h=170, pointers={'j': 'pink'},
             color=lambda S, i, v: ('pink' if i == S.get('j') else None)),
        dict(type='array', var=lambda S: [int(x) for x in S['f']] if 'f' in S else [], label='f[j]：能否跳到 j（1 = 能）', h=170,
             color=_fcolor),
        dict(type='array', var='sum_', label='sum_：f 的前缀和', h=170,
             color=lambda S, i, v: ('blue' if S.get('_line') in (9, 10) and 'j' in S and i in (max(S['j'] - S['maxJump'], 0), S['j'] - S['minJump'] + 1) else None)),
    ],
    watch=[('j', 'j', 'pink'), ('minJump', 'minJump', 'blue'), ('maxJump', 'maxJump', 'blue')],
    captions={
        'f = [False]': '`f[j]` 表示能否从 0 跳到 `j`',
        'sum_ = [0]': '`sum_[k]` = `f[0..k-1]` 里 True 的个数，用来 `O(1)` 查区间里有没有 True',
        'f[0] = True': '起点 0 一定在，`f[0] = True`',
        'sum_[1] = 1': '`sum_[1] = 1`：前 1 个里有 1 个 True',
        'f[j] = ': lambda S, B, ret: (f'`j = {S.j}` < `minJump = {S.minJump}`：最近一步也跳不到 → `f[{S.j}] = False`' if S.j < S.minJump else (f'`s[{S.j}] = 1`：落脚点是 1，不能跳 → `f[{S.j}] = False`' if S.s[S.j] != '0' else f'起跳点区间 `[{max(S.j - S.maxJump, 0)}, {S.j - S.minJump}]`：`sum_[{S.j - S.minJump + 1}] = {S.sum_[S.j - S.minJump + 1]}` {">" if S.sum_[S.j - S.minJump + 1] > S.sum_[max(S.j - S.maxJump, 0)] else "<="} `sum_[{max(S.j - S.maxJump, 0)}] = {S.sum_[max(S.j - S.maxJump, 0)]}` → 区间内{"==有==" if S.f[S.j] else "==没有=="} True → `f[{S.j}] = {S.f[S.j]}`')),
        'sum_[j + 1] =': '`sum_[{j+1}] = sum_[{j}] + f[{j}]` = {sum_[j+1]}',
        'return f[-1]': '`f[n-1] = {f[-1]}`',
    },
    cards=dict(
        one_liner='把「区间里有没有能到的点」变成前缀和相减',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二进制串 `s`，从下标 0 出发，可跳 `[minJump, maxJump]` 步，只能落在 `\'0\'` 上',
                 '问能否到达最后一个下标',
                 '本视频：`s="01101000"`，`minJump=2`，`maxJump=3` → `true`'],
        quote='换句话说，能跳到 j 的 i 必须满足 max(j-maxJump, 0) ≤ i ≤ j-minJump。……区间中存在下标 i 满足 f[i] = true，等价于 f 的子数组元素和大于 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[j]`：能否从 0 跳到 `j`；枚举最后一步的起跳点 `i`',
              '起跳点是一段连续区间，暴力枚举是 `O(n^2)`',
              '把 True 当 1 做前缀和，区间和 > 0 就说明区间里有能到的点'],
        after=[dict(heading='另外两种写法', lines=['差分：跳到 `i` 就把 `[i+minJump, i+maxJump]` 整段加一，前缀和 > 0 即可到达',
                                                 '同向双指针：`j` 记录还没标记过的位置，每个下标最多标记一次'])],
        summary=['时间 `O(n)`，`f` 可以进一步用 `sum_` 代替',
                 '易错：`j >= minJump` 要先判断，否则 `j - minJump + 1` 会是负下标',
                 '区间左端点是 `max(j - maxJump, 0)`，别忘了和 0 取最大',
                 '同类题：1696 跳跃游戏 VI、55 跳跃游戏'],
    ),
)
