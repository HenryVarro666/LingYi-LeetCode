CONFIG = dict(
    num=3803, title='统计残差前缀', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='哈希集合 + 提前退出',
    tags=[],
    code='''
class Solution:
    def residuePrefixes(self, s: str) -> int:
        st = set()
        ans = 0
        for i, ch in enumerate(s):
            st.add(ch)
            if len(st) == 3:
                break
            if len(st) == (i + 1) % 3:
                ans += 1
        return ans
''',
    call="Solution().residuePrefixes('abbaac')",
    expect=3,
    views=[
        dict(type='string', var='s', h=200, cell=90, pointers={'i': 'blue'},
             window=('0', 'i'),
             label='s（框 = 当前前缀）'),
        dict(type='set', var='st', h=200, fmt=lambda x: str(x), label='st：前缀里出现过的字母'),
        dict(type='text', size=32, fn=lambda S: (f"不同字符 `{len(S['st'])}`  vs  长度模 3 = `({S['i']}+1) % 3` = `{(S['i'] + 1) % 3}`" if 'i' in S and 'st' in S else '')),
    ],
    watch=['i', ('len(st)', 'len(st)', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'st.add': '把 `{ch}` 加入集合，前缀 `s[:{i+1}]` 有 =={len(st)}== 个不同字母',
        'len(st) == 3': lambda S, B, r: (f'集合大小到 3：而 `(i+1)%3` 最大才 2，往后永远不可能相等 → ==提前 break==' if len(S.st) == 3
                                         else f'`len(st) = {len(S.st)}` < 3，还有可能满足，继续'),
        'len(st) == (i + 1) % 3': lambda S, B, r: (f'`{len(S.st)} == {(S.i + 1) % 3}` → 成立，是残差前缀' if len(S.st) == (S.i + 1) % 3
                                                   else f'`{len(S.st)} != {(S.i + 1) % 3}` → 不是残差前缀'),
        'ans += 1': '前缀长度 `{i+1}`，不同字符数相同 → `ans` = =={ans}==',
    },
    cards=dict(
        one_liner='边遍历边用集合数不同字母，数到 3 就收工',
        complexity='时间 `O(n)`，空间 `O(min(n, 26))`',
        problem=['前缀的「不同字符数」等于「前缀长度 % 3」，称为残差前缀',
                 '求 `s` 中残差前缀的个数',
                 '示例：`abc` → `2`；`dd` → `1`'],
        quote='从左到右遍历 s，用一个哈希集合保存遍历过的字母。如果哈希集合的大小等于遍历过的字母个数模 3，即 (i+1) mod 3，那么把答案加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['集合里始终是当前前缀的字母，所以大小就是不同字符数',
              '前缀长度是 `i + 1`，和 `(i+1) % 3` 比较即可',
              '优化：`(i+1) % 3 < 3`，集合大小一旦到 3 就永远不会再相等，直接 `break`'],
        summary=['时间 `O(n)`，空间 `O(min(n, 26))`',
                 '易错：长度是 `i + 1` 不是 `i`',
                 '方法二用二进制数当集合：`st |= 1 << (ord(ch) - ord(\'a\'))`，`st.bit_count()` 数不同字母，思路相同',
                 '本视频演示方法一'],
    ),
)
