CONFIG = dict(
    num=3746, title='等量移除后的字符串最小长度', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='数 a 的个数 → |2k-n|',
    tags=['贪心与思维', '脑筋急转弯', '难度分 1327'],
    code='''
class Solution:
    def minLengthAfterRemovals(self, s: str) -> int:
        return abs(s.count('a') * 2 - len(s))
''',
    call="Solution().minLengthAfterRemovals('aaabb')",
    expect=1,
    views=[
        dict(type='string', var='s', label='s：a 和 b 一对一对消掉，剩下多出来的那种', h=240,
             color=lambda S, i, v: 'blue' if v == 'a' else 'pink'),
        dict(type='text', fn=lambda S: f"`k = {S['s'].count('a')}` 个 a，`n - k = {len(S['s']) - S['s'].count('a')}` 个 b → 剩 `|2k - n|` = =={abs(S['s'].count('a') * 2 - len(S['s']))}==" if 's' in S else '', size=30),
    ],
    watch=[('s', 's', 'blue')],
    captions={
        'return': "`a` 有 `k = {s.count('a')}` 个，总长 `n = {len(s)}`：每次消掉一个 a 和一个 b，剩 `|2k - n| = |{s.count('a') * 2} - {len(s)}|` = =={ret}==",
    },
    cards=dict(
        one_liner='每次消掉相邻的 ab，最后只剩下多出来的那种字母',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串 `s` 只含 `a`、`b`，可反复删除 a、b 数量相等的子串',
                 '求最后能剩下的最小长度',
                 '示例：`"aaabb"` → `1`；`"aabbab"` → `0`'],
        quote='只要 s 有不同字母，那么 s 一定存在相邻不同的字母，我们就可以把这两个字母（作为一个子串）移除，直到 s 只剩下一种字母为止。',
        quote_src='—— 灵茶山艾府题解',
        idea=['有两种字母 → 必有相邻的 `ab` 或 `ba`，直接删掉这一对',
              '设 a 有 `k` 个，b 有 `n-k` 个，每次各少一个',
              '直到某种字母没了，剩下 `|k - (n-k)| = |2k - n|`'],
        before=[dict(heading='先看一个例子', lines=['`aaabb`：消掉一个 `ab` → `aab`', '再消掉一个 `ab` → `a`，没法再消', '3 个 a、2 个 b：剩 `3 - 2 = 1`'])],
        after=[dict(heading='为什么不能更小', lines=['每次删除的子串 a、b 数量相等，所以 `a 个数 - b 个数` 永远不变', '最后只剩一种字母，长度至少是 `|a - b|`', '上面的做法又恰好能达到，所以答案就是它'])],
        summary=['时间 `O(n)`（`count` 扫一遍），空间 `O(1)`',
                 '关键：删除不改变 a、b 个数之差，所以它是下界',
                 '易错点：别去模拟删除，直接数个数',
                 '同类题：脑筋急转弯 · 抵消后看剩余'],
    ),
)
