A_ = [1, 2, 3, 2, 1]
B_ = [3, 2, 1, 4, 7]


def _cell(S, r, c, v):
    if 'i' not in S or 'j' not in S or S['_line'] not in (10, 11, 12):
        return None
    i, j = S['i'], S['j']
    if (r, c) == (i, j):
        return 'yellow'
    if A_[i - 1] == B_[j - 1]:
        k = 1
        while k <= S['f'][i][j] - 1:       # 整条对角线：当前匹配到的公共子串
            if (r, c) == (i - k, j - k):
                return 'cyan'
            k += 1
    return None


def _match(S):
    if 'i' in S and 'j' in S and S['_line'] in (11, 12):
        i, j, L = S['i'], S['j'], S['f'][S['i']][S['j']]
        return f'对角线上的公共子串：`A[{i - L}..{i - 1}] = B[{j - L}..{j - 1}] = {A_[i - L:i]}`，长度 =={L}=='
    if 'i' in S and 'j' in S and S['_line'] == 10:
        i, j = S['i'], S['j']
        return f'比较 `A[{i - 1}] = {A_[i - 1]}` 和 `B[{j - 1}] = {B_[j - 1]}`'
    return '`f[i][j]`：以 `A[i-1]` 和 `B[j-1]` ==结尾==的子串最长能匹配多长'


def _if(S, B, ret):
    i, j = S.i, S.j
    a, b = A_[i - 1], B_[j - 1]
    if a == b:
        return f'`A[{i - 1}] = B[{j - 1}] = {a}` → 匹配可以延长'
    return f'`{a}` ≠ `{b}` → `f[{i}][{j}] = 0`'


CONFIG = dict(
    num=718, title='最长重复子数组', difficulty='Medium', category='多维动态规划',
    author='yiduobo', technique='最长公共子串 · O(n^2) 动态规划',
    tags=['字节30天', '热题173'],
    code='''
class Solution(object):
    def findLength(self, A, B):

        n = len(A)
        m = len(B)
        f = [[0] * (m + 1) for _ in range(n + 1)]
        res = 0
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if A[i - 1] == B[j - 1]:
                    f[i][j] = f[i - 1][j - 1] + 1
                    res = max(res, f[i][j])

        return res
''',
    call=f'Solution().findLength({A_}, {B_})',
    expect=3,
    skip=['n = len', 'm = len', 'for j in range'],
    views=[
        dict(type='text', fn=_match, size=26),
        dict(type='table', var='f', label='f：行头 = A [1,2,3,2,1]，列头 = B [3,2,1,4,7]（青 = 同一条对角线上的匹配）', h=560, cell=84,
             color=_cell, rows=lambda S: ['—'] + [str(x) for x in A_], cols=lambda S: ['—'] + [str(y) for y in B_],
             cursors=[('i', 'j', 'yellow', '')]),
    ],
    watch=[('i', 'i', 'pink'), ('j', 'j', 'cyan'), ('res', 'res', 'green')],
    captions={
        'f = [[0]': '`f[i][j]` 对应 `A[i-1]`、`B[j-1]`，第 0 行/列全为 0',
        'res = 0': '`res` 记录最长匹配长度',
        'for i in range(1, n + 1)': lambda S, B, ret: (f'`i = {S.i}`：以 `A[{S.i - 1}] = {A_[S.i - 1]}` 结尾'
                                                       if B.get('i') != S.i else '所有 `i` 都处理完'),
        'if A[i - 1] == B[j - 1]': _if,
        'f[i][j] = f[i - 1][j - 1] + 1': '`f[{i}][{j}] = f[{i - 1}][{j - 1}] + 1 = {f[i][j]}`：沿对角线接上',
        'res = max': lambda S, B, ret: (f'`res = max({B.res}, {S.f[S.i][S.j]}) = {S.res}`' + ('，==更新==' if S.res > B.res else '')),
        'return res': '最长公共子串长度 =={ret}==',
    },
    cards=dict(
        one_liner='最长公共子串：相等就沿对角线 +1，不等就归零',
        complexity='时间 `O(nm)`，空间 `O(nm)`',
        problem=['给两个整数数组 `A`、`B`，返回两个数组中==公共的、长度最长的子数组==的长度',
                 '子数组必须==连续==',
                 '示例：`[1,2,3,2,1]`、`[3,2,1,4,7]` → `3`（`[3,2,1]`）'],
        quote='最长公共子串问题，经典做法是O(n^2)的动态规划，令f[i][j]表示==以A[i - 1]以及B[j - 1]结尾的子串最长能匹配的长度==，若A[i - 1] = B[j - 1]，f[i][j] = f[i - 1][j - 1] + 1，否则f[i][j] = 0。',
        quote_src='—— yiduobo 题解原文',
        idea=['子数组就是“子串”：要求以某个位置结尾才能保证连续',
              '相等：在 `f[i-1][j-1]` 的基础上延长一位；不相等：匹配断了，归零',
              '每次更新顺手维护 `res`'],
        result='最长公共子串 `[3,2,1]`，长度 `3` ✓',
        after=[dict(heading='yiduobo 提到的更好做法：后缀数组', lines=[
            '把 `A`、`B` 用分隔符拼起来：`1 2 3 2 1 # 3 2 1 4 7`',
            '找两个后缀：一个含 `#`、一个不含，使==最长公共前缀==最长',
            '这里是 `3 2 1 4 7` 和 `3 2 1 # 3 2 1 4 7` → `3 2 1`',
            '后缀排序用倍增 `O(n log n)` 或 DC3 `O(n)`；但 DP 实现简单得多',
        ])],
        summary=['时间 `O(nm)`，空间 `O(nm)`',
                 '不相等时是 `0`（匹配断了），这是子串和子序列（1143）的区别',
                 '答案不在右下角，要一路维护 `res`',
                 '原文为 Python 2 风格，只删去了文档字符串',
                 '对比灵神：同一个 DP，灵神从 1143 类比入手，最后用 `max(map(max, f))` 取答案'],
    ),
)
