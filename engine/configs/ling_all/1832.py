def _bits(S):
    return [(S['m'] >> k) & 1 for k in range(26)] if 'm' in S else [0] * 26


CONFIG = dict(
    num=1832, title='判断句子是否为全字母句', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='26 位二进制掩码（Go 原文转写）',
    code='''
class Solution:
    def checkIfPangram(self, s: str) -> bool:
        m = 0
        for b in s:
            m |= 1 << (ord(b) - ord('a'))
        return m == (1 << 26) - 1
''',
    call='Solution().checkIfPangram("qwertyuiopasdfghjklzxcvbnm")',
    expect=True,
    views=[
        dict(type='string', var='s', label='s', cell=36, h=150),
        dict(type='array', var=_bits, label='m 的第 k 位（k = 0 对应 a，… 25 对应 z；1 = 出现过）', cell=36, h=190,
             color=lambda S, i, v: 'green' if v == 1 else None),
        dict(type='text', h=80, size=30,
             fn=lambda S: f"`m` = {S['m']}，全 26 位为 1 应等于 {(1 << 26) - 1}" if 'm' in S else ''),
    ],
    watch=[('b', 'b', 'blue'), ('m', 'm', 'green'), ('已出现字母数', 'bin(m).count("1")', 'orange')],
    captions={
        'm = 0': '`m` 当作 26 位的二进制集合，第 k 位表示第 k 个字母出现过，一开始全 0',
        'for b in s': lambda S, B, r: (f'看字母 `{S.b!r}`' if 'b' not in B or S.b != B.b else '字母都看完了'),
        'm |= 1': '`{b!r}` 对应第 `{ord(b) - ord("a")}` 位，把这一位置 1 → `m = {m}`，已有 `{bin(m).count("1")}` 种字母',
        'return': lambda S, B, r: (f'`m = {S.m}` 等于 `2^26 − 1 = {(1 << 26) - 1}` → 26 位全是 1，每个字母都出现过 → `True`'
                                   if r else f'`m = {S.m}` 不等于 `{(1 << 26) - 1}`，缺字母 → `False`'),
    },
    cards=dict(
        one_liner='用一个整数的 26 个二进制位，当作字母出现的集合',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['全字母句：英文 26 个小写字母每个至少出现一次',
                 '给纯小写字符串 `sentence`，判断它是不是全字母句',
                 '本视频：`"qwertyuiopasdfghjklzxcvbnm"` → `true`'],
        quote='m |= 1 << (b - \'a\') ……  return m == 1<<26-1',
        quote_src='—— 灵茶山艾府题解（Go 代码）',
        idea=['字母 `b` 映射到第 `b - a` 位，`m |= 1 << …` 把它标记为出现过',
              '全部 26 位都是 1 的整数是 `2^26 − 1`，`m` 等于它就说明 26 个字母都出现了'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python：`b - \'a\'` → `ord(b) - ord(\'a\')`',
                 '注意优先级：Go 里 `1<<26-1` 是 `(1<<26)-1`，Python 里要写成 `(1 << 26) - 1`',
                 '时间 `O(n)`，空间 `O(1)`',
                 '同类思路：小字符集的集合判断都可以用位掩码代替哈希集合'],
    ),
)
