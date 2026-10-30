A0, B0 = 'abac', 'cab'


def _ij(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or 'last' not in S:
        return None
    return i, j


def _cell(S, r, c, v):
    p = _ij(S)
    if p is None:
        return None
    i, j = p
    if (r, c) == (i, j):
        return 'yellow'
    if 'res' in S:
        return None
    if i > 0 and j > 0:
        if S['str1'][i - 1] == S['str2'][j - 1]:
            return 'green' if (r, c) == (i - 1, j - 1) else None
        return 'blue' if (r, c) in ((i - 1, j), (i, j - 1)) else None
    return 'blue' if (r, c) in ((i - 1, j), (i, j - 1)) else None


def _lcell(S, r, c, v):
    p = _ij(S)
    if p is not None and (r, c) == p:
        return 'yellow'
    return None


def _c1(S, k, v):
    p = _ij(S)
    return 'blue' if p and k == p[0] - 1 else None


def _c2(S, k, v):
    p = _ij(S)
    return 'pink' if p and k == p[1] - 1 else None


def _formula(S):
    p = _ij(S)
    if p is None:
        return '`f[i][j]` = 前 i 个与前 j 个字符的 LCS 长度；`last[i][j]` 记录从哪来'
    i, j = p
    if 'res' in S:
        return f'倒推：`last[{i}][{j}] = {S["last"][i][j]}`（0 = 补 str2，1 = 补 str1，2 = 公共字符）'
    return '`last`：0 = 补 str2[j-1]，1 = 补 str1[i-1]，2 = 公共字符（同时退两格）'


CONFIG = dict(
    num=1092, title='最短公共超序列', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='LCS + last 数组倒推还原',
    tags=['灵神题单', '动态规划', '难度分 1977'],
    code='''
class Solution(object):
    def shortestCommonSupersequence(self, str1, str2):

        m = len(str1)
        n = len(str2)
        f = [[0] * (n + 1) for _ in range(m + 1)]
        last = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0:
                    if j == 0:
                        continue
                    else:
                        f[i][j] = f[i][j - 1]
                        last[i][j] = 0
                elif j == 0:
                    f[i][j] = f[i - 1][j]
                    last[i][j] = 1
                elif str1[i - 1] == str2[j - 1]:
                    f[i][j] = f[i - 1][j - 1] + 1
                    last[i][j] = 2
                elif f[i][j - 1] > f[i - 1][j]:
                    f[i][j] = f[i][j - 1]
                    last[i][j] = 0
                else:
                    f[i][j] = f[i - 1][j]
                    last[i][j] = 1
                
        
        res = ''
        i = m
        j = n
        while i != 0 or j != 0:
            if last[i][j] == 0:
                res = str2[j - 1] + res
                j -= 1
            else:
                res = str1[i - 1] + res
                if last[i][j] == 2:
                    i -= 1
                    j -= 1
                else:
                    i -= 1
        
        return res
''',
    call=f'Solution().shortestCommonSupersequence({A0!r}, {B0!r})',
    expect='cabac',
    skip=['for j in range(n + 1)', 'else:', 'continue', 'last[i][j] = ', 'if i == 0', 'if j == 0', 'elif j == 0', 'i = m', 'j = n', 'last = [[0]', 'if last[i][j] == 2'],
    max_steps=100,
    views=[
        dict(type='string', var='str1', label='str1（蓝 = i-1）', h=125, cell=50, color=_c1),
        dict(type='string', var='str2', label='str2（粉 = j-1）', h=125, cell=50, color=_c2),
        dict(type='text', fn=_formula, size=22, h=80),
        dict(type='table', var='f', label='f[i][j]（黄 = 当前格，绿/蓝 = 来源）', h=280, cell=58,
             rows=lambda S: ['∅'] + list(A0), cols=lambda S: ['∅'] + list(B0), color=_cell),
        dict(type='table', var='last', label='last[i][j]', h=280, cell=58,
             rows=lambda S: ['∅'] + list(A0), cols=lambda S: ['∅'] + list(B0), color=_lcell),
    ],
    watch=['i', 'j', ('res', "res if 'res' in S else ''", 'green')],
    captions={
        'm = len(str1)': '`m = {m}`',
        'n = len(str2)': '`n = {n}`',
        'f = [[0]': '`f[i][j]`：`str1` 前 `i` 个与 `str2` 前 `j` 个的 LCS 长度；`last[i][j]`：记下它从哪个状态转移来，倒推用',
        'last = [[0]': '`last[i][j]`：记下 `f[i][j]` 是从哪个状态转移来的，最后倒推用',
        'for i in range(m + 1)': lambda S, B, r: (f'`i = {S.i}`：处理 `str1` 前 `i` 个字符' if S.i != B.get('i') else '`i` 枚举完了，表填完'),
        'if i == 0': lambda S, B, r: (f'`i = 0`：`str1` 为空' if S.i == 0 else f'`i = {S.i} ≠ 0`：`str1` 非空'),
        'elif j == 0': lambda S, B, r: (f'`j = 0`：`str2` 为空，答案只能是 `str1` 的前缀' if S.j == 0 else f'`j = {S.j} ≠ 0`，继续比较字符'),
        'if j == 0': lambda S, B, r: ('`j = 0`：两个都是空串，跳过' if S.j == 0 else f'`j = {S.j} ≠ 0`：`str1` 为空，答案只能是 `str2` 的前缀'),
        'elif str1[i - 1] == str2[j - 1]': lambda S, B, r: (f'`str1[{S.i-1}] = str2[{S.j-1}] = {S.str1[S.i-1]}` → ==公共字符，一个字符覆盖两边=='
                                                          if S.str1[S.i-1] == S.str2[S.j-1] else f'`str1[{S.i-1}] = {S.str1[S.i-1]}` ≠ `str2[{S.j-1}] = {S.str2[S.j-1]}`，不能共用'),
        'f[i][j] = f[i - 1][j - 1] + 1': '`f[{i}][{j}] = f[{i-1}][{j-1}] + 1` = =={f[i][j]}==，`last = 2`',
        'elif f[i][j - 1] > f[i - 1][j]': lambda S, B, r: (f'`f[{S.i}][{S.j-1}] = {S.f[S.i][S.j-1]}` > `f[{S.i-1}][{S.j}] = {S.f[S.i-1][S.j]}` → 从左边来，`str2[{S.j-1}]` 要另外补'
                                                          if S.f[S.i][S.j-1] > S.f[S.i-1][S.j] else f'`f[{S.i}][{S.j-1}] = {S.f[S.i][S.j-1]}` ≤ `f[{S.i-1}][{S.j}] = {S.f[S.i-1][S.j]}` → 从上边来，`str1[{S.i-1}]` 要另外补'),
        'f[i][j] = f[i][j - 1]': '`f[{i}][{j}]` = =={f[i][j]}==，`last = 0`：补 `str2[{j-1}]`',
        'f[i][j] = f[i - 1][j]': '`f[{i}][{j}]` = =={f[i][j]}==，`last = 1`：补 `str1[{i-1}]`',
        'res = \'\'': '动态规划结束，从右下角 `last[{m}][{n}]` 开始倒推答案',
        'i = m': '`i = {i}`',
        'j = n': '`j = {j}`',
        'while i != 0': lambda S, B, r: (f'`({S.i}, {S.j})` 还没回到原点，继续' if (S.i or S.j) else '回到 `(0, 0)`，倒推完成'),
        'if last[i][j] == 0': lambda S, B, r: (f'`last[{S.i}][{S.j}] = 0` → 补 `str2[{S.j-1}]` = `{S.str2[S.j-1]}`' if S.last[S.i][S.j] == 0
                                              else f'`last[{S.i}][{S.j}] = {S.last[S.i][S.j]}` → 补 `str1[{S.i-1}]` = `{S.str1[S.i-1]}`'),
        'res = str2[j - 1] + res': '补在最前面：`res = {res}`',
        'res = str1[i - 1] + res': '补在最前面：`res = {res}`',
        'if last[i][j] == 2': lambda S, B, r: ('`last = 2`：公共字符，`i`、`j` 一起退' if S.last[S.i][S.j] == 2 else '`last = 1`：只退 `i`'),
        'j -= 1': '`j` → {j}',
        'i -= 1': '`i` → {i}',
        'return res': '最短公共超序列：==`{ret}`==',
    },
    cards=dict(
        one_liner='先求 LCS，倒推时公共字符只放一次，其余各补各的',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['给两个字符串，求同时以它们为子序列的==最短字符串==',
                 '示例：`"abac"`、`"cab"` → `"cabac"`',
                 '本视频：同上，长度 `4 + 3 − LCS 2 = 5`'],
        quote='为了使答案最短，我们就需要尽可能地利用str1和str2中重复的部分，也就是说应当在str1和str2的最长公共子序列的基础上，在合适的位置插入str1和str2中剩余的字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用 DP 求 LCS：相同就 `f[i-1][j-1] + 1`，否则取上或左的较大者',
              '同步拼字符串空间太大，改记 `last[i][j]`：来自左、上、还是左上',
              '倒推：左上补公共字符；左补 `str2[j-1]`；上补 `str1[i-1]`'],
        summary=['时间 `O(mn)`，空间 `O(mn)`（`f` 和 `last` 两张表）',
                 '易错：下标 `i-1`、`j-1`，因为表多了空串的一行一列',
                 '易错：倒推要把字符补在 `res` ==最前面==，直到 `i` 和 `j` 都回到 0',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神 `f` 直接存超序列长度，yiduobo 存 LCS 长度并记录来源'],
    ),
)
