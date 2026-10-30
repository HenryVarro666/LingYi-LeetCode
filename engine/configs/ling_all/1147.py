def _I(S):
    return S['_inner'].get('i')


def _pre(S, i, v):
    s, k = S['_inner'].get('s'), S['_inner'].get('i')
    if s is None or k is None or S['_line'] not in (5, 6, 7, 8):
        return None
    if i < k:
        return 'blue'
    if i >= len(s) - k:
        return 'pink'
    return None


def _top(S):
    inn = S['_inner']
    s, i = inn.get('s'), inn.get('i')
    if s is None:
        return ''
    if i is None or S['_line'] not in (5, 6, 7, 8):
        return f'当前要分解的串 `s = "{s}"`'
    return f'前缀 `s[:{i}] = "{s[:i]}"`　后缀 `s[-{i}:] = "{s[-i:]}"`　' + ('==相同，立刻切下==' if s[:i] == s[-i:] else '不同，换更长的')


CONFIG = dict(
    num=1147, title='段式回文', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='贪心 · 最短前后缀立刻切 · 递归',
    tags=['灵神题单', '难度分 1912'],
    code='''
class Solution:
    def longestDecomposition(self, s: str) -> int:
        if s == "":
            return 0
        for i in range(1, len(s) // 2 + 1):  # 枚举前后缀长度
            if s[:i] == s[-i:]:  # 立刻分割
                return 2 + self.longestDecomposition(s[i:-i])
        return 1  # 无法分割
''',
    call='Solution().longestDecomposition("antaprezatepzapreanta")',
    expect=11,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='s', label='s（蓝 = 当前前缀，粉 = 当前后缀）', cell=60, h=170, pointers={},
             color=_pre),
        dict(type='calls', h=330),
    ],
    watch=[('i', _I, 'blue'), ('len(s)', lambda S: len(S['_inner'].get('s', '')), 'pink')],
    captions={
        'if s == ""': lambda S, B, r: ('`s` 已经切空了 → 返回 `0`，不再有段' if S.s == '' else f'`s = "{S.s}"` 非空，继续切'),
        'return 0': '空串没有段 → 返回 `0`',
        'for i in range': lambda S, B, r: (f'`i` 已经枚举到上限 `len(s) // 2 = {len(S.s) // 2}` 还没有相同的前后缀 → 跳出循环'
                                           if B['_inner'].get('i') is not None and B['_inner'].get('i') == S['_inner'].get('i')
                                           else f'枚举前后缀长度 `i = {S.i}`（从最短的开始，最多到 `len(s) // 2 = {len(S.s) // 2}`）'),
        'if s[:i] == s[-i:]': lambda S, B, r: (f'前缀 `"{S.s[:S.i]}"` == 后缀 `"{S.s[-S.i:]}"` → ==相同，立刻切下==（越短越好，段数才多）' if S.s[:S.i] == S.s[-S.i:]
                                              else f'前缀 `"{S.s[:S.i]}"` ≠ 后缀 `"{S.s[-S.i:]}"` → 试更长的前后缀'),
        'return 2 + self': '切下前后缀 `"{B.s[:B.i]}"`（各一段，共 `2` 段），中间 `"{B.s[B.i:-B.i]}"` 交给下一层递归',
        'return 1': lambda S, B, r: f'`"{S.s}"` 找不到相同的前后缀，只能整体当 ==1 段== → 返回 `1`',
    },
    cards=dict(
        one_liner='从两端向中间，一见到相同的前后缀就立刻切下',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['把字符串 `text` 分成 `k` 个非空子串，使得第 `i` 段 == 倒数第 `i` 段',
                 '求 `k` 的==最大值==',
                 '示例：`"ghiabcdefhelloadamhelloabcdefghi"` → `7`',
                 '`"antaprezatepzapreanta"` → `11`'],
        quote='如果短的长度超过了长的长度的一半呢？这是不可能的。用反证法证明。……这说明短的 aba 还可以继续分割出更短的子串 a，而不是作为一个无法分割的整体，矛盾。',
        quote_src='—— 灵茶山艾府题解答疑',
        idea=['枚举前后缀长度 `i`，==最短的相同前后缀立刻切下==，对中间部分递归',
              '贪心的理由：长的前后缀若相同，里面必然还能再切出短的，切短的段数不会更少',
              '前后缀长度不会超过 `len(s) // 2`；一个相同前后缀都找不到，整串当 1 段'],
        result='一层层切下 `a`、`nt`、`a`、`pre`、`za`（各 2 段），最后剩 `tep` 整段当 1 段 → 11',
        after=[dict(heading='另一种写法：迭代', lines=[
            '用 `while s:` 循环，`ans` 累加，`s = s[i:-i]` 向中间收缩',
            '找不到相同前后缀时 `ans += 1` 然后 `break`',
            '逻辑与递归完全一致，空间不用递归栈（切片仍有拷贝）'])],
        summary=['时间 `O(n^2)`：最坏每层要比较 `O(n)` 次长为 `O(n)` 的字符串',
                 '空间 `O(n)`（递归 + 切片）；Go 切片不拷贝可做到 `O(1)`',
                 '易错：枚举上限是 `len(s) // 2`，否则前后缀会重叠',
                 '易错：中间串为空返回 `0`；找不到相同前后缀返回 `1`（整串算一段）'],
    ),
)
