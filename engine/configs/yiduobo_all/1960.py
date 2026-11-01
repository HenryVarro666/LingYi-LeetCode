CONFIG = dict(
    num=1960, title='两个回文子字符串长度的最大乘积', difficulty='Hard', category='字符串',
    author='yiduobo', technique='马拉车 + 左右最长奇回文的前后缀预处理',
    tags=['灵神题单', '字符串', '难度分 2691'],
    code='''
class Solution(object):
    def maxProduct(self, s):

        s = '$' + s + '#'
        mid = 0
        right = 0
        f = [0]
        for index in range(1, len(s) - 1):
            if index <= right:
                f.append(min(right - index, f[mid + mid - index]))
            else:
                f.append(1)
            
            while s[index + f[index]] == s[index - f[index]]:
                f[index] += 1
            
            if right < f[index] + index:
                right = f[index] + index
                mid = index
        
        l_max = [0]
        pos = 0
        for index in range(1, len(s) - 1):
            while pos < index + f[index] - 1:
                pos += 1
                l_max.append(max(l_max[-1], (pos - index) * 2 + 1))
        
        r_max = [0]
        pos = len(s) - 1
        for index in range(len(s) - 2, 0, -1):
            while pos > index - f[index] + 1:
                pos -= 1
                r_max.append(max(r_max[-1], (index - pos) * 2 + 1))
        r_max.append(0)
        r_max.reverse()

        res = l_max[1] * r_max[2]
        for index in range(2, len(s) - 1):
            res = max(res, l_max[index - 1] * r_max[index])

        return res
''',
    call='Solution().maxProduct("abab")',
    expect=3,
    views=[
        dict(type='string', var='s', label='s（首尾加哨兵 $ 和 #，下标从 1 开始）', cell=76, h=150, pointers={'index': 'blue', 'pos': 'pink'}),
        dict(type='array', var='f', label='f[i]：以 i 为中心的回文半长', cell=76, h=150),
        dict(type='array', var='l_max', label='l_max[i]：s[1..i] 里最长奇回文长度', cell=76, h=150),
        dict(type='array', var='r_max', label='r_max（r_max 生成中：从右往左）', cell=76, h=150),
    ],
    watch=[('index', 'index', 'blue'), ('mid', 'mid', 'cyan'), ('right', 'right', 'orange'), ('pos', 'pos', 'pink'), ('res', 'res', 'green')],
    skip=['mid = 0', 'right = 0', 'f = [0]', 'l_max = [0]', 'r_max = [0]', 'pos = 0', 'for index in range(2, len(s) - 1)',
          'res = l_max[1]', 'pos = len(s) - 1', 'r_max.append(0)', 'pos += 1', 'pos -= 1', 'f[index] += 1', 'right = f[index] + index', 'mid = index'],
    captions={
        "s = '$'": '`s` 两头加哨兵 `$`、`#`：回文扩展时不用判越界 → `{s}`',
        8: lambda S, B, ret: ('马拉车跑完，`f` 就是每个位置的回文半长' if B.get('index') == S.index and 'index' in B else f'求以 `s[{S.index}] = {S.s[S.index]}` 为中心的回文半长'),
        'if index <= right': lambda S, B, ret: (f'`index = {S.index} <= right = {S.right}`：在已知回文里，可借对称点 `{S.mid + S.mid - S.index}`' if S.index <= S.right else f'`index = {S.index} > right = {S.right}`：不在已知回文里，从头扩'),
        'f.append(min': '借对称点：`f[{index}] = min(right - index, f[{mid + mid - index}]) = {f[index]}`',
        'f.append(1)': '没有可借的，半长至少为 1：`f[{index}] = 1`',
        'while s[index + f[index]]': lambda S, B, ret: ('`f = 0`：先把中心自己算进去，半长变 1' if S.f[S.index] == 0 else f'`s[{S.index + S.f[S.index]}] = {S.s[S.index + S.f[S.index]]}` == `s[{S.index - S.f[S.index]}]` → 半长再 +1' if S.s[S.index + S.f[S.index]] == S.s[S.index - S.f[S.index]] else f'左右字符不同，停止：`f[{S.index}] = {S.f[S.index]}`（哨兵保证到边界必不等）'),
        'if right < f[index] + index': lambda S, B, ret: (f'`right = {S.right} < {S.f[S.index] + S.index}`：这个回文的右边界更远 → `right = {S.f[S.index] + S.index}`，`mid = {S.index}`，以后借它' if S.right < S.f[S.index] + S.index else f'`right = {S.right}` 不小于 `{S.f[S.index] + S.index}`，不变'),
        23: lambda S, B, ret: ('`l_max` 就绪' if B.get('index') == S.index and 'index' in B else f'中心 `index = {S.index}`，回文右端能到 `index + f[index] - 1 = {S.index + S.f[S.index] - 1}`'),
        30: lambda S, B, ret: ('`r_max`（从右往左）就绪' if len(S.r_max) > 1 and B.get('index') == S.index else f'中心 `index = {S.index}`，回文左端能到 `index - f[index] + 1 = {S.index - S.f[S.index] + 1}`'),
        'while pos < index + f[index] - 1': lambda S, B, ret: (f'`pos = {S.pos} < {S.index + S.f[S.index] - 1}`：这个回文还覆盖到新的右端点 `{S.pos + 1}`，要更新' if S.pos < S.index + S.f[S.index] - 1 else '`pos` 已追上回文右端，没有新的右端点'),
        'l_max.append': '右端点 `{pos}` 能结尾的奇回文长 `({pos} - {index}) * 2 + 1 = {(pos - index) * 2 + 1}`，`l_max` 取前缀最大 → `{l_max[-1]}`',
        'while pos > index - f[index] + 1': lambda S, B, ret: (f'`pos = {S.pos} > {S.index - S.f[S.index] + 1}`：回文还覆盖到新的左端点 `{S.pos - 1}`' if S.pos > S.index - S.f[S.index] + 1 else '`pos` 已追上回文左端，没有新的左端点'),
        'r_max.append(max': '左端点 `{pos}` 的回文长 `({index} - {pos}) * 2 + 1 = {(index - pos) * 2 + 1}`，`r_max` 取最大 → `{r_max[-1]}`',
        'r_max.reverse()': '翻转：`r_max[i]` 表示 `s[i..]` 里最长奇回文长 → `{r_max}`',
        'res = max': '`l_max[{index - 1}] * r_max[{index}] = {l_max[index - 1]} × {r_max[index]} = {l_max[index - 1] * r_max[index]}` → `res = {res}`',
        'return res': '最大乘积 `{res}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='枚举分割线，左右各取最长奇回文；用马拉车预处理',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['在字符串中选两个 ==不重叠、奇数长度== 的回文子串，使长度乘积最大',
                 '例：`"ababbb"` → `"aba"`、`"bbb"` → `9`',
                 '本视频：`"abab"` → `"aba"` 和 `"b"` → `3`'],
        quote='因此有必要预处理出所有位置左侧和右侧最长回文子串的长度，分别记为l_max和r_max。',
        quote_src='—— yiduobo 题解原文',
        idea=['马拉车得到 `f[p]`：以 `p` 为中心的最长奇回文半长',
              '回文 `s[p-f+1..p+f-1]` 里，以 `q` 为右端点的奇回文长 `(q-p)*2+1`，右端点越靠右越长',
              '`pos` 只往右走：只处理还没覆盖过的右端点，`l_max` 整体是 `O(n)`；`r_max` 同理从右往左'],
        result='`l_max` 和 `r_max` 错开一位相乘，最大 `3` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '哨兵 `$`、`#` 使马拉车的 `while` 无需判越界',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改；`l_max`/`r_max` 是前后缀最大',
                 '对比灵神：灵神用 `startPL/endPL` 一次扩散；yiduobo 用 `pos` 指针逐端点更新'],
    ),
)
