def _top(S):
    if 'pre' not in S:
        return '先在前后各加一个哨兵 `L` 和 `R`，免得单独处理开头结尾'
    s, pre, i = S['s'], S['pre'], S['i']
    if s[i] == '.':
        return f'`s[{i}]` 是点，跳过'
    a, b = s[pre], s[i]
    kind = {('L', 'L'): '`L...L` 全变 L', ('R', 'R'): '`R...R` 全变 R', ('R', 'L'): '`R...L` 向中间倒', ('L', 'R'): '`L...R` 不变'}[(a, b)]
    return f'`s[{pre}]={a}`，`s[{i}]={b}`：{kind}'


def _col(S, k, v):
    if v == 'L':
        return 'pink'
    if v == 'R':
        return 'blue'
    return None


CONFIG = dict(
    num=838, title='推多米诺', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环 · 分类讨论',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·贪心与思维', '难度分 1638'],
    code='''
class Solution:
    def pushDominoes(self, dominoes: str) -> str:
        s = list('L' + dominoes + 'R')  # 前后各加一个哨兵
        pre = 0  # 上一个 L 或 R 的位置
        for i, ch in enumerate(s):
            if ch == '.':
                continue
            if ch == s[pre]:  # L...L 或 R...R
                s[pre + 1: i] = ch * (i - pre - 1)  # 全变成 s[i]
            elif ch == 'L':  # R...L
                half = (i - pre - 1) // 2
                s[pre + 1: pre + half + 1] = 'R' * half  # 前一半变 R
                s[i - half: i] = 'L' * half  # 后一半变 L
            pre = i
        return ''.join(s[1:-1])  # 去掉前后哨兵
''',
    call='Solution().pushDominoes(".L.R...LR..L")',
    expect='LL.RR.LLRRLL',
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='s', label='s（蓝 = R，粉 = L，首尾是哨兵）', cell=70, pointers={'pre': 'blue', 'i': 'pink'},
             color=_col, window=('pre', 'i'), h=300),
        dict(type='text', fn=lambda S: f"`half = {S['half']}`：中间 {S['i']-S['pre']-1} 个点，各取一半" if 'half' in S and S['_line'] in (11, 12, 13) else '', size=24),
    ],
    watch=[('pre', 'pre', 'blue'), ('i', 'i', 'pink'), 'ch', 'half'],
    captions={
        "s = list": '`s = "{\'\'.join(s)}"`：首尾加哨兵 `L`、`R`，开头的点相当于被左边的 `L` 管，结尾的点被右边的 `R` 管',
        'pre = 0': '`pre` 记录上一个非点字符的位置，初始是左哨兵 `0`',
        'for i, ch': '`i = {i}`，`ch = {ch}`',
        "if ch == '.'": lambda S, B, r: ('是点，状态还没定，跳过' if S.ch == '.' else f"`{S.ch}` 不是点：它和 `s[{S.pre}] = {S.s[S.pre]}` 围出一段，要结算中间的点"),
        'if ch == s[pre]': lambda S, B, r: (f"`{S.ch} == s[{S.pre}]`：`{S.ch}...{S.ch}`，同方向 → 中间全部被推成 `{S.ch}`" if S.ch == S.s[S.pre]
                                            else f"`{S.ch} ≠ s[{S.pre}] = {S.s[S.pre]}`：方向不同，继续分类"),
        'ch * (i - pre - 1)': '中间 `{i - pre - 1}` 个点全变成 `{ch}`',
        "elif ch == 'L'": lambda S, B, r: ('`R...L`：两边相向倒，中间各推一半' if S.ch == 'L' else '`L...R`：两边都往外倒，中间的点纹丝不动，什么也不改'),
        'half =': '中间 `{i - pre - 1}` 个点，一半 `half = {half}`；==奇数个点时正中间那个受力平衡，保持 `.`==',
        "'R' * half": '靠近左边 `R` 的前 `{half}` 个点变成 `R`',
        "'L' * half": '靠近右边 `L` 的后 `{half}` 个点变成 `L`',
        'pre = i': '这一段结算完，`pre = {i}`，下一段从这里算起',
        'return': '去掉哨兵得到 `{ret}`',
    },
    cards=dict(
        one_liner='相邻两个非点字符之间，四种情况分类讨论',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`L` 向左推、`R` 向右推、`.` 是竖立的骨牌；两边同时有力则保持不变',
                 '求最终状态',
                 '示例：`".L.R...LR..L"` → `"LL.RR.LLRRLL"`'],
        quote='根据题意，有四种情况：L...L 中间全变 L；R...R 中间全变 R；R...L 前一半变 R、后一半变 L，奇数个点则正中间不变；L...R 不变。',
        quote_src='—— 灵茶山艾府题解（节选）',
        idea=['每次只看相邻两个非点字符，它们夹住的点由这两端决定',
              '前后加哨兵 `L`、`R`，开头结尾就不用特判',
              '`R...L` 用 `half = (i-pre-1)//2` 对半分，奇数时中间留点'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`R...L` 点数为奇数时，中间那个点保持 `.`，`half` 向下取整刚好空出它',
                 '`L...R` 什么都不用改；哨兵不影响答案，最后记得去掉',
                 '同类题：2211. 统计道路上的碰撞次数'],
    ),
)
