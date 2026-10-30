def _txt(S):
    ll = S.get('length_list')
    if ll is None or S.get('_line', 0) < 19:
        return ''
    ll = list(ll)
    r = S.get('res', 0)
    return f'`{S["char"]}` 的长度（降序）`{ll}`，目前 `res = {r}`'


CONFIG = dict(
    num=2982, title='找出出现至少三次的最长特殊子字符串 II', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='按字符收集长度 · 最长拆三份',
    tags=['二分算法', '贪心与思维', '难度分 1773'],
    code='''
class Solution(object):
    def maximumLength(self, s):

        length_dict = {}
        p = 0
        while p < len(s):
            q = p
            while q + 1 < len(s) and s[q + 1] == s[q]:
                q += 1
            
            if s[p] not in length_dict:
                length_dict[s[p]] = []
            length_dict[s[p]].append(q - p + 1)
            p = q + 1
        
        res = 0
        for char in length_dict:
            length_list = sorted(length_dict[char], reverse=True)
            res = max(res, length_list[0] - 2)
            if len(length_list) > 1:
                if length_list[1] == length_list[0]:
                    res = max(res, length_list[0] - 1)
                else:
                    res = max(res, length_list[1])
            if len(length_list) > 2:
                res = max(res, length_list[2])
        
        if res == 0:
            res = -1
        return res
''',
    call="Solution().maximumLength('aaaabbbabbaa')",
    expect=2,
    views=[
        dict(type='string', var='s', label='s（蓝 = p，粉 = q，框住当前连续段）', pointers={'p': 'blue', 'q': 'pink'}, window=('p', 'q'), cell=70, h=210),
        dict(type='map', var='length_dict', label='length_dict：字符 → 各段长度', fmt=lambda k, v: f"'{k}': {v}", h=170, font=34),
        dict(type='text', fn=_txt, size=30, h=90),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink'), ('char', 'char', 'purple'), ('res', 'res', 'green')],
    captions={
        'length_dict = {}': '`length_dict`：字符 → 它所有连续段的长度',
        'p = 0': '`p` 指向当前连续段的开头',
        'while p < len(s)': lambda S, B, r: (f'`p = {S.p} < {len(S.s)}`，还有字符没分段' if S.p < len(S.s) else f'`p = {S.p}` 走到末尾，全部分完段'),
        'q = p': '先让 `q = p`，向右找这一段的结尾',
        'while q + 1 < len(s)': lambda S, B, r: (f"`s[{S.q+1}] = '{S.s[S.q+1]}'` 和 `s[{S.q}]` 相同 → 段继续往右" if S.q + 1 < len(S.s) and S.s[S.q + 1] == S.s[S.q]
                                                   else '下一个字符不同（或到头）→ ==这一段结束=='),
        'q += 1': '`q` 右移到 {q}',
        'if s[p] not in length_dict': lambda S, B, r: (f"`'{S.s[S.p]}'` 还没有记录 → 先建空列表" if S.s[S.p] not in S.length_dict else f"`'{S.s[S.p]}'` 已有记录，直接追加"),
        'length_dict[s[p]] = []': '新建 `length_dict[{s[p]!r}] = []`',
        'append(q - p + 1)': "段长 `q − p + 1 = {q-p+1}` → `length_dict['{s[p]}'] = {length_dict[s[p]]}`",
        'p = q + 1': '`p` 跳到下一段开头 `{p}`',
        'res = 0': '`res` 保存目前最长的合法长度',
        'for char in length_dict': '逐个字符考察，现在是 `{char!r}`',
        'sorted(length_dict': '长度从大到小：`{length_list}`',
        'res = max(res, length_list[0] - 2)': '最长段 `{length_list[0]}` 可拆成三个长 `{length_list[0]}−2` 的子串 → `res = {res}`',
        'if len(length_list) > 1': lambda S, B, r: ('至少有两段，可以用前两名' if len(S.length_list) > 1 else '只有一段，没有第二名'),
        'if length_list[1] == length_list[0]': lambda S, B, r: (f'`{S.length_list[1]} == {S.length_list[0]}`：两段等长，只能凑出 4 个长 `{S.length_list[0]}−1` 的' if S.length_list[1] == S.length_list[0]
                                                                  else f'`{S.length_list[1]} ≠ {S.length_list[0]}`：最长段至少含两个长 `{S.length_list[1]}` 的，加上次长段共三个'),
        'res = max(res, length_list[0] - 1)': '等长 → 用 `{length_list[0]}−1` 更新 → `res = {res}`',
        'res = max(res, length_list[1])': '不等长 → 用次长 `{length_list[1]}` 更新 → `res = {res}`',
        'if len(length_list) > 2': lambda S, B, r: ('至少有三段，可以用第三名' if len(S.length_list) > 2 else '不足三段，跳过'),
        'res = max(res, length_list[2])': '三段各取一个长 `{length_list[2]}` 的 → `res = {res}`',
        'if res == 0': lambda S, B, r: ('`res == 0`：没有任何字符能出现三次' if S.res == 0 else f'`res = {S.res}` 不是 0，保留'),
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='一段长 k 的连续字符，可以切出三段长 k−2 的',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`s` 是小写字母串；特殊子串 = 全由同一个字符组成',
                 '求至少出现 ==三次== 的最长特殊子串长度，没有则 `-1`',
                 '示例：`"aaaa"` → `2`；`"abcdef"` → `-1`'],
        quote='对于一个长度为k的由相同字符构成的子串，可以拆除三个长度为k - 2的子串。更进一步的，其也可以提供两个长度为k - 1的子串以及一个长度为k的子串。',
        quote_src='—— yiduobo 题解原文',
        idea=['先一趟遍历，把相同字符的连续段按字符收集长度',
              '对每个字符：最长段拆三份用 `最长−2`',
              '有两段：等长用 `最长−1`，不等长用次长；有三段：用第三名'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '`res` 为 0 说明无解，要改成 `-1`',
                 '易错：两段等长时是 `长度−1`，不是次长',
                 '原文为 Python 2 风格，未改动代码，本题无需转换',
                 '对比灵神：灵神补两个 0 免判断，yiduobo 用 `len > 1/2` 逐一判断'],
    ),
)
