def _pad(S):
    w = S.get('words')
    if not w:
        return None
    n = max(len(x) for x in w)
    return [list(x) + [''] * (n - len(x)) for x in w]


def _color(S, r, c, v):
    if 'i' not in S or 'j' not in S:
        return None
    i, j = S['i'], S['j']
    if (r, c) == (i, j):
        return 'blue'
    if (r, c) == (j, i):
        return 'pink'
    return None


def _cap_i(S, B, ret):
    return f'第 `{S.i}` 行：`n = len(words[{S.i}]) = {S.n}`，只枚举这一行实际有的 {S.n} 个字符'


def _cap_len_rows(S, B, ret):
    i, j = S.i, S.j
    return f'`len(words) = {len(S.words)}` ' + (f'≤ `j = {j}` → ==没有第 {j} 行==，对不上 → 返回 False' if len(S.words) <= j else f'> `j = {j}` → 有第 {j} 行')


def _cap_len_cols(S, B, ret):
    i, j = S.i, S.j
    return f'`len(words[{j}]) = {len(S.words[j])}` ' + (f'≤ `i = {i}` → 第 {j} 行==没有第 {i} 列==，返回 False' if len(S.words[j]) <= i else f'> `i = {i}` → 第 {j} 行有第 {i} 个字符')


def _cap_cmp(S, B, ret):
    i, j = S.i, S.j
    a, b = S.words[j][i], S.words[i][j]
    return f"比较 `words[{j}][{i}] = '{a}'` 和 `words[{i}][{j}] = '{b}'`" + (' → ==相等==' if a == b else ' → ==不等，转置后对不上== → 返回 False')


CONFIG = dict(
    num=422, title='有效单词方块', difficulty='Easy', category='字符串',
    author='yiduobo', technique='枚举字符 · 对比转置位置',
    tags=[],
    code='''
class Solution(object):
    def validWordSquare(self, words):

        m = len(words)
        for i in range(m):
            n = len(words[i])
            for j in range(n):
                if i == j:
                    continue
                if len(words) <= j:
                    return False
                if len(words[j]) <= i:
                    return False
                if words[j][i] != words[i][j]:
                    return False
        return True
''',
    call='''Solution().validWordSquare(["abc", "bd", "c"])
Solution().validWordSquare(["ball", "area", "read", "lady"])''',
    expect=False,
    views=[
        dict(type='grid', var=_pad, label='words 排成字符方块（蓝 = words[i][j]，粉 = 它的镜像 words[j][i]）', cell=96, h=420,
             color=_color),
        dict(type='text', size=24, h=60,
             fn=lambda S: (f"第 k 行 = 第 k 列：`words[{S['j']}][{S['i']}]` 要等于 `words[{S['i']}][{S['j']}]`" if 'j' in S and 'i' in S
                           else '有效方块：第 k 行和第 k 列读出来的字符串完全相同')),
        dict(type='text', fn=lambda S: '两个示例依次运行：第一个有效 → True；第二个不对称 → False', size=22, h=50),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'm', 'n'],
    captions={
        'm = len(words)': '`m = {m}`：一共 {m} 行',
        'for i in range': lambda S, B, r: (f'枚举第 `{S.i}` 行' if S.get('i') != B.get('i') or 'i' not in B else '所有行都检查完了'),
        'n = len(words[i])': _cap_i,
        'if i == j': lambda S, B, r: (f'`i == j = {S.i}`：对角线上的字符转置后还在原位，不用比 → 跳过' if S.i == S.j
                                      else f'`i = {S.i}` ≠ `j = {S.j}` → 需要和镜像位置比较'),
        'continue': '对角线，跳过',
        'if len(words) <= j': _cap_len_rows,
        'if len(words[j]) <= i': _cap_len_cols,
        'if words[j][i] != words[i][j]': _cap_cmp,
        'return False': '有一个位置对不上 → 不是有效单词方块，返回 `False`',
        'return True': '所有位置都对得上 → 返回 `True`',
    },
    cards=dict(
        one_liner='枚举每个字符，看它转置后的位置是不是同一个字母',
        complexity='时间 `O(总字符数)`，空间 `O(1)`',
        problem=['给你一个单词序列 `words`，判断它是否构成有效单词方块',
                 '有效：对任意 `k`，==第 k 行读出的字符串 = 第 k 列读出的字符串==',
                 '各行长度可以不同。示例：`["abc","bd","c"]` → `true`（各行长度不同）',
                 '`["ball","area","read","lady"]` → `false`'],
        quote='对于所有i与j不同的word[i][j]，其对应的字符应该是word[j][i]，那么若word没有j这一行，或者word[j]没有i这一列，或者word[i][j]不等于word[j][i]，那么就直接返回false。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模小，直接枚举每个字符 `words[i][j]`',
              '它的镜像是 `words[j][i]`；行数不够、列数不够、字符不同，任何一种都说明不对称',
              '`i == j` 的对角线字符不用比'],
        summary=['时间 `O(总字符数)`，空间 `O(1)`',
                 '易错：访问 `words[j][i]` 前，必须先检查 `len(words) > j` 和 `len(words[j]) > i`',
                 '各行长度可以不同，所以每行重新取 `n = len(words[i])`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
