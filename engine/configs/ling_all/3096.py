def _txt(S):
    if 's' not in S:
        return ''
    s, pre = S['s'], S['pre']
    base = f'总得分 `s = {s}`'
    if 'i' in S and 'x' in S:
        return f'{base}　｜　`pre`（2×前缀得分）= {pre}　→　{"==pre > s，Alice 赢==" if pre > s else "pre ≤ s，没赢"}'
    return base


CONFIG = dict(
    num=3096, title='得到更多分数的最少关卡数目', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='前缀和 · 1 记 2、0 记 −2',
    tags=['前后缀分解'],
    code='''
class Solution:
    def minimumLevels(self, possible: List[int]) -> int:
        # s = cnt1 - cnt0 = cnt1 - (n - cnt1) = cnt1 * 2 - n
        s = sum(possible) * 2 - len(possible)
        pre = 0
        for i, x in enumerate(possible[:-1]):
            pre += 2 if x else -2
            if pre > s:
                return i + 1
        return -1
''',
    call='Solution().minimumLevels([1,0,1,1,1])',
    expect=4,
    views=[
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='array', var='possible', pointers={'i': 'blue'}, window=('0', 'i'), h=250,
             label='possible（1 = 简单，0 = 困难）',
             dim=lambda S, i, v: 'i' in S and i > S['i'],
             color=lambda S, i, v: ('green' if v else 'pink') if 'i' in S and i <= S['i'] else None),
    ],
    watch=['s', 'pre', ('i', 'i', 'blue'), 'x'],
    max_steps=60,
    captions={
        's = sum': '`s` = 全部关卡的总得分：`cnt1 × 2 − n` = =={s}==（1 个 +1，0 个 −1）',
        'pre = 0': '`pre` 是 Alice 已打关卡得分的 2 倍，从 0 开始',
        'for i, x': '枚举 Alice 打到第 `{i}` 关（`{x}` 表示{"简单" if x else "困难"}）；==最后一关留给 Bob==，所以切片 `[:-1]`',
        'pre += 2 if x else -2': '`x = {x}` → `pre` {"+2" if x else "−2"}，变成 =={pre}==',
        'if pre > s': '`pre = {pre}` 是 Alice 得分的 2 倍，`pre > s` 就是 Alice > 剩余（Bob）→ {"==成立==" if pre > s else "不成立，再多打一关"}',
        'return i + 1': 'Alice 打了前 `{i + 1}` 关就比 Bob 高 → 返回 =={i + 1}==',
        'return -1': '所有前缀都不够 → `-1`',
    },
    cards=dict(
        one_liner='0 当 −1，找最短前缀，使 pre > 剩余和',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`possible[i]` 为 1 得 1 分，为 0 扣 1 分；Alice 先按顺序打一个前缀，Bob 打剩下的',
                 '求 Alice 得分严格大于 Bob 的最短前缀长度，两人都至少打 1 关，没有则 `-1`',
                 '示例：`[1,0,1,0]` → `1`；本视频：`[1,0,1,1,1]` → `4`'],
        quote='把 0 视作 −1，找一个最短前缀，其元素和大于剩余元素和。……即 pre·2 > s',
        quote_src='—— 灵茶山艾府题解',
        idea=['总和 `s`，前缀和 `pre`，剩余就是 `s − pre`',
              '`pre > s − pre` 等价于 `pre×2 > s`',
              '把 1 记作 2、0 记作 −2，就不用再乘 2'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`possible[:-1]`：Bob 至少要打 1 关，不能枚举到最后一个',
                 '`s = sum × 2 − n`：1 的个数 ×2 − 总数，等价于 cnt1 − cnt0 的 2 倍',
                 '同类：DP 题单里的「前后缀分解」'],
    ),
)
