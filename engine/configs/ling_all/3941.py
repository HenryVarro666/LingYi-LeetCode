CONFIG = dict(
    num=3941, title='密码强度', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希集合去重 + 分类累加',
    tags=[],
    code='''
class Solution:
    def passwordStrength(self, password: str) -> int:
        vis = set()
        ans = 0
        for ch in password:
            if ch in vis:
                continue
            vis.add(ch)
            if ch.islower():
                ans += 1
            elif ch.isupper():
                ans += 2
            elif ch.isdigit():
                ans += 3
            else:
                ans += 5
        return ans
''',
    call='Solution().passwordStrength("bbB11#a")',
    expect=12,
    views=[
        dict(type='string', var='password', h=200,
             color=lambda S, i, v: ('green' if v in S.get('vis', ()) else None)),
        dict(type='set', var='vis', h=200, fmt=lambda x: x),
        dict(type='text', size=36, h=110, fn=lambda S: f"当前得分 `{S.get('ans', 0)}`：小写 1 · 大写 2 · 数字 3 · 特殊 5"),
    ],
    watch=['ch', ('ans', 'ans', 'green')],
    captions={
        'for ch in password': '取下一个字符 `ch = {ch!r}`',
        'if ch in vis': '`{ch!r}` 在 `vis` 里吗？→ {"==在，已算过分，跳过==" if ch in vis else "不在，第一次见"}',
        'continue': '重复字符不再计分，直接看下一个',
        'vis.add(ch)': '记下 `{ch!r}`：以后再遇到就不重复算分',
        'if ch.islower()': '`{ch!r}.islower()` → {ch.islower()}',
        'elif ch.isupper()': '不是小写；`{ch!r}.isupper()` → {ch.isupper()}',
        'elif ch.isdigit()': '不是字母；`{ch!r}.isdigit()` → {ch.isdigit()}',
        'ans += 1': '小写字母 +1 → `ans = {ans}`',
        'ans += 2': '大写字母 +2 → `ans = {ans}`',
        'ans += 3': '数字 +3 → `ans = {ans}`',
        'ans += 5': '剩下只能是 `!@#$` 特殊字符 +5 → `ans = {ans}`',
        'return ans': '密码强度 =={ans}==',
    },
    cards=dict(
        one_liner='用哈希集合给字符去重，每个不同字符按类别计一次分',
        complexity='时间 `O(n)`，空间 `O(min(n, |Σ|))`',
        problem=['小写 1 分、大写 2 分、数字 3 分、`!@#$` 特殊字符 5 分',
                 '==同一个字符只计一次分==，求密码强度',
                 '本视频：`"bbB11#a"` → `1+2+3+5+1 = 12`'],
        quote='注意同一个字符只能算一次得分。可以用一个 vis 哈希集合（或者布尔数组）标记遍历过的字符。',
        quote_src='—— 灵茶山艾府题解',
        idea=['遍历 `password`，已在 `vis` 里的字符直接 `continue`',
              '第一次见到才 `vis.add`，再用 `islower / isupper / isdigit` 判类别',
              '都不是就只剩特殊字符，+5'],
        summary=['时间 `O(n)`，空间 `O(|Σ|)`，字符集大小 128',
                 '易错点：重复字符不能再加分，`b` 和 `B` 是两个不同的字符',
                 '也可以用长度 128 的布尔数组代替集合'],
    ),
)
