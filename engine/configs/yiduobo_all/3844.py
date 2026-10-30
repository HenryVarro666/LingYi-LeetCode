def _top(S):
    if 'index' not in S:
        return '准回文 = ==中心回文 + 1 个被删字母 + 外侧回文==；先扩展中心，再跳过一个字母继续扩展'
    if 'p1' in S and S.get('_line', 0) >= 14:
        return f"跳过一个字母后继续扩展：`[{S['p1']}, {S['p2']}]`"
    if 'left' in S:
        return f"中心回文 `[{S['left']}, {S['right']}]`"
    return ''


CONFIG = dict(
    num=3844, title='最长的准回文子字符串', difficulty='Medium', category='字符串',
    author='yiduobo', technique='中心回文 + 单个额外字符 + 外侧回文',
    tags=['灵神题单', '字符串', '难度分 1990'],
    code='''
class Solution(object):
    def almostPalindromic(self, s):
        
        def calc(left, right):
            while left > 0 and right + 1 < n and s[left - 1] == s[right + 1]:
                left -= 1
                right += 1
            
            if right - left + 1 == n:
                return n
            
            ma = 0
            
            if left > 0:
                p1 = left - 1
                p2 = right
                while p1 > 0 and p2 + 1 < n and s[p1 - 1] == s[p2 + 1]:
                    p1 -= 1
                    p2 += 1
                
                ma = max(ma, p2 - p1 + 1)
            
            if right + 1 < n:
                p1 = left
                p2 = right + 1
                while p1 > 0 and p2 + 1 < n and s[p1 - 1] == s[p2 + 1]:
                    p1 -= 1
                    p2 += 1
                ma = max(ma, p2 - p1 + 1)

            return ma

        res = 0
        n = len(s)

        for index in range(n):
            res = max(res, calc(index, index))
            if res == n:
                break
            
            if index > 0 and s[index - 1] == s[index]:
                res = max(res, calc(index - 1, index))
            if res == n:
                break

        return res
''',
    call='Solution().almostPalindromic("abca")',
    expect=4,
    skip=['res = 0', 'n = len(s)', 'ma = 0', 'p1 = left - 1', 'p2 = right', 'p1 = left', 'p2 = right + 1'],
    views=[
        dict(type='text', fn=_top, size=24, h=60),
        dict(type='string', var='s', label='s（蓝 = 中心回文 [left, right]，粉 = 跳过一字母后的范围 [p1, p2]）', cell=84, h=250,
             pointers={'left': 'blue', 'right': 'blue', 'p1': 'pink', 'p2': 'pink'},
             color=lambda S, k, v: ('pink' if 'p1' in S and S['p1'] <= k <= S['p2'] and S.get('_line', 0) >= 14 else
                                    'blue' if 'left' in S and S['left'] <= k <= S['right'] else None)),
        dict(type='text', fn=lambda S: f"`res = {S['res']}`，整串长度 `n = {S['n']}`" if 'res' in S and 'n' in S else '', size=24, h=60),
    ],
    watch=[('index', 'index'), ('left', 'left', 'blue'), ('right', 'right', 'blue'), ('p1', 'p1', 'pink'), ('p2', 'p2', 'pink'), ('ma', 'ma'), ('res', 'res', 'green')],
    captions={
        'while left > 0': lambda S, B, ret: (
            f'`s[{S.left-1}] = {S.s[S.left-1]}` == `s[{S.right+1}] = {S.s[S.right+1]}` → 中心回文向两侧扩展'
            if S.left > 0 and S.right + 1 < S.n and S.s[S.left-1] == S.s[S.right+1]
            else '外侧不再相同（或到边界）→ 中心回文就是 `[%d, %d]`' % (S.left, S.right)),
        'left -= 1': '`left` → {left}',
        'right += 1': '`right` → {right}',
        'if right - left + 1 == n': lambda S, B, ret: (f'中心回文长度 `{S.right-S.left+1}` == `n`：整串是回文，直接返回 `n`' if S.right-S.left+1 == S.n
                                                       else f'中心回文长度 `{S.right-S.left+1}` < `n`，还要试试多删一个字母'),
        'if left > 0': lambda S, B, ret: (f'左边还有字母 `s[{S.left-1}]`：把它==当作被删的字母==' if S.left > 0 else '左边没有字母了，不能删左边'),
        'p1 = left - 1': '',
        'while p1 > 0': lambda S, B, ret: (
            f'外侧 `s[{S.p1-1}] = {S.s[S.p1-1]}` == `s[{S.p2+1}] = {S.s[S.p2+1]}` → 继续向外'
            if S.p1 > 0 and S.p2 + 1 < S.n and S.s[S.p1-1] == S.s[S.p2+1]
            else '外侧不再相同（或到边界）→ 停'),
        'p1 -= 1': '`p1` → {p1}',
        'p2 += 1': '`p2` → {p2}',
        'ma = max': '`[{p1}, {p2}]` 长度 `{p2-p1+1}`（含被删字母），`ma = {ma}`',
        'if right + 1 < n': lambda S, B, ret: (f'右边还有字母 `s[{S.right+1}]`：把它==当作被删的字母==' if S.right + 1 < S.n else '右边没有字母了，不能删右边'),
        'return ma': '这个中心能得到的最长准回文：`{ma}`',
        'return n': '整串已是回文 → 返回 `n`',
        'res = max(res, calc(index, index))': '奇数中心 `index = {index}`：`res = {res}`',
        'res = max(res, calc(index - 1, index))': '偶数中心 `[{index-1}, {index}]`：`res = {res}`',
        'if res == n': lambda S, B, ret: ('`res == n`：已经是整串，提前结束' if S.res == S.n else f'`res = {S.res} < n = {S.n}`，继续'),
        'if index > 0 and': lambda S, B, ret: ('`s[index-1] == s[index]`：还要试==偶数长度==的中心' if S.index > 0 and S.s[S.index-1] == S.s[S.index]
                                              else '相邻不同，没有偶数中心'),
        'return res': '最长准回文串长度 `{res}`',
    },
    max_steps=130,
    cards=dict(
        one_liner='准回文 = 中心回文 + 一个被删字母 + 外侧回文',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['子串==恰好删一个字符==后变成回文 → 准回文串',
                 '求 `s` 中最长准回文串的长度',
                 '本视频：`"abca"` → `4`'],
        quote='对于非标准回文串，其必然可以拆解为三个部分，分别为：中心回文部分、单个额外字符、外侧回文部分。这个字符就是恰好删掉的那个字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['标准回文也是准回文（删中心字符），所以先用中心回文长度更新答案',
              '中心回文 `[left, right]` 的左边或右边各取一个字母当作被删的那个',
              '跳过它后，从 `[left-2, right+1]` 或 `[left-1, right+2]` 继续向外匹配'],
        summary=['时间 `O(n^2)`，空间 `O(1)`',
                 '`calc` 先把中心回文扩到最大，再分别试删左、删右',
                 '偶数长度的中心要单独试：`s[index-1] == s[index]` 时才有',
                 '中心回文已占满整串时直接返回 `n`，外层 `res == n` 也提前 `break`',
                 '对比灵神：他扩展到失配再删 `s[l]` 或 `s[r]`，yiduobo 把它拆成三段结构'],
    ),
)
