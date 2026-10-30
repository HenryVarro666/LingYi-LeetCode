def _txt(S):
    if 'c0' not in S:
        return ''
    n = len(S['s'])
    c0 = S['c0']
    t = f"`n = {n}`，0 有 =={c0}== 个，1 有 =={n - c0}== 个"
    if 'c1' in S:
        t += f"；最多保留 1 的个数方案：`c1 = {S['c1']}`"
    return t


CONFIG = dict(
    num=3922, title='使二进制字符串连贯的最少翻转次数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='分类讨论：全变 1 / 少留几个 1',
    tags=['灵神题单', '难度分 1759'],
    code='''
class Solution:
    def minFlips(self, s: str) -> int:
        c0 = s.count('0')
        c1 = len(s) - c0 - 1
        if s[0] == '1' and s[-1] == '1':
            c1 -= 1
        return min(c0, max(c1, 0))
''',
    call='Solution().minFlips("1010101")',
    expect=2,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='string', var='s', label='s', h=170,
             color=lambda S, i, v: ('green' if v == '1' else None)),
        dict(type='text', fn=lambda S: ('两端都是 1 → 可以多留一个 1：`c1 -= 1`' if S.get('s') and S['s'][0] == '1' and S['s'][-1] == '1' and 'c1' in S
                                         else ('有 0 在端点 → 至多留一个 1' if 'c1' in S else '')), h=60),
    ],
    watch=['c0', 'c1', ('答案候选', 'min(c0, max(c1, 0)) if "c1" in S else ""', 'green')],
    captions={
        'c0 = s.count': '`c0` = 0 的个数 = =={c0}==；全部翻成 1，代价就是 `c0`',
        'c1 = len(s)': '至多保留一个 1，其余 1 全翻成 0：代价 `n - c0 - 1` = =={c1}==',
        "if s[0] == '1'": lambda S, B, r: ('两端 `s[0]`、`s[-1]` 都是 1 → 两端的 1 可以一起保留' if S.s[0] == '1' and S.s[-1] == '1'
                                         else '端点有 0 → 只能留一个 1，否则会出现 011 或 110'),
        'c1 -= 1': '多保留一个 1：`c1` 减 1 → =={c1}==',
        'return min': '`min(c0, max(c1, 0))` = `min({c0}, {max(c1, 0)})` = =={ret}==；`max(.., 0)` 兼容没有 1 的情况',
    },
    cards=dict(
        one_liner='修改后的串：要么全是 1，要么最多留一两个 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制串 `s`，翻转任意字符，使它不含子序列 `011` 和 `110`',
                 '求最少翻转次数',
                 '示例：`"1010"` → `1`；`"0110"` → `1`；`"1000"` → `0`'],
        quote='不能包含子序列 110 或 011，意味着对于修改后的 s 中的任意一个 0，其左侧不能有超过一个 1，右侧也不能有超过一个 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先想简化版：禁止 `01`、`10` → 只能全 0 或全 1，由此想到「全 1」方向',
              '全变 1：没有 0 就万事大吉，代价 `c0`',
              '端点是 0：至多留一个 1；两端都是 1：可以留这两个 1，其余变 0'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`max(c1, 0)` 是为了兼容没有 1（或 n=1）时算出 -1',
                 '三种情况取最小：全 1 / 留一个 1 / 留两端的 1',
                 '变形题：禁止 `010`、`101` 怎么做'],
    ),
)
