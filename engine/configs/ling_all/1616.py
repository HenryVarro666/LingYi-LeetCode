CONFIG = dict(
    num=1616, title='分割两个字符串得到回文串', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='相向双指针 · 前后缀匹配',
    tags=['贪心与思维', '难度分 1868'],
    code='''
class Solution:
    def checkPalindromeFormation(self, a: str, b: str) -> bool:
        # 如果 a_prefix + b_suffix 可以构成回文串则返回 True，否则返回 False
        def check(a: str, b: str) -> bool:
            i, j = 0, len(a) - 1  # 相向双指针
            while i < j and a[i] == b[j]:  # 前后缀尽量匹配
                i += 1
                j -= 1
            s, t = a[i: j + 1], b[i: j + 1]  # 中间剩余部分
            return s == s[::-1] or t == t[::-1]  # 判断是否为回文串
        return check(a, b) or check(b, a)
''',
    call='Solution().checkPalindromeFormation("ulacfd", "jizalu")',
    expect=True,
    views=[
        dict(type='string', var='a', label='a（前缀来自这里）', h=200, cell=80, pointers={'i': 'blue'},
             window=('i', 'j')),
        dict(type='string', var='b', label='b（后缀来自这里）', h=200, cell=80, pointers={'j': 'pink'},
             window=('i', 'j')),
        dict(type='text', size=26, h=60, fn=lambda S: (f"剩余中间：`a[{S['i']}:{S['j']+1}] = {S['s']!r}`，`b[{S['i']}:{S['j']+1}] = {S['t']!r}`" if 's' in S and 't' in S else '`a` 的前缀 + `b` 的后缀，从两头往里匹配')),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('s', 's', 'cyan'), ('t', 't', 'orange')],
    captions={
        'i, j = 0': '`i` 从 a 头、`j` 从 b 尾出发，相向而行',
        'while i < j and a[i] == b[j]': lambda S, B, r: (f'`a[{S.i}] = {S.a[S.i]}`，`b[{S.j}] = {S.b[S.j]}`：' + ('==相等==，这一对可以在回文两端配对 → 往里走' if S.i < S.j and S.a[S.i] == S.b[S.j] else '不等（或指针相遇），==前后缀匹配到此为止==')),
        'i += 1': '`i` → {i}',
        'j -= 1': '`j` → {j}',
        's, t = ': '匹配停下的位置正好是中间段的边界：`s = a[{i}:{j+1}] = {s!r}`，`t = b[{i}:{j+1}] = {t!r}`',
        'return s == s[::-1]': '中间段只要 `s`（取自 a）或 `t`（取自 b）有一个是回文，整体就是回文 → =={ret}==',
        'return check(a, b)': '先试 `a 前缀 + b 后缀`；不行再把 a、b 互换试 `b 前缀 + a 后缀`，两者有一个成立即可',
    },
    cards=dict(
        one_liner='先让两头尽量互相配对，剩下的中间段自己是回文即可',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`a`、`b` 等长，在同一下标把两个串都切开',
                 '判断 `a前缀 + b后缀` 或 `b前缀 + a后缀` 能否是回文串',
                 '示例：`a="ulacfd"`, `b="jizalu"` → `True`（`ula + alu`）'],
        quote='双指针前后缀匹配结束后，两个指针指向的位置恰好就是接下来要判断的回文串的左右边界，所以这两块代码逻辑可以无缝对接。',
        quote_src='—— 灵茶山艾府题解',
        idea=['拼接串的两头必须配对：`a[i] == b[j]` 就一直往里走',
              '停下后，中间段整个取自 a 或整个取自 b',
              '所以只要 `a[i..j]` 或 `b[i..j]` 是回文就行；a、b 角色互换再来一次'],
        summary=['时间 `O(n)`，空间 `O(1)`（切片会额外占空间，可手写回文判断）',
                 '易错：`check(a, b)` 与 `check(b, a)` 都要试',
                 '双指针停下的 `i, j` 直接作为中间段边界，不要多切或少切',
                 '对比 yiduobo：他先找中心回文再向外匹配，灵神是从外向内匹配'],
    ),
)
