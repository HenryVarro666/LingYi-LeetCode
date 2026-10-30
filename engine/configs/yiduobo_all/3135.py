_A, _B = 'axbcy', 'bcdy'


def _col(S, i, j, v):
    if 'ma' in S and v == S['ma'] and v > 0:
        return 'green'
    return None


CONFIG = dict(
    num=3135, title='通过添加或删除结尾字符来同化字符串', difficulty='Medium', category='字符串',
    author='yiduobo', technique='最长公共子串 DP',
    tags=['灵神题单', '字符串'],
    code='''
class Solution(object):
    def minOperations(self, initial, target):

        m = len(initial)
        n = len(target)

        f = [[0] * (n + 1) for _ in range(m + 1)]
        ma = 0
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if initial[i - 1] == target[j - 1]:
                    f[i][j] = f[i - 1][j - 1] + 1
                    ma = max(ma, f[i][j])
        
        return m + n - ma * 2
''',
    call="Solution().minOperations('axbcy', 'bcdy')",
    expect=5,
    views=[
        dict(type='string', var='initial', label='initial（蓝 = initial[i-1]）', h=120, index=False,
             color=lambda S, k, v: 'blue' if 'i' in S and k == S['i'] - 1 else None),
        dict(type='string', var='target', label='target（粉 = target[j-1]）', h=120, index=False,
             color=lambda S, k, v: 'pink' if 'j' in S and k == S['j'] - 1 else None),
        dict(type='table', var='f', label='f[i][j]：以这两个字符结尾的最长公共子串', h=360, cell=70,
             rows=lambda S: [''] + list(_A), cols=lambda S: [''] + list(_B),
             cursors=[('i', 'j', 'yellow', '(i,j)')], color=_col),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ma', 'ma', 'green')],
    captions={
        'm = len': '`m = {m}`，`initial` 的长度',
        'n = len': '`n = {n}`，`target` 的长度',
        'f = [[0]': '建 `f`，多一行一列放 0：公共子串长度从 0 开始数',
        'ma = 0': '`ma` 记录最长公共子串的长度',
        'if initial[i - 1]': lambda S, B, r: (f"`initial[{S.i-1}] = '{S.initial[S.i-1]}'` == `target[{S.j-1}] = '{S.target[S.j-1]}'` → ==能接在上一格后面=="
                                              if S.initial[S.i-1] == S.target[S.j-1]
                                              else f"`'{S.initial[S.i-1]}'` ≠ `'{S.target[S.j-1]}'` → 子串断开，`f[{S.i}][{S.j}]` 保持 0"),
        'f[i][j] = f[i - 1][j - 1] + 1': '`f[{i}][{j}] = f[{i-1}][{j-1}] + 1 = {f[i][j]}`：沿对角线把公共子串加长一位',
        'ma = max': '`ma = max({B.ma}, {f[i][j]}) = {ma}`',
        'return': '`{m} + {n} − 2×{ma}` = =={m + n - ma * 2}==：先删到只剩公共部分，再扩成 target',
    },
    cards=dict(
        one_liner='不用动的部分必是连续子串：求最长公共子串',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['每次操作可在 `initial` 的开头或末尾添加或删除一个字符',
                 '求把 `initial` 变成 `target` 的最少操作次数',
                 '本视频：`axbcy` → `bcdy`，答案 `5`'],
        quote='不需要进行操作的字符要么为空，要么是其中的一个连续子串……本题实际上求解的是initial和target的最长公共子串。',
        quote_src='—— yiduobo 题解原文',
        idea=['只能动两头 → 中间留下的字符必须连成一段，否则夹在中间的字符改不了',
              '留得越长越省，所以找最长公共子串',
              '`f[i][j]`：只有两个字符相等才等于 `f[i-1][j-1] + 1`，否则为 0'],
        summary=['答案 `m + n − 2×ma`：删 `m − ma` 个，再加 `n − ma` 个',
                 '子串要求连续，所以不等时置 0，不能像子序列那样取 max',
                 '时间 `O(mn)`，空间可滚动优化到 `O(n)`',
                 '原文为 Python 2 风格，但无需修改，代码逐字照搬'],
    ),
)
