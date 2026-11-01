_N = lambda S: S['_inner'].get('now')


CONFIG = dict(
    num=2002, title='两个回文子序列长度的最大乘积', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='dfs 二分字符 + 区间 DP 求最长回文子序列',
    tags=['灵神题单·动态规划', '灵神题单·链表树与回溯', '难度分 1869'],
    code='''
class Solution(object):
    def maxProduct(self, s):
        self.res = 0
        self.dfs(0, [], [], s)
        return self.res

    def dfs(self, now, part1, part2, s):
        if now == len(s):
            self.res = max(self.res, self.dp(part1) * self.dp(part2))
            return

        part1.append(s[now])
        self.dfs(now + 1, part1, part2, s)
        part1.pop()

        part2.append(s[now])
        self.dfs(now + 1, part1, part2, s)
        part2.pop()

    def dp(self, s):
        n = len(s)
        if n == 0:
            return 0
        f = [[0] * n for _ in range(n)]
        for l in range(1, n + 1):
            for left in range(n - l + 1):
                right = left + l - 1
                if left == right:
                    f[left][right] = 1
                elif s[left] == s[right]:
                    f[left][right] = f[left + 1][right - 1] + 2
                else:
                    f[left][right] = max(f[left + 1][right], f[left][right - 1])

        return f[0][n - 1]
''',
    call="Solution().maxProduct('aba')",
    expect=2,
    views=[
        dict(type='string', var=lambda S: S['_inner'].get('s') if isinstance(S['_inner'].get('s'), str) else S.get('s'),
             label='s', cell=84, h=130, pointers={_N: 'blue'}, pointer_labels={_N: 'now'}),
        dict(type='array', var='part1', label='part1', cell=64, h=110),
        dict(type='array', var='part2', label='part2', cell=64, h=110),
        dict(type='table', var=lambda S: S['_inner'].get('f'), label='f[left][right]：s[left..right] 的最长回文子序列', cell=64, h=150,
             color=lambda S, i, j, v: 'yellow' if (i, j) == (S['_inner'].get('left'), S['_inner'].get('right')) else None),
        dict(type='calls', h=150, hide=('s',)),
    ],
    watch=[('now', _N, 'blue'), ('res', 'self.res', 'green'), ('n', lambda S: S['_inner'].get('n'), 'cyan')],
    skip=['self.res = 0', 'n = len(s)', 'right = left'],
    max_steps=75,
    captions={
        'self.dfs(0, [], [], s)': '从第 0 个字符开始：每个字符要么进 part1，要么进 part2',
        'if now == len(s)': lambda S, B, r: ('每个字符都分好了，两部分各算最长回文子序列' if S['_inner']['now'] == len(S['_inner']['s'])
                                              else f'`now = {S["_inner"]["now"]}`：还要分配 `s[{S["_inner"]["now"]}]`'),
        'self.res = max': '两部分各求最长回文子序列 `dp(part1)`、`dp(part2)`，乘积和 `res` 取大',
        10: lambda S, B, r: f'这种分法处理完，当前 `res` = =={S.self.res}==',
        'part1.append': '`s[now]` 放入 part1',
        'part2.append': '`s[now]` 放入 part2',
        'part1.pop': '回溯：把它从 part1 拿出来',
        'part2.pop': '回溯：把它从 part2 拿出来',
        'self.dfs(now + 1, part1, part2, s)': '继续分配下一个字符',
        'if n == 0': lambda S, B, r: ('空串，最长回文子序列长度 0' if S['_inner']['n'] == 0 else f'长度 `n = {S["_inner"]["n"]}`，用区间 DP'),
        'for l in range': lambda S, B, r: (f'枚举区间长度 `l = {S["_inner"].get("l")}`：短区间先算'
                                                 if S['_inner'].get('l') != B.get('l') else '所有长度都算完'),
        'for left in range': lambda S, B, r: (f'枚举左端点 `left = {S["_inner"].get("left")}`'
                                                    if S['_inner'].get('left') != B.get('left') else '这个长度的区间都算完'),
        'if left == right': lambda S, B, r: f'区间 [{S["_inner"]["left"]}, {S["_inner"]["right"]}]：' + ('只有一个字符 → 长度 1' if S['_inner']['left'] == S['_inner']['right'] else '有多个字符，比较两端'),
        'elif s[left] == s[right]': lambda S, B, r: f'`s[{S["_inner"]["left"]}] = {S["_inner"]["s"][S["_inner"]["left"]]}`，`s[{S["_inner"]["right"]}] = {S["_inner"]["s"][S["_inner"]["right"]]}`：' + ('相同 → 两端都选，加里面' if S['_inner']['s'][S['_inner']['left']] == S['_inner']['s'][S['_inner']['right']] else '不同 → 去掉一端取较大'),
        'f[left][right] = 1': '单个字符是回文：`f[{left}][{right}] = 1`',
        'f[left + 1][right - 1] + 2': '两端相同：`f[{left}][{right}]` = 里面 + 2 = =={f[left][right]}==',
        'max(f[left + 1][right]': '两端不同：取去掉一端的较大值 → `f[{left}][{right}]` = =={f[left][right]}==',
        'return f[0][n - 1]': '整段的最长回文子序列长度 `{ret}`',
        'return self.res': '所有分法都试过，最大乘积 `{ret}`',
    },
    cards=dict(
        one_liner='n 很小：枚举所有分法，再用 DP 求各部分最长回文',
        complexity='时间 `O(2^n · n^2)`，空间 `O(n^2)`',
        problem=['在 `s` 里选两个==下标不相交==的回文子序列，使长度乘积最大',
                 '`2 <= s.length <= 12`',
                 '本视频：`s = "aba"` → `2`'],
        quote='注意到字符串的长度n非常小，那么完全可以找出所有的将字符划分成两个部分的划分方式。',
        quote_src='—— yiduobo 题解原文',
        idea=['dfs 把每个字符分给 part1 或 part2，最多 `2^12 = 4096` 种',
              '不选的字符等价于放进某部分后不参与回文，所以只需分成两部分',
              '每部分取==最长回文子序列==（区间 DP），乘积更新答案'],
        summary=['时间 `O(2^n · n^2)`，`n ≤ 12` 足够',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '易错点：part 为空时 `dp` 返回 0；dfs 里 append 后必须 pop 恢复',
                 '对比灵神：灵神每字符三选一再判回文；yiduobo 两选一，用 DP 求最长回文'],
    ),
)
