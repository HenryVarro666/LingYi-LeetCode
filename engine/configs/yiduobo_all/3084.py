CONFIG = dict(
    num=3084, title='统计以给定字符开头和结尾的子字符串总数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='计数 + 等差数列求和',
    tags=[],
    code='''
class Solution(object):
    def countSubstrings(self, s, c):

        freq = 0
        for char in s:
            if char == c:
                freq += 1
        
        return freq * (freq + 1) // 2
''',
    call="Solution().countSubstrings('zazbzz', 'z')",
    expect=10,
    views=[
        dict(type='string', var='s', h=220, cell=70,
             color=lambda S, i, v: ('green' if v == S['c'] and 'freq' in S else None) if 'c' in S else None,
             dim=lambda S, i, v: 'c' in S and v != S['c']),
        dict(type='text', h=150, size=38, fn=lambda S: (f"`freq = {S['freq']}`：已数到 {S['freq']} 个 `{S['c']}`" if 'freq' in S else '')),
    ],
    watch=['char', ('freq', 'freq', 'green')],
    captions={
        'freq = 0': '`freq` 记录字符 `{c}` 在 `s` 中出现的次数，从 0 开始',
        'for char in s': '看下一个字符：`char = {char!r}`',
        'if char == c': '`{char!r} == {c!r}`？→ {"==是==，计数" if char == c else "不是，跳过"}',
        'freq += 1': '又见到一个 `{c}`：`freq` 从 {B.freq} 变成 =={freq}==',
        'return freq': '第 1 个 `{c}` 有 `{freq}` 个可作结尾，第 2 个有 `{freq-1}` 个……共 `{freq}+{freq-1}+…+1` = `{freq}×{freq+1}÷2` = =={ret}==',
    },
    cards=dict(
        one_liner='数出 c 的个数 freq，答案是 freq+(freq-1)+…+1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['统计 `s` 中以字符 `c` 开头、也以 `c` 结尾的非空子串个数',
                 '示例：`"abada"`, `"a"` → `6`；`"zzz"`, `"z"` → `6`',
                 '本例演示：`s = "zazbzz"`，`c = "z"`'],
        quote='对于第一个 c，如果以这个 c 作为子串的开头，那么其后方包括其自身一共有 freq 个 c 可以作为子串的结尾，而对于第二个 c，则有 freq - 1 个可用的结尾，以此类推。',
        quote_src='—— yiduobo 题解',
        idea=['先遍历一遍数出 `c` 的个数 `freq`',
              '以第 `i` 个 `c` 开头：结尾可选它自己和后面所有的 `c`',
              '求和 `freq + (freq-1) + … + 1 = (freq+1)×freq/2`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '代码本身已是 `//` 整数除法，Python 3 下可直接运行',
                 '==开头可以和结尾是同一个字符==（单字符子串），所以求和从 `freq` 开始到 1',
                 '与灵神「每个 c 配左边的 c」是同一个等差数列，只是数的方向相反']),
)
