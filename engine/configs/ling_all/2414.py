CONFIG = dict(
    num=2414, title='最长的字母序连续子字符串的长度', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环 · pairwise',
    tags=['灵神题单', '难度分 1222'],
    code='''
class Solution:
    def longestContinuousSubstring(self, s: str) -> int:
        ans = cnt = 1
        for x, y in pairwise(map(ord, s)):
            cnt = cnt + 1 if x + 1 == y else 1
            ans = max(ans, cnt)
        return ans
''',
    call="Solution().longestContinuousSubstring('abcabcdea')",
    expect=5,
    views=[
        dict(type='string', var='s', h=170),
        dict(type='text', h=90, fn=lambda S: (f"比较 `{chr(S['x'])}`(ord={S['x']}) 的下一个字母是不是 `{chr(S['y'])}`(ord={S['y']})" if 'x' in S and 'y' in S else '')),
        dict(type='text', h=90, fn=lambda S: f"当前连续长度 cnt = =={S['cnt']}==，最长 ans = =={S['ans']}==" if 'cnt' in S else ''),
    ],
    watch=['x', 'y', ('cnt', 'cnt', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = cnt = 1': '单个字母本身就是连续串：`ans = cnt = 1`',
        'for x, y in pairwise': '取相邻两个字符的编码：`x = {x}`，`y = {y}`',
        'cnt = cnt + 1': lambda S, B, r: (f'`x + 1 = {S.x + 1} == y = {S.y}`：字母紧挨着 → 连续长度加一，`cnt` → =={S.cnt}==' if S.x + 1 == S.y
                                          else f'`x + 1 = {S.x + 1} != y = {S.y}`：断开了 → `cnt` 重置为 =={S.cnt}=='),
        'ans = max': '`ans = max({B.ans}, {cnt}) = {ans}`',
        'return ans': '最长的字母序连续子串长度 `{ans}`',
    },
    cards=dict(
        one_liner='相邻字符差 1 就累加，否则重置为 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字母表中连续的字母组成的串（如 `abc`）叫字母序连续字符串',
                 '求 `s` 里最长的字母序连续子串的长度',
                 '示例：`abacaba` → `2`；本视频：`abcabcdea` → `5`'],
        quote='从左到右遍历 s，同时维护连续递增长度 cnt：如果 s[i-1]+1 = s[i]，把 cnt 加一，然后用 cnt 更新答案的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`pairwise` 每次给出相邻两个字符 `(x, y)` 的 ASCII 码',
              '`x + 1 == y` 就接着往下数，否则新起一段，从 1 开始',
              '每一步都用 `cnt` 刷新答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`ans` 和 `cnt` 初始都是 1：长度至少为 1',
                 '不连续时 `cnt` 重置为 1，不是 0（y 自己算一个）',
                 '`pairwise` 是 Python 3.10 才有的，但 LeetCode 环境已预置'],
    ),
)
