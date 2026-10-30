CONFIG = dict(
    num=3760, title='不同首字母的子字符串数目', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='不同字母个数 · 位运算集合',
    tags=['灵神题单', '难度分 1364'],
    code='''
class Solution:
    def maxDistinct(self, s: str) -> int:
        st = 0
        for c in s:
            st |= 1 << (ord(c) - ord('a'))
        return st.bit_count()
''',
    call='Solution().maxDistinct("abacbd")',
    expect=4,
    views=[
        dict(type='string', var='s', h=200, label='s（绿色 = 该字母已在集合 st 里）',
             color=lambda S, i, v: 'green' if 'st' in S and (S['st'] >> (ord(v) - 97)) & 1 else None),
        dict(type='text', fn=lambda S: ('集合 st = `' + ''.join(chr(97 + k) for k in range(26) if (S['st'] >> k) & 1) + f"`　二进制 `{S['st']:b}`") if 'st' in S else ''),
        dict(type='text', fn=lambda S: f"当前字母 `{S['c']}` → 第 {ord(S['c'])-97} 位" if 'c' in S else ''),
    ],
    watch=['c', 'st', ('不同字母数', 'bin(st).count("1") if "st" in dir() else 0', 'green')] if False else ['c', 'st'],
    captions={
        'st = 0': '`st = 0`：用一个二进制数当集合，初始为空',
        'st |= ': '字母 `{c}` 对应第 `{ord(c) - ord("a")}` 位：把这一位置 1，已有的字母不会重复计数 → `st = {st}`',
        'return': '`st` 里 1 的个数 = 不同字母个数 = =={ret}==，每个字母首次出现前切一刀就能取到',
    },
    cards=dict(
        one_liner='答案就是 s 里不同字母的个数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 `s` 切成若干子串，每个子串的首字母互不相同',
                 '求最多能切成几段',
                 '示例：`"abab"` → `2`，`"abcd"` → `4`，`"aaaa"` → `1`'],
        quote='答案的理论最大值为 s 中的不同字母个数。可以达到理论最大值吗？可以，在每种字母首次出现的位置前切一刀即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每段首字母都不同 → 段数不会超过字母种数',
              '每种字母首次出现处切一刀 → 恰好取到上界',
              '优化：用整数的二进制位当集合，`|=` 加入字母，`bit_count()` 数个数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先想上界，再构造方案证明能取到',
                 '优化前写法是 `len(set(s))`，位运算版省去了哈希表',
                 '同类：集合论到位运算的常见技巧'],
    ),
)
