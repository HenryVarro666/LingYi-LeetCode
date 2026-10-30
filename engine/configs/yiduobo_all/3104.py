CONFIG = dict(
    num=3104, title='找出最长的超能字符串', difficulty='Hard', category='字符串',
    author='yiduobo', technique='首末位置 · 按首次出现顺序枚举', tags=[],
    code='''
class Solution(object):
    def maxSubstringLength(self, s):

        first = {}
        last = {}
        freq = {}
        for index, char in enumerate(s):
            if char not in first:
                first[char] = index
                last[char] = index
                freq[char] = 1
            else:
                last[char] = index
                freq[char] += 1
        
        sorted_char = sorted(first.keys(), key=lambda d:first[d])
        res = -1
        for i, char in enumerate(sorted_char):
            left, right, cnt = first[char], last[char], freq[char]
            if cnt < len(s) and cnt == right - left + 1:
                res = max(res, cnt)
            for j in range(i + 1, len(sorted_char)):
                right = max(right, last[sorted_char[j]])
                cnt += freq[sorted_char[j]]
                if cnt < len(s) and cnt == right - left + 1:
                    res = max(res, cnt)
            
        return res
''',
    call='Solution().maxSubstringLength("abcbdd")',
    expect=5,
    setup='',
    views=[
        dict(type='string', var='s', h=170,
             color=lambda S, i, v: ('green' if 'left' in S and 'right' in S and 'sorted_char' in S and S['left'] <= i <= S['right'] else None)),
        dict(type='map', var='first', h=110, label='first 首次位置', fmt=lambda k, v: str(v)),
        dict(type='map', var='last', h=110, label='last 末次位置', fmt=lambda k, v: str(v)),
        dict(type='map', var='freq', h=110, label='freq 出现次数', fmt=lambda k, v: str(v)),
        dict(type='text', size=30, fn=lambda S: (f"窗口 `[{S['left']}, {S['right']}]` 长 `{S['right']-S['left']+1}`，其中字符总数 `cnt = {S['cnt']}` → " + ('==相等，合法==' if S['cnt'] == S['right']-S['left']+1 else '不等，还夹着别的字符')) if 'cnt' in S and 'left' in S and 'right' in S else ''),
    ],
    watch=[('char', 'char', 'blue'), 'left', 'right', 'cnt', ('res', 'res', 'green')],
    skip=['first[char] = index', 'last[char] = index', 'freq[char] = 1'],
    max_steps=80,
    captions={
        'first = {}': '`first / last / freq` 分别记每种字符的首次位置、末次位置、出现次数',
        'for index, char in enumerate': '`index = {index}`，字符 `{char}`',
        'if char not in first': lambda S, B, r: (f"`{S.char}` 第一次出现 → 登记首次位置" if S.char not in S.first else f"`{S.char}` 之前出现过"),
        'freq[char] += 1': '`{char}` 又出现了：末次位置 `{last[char]}`，次数 `{freq[char]}`',
        'sorted_char = sorted': '字符按首次出现位置排序：`{sorted_char}`，作为窗口左端点的候选顺序',
        'res = -1': '`res = -1`：没有合法子串时返回 -1',
        'for i, char in enumerate(sorted_char)': lambda S, B, r: ('每个字符都当过左端了，循环结束' if B.get('i') == S.i and 'i' in B else f"枚举左端点字符 `{S.char}`（从它第一次出现的位置开始）"),
        'left, right, cnt =': '窗口从 `{char}` 第一次出现 `{left}` 到最后一次 `{right}`，字符总数 `cnt = {cnt}`',
        'if cnt < len(s) and': lambda S, B, r: (f"窗口长 `{S.right-S.left+1}`，窗口内这些字符总数 `{S.cnt}`；" +
                                                ('相等说明字符全在窗口内，且 `cnt < len(s)` 不是整个 s' if S.cnt == S.right-S.left+1 and S.cnt < len(S.s)
                                                 else ('等于整个 s，不允许' if S.cnt == S.right-S.left+1 else '不等：中间夹了别的字符，不合法'))),
        'res = max(res, cnt)': '合法 → `res = max({B.res}, {cnt}) = {res}`',
        'for j in range': lambda S, B, r: (f"`j = {S.j}`：尝试把后面的字符 `{S.sorted_char[S.j]}` 并入" if (S.j == S.i + 1 and S.cnt == S.freq[S.char]) or B.get('j') != S.j
                                           else '后面的字符都试过了，这一轮结束'),
        'right = max(right': '纳入 `{sorted_char[j]}` 后右端要扩到它的末次位置：`right` = {right}',
        'cnt += freq': '再把它的 `{freq[sorted_char[j]]}` 个字符计入：`cnt` = {cnt}',
        'return res': '最长合法长度：=={res}==',
    },
    cards=dict(
        one_liner='按首次出现顺序枚举左端字符，逐个并入后面的字符',
        complexity='时间 `O(26²)`，空间 `O(26)`',
        problem=['小写字符串 `s`，找最长子串 `t`（`t` 不是 `s` 本身）', '`t` 里每种字符都只出现在 `t` 中，`s` 里其它位置不能再有',
                 '没有则返回 `-1`；本视频：`"abcbdd"` → `5`'],
        quote='只有当t的长度等于其中各种字符出现的总数时，t才是一个合法的字符串。',
        quote_src='—— yiduobo 题解原文',
        idea=['记每种字符的首次位置、末次位置、总次数', '左端必从某字符首次位置开始；右端至少扩到它的末次位置',
              '窗口长度 == 窗口内字符总数，才没有夹带外来字符'],
        summary=['时间 `O(26²)`，空间 `O(26)`', '`cnt < len(s)` 排除整个 s，易漏',
                 '后面的字符按 sorted_char 顺序并入，因此只要往后扫',
                 '原文题面缺失，题意按题解和原题理解；代码原样可在 Python 3 运行'],
    ),
)
