
CONFIG = dict(
    num=2002, title='两个回文子序列长度的最大乘积', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='DFS 枚举两两划分 + 区间 DP 求最长回文子序列',
    tags=['动态规划', '链表树与回溯', '难度分 1869'],
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
    call='Solution().maxProduct("aab")',
    expect=2,
    views=[
        dict(type='string', var='s', label='s（蓝箭头 = 正在决定归属的字符 now）', pointers={'now': 'blue'}, cell=70, h=140),
        dict(type='array', var='part1', label='part1（放进第一部分的字符）', cell=60, h=110, index=False),
        dict(type='array', var='part2', label='part2（放进第二部分的字符）', cell=60, h=110, index=False),
        dict(type='calls', h=170, hide=('maxProduct', 'dfs', 'dp')),
    ],
    watch=[('now', 'now', 'blue'), ('part1', lambda S: ''.join(S['part1']), 'blue'), ('part2', lambda S: ''.join(S['part2']), 'pink'),
           ('res', 'self.res', 'green')],
    skip=['n = len(s)', 'if n == 0', 'f = [[0]', 'for l in range', 'for left in range', 'right = left', 'if left == right', 'f[left][right] =',
          'elif s[left]', 'else:', 'return 0'],
    captions={
        'self.res = 0': '`res` 记录目前最大的乘积',
        'self.dfs(0, [], [], s)': '从第 0 个字符开始，给每个字符决定放进 part1 还是 part2',
        'if now == len(s)': lambda S, B, r: (f'`now = {S.now} = len(s)`：字符都分完了 → 算这一种划分' if S.now == len(S.s)
                                             else f'`now = {S.now}`：还有字符没分，继续'),
        'self.res = max': lambda S, B, r: f'划分好了：`part1={"".join(S.part1)}`、`part2={"".join(S.part2)}`，各求最长回文子序列再相乘，更新 `res`',
        'part1.append': '`{s[now]}` 放进 part1',
        'part1.pop()': '回溯：把它从 part1 拿出来',
        'part2.append': '换个选择：`{s[now]}` 放进 part2',
        'part2.pop()': '回溯：把它从 part2 拿出来',
        'self.dfs(now + 1': '递归处理下一个字符：`now = {B.now + 1}`',
        'return f[0][n - 1]': lambda S, B, r: f'区间 DP 的答案：`{"".join(S.s)}` 的最长回文子序列长度 = =={r}==',
        '            return': '这一种划分处理完，回到上一层',
        'return self.res': '所有 `2^n` 种划分试完，最大乘积 `{self.res}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='字符串很短：把每个字符分给两边，全试一遍',
        complexity='时间 `O(2^n · n^2)`，空间 `O(n^2)`',
        problem=['找 `s` 的两个==不相交==回文子序列，使长度乘积最大',
                 '示例：`s = "leetcodecom"` → `9`（`ete` 和 `cdc`）',
                 '本视频：`s = "aab"` → `2`（`aa` 和 `b`）'],
        quote='注意到字符串的长度n非常小，那么完全可以找出所有的将字符划分成两个部分的划分方式。由于n最大是12，那么最多也只有4096种不同的划分方式。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dfs` 给每个字符两种选择：进 `part1` 或进 `part2`，共 `2^n` 种',
              '划分好后，各自用区间 DP 求最长回文子序列：`s[l]==s[r]` 加 2，否则取较大者',
              '把两个长度相乘，用来更新 `res`'],
        result='所有划分试完，返回最大乘积 ✓',
        summary=['时间 `O(2^n · n^2)`，`n ≤ 12` 完全够用',
                 '不选的字符相当于丢掉：不选的情形被“选了更多字符不会更差”覆盖',
                 '`dp` 里的区间 DP 视频中折叠了：每次只给出结果',
                 '原文已是 Python 3 可运行写法，未作修改'],
    ),
)
