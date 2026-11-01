CONFIG = dict(
    num=2055, title='蜡烛之间的盘子', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 最近蜡烛位置（Go 原文转写）',
    tags=['一、前缀和', '§1.5 进阶', '难度分 1819'],
    code='''
class Solution:
    def platesBetweenCandles(self, s: str, queries: List[List[int]]) -> List[int]:
        n = len(s)
        sum = [0] * (n + 1)  # sum[i] 表示 s[:i] 中盘子的个数
        left = [0] * n  # left[i] 表示 i 左侧最近蜡烛位置
        p = -1
        for i, b in enumerate(s):
            sum[i + 1] = sum[i]
            if b == '|':
                p = i
            else:
                sum[i + 1] += 1
            left[i] = p

        right = [0] * n  # right[i] 表示 i 右侧最近蜡烛位置
        p = n
        for i in range(n - 1, -1, -1):
            if s[i] == '|':
                p = i
            right[i] = p

        ans = [0] * len(queries)
        for i, q in enumerate(queries):
            l, r = right[q[0]], left[q[1]]  # 用最近蜡烛位置来代替查询的范围，从而去掉不符合要求的盘子
            if l < r:
                ans[i] = sum[r] - sum[l]
        return ans
''',
    call='Solution().platesBetweenCandles("*|*|*|", [[0,5],[2,4]])',
    expect=[2, 0],
    views=[
        dict(type='string', var='s', label='s（* 盘子，| 蜡烛）', h=150,
             color=lambda S, i, v: 'yellow' if v == '|' else None),
        dict(type='array', var=lambda S: S.get('sum'), label='sum：前 i 个字符里的盘子数', h=150),
        dict(type='array', var='left', label='left：左侧最近蜡烛', h=150),
        dict(type='array', var='right', label='right：右侧最近蜡烛', h=150),
        dict(type='array', var='ans', label='ans', h=130),
    ],
    watch=['i', 'p', ('l', 'l', 'blue'), ('r', 'r', 'pink')],
    captions={
        'sum = [0] * (n + 1)': '`sum[i]`：`s[:i]` 里盘子的个数，区间盘子数就是两个前缀和相减',
        'left = [0] * n': '`left[i]`：`i` 左侧最近的蜡烛位置',
        'p = -1': '`p` 记录最近见到的蜡烛，开始还没有，设为 -1',
        'for i, b in enumerate(s)': '从左到右扫描，同时算前缀和和 left',
        'sum[i + 1] = sum[i]': '先继承前面的盘子数：`sum[{i + 1}] = {sum[i]}`',
        "if b == '|'": '`s[{i}] = {b}`：{"是蜡烛，更新最近蜡烛" if b == "|" else "是盘子，盘子数加 1"}',
        'p = i': '最近蜡烛位置 `p = {p}`',
        'sum[i + 1] += 1': '盘子：`sum[{i + 1}] = =={sum[i + 1]}==`',
        'left[i] = p': '`left[{i}] = {p}`（无蜡烛则为 -1）',
        'right = [0] * n': '`right[i]`：`i` 右侧最近的蜡烛位置，从右往左扫',
        'p = n': '`p = n` 表示右边还没有蜡烛',
        'for i in range(n - 1, -1, -1)': '倒着扫描，算 right',
        "if s[i] == '|'": '`s[{i}] = {s[i]}`：{"是蜡烛，最近蜡烛更新为自己" if s[i] == "|" else "是盘子，沿用右边最近蜡烛"}',
        'right[i] = p': '`right[{i}] = {p}`',
        'ans = [0] * len': '每个查询答案先设 0（范围内蜡烛不足两支就是 0）',
        'l, r = right[q[0]], left[q[1]]': '查询 `{q}`：左端点向右靠到最近蜡烛 `l = {l}`，右端点向左靠到最近蜡烛 `r = {r}`，多余的盘子就被去掉了',
        'if l < r': '`l = {l}`，`r = {r}`：{"两支蜡烛之间有区间，可以算" if l < r else "不足两支蜡烛，答案 0"}',
        'ans[i] = sum[r] - sum[l]': '`sum[{r}] - sum[{l}] = {sum[r]} - {sum[l]}` = =={ans[i]}== 个盘子',
    },
    max_steps=100,
    cards=dict(
        one_liner='把查询端点各自「缩」到最近的蜡烛，再用前缀和数盘子',
        complexity='时间 `O(n + q)`，空间 `O(n)`',
        problem=['`s` 里 `*` 是盘子，`|` 是蜡烛；每次查询 `[l, r]`',
        '统计子串里左右两边都有蜡烛的盘子数',
        '示例：`"*|*|*|"`，`[[0,5],[2,4]]` → `[2,0]`'],
        quote='用最近蜡烛位置来代替查询的范围，从而去掉不符合要求的盘子',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['`right[l]`：`l` 右边第一支蜡烛；`left[r]`：`r` 左边第一支蜡烛',
              '这两支蜡烛之间的盘子必定两边都有蜡烛，两端被去掉的盘子都不算',
              '盘子数用前缀和 `sum[r] - sum[l]` 一减即得'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n + q)`，空间 `O(n)`',
                 '易错点：`l < r` 才有答案，否则保持 0；`sum` 长度是 `n+1`',
                 '`left` 无蜡烛时为 -1，`right` 无蜡烛时为 `n`，这样 `l < r` 会自然不成立'],
    ),
)
