def _top(S):
    if 'diff' not in S:
        return ''
    s = S['s']
    n = len(s)
    return f"和 `0101…` 不同的位置数 `diff = {S['diff']}`；和 `1010…` 不同的就是 `{n} − {S['diff']} = {n - S['diff']}`"


CONFIG = dict(
    num=1758, title='生成交替二进制字符串的最少操作数', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='枚举两种目标，互补',
    code='''
class Solution:
    def minOperations(self, s: str) -> int:
        diff = 0
        for i, ch in enumerate(s):
            # 如果 i 是偶数，把 ch 变成 0，否则变成 1
            if int(ch) != i % 2:
                diff += 1
        return min(diff, len(s) - diff)
''',
    call='Solution().minOperations("010011")',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='s', label='s（红 = 与 010101 不同的位置）', cell=90, pointers={'i': 'pink'},
             color=lambda S, i, v: (('red' if int(v) != i % 2 else 'green') if 'i' in S and i <= S['i'] else None)),
        dict(type='string', var=lambda S: ''.join(str(k % 2) for k in range(len(S['s']))), label='目标 t0 = 010101…', cell=90,
             color=lambda S, i, v: None),
    ],
    watch=[('i', 'i', 'pink'), ('ch', 'ch'), ('diff', 'diff', 'red')],
    captions={
        'diff = 0': '`diff` 统计和目标 `010101…` ==不一样的位置数==',
        'for i, ch in enumerate': '看第 `{i}` 个字符 `{ch}`，目标位应该是 `{i % 2}`',
        'if int(ch) != i % 2': lambda S, B, r: (f'`{S.ch}` ≠ 目标 `{S.i % 2}` → 这一位要改' if int(S.ch) != S.i % 2
                                                else f'`{S.ch}` = 目标 `{S.i % 2}` → 不用改'),
        'diff += 1': '需要修改 → `diff` = {diff}',
        'return min': lambda S, B, ret: (f'变成 `1010…` 恰好是反过来的：`{len(S.s)} − {S.diff} = {len(S.s) - S.diff}` 次；'
                                         f'取较小值 → =={ret}=='),
    },
    cards=dict(
        one_liner='交替串只有两种：010101… 和 101010…，改的次数互补',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s` 只含 `0` 和 `1`，一步可翻转一个字符，要让相邻字符都不相等',
                 '求最少操作数',
                 '示例：`"0100"` → `1`；`"1111"` → `2`；本视频：`"010011"` → `2`'],
        quote='如果变成 t0 = 010101… 需要修改 k 次，那么由于 t1 = 101010… 每个位置都和 t0 不同，变成 t1 需要修改 n−k 次。答案为 min(k, n−k)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['交替字符串只有两种，首位是 0 或首位是 1',
              '只数变成 `010101…` 要改的位置数 `diff`，另一种就是 `n - diff`',
              '`i` 是偶数目标是 0，奇数目标是 1，所以直接比较 `int(ch) != i % 2`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`ch` 是字符，要用 `int(ch)` 才能和 `i % 2` 比较',
                 '易错：别忘了取 `min(diff, len(s) - diff)`，只算一种不对',
                 '变形：只能删除字符；子串查询（3777 题）'],
    ),
)
