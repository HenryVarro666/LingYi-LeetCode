def _col(S, j, v):
    s = S['s']
    n = len(s)
    if 'index' in S and S.get('_line', 0) <= 8:
        if j in (S['index'], S['index'] - 1):
            return 'yellow' if s[S['index']] == s[S['index'] - 1] else 'cyan'
        return None
    if S.get('_line', 0) > 8 and j in (0, n - 1):
        return 'orange'
    return None


def _txt(S):
    if 'cnt' not in S:
        return '先数原始 `s` 的相邻相同对数 `cnt`'
    s = S['s']
    if S.get('_line', 0) <= 8:
        return f"原始 `s` 中相邻相同：`cnt = {S['cnt']}`"
    same = s[0] == s[-1]
    return (f"`cnt = {S['cnt']}`，`k = {S['k']}`；首尾 `s[0]` {'==' if same else '≠'} `s[-1]` → "
            + ('移位会==新增==一对' if same else '移位==不会新增=='))


CONFIG = dict(
    num=4043, title='恰好有 K 对相等相邻字符的循环移位数量', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='分类讨论 · 移位对得分影响至多为 1',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def countRotations(self, s, k):

        cnt = 0
        n = len(s)
        for index in range(1, n):
            if s[index] == s[index - 1]:
                cnt += 1

        if cnt == k - 1:
            if s[0] == s[-1]:
                return n - k
            else:
                return 0

        elif cnt == k:
            if s[0] == s[-1]:
                return k + 1
            else:
                return n - k

        elif cnt == k + 1:
            if s[0] == s[-1]:
                return 0
            else:
                return cnt
        else:
            return 0
''',
    call="Solution().countRotations('aabcbb', 1)",
    expect=2,
    views=[
        dict(type='string', var='s', label='s（黄 = 相邻相同，橙 = 首尾 s[0] 与 s[-1]）', h=250, cell=100,
             pointers={'index': 'blue'}, color=_col),
        dict(type='text', h=110, size=30, fn=_txt),
    ],
    watch=['n', ('k', 'k'), ('index', 'index', 'blue'), ('cnt', 'cnt', 'orange')],
    captions={
        'cnt = 0': '`cnt`：==不移位==时的得分（原始相邻相同对数）',
        'n = len': '`n = {n}`',
        'for index in range': lambda S, B, ret: (f'比较 `s[{S.index - 1}]` 和 `s[{S.index}]`'
                                                if 'index' not in B or S.index != B.index else '原始得分统计完了'),
        'if s[index] == s[index - 1]': lambda S, B, ret: (f"`{S.s[S.index - 1]!r} == {S.s[S.index]!r}`：相同" if S.s[S.index] == S.s[S.index - 1]
                                                         else f"`{S.s[S.index - 1]!r} ≠ {S.s[S.index]!r}`"),
        'cnt += 1': '`cnt` → {cnt}',
        'if s[0] == s[-1]': lambda S, B, ret: ("首尾 `s[0] == s[-1]`：移位后它们相邻，==会多出一对==" if S.s[0] == S.s[-1]
                                               else f"首尾 `{S.s[0]!r} ≠ {S.s[-1]!r}`：移位后==不会新增==相同对"),
        'if cnt == k - 1': lambda S, B, ret: (f'`cnt = {S.cnt} == k − 1`：要靠移位==多出一对==' if S.cnt == S.k - 1
                                              else f'`cnt = {S.cnt} ≠ k − 1 = {S.k - 1}`'),
        'elif cnt == k:': lambda S, B, ret: (f'`cnt = {S.cnt} == k`：不移位就满足，==保底 1 个==' if S.cnt == S.k
                                             else f'`cnt = {S.cnt} ≠ k = {S.k}`'),
        'elif cnt == k + 1': lambda S, B, ret: (f'`cnt = {S.cnt} == k + 1`：要靠移位==断开一对==' if S.cnt == S.k + 1
                                                else f'`cnt = {S.cnt}` 和 k 差了不止 1'),
        'return n - k': lambda S, B, ret: (f'首尾==相同==，在原本不相同的 `n − k = {ret}` 个位置断开都行（含不移位）' if S.cnt == S.k
                                           else f'首尾相同，在 `n − k = {ret}` 个原本不相同的位置断开，得分 +1'),
        'return k + 1': '首尾==相同==：断开一对相同的、首尾又拼出一对 → 得分不变，`cnt` 种 + 不移位 1 种 = =={ret}==',
        'return cnt': '首尾==不同==：断开 `cnt` 对相同中的任意一对，得分 −1 → =={ret}== 种',
        'return 0': '凑不出 k，答案 `0`',
    },
    cards=dict(
        one_liner='移位只会断开一处、拼上首尾一处：得分最多变化 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 `s` 的一个前缀（长 0 到 n−1）移到末尾，得到循环移位',
                 '得分 = 相邻相同字符的对数；问得分==恰好为 k== 的循环移位有几个',
                 '示例：`"aab", k = 1` → `2`；本视频 `"aabcbb", k = 1`'],
        quote='原始s中的s[p - 1]与s[p]将不再相邻，而s[0]和s[-1]将会因为此次移位操作变为相邻。换言之，==循环移位操作对得分的影响至多为1==。',
        quote_src='—— yiduobo 题解原文',
        idea=['先算不移位的得分 `cnt`，再按 `cnt` 与 k 的关系分类',
              '首尾 `s[0] == s[-1]`：移位会多出一对；断开相同的位置会少一对',
              '`cnt` 与 k 相差超过 1 → 不可能，答案 0'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`cnt = k − 1`：首尾相同 → `n − k`；`cnt = k + 1`：首尾不同 → `cnt`',
                 '`cnt = k`：首尾相同 → `k + 1`，否则 `n − k`（都含不移位那 1 种）',
                 '原文为 Python 2 风格（`class Solution(object)`），代码无需改动',
                 '对比灵神：灵神主写法在 `s + s` 上滑窗，不用分类讨论'],
    ),
)
