WORD = 'noosaba'


def _fn(S):
    if 'index' not in S:
        return '每个元音出现在多少个子字符串里，就贡献多少'
    i, n = S['index'], S['n']
    if S['word'][i] in S['char_set']:
        return f"元音 `{S['word'][i]}`：左边 {i + 1} 种起点 × 右边 {n - i} 种终点 = =={(i + 1) * (n - i)}=="
    return f"`{S['word'][i]}` 不是元音，没有贡献"


CONFIG = dict(
    num=2063, title='所有子字符串中的元音', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='贡献法',
    tags=['灵神题单·贪心与思维', '难度分 1663'],
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
    call=f'Solution().countVowels({WORD!r})',
    expect=49,
    views=[
        dict(type='string', var='word', label='word（绿 = 元音）', h=190, cell=90, pointers={'index': 'blue'},
             color=lambda S, i, v: ('green' if v in 'aeiou' else None) if 'char_set' in S else None),
        dict(type='text', fn=_fn, size=26, h=70),
        dict(type='set', var='char_set', label='char_set', h=110),
    ],
    watch=['n', 'index', ('res', 'res', 'green')],
    captions={
        'n = len(word)': '`n = {n}`',
        'res = 0': '`res` 累计所有子字符串里的元音总数',
        'char_set = set': '元音集合，`O(1)` 判断一个字符是不是元音',
        'for index in range(n)': '从左到右看第 `{index}` 个字符 `{word[index]}`',
        'if word[index] in char_set': lambda S, B, r: (f'`{S.word[S.index]}` ' + ('是元音 → 要算它的贡献' if S.word[S.index] in S.char_set else '不是元音 → 跳过')),
        'res += (index + 1)': '包含它的子串：起点 `{index + 1}` 种 × 终点 `{n - index}` 种 = `{(index + 1) * (n - index)}`，`res` → =={res}==',
        'return res': '所有子字符串里的元音总数 = =={ret}==',
    },
    cards=dict(
        one_liner='不数子串，数每个元音被多少个子串包含',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给你字符串 `word`，求它==所有子字符串==里元音（`a e i o u`）的总个数',
                 '示例：`"aba"` → `6`，`"abc"` → `3`',
                 '本视频：`"noosaba"`'],
        quote='对于单个元音字符而言，有多少个子字符串包含了该字符，该字符就会对最终答案做出多少贡献。',
        quote_src='—— yiduobo 题解原文',
        idea=['从单个字符出发：下标 `index` 的元音，左侧有 `index + 1` 种起点',
              '右侧有 `n - index` 种终点，相乘就是包含它的子串数',
              '一趟遍历，遇到元音就累加这个乘积'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：起点是 `index + 1` 种（含自己），终点是 `n - index` 种',
                 'Python 整数不会溢出；其他语言要用 64 位整数',
                 '原文为 Python 2 风格，本题代码无需改动'],
    ),
)
