CONFIG = dict(
    num=2981, title='找出出现至少三次的最长特殊子字符串 I', difficulty='Medium', category='字符串',
    author='yiduobo', technique='双指针分段 · 逐字符取最长三段',
    tags=[],
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
    call='Solution().maximumLength("aaaabbbabb")',
    expect=2,
    views=[
        dict(type='text', size=26, fn=lambda S: (f"这一段是 `s[{S['p']}:{S['q']+1}]` = `{S['s'][S['p']:S['q']+1]}`，长度 {S['q']-S['p']+1}" if 'q' in S and 'p' in S and S['_line'] <= 15 and 'char' not in S
                                                  else (f"字母 `{S['char']}` 的段长（降序）：`{S['length_list']}`" if 'length_list' in S else '先把每个字母的连续段长度收集起来'))),
        dict(type='string', var='s', label='s（蓝 = p，粉 = q，黄色 = 当前这一段）', cell=70, pointers={'p': 'blue', 'q': 'pink'}, h=170,
             color=lambda S, k, v: 'yellow' if 'p' in S and 'q' in S and 'char' not in S and S['p'] <= k <= S['q'] else None),
        dict(type='map', var='length_dict', label='length_dict：字母 → 各段长度', fmt=lambda k, v: f'{k}: {v}', h=200),
        dict(type='array', var='length_list', label='length_list（降序）', cell=84, h=160),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink'), ('res', 'res', 'green')],
    captions={
        'length_dict = {}': '`length_dict` 按字符收集所有连续段的长度',
        'p = 0': '`p` 是当前这一段的起点',
        'while p < len(s)': lambda S, B, r: (f'`p = {S.p} < {len(S.s)}`，还有字符没处理' if S.p < len(S.s) else f'`p = {S.p}` 走到末尾 → 分段结束：`{S.length_dict}`'),
        'q = p': '`q` 从 `p` 出发，向右找这一段的末尾',
        'while q + 1 < len(s)': lambda S, B, r: ((f"`s[{S.q+1}] = '{S.s[S.q+1]}'` == `s[{S.q}]` → 同一段，`q` 继续右移") if S.q + 1 < len(S.s) and S.s[S.q+1] == S.s[S.q] else f'下一个字符和当前不同（或到头了）→ 这一段到 `q = {S.q}` 结束'),
        'q += 1': '`q` → `{q}`',
        'if s[p] not in length_dict': lambda S, B, r: (f"`'{S.s[S.p]}'` 第一次出现，先建一个空列表" if S.s[S.p] not in S.length_dict else f"`'{S.s[S.p]}'` 之前出现过，直接追加"),
        'length_dict[s[p]] = []': '为字母 `{s[p]}` 建空列表',
        'length_dict[s[p]].append': "字母 `'{s[p]}'` 这一段长度 `q-p+1 = {q-p+1}` → `{length_dict[s[p]]}`",
        'p = q + 1': '跳到下一段起点：`p` → `{p}`',
        'res = 0': '`res` 记录答案，0 表示还没有',
        'for char in length_dict': lambda S, B, r: (f"考察字母 `'{S.char}'`" if 'char' in S and S.get('char') != B.get('char') else '所有字母考察完了'),
        'length_list = sorted': '把 `{char}` 的段长从大到小排：`{length_list}`',
        'res = max(res, length_list[0] - 2)': '==最长的一段切三份==：`length_list[0]-2 = {length_list[0]-2}` → `res = {res}`',
        'if len(length_list) > 1': lambda S, B, r: (f'有 `{len(S.length_list)}` 段，至少两段，可以看最长和次长' if len(S.length_list) > 1 else '只有一段，没有次长'),
        'if length_list[1] == length_list[0]': lambda S, B, r: ('最长和次长相等 → 只能切出 4 个“最长-1”的子串' if S.length_list[1] == S.length_list[0] else '最长比次长长 → 最长段里至少能切出两个“次长”长度的子串'),
        'res = max(res, length_list[0] - 1)': '两段一样长 `{length_list[0]}`：各取两个长为 `{length_list[0]-1}` → `res = {res}`',
        'res = max(res, length_list[1])': '最长段出两个、次长段出一个，长度都是 `{length_list[1]}` → `res = {res}`',
        'if len(length_list) > 2': lambda S, B, r: (f'有 `{len(S.length_list)}` 段，至少三段' if len(S.length_list) > 2 else '不足三段，跳过第三条规则'),
        'res = max(res, length_list[2])': '三段各取一个第三长的长度 `{length_list[2]}` → `res = {res}`',
        'if res == 0': lambda S, B, r: ('`res == 0`：没有出现三次的特殊子串' if S.res == 0 else f'`res = {S.res}`，找到了'),
        'res = -1': '返回 `-1`',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='先分段收集长度，再按“最长一段、两段、三段”三种情况更新',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['特殊字符串只由同一个字符组成。求在 `s` 中==至少出现三次==的最长特殊子串长度，没有返回 `-1`',
                 '示例：`"aaaa"` → `2`；`"abcdef"` → `-1`；`"abcaba"` → `1`',
                 '本视频：`"aaaabbbabb"` → `2`'],
        quote='对于一个长度为k的由相同字符构成的子串，可以拆除三个长度为k - 2的子串。更进一步的，其也可以提供两个长度为k - 1的子串以及一个长度为k的子串。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历，用 `p`、`q` 找出每段相同字符，按字符收集长度',
              '最长段拆三份：长度 `最长-2`；有两段时看最长和次长是否相等',
              '有三段时，第三长的长度一定可行'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '两段相等取 `最长-1`，否则取次长；顺序不能搞反',
                 '`len(length_list)` 不够时要先判断再访问下标',
                 '原文本身可直接在 Python 3 运行，未做修改',
                 '对比灵神：灵神补两个 0 免去特判，这里用 `if len(...)` 分情况'],
    ),
)
