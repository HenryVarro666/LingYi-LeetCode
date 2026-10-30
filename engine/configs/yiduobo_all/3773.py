CONFIG = dict(
    num=3773, title='最大等长连续字符组', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='分组遍历 + 哈希表计数',
    tags=['灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def maxSameLengthRuns(self, s):
        
        freq = {}
        p = 0
        while p < len(s):
            q = p + 1
            while q < len(s) and s[q] == s[p]:
                q += 1
            freq[q - p] = freq.get(q - p, 0) + 1
            p = q

        return max(freq.values())
''',
    call="Solution().maxSameLengthRuns('aabbbcdd')",
    expect=2,
    views=[
        dict(type='string', var='s', label='s（框 = 当前字符组 [p, q)）', pointers={'p': 'blue', 'q': 'pink'},
             window=('p', lambda S: S['q'] - 1), h=230, cell=100),
        dict(type='map', var='freq', label='freq（组长度 → 出现次数）', fmt=lambda k, v: f'长 {k}: {v} 组', h=180, font=32),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink')],
    captions={
        'freq = {}': '`freq`：键是==字符组的长度==，值是这种长度出现了几次',
        'p = 0': '`p` 指向当前字符组的开头',
        'while p < len(s)': lambda S, B, r: (f'`p = {S.p} < {len(S.s)}`：还有字符组没处理' if S.p < len(S.s) else '`p` 走到末尾，所有字符组都统计完了'),
        'q = p + 1': '`q` 从 `p+1` 出发，去找这一组的右边界',
        'while q < len(s) and': lambda S, B, r: (f"`s[{S.q}] == s[{S.p}]`（'{S.s[S.q]}' == '{S.s[S.p]}'）→ 成立，同一组还能延伸" if S.q < len(S.s) and S.s[S.q] == S.s[S.p]
                                                  else '`q` 到头或遇到不同字符 → ==这一组到此为止=='),
        'q += 1': '组再长一格：`q` → {q}',
        'freq[q - p]': '这一组 `s[{p}:{q}]` 长 `{q - p}` → `freq[{q - p}]` = =={freq[q - p]}==',
        'p = q': '下一组从 `q` 开始：`p` → {p}',
        'return max': '各长度的出现次数里取最大：`max({list(freq.values())})` = =={ret}==',
    },
    cards=dict(
        one_liner='把字符串切成一组组相同字符，按组长计数，取最大次数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['连续字符组：==不能再扩展的相同字符子串==，如 `hello` → `h`、`e`、`ll`、`o`',
                 '求长度相同的字符组，最多出现了几次',
                 '示例：`aabbbcdd` 组长为 2、3、1、2 → 长为 2 的出现 `2` 次'],
        quote='一趟遍历，将s分离成由相同字符组成的子串，并使用哈希表记录每种长度出现的次数。接下来返回哈希表中的最大次数即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`p` 是组头，`q` 向右扩到第一个不同字符，`[p, q)` 就是一整组',
              '组长 `q - p` 作为键，在 `freq` 里加一',
              '下一组直接从 `q` 开始，整串只扫一遍'],
        summary=['时间 `O(n)`，空间 `O(n)`（`freq` 最多 `O(√n)` 个键）',
                 '答案是==次数的最大值==，不是最长的组长',
                 '`freq.get(k, 0) + 1` 处理第一次出现的长度',
                 '原文为 Python 2 风格，无需修改即可在 Python 3 运行'],
    ),
)
