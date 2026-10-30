CONFIG = dict(
    num=408, title='有效单词缩写', difficulty='Easy', category='双指针',
    author='yiduobo', technique='遍历缩写串 + 原串指针',
    code='''
class Solution(object):
    def validWordAbbreviation(self, word, abbr):

        p = 0
        n = len(word)

        now = 0
        for char in abbr:
            if char >= '0' and char <= '9':
                if now == 0 and char == '0':
                    return False
                now = now * 10 + int(char)
            else:
                if now > 0:
                    p += now
                    now = 0
                
                if p >= n or word[p] != char:
                    return False
                p += 1

        if now > 0:
            p += now
        
        return p == n
''',
    call='Solution().validWordAbbreviation("substitution", "s10n")',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: (f"缩写里的数字 `now = {S['now']}`：等着当作要跳过的长度" if S.get('now') else '`now = 0`：当前没有攒着的数字') if 'now' in S else '', size=26),
        dict(type='string', var='abbr', label='abbr（缩写）', cell=84),
        dict(type='string', var='word', label='word（原串，p 指向下一个待匹配位置）', cell=70, pointers={'p': 'pink'},
             dim=lambda S, i, v: 'p' in S and i < S['p']),
    ],
    watch=[('char', 'char', 'blue'), ('p', 'p', 'pink'), ('now', 'now', 'cyan'), ('n', 'n')],
    captions={
        'p = 0': '`p` 记录原串中==下一个==要和缩写匹配的下标',
        'n = len(word)': '`n = {n}`，`p` 不能超过它',
        7: '`now` 攒着连续的数字，表示要跳过的字符数',
        "if char >= '0'": lambda S, B, r: (f"`'{S.char}'` 是数字" if '0' <= S.char <= '9' else f"`'{S.char}'` 是字母"),
        "if now == 0 and char == '0'": lambda S, B, r: ('数字以 `0` 开头 → ==不合法==' if S.now == 0 and S.char == '0' else f'`now = {S.now}`，不是前导零，合法'),
        'now = now * 10 + int(char)': '把这一位接到数字后面：`now = {B.now}×10 + {char}` = =={now}==',
        'if now > 0': lambda S, B, r: (f'前面攒了数字 `now = {S.now}` → 原串跳过这么多字符' if S.now > 0 else '没有攒着的数字，直接比较字母'),
        'p += now': '`p` 向后跳 `{B.now}` 位 → =={p}==',
        16: '数字用完，清零',
        'if p >= n or word[p] != char': lambda S, B, r: (f'`p = {S.p} >= n = {S.n}` 越界 → False' if S.p >= S.n else
                                                         (f"`word[{S.p}] = '{S.word[S.p]}'` 和 `'{S.char}'` ==相同== → 匹配" if S.word[S.p] == S.char else f"`word[{S.p}] = '{S.word[S.p]}'` ≠ `'{S.char}'` → 失败")),
        'p += 1': '字母匹配上了，`p` 前进一位 → {p}',
        'if now > 0:': lambda S, B, r: (f'缩写以数字结尾，`now = {S.now}` 还没用' if S.now > 0 else '缩写以字母结尾，没有剩余数字'),
        'return p == n': lambda S, B, r: f'`p = {S.p}`，`n = {S.n}`：原串=={"正好用完" if S.p == S.n else "没有对齐"}== → `{r}`',
    },
    cards=dict(
        one_liner='缩写里的数字就是要跳过的长度，用指针 p 在原串里对齐',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['缩写把不相邻的若干子串替换成它们的长度；数字不能有前导 0',
                 '判断缩写 `abbr` 能否对应原串 `word`',
                 '示例：`word = "substitution"`，`abbr = "s10n"` → `true`'],
        quote='缩写中出现的数字唯一地代表了某个子串的长度，因此可以遍历缩写子串，然后使用一个变量p记录原串中下一个与缩写子串匹配的下标位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['遇到字母：和 `word[p]` 比较，相同则 `p += 1`',
              '遇到数字：用 `now` 拼出完整的数，下一个字母前把 `p` 向后移动 `now` 位',
              '中途不匹配或 `p` 越界返回 False；扫完 `p` 必须正好等于 `n`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：数字不能以 `0` 开头；多位数字要拼起来再跳',
                 '易错：缩写以数字结尾时，循环后还要把最后的 `now` 加到 `p` 上',
                 '最后必须 `p == n`，不然原串还有没匹配的字符'],
    ),
)
