def _txt(S):
    s, c = S.get('s'), S.get('c')
    if s is None:
        return ''
    k = s.count(c)
    return f"`s` 中有 `k = {k}` 个 `{c}`：每个 `{c}` 配上自己或左边的 `{c}`，共 `1+2+…+{k} = {k}×{k+1}/2` = =={k*(k+1)//2}=="


CONFIG = dict(
    num=3084, title='统计以给定字符开头和结尾的子字符串总数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='组合数 · C(k+1, 2)',
    tags=[],
    code='''
class Solution:
    def countSubstrings(self, s: str, c: str) -> int:
        return comb(s.count(c) + 1, 2)
''',
    call="Solution().countSubstrings('abcabadaa', 'a')",
    expect=15,
    views=[
        dict(type='string', var='s', h=220, cell=70, color=lambda S, i, v: 'green' if S.get('c') is not None and v == S['c'] else None,
             dim=lambda S, i, v: S.get('c') is not None and v != S['c']),
        dict(type='text', h=150, size=38, fn=_txt),
    ],
    watch=['s', 'c'],
    captions={
        'return comb': '`s.count(c)` = ==`{s.count(c)}`== 个 `{c}`；每个 `{c}` 可以和自己或左边的 `{c}` 配成一个子串，共 `1+2+…+{s.count(c)}`，即 `comb({s.count(c)}+1, 2)` = =={ret}==',
    },
    cards=dict(
        one_liner='k 个 c，每个 c 配自己和左边的 c，共 k(k+1)/2 个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数 `s` 里以字符 `c` 开头并以 `c` 结尾的非空子串个数',
                 '示例：`s = "abada", c = "a"` → `6`；`"zzz"`, `"z"` → `6`',
                 '本例演示：`s = "abcabadaa"`，`c = "a"`'],
        quote='每个 c 都可以和它自己或左边的 c 形成（对应着）一个符合要求的子串，所以一共有 1+2+⋯+k = k(k+1)/2 个符合要求的子串。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把子串看成「右端点是某个 `c`」，左端点可选它自己或更左的 `c`',
              '第 1 个 `c` 有 1 种，第 2 个有 2 种……第 `k` 个有 `k` 种',
              '求和得 `k(k+1)/2`，也就是 `comb(k+1, 2)`：从 `k+1` 个位置里选 2 个'],
        after=[dict(heading='本例拆开数一遍', lines=[
            '`abcabadaa` 里有 5 个 `a`（下标 0, 3, 5, 7, 8）',
            '右端点依次是第 1…5 个 `a`：分别有 1, 2, 3, 4, 5 种左端点',
            '`1+2+3+4+5` = ==15==，与 `comb(6, 2) = 15` 一致'])],
        summary=['时间 `O(n)`，空间 `O(1)`：只要数一遍 `c` 的个数',
                 '==别漏掉单个字符的子串==（自己配自己），所以是 `k+1` 而不是 `k`',
                 '`comb(k+1, 2)` 等价于 `k*(k+1)//2`',
                 '`k = 0` 时 `comb(1, 2) = 0`，没有 `c` 就是 0']),
)
