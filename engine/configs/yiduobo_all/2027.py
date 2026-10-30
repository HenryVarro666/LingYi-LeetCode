CONFIG = dict(
    num=2027, title='转换字符串的最少操作次数', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='最左侧的 X 必须操作 · 跳三格',
    tags=['灵神题单', '贪心与思维', '难度分 1346'],
    code='''
class Solution(object):
    def minimumMoves(self, s):

        p = 0
        res = 0
        while p < len(s):
            if s[p] == 'X':
                res += 1
                p += 3
            else:
                p += 1
        
        return res
''',
    call="Solution().minimumMoves('XXOXOXXXO')",
    expect=3,
    views=[
        dict(type='text', fn=lambda S: f"指针在 `{S['p']}`" + (f"：`s[{S['p']}] = {S['s'][S['p']]}`" if S['p'] < len(S['s']) else '：已越过末尾') if 'p' in S else '', size=30),
        dict(type='string', var='s', pointers={'p': 'blue'}, label='s', h=300,
             color=lambda S, i, v: ('green' if i < S['p'] and v == 'X' else None) if 'p' in S else None,
             dim=lambda S, i, v: 'p' in S and i < S['p'] and v == 'O'),
    ],
    watch=[('p', 'p', 'blue'), ('res', 'res', 'green')],
    captions={
        'p = 0': '从最左边开始，`p = {p}`',
        'res = 0': '`res` 记录操作次数',
        "if s[p] == 'X'": lambda S, B, r: (f"`s[{S.p}] = 'X'`：它是当前最左侧的 X，==必须有一次操作盖住它==" if S.s[S.p] == 'X' else f"`s[{S.p}] = 'O'`：不用管，看下一个"),
        'res += 1': '操作一次，让它从这里开始盖三格 → `res` = =={res}==',
        'p += 3': '这三格都变成 O 了，直接跳过 → `p` = {p}',
        'p += 1': '这格已经是 O，`p` → {p}',
        'return res': '扫完了，最少操作 `{res}` 次',
    },
    cards=dict(
        one_liner='最左侧的 X 必须处理，那就让这次操作尽量往右盖',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次操作选三个连续字符，全部变成 `O`',
                 '求把 `s` 全变成 `O` 的最少操作次数',
                 '示例：`XXOXOXXXO` → `3`'],
        quote='对于当前字符串中最左侧的X，必须执行一次操作。为了使得这次操作尽可能惠及到后面的位置，那么现在应该将从该位置开始的三个字符变为O。',
        quote_src='—— yiduobo 题解原文',
        idea=['最左侧的 X 左边没有别的 X，只能靠包含它的操作',
              '让操作从它开始，向右盖三格，惠及最多后面的位置',
              '遇到 X：答案加一、位置跳三格；否则只前进一格'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '操作覆盖越过末尾也没关系，循环条件 `p < len(s)` 自然结束',
                 '易错点：遇到 X 跳 3 格，不是 1 格',
                 '同类题：灵神题单 §1.4 从最左开始贪心'],
    ),
)
