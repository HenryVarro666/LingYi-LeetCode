CONFIG = dict(
    num=2957, title='消除相邻近似相等字符', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='从左到右贪心 · 改右边那个',
    tags=['灵神题单', '难度分 1430'],
    code='''
class Solution:
    def removeAlmostEqualCharacters(self, s: str) -> int:
        ans = 0
        i, n = 1, len(s)
        while i < n:
            if abs(ord(s[i - 1]) - ord(s[i])) <= 1:
                ans += 1
                i += 2
            else:
                i += 1
        return ans
''',
    call='Solution().removeAlmostEqualCharacters("zyxyxyz")',
    expect=3,
    views=[
        dict(type='text', size=34, fn=lambda S: (f"比较 `{S['s'][S['i']-1]}` 和 `{S['s'][S['i']]}`：差 =={abs(ord(S['s'][S['i']-1]) - ord(S['s'][S['i']]))}==" + ('，近似相等 → 改右边' if abs(ord(S['s'][S['i']-1]) - ord(S['s'][S['i']])) <= 1 else '，没问题') if 'i' in S and 1 <= S['i'] < len(S['s']) else '')),
        dict(type='string', var='s', pointers={'i': 'blue'}, h=300,
             color=lambda S, k, v: 'orange' if 'i' in S and k == S['i'] - 1 and S['i'] < len(S['s']) else None),
    ],
    watch=[('i', 'i', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'i, n = 1': '从 `i = 1` 开始，每次看 `s[i-1]` 和 `s[i]` 这一对',
        'while i < n': lambda S, B, r: (f'`i = {S.i} < n = {S.n}`：还有一对没看' if S.i < S.n else f'`i = {S.i} >= n = {S.n}`：看完了'),
        'if abs': '近似相等 = 相同或字母表相邻，即 `|差| <= 1`：`{abs(ord(s[i-1]) - ord(s[i]))} <= 1`',
        'ans += 1': '==必须改一个==：改右边那个，这样 `s[i]` 和 `s[i+1]` 也不会再近似相等。`ans` → {ans}',
        'i += 2': '右边已被改成"和谁都不近似"的字母，`s[i]` 与 `s[i+1]` 这一对不用看了 → `i` 直接跳 2，到 {i}',
        'i += 1': '这一对没问题，看下一对：`i` → {i}',
        'return ans': '一共改了 `{ans}` 次',
    },
    cards=dict(
        one_liner='发现近似相等就改右边那个，顺手跳过下一对',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['近似相等：两个字符相同，或在字母表中相邻',
                 '每次可把任意一个字符改成任意小写字母，求让所有相邻字符都不近似相等的最少次数',
                 '示例：`"zyxyxyz"` → `3`'],
        quote='如果改 s[i-1]，那么 s[i] 和 s[i+1] 是可能近似相等的，但如果改 s[i]，就可以避免 s[i] 和 s[i+1] 近似相等。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从左往右扫，遇到一对近似相等就必须改一个',
              '改左边：右边那个还可能和它后面的字符冲突',
              '==改右边==：能改成和左右都不近似的字母，所以下一对直接跳过'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '命中后 `i += 2` 而不是 `+= 1`，因为被改的字符不会再冲突',
                 '没命中才 `i += 1`；下标从 1 开始比较 `s[i-1]`',
                 '相似题：2560 打家劫舍 IV'],
    ),
)
