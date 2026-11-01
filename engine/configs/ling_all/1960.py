CONFIG = dict(
    num=1960, title='两个回文子字符串长度的最大乘积', difficulty='Hard', category='字符串',
    author='灵茶山艾府', technique='Manacher 算法 + 前后缀最长奇回文（Go 原文转写）',
    tags=['灵神题单', '字符串', '难度分 2691'],
    code='''
class Solution:
    def maxProduct(self, s: str) -> int:
        n = len(s)
        halfLen = [0] * n
        mid = r = 0
        for i in range(n):
            hl = 1
            if i < r:
                hl = min(halfLen[mid * 2 - i], r - i)
            while i >= hl and i + hl < n and s[i - hl] == s[i + hl]:
                hl += 1
            if i + hl > r:
                mid, r = i, i + hl
            halfLen[i] = hl

        startPL = [0] * n
        endPL = [0] * n
        for i, hl in enumerate(halfLen):
            left, right = i - hl + 1, i + hl - 1
            startPL[left] = max(startPL[left], hl * 2 - 1)
            endPL[right] = max(endPL[right], hl * 2 - 1)
        for i in range(1, n):
            startPL[i] = max(startPL[i], startPL[i - 1] - 2)
        for i in range(n - 2, -1, -1):
            startPL[i] = max(startPL[i], startPL[i + 1])
        for i in range(n - 2, -1, -1):
            endPL[i] = max(endPL[i], endPL[i + 1] - 2)
        for i in range(1, n):
            endPL[i] = max(endPL[i], endPL[i - 1])

        ans = 0
        for i in range(1, n):
            ans = max(ans, endPL[i - 1] * startPL[i])
        return ans
''',
    call='Solution().maxProduct("ababb")',
    expect=3,
    views=[
        dict(type='string', var='s', label='s', cell=84, pointers={'i': 'blue'}, h=150),
        dict(type='array', var='halfLen', label='halfLen[i]：以 i 为中心的最长奇回文半长', cell=84, h=150),
        dict(type='array', var='startPL', label='startPL[i]：i 及右侧开头的最长奇回文长度', cell=84, h=150),
        dict(type='array', var='endPL', label='endPL[i]：i 及左侧结尾的最长奇回文长度', cell=84, h=150),
    ],
    watch=[('i', 'i', 'blue'), ('mid', 'mid', 'cyan'), ('r', 'r', 'orange'), ('hl', 'hl', 'pink'), ('ans', 'ans', 'green')],
    skip=['n = len(s)', 'halfLen = [0] * n', 'startPL = [0] * n', 'endPL = [0] * n', 'mid = r = 0', 'ans = 0', 'hl = 1',
          'for i in range(1, n)', 'for i in range(n - 2', 'for i, hl in enumerate(halfLen)', 'left, right =', 'hl += 1', 'endPL[right] = max'],
    captions={
        'for i in range(n)': lambda S, B, ret: ('`halfLen` 全部算完，接着求两个 PL 数组' if B.get('i') == S.i and 'i' in B else f'求以 `s[{S.i}]` 为中心的最长奇回文'),
        'if i < r': lambda S, B, ret: (f'`i = {S.i} < r = {S.r}`：落在 `mid = {S.mid}` 的大回文内，可以借对称点 `{S.mid * 2 - S.i}` 的结果' if S.i < S.r else f'`i = {S.i} ≥ r = {S.r}`：不在已知回文内，从 1 开始扩'),
        'hl = min': '借对称位置：`hl = min(halfLen[{mid * 2 - i}], r - i) = {hl}`，不能超出右边界',
        'while i >= hl': lambda S, B, ret: (f'`s[{S.i - S.hl}] = {S.s[S.i - S.hl]}` == `s[{S.i + S.hl}] = {S.s[S.i + S.hl]}` → `hl` 加一，再向外扩'
                                           if S.i >= S.hl and S.i + S.hl < len(S.s) and S.s[S.i - S.hl] == S.s[S.i + S.hl] else f'扩不动了，半长 `hl = {S.hl}`'),
        'hl += 1': '`hl` → {hl}',
        'if i + hl > r': lambda S, B, ret: (f'`i + hl = {S.i + S.hl} > r = {S.r}`：右边界更靠右，更新 `mid`、`r`' if S.i + S.hl > S.r else f'`i + hl = {S.i + S.hl} ≤ r`，右边界不变'),
        'mid, r = i, i + hl': '`mid = {mid}`，`r = {r}`：以后借这个回文',
        'halfLen[i] = hl': '`halfLen[{i}] = {hl}`，即最长奇回文长 `{hl * 2 - 1}`',
        'for i, hl in enumerate(halfLen)': lambda S, B, ret: ('`halfLen` 处理完' if B.get('hl') == S.hl and B.get('i') == S.i else f'回文 `s[{S.i - S.hl + 1}..{S.i + S.hl - 1}]`'),
        'startPL[left] = ': '回文 `s[{left}..{right}]` 长 `{hl * 2 - 1}`：它是以 `s[{left}]` 开头、也是以 `s[{right}]` 结尾的 → 更新 `startPL[{left}]`、`endPL[{right}]`',
        'endPL[right] = ': '同一个回文也是以 `s[{right}]` 结尾的：`endPL[{right}] = {endPL[right]}`',
        'startPL[i] = max(startPL[i], startPL[i - 1] - 2)': '`startPL[{i}] = {startPL[i]}`：左边开头的回文，去掉首尾各一个字符后，也是以 `s[{i}]` 开头的回文',
        'startPL[i] = max(startPL[i], startPL[i + 1])': '`startPL[{i}] = {startPL[i]}`：变成后缀最大值，表示从 `i` 往右能找到的最长奇回文',
        'endPL[i] = max(endPL[i], endPL[i + 1] - 2)': '`endPL[{i}] = {endPL[i]}`：右边结尾的回文缩短后，也是以 `s[{i}]` 结尾的回文',
        'endPL[i] = max(endPL[i], endPL[i - 1])': '`endPL[{i}] = {endPL[i]}`：变成前缀最大值，表示 `[0, i]` 内最长奇回文',
        'for i in range(1, n)': lambda S, B, ret: (f'枚举分割线：左边 `[0, {S.i - 1}]`，右边 `[{S.i}, n)`' if S['_line'] == 33 else f'`i = {S.i}`'),
        'ans = max': '`endPL[{i - 1}] * startPL[{i}] = {endPL[i - 1]} × {startPL[i]} = {endPL[i - 1] * startPL[i]}` → `ans = {ans}`',
        'return ans': '最大乘积 `{ans}`',
    },
    max_steps=130,
    cards=dict(
        one_liner='Manacher 求每个中心的回文，再预处理两侧最长奇回文，枚举分割线',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['在 `s` 中选两个 ==不重叠、长度为奇数== 的回文子串',
                 '求它们长度乘积的最大值',
                 '示例：`"ababbb"` → `"aba"` 和 `"bbb"` → `9`',
                 '本视频：`"ababb"` → `"aba"` 和 `"b"` → `3`'],
        quote='由于本题只要求奇回文串，所以不需要将 s 改造',
        quote_src='—— 灵茶山艾府题解',
        idea=['Manacher：`halfLen[i]` 记录以 `i` 为中心的最长奇回文半长，右边界 `r` 只会右移，复杂度 `O(n)`',
              '回文缩短后还是回文：`startPL[i]` 从左边的 `startPL[i-1] - 2` 继承，`endPL` 同理',
              '再取后缀 / 前缀最大值，最后枚举分割线 `endPL[i-1] * startPL[i]`'],
        result='分割在 `"aba"` 与 `"b"` 之间，`3 × 1 = 3` ✓',
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（原文给出两种写法，取不改造 s 的简化版）',
                 '时间 `O(n)`；`r` 单调不减，所以扩展总次数是 `O(n)`',
                 '易错：`startPL`、`endPL` 要先 `-2` 继承，再取最大值',
                 '同类题：5 题最长回文子串、647 回文子串'],
    ),
)
