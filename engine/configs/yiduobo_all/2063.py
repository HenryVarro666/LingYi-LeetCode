def _txt(S):
    if 'index' not in S or 'res' not in S:
        return ''
    n, k = S['n'], S['index']
    c = S['word'][k]
    if c in 'aeiou':
        return f"`{c}` 是元音：左侧 `{k+1}` 种 × 右侧 `{n-k}` 种 = =={(k+1)*(n-k)}=="
    return f"`{c}` 不是元音，不贡献"


CONFIG = dict(
    num=2063, title='所有子字符串中的元音', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='换个角度 · 单个元音的贡献',
    tags=['灵神题单', '贪心与思维', '难度分 1663'],
    code='''
class Solution(object):
    def countVowels(self, word):

        n = len(word)
        res = 0
        char_set = set(['a', 'e', 'i', 'o', 'u'])
        for index in range(n):
            if word[index] in char_set:
                res += (index + 1) * (n - index)
        return res
''',
    call='Solution().countVowels("abeco")',
    expect=19,
    views=[
        dict(type='string', var='word', label='word（蓝 = index，绿 = 已处理的元音）', cell=96, pointers={'index': 'blue'},
             color=lambda S, i, v: ('green' if v in 'aeiou' and 'index' in S and i <= S['index'] else None)),
        dict(type='set', var='char_set', label='char_set', h=110),
        dict(type='text', size=34, h=120, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('n', 'n'), ('res', 'res', 'green')],
    skip=['char_set = '],
    captions={
        'n = len': '`n = {n}`：字符串长度',
        'res = 0': '`res` 累计元音的总贡献',
        'for index': '看下标 `{index}` 的字符 `{word[index]}`',
        'if word[index] in char_set': lambda S, B, r: (f"`{S.word[S.index]}` 在元音集合里 → 算它的贡献" if S.word[S.index] in S.char_set else f"`{S.word[S.index]}` 不是元音 → 不算"),
        'res += (index + 1)': '左侧有 `{index+1}` 种选法、右侧有 `{n-index}` 种 → 包含它的子串 `{(index+1)*(n-index)}` 个，`res` = =={res}==',
        'return res': '总贡献 =={res}==',
    },
    cards=dict(
        one_liner='从单个元音出发：它出现在几个子串里，就贡献几次',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['求 `word` 所有子字符串中元音字母（`aeiou`）的总个数',
                 '示例：`"aba"` → `6`',
                 '本视频：`"abeco"` → `19`'],
        quote='从单个字符串的角度出发考虑是比较麻烦的，不妨转换一下思路，从单个元音字符串的角度出发来考虑。',
        quote_src='—— yiduobo 题解原文',
        idea=['下标 `index` 左侧有 `index` 个字符，右侧有 `n-index-1` 个',
              '子串左端有 `index+1` 种选法（可以就是它自己），右端有 `n-index` 种',
              '两者相乘 = 包含该字符的子串数，从左到右扫一遍累加'],
        summary=['时间 `O(n)`，空间 `O(1)`（元音集合大小固定）',
                 '易错点：左右两侧都要把「选自己」算进去，所以是 `index+1` 和 `n-index`',
                 '对比灵神：灵神直接写 `ch in "aeiou"`，yiduobo 先建元音集合',
                 '原文为 Python 2 风格，仅为 Python 3 运行，代码无需改动'],
    ),
)
