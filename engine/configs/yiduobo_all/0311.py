def _fmt_map(k, v):
    return f"{k}: " + ' '.join(f"({a},{b})" for a, b in v)


CONFIG = dict(
    num=311, title='稀疏矩阵的乘法', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='哈希表收集非零元素',
    tags=[],
    code='''
class Solution(object):
    def multiply(self, mat1, mat2):

        m = len(mat1)
        k = len(mat1[0])
        n = len(mat2[0])

        h1 = {}
        for i in range(m):
            for j in range(k):
                if mat1[i][j] != 0:
                    if j not in h1:
                        h1[j] = []
                    h1[j].append([i, mat1[i][j]])
        
        h2 = {}
        for j in range(k):
            for p in range(n):
                if mat2[j][p] != 0:
                    if j not in h2:
                        h2[j] = []
                    h2[j].append([p, mat2[j][p]])

        res = [[0] * n for _ in range(m)]
        for j in h1:
            for i, v1 in h1[j]:
                for p, v2 in h2.get(j, []):
                    res[i][p] += v1 * v2
        
        return res
''',
    call='Solution().multiply([[1, 0, 0], [-1, 0, 3]], [[7, 0, 0], [0, 0, 0], [0, 0, 1]])',
    expect=[[7, 0, 0], [-7, 0, 3]],
    views=[
        dict(type='grid', var='mat1', label='mat1（m × k）', cursors=[('i', 'j', 'blue')], cell=56, h=140),
        dict(type='grid', var='mat2', label='mat2（k × n）', cursors=[('j', 'p', 'pink')], cell=56, h=190),
        dict(type='grid', var='res', label='res（m × n）', cursors=[('i', 'p', 'green')], cell=56, h=140),
        dict(type='map', var='h1', label='h1：mat1 第 j 列的非零 (行 i, 值)', fmt=_fmt_map, h=125, font=26),
        dict(type='map', var='h2', label='h2：mat2 第 j 行的非零 (列 p, 值)', fmt=_fmt_map, h=125, font=26),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'cyan'), ('p', 'p', 'pink'), 'v1', 'v2'],
    skip=['m = len', 'k = len', 'n = len', 'h1 = {}', 'h2 = {}'],
    max_steps=110,
    captions={
        'if mat1[i][j] != 0': lambda S, B, r: (f"`mat1[{S.i}][{S.j}] = {S.mat1[S.i][S.j]}`：==非零== → 收集" if S.mat1[S.i][S.j] != 0
                                               else f"`mat1[{S.i}][{S.j}] = 0`：零不影响乘积 → 跳过"),
        'if j not in h1': '`h1` 里还没有第 {j} 列：先建空列表' ,
        'h1[j] = []': '为第 `{j}` 列建一个空列表',
        'h1[j].append': '第 `{j}` 列记下 `[行 {i}, 值 {mat1[i][j]}]`',
        'if mat2[j][p] != 0': lambda S, B, r: (f"`mat2[{S.j}][{S.p}] = {S.mat2[S.j][S.p]}`：==非零== → 收集" if S.mat2[S.j][S.p] != 0
                                               else f"`mat2[{S.j}][{S.p}] = 0`：零不影响乘积 → 跳过"),
        'if j not in h2': '`h2` 里还没有第 {j} 行：先建空列表',
        'h2[j] = []': '为第 `{j}` 行建一个空列表',
        'h2[j].append': '第 `{j}` 行记下 `[列 {p}, 值 {mat2[j][p]}]`',
        'res = [[0]': '结果矩阵 `res` 先全是 0',
        'for j in h1': '只枚举 mat1 里有非零元素的列（当前 `j = {j}`，没有下一列就结束）',
        'for i, v1 in h1[j]': '取 mat1 第 `{j}` 列的下一个非零元素（没有就换下一列）',
        'for p, v2 in h2.get': '取 mat2 第 `{j}` 行的下一个非零元素（行号必须等于 j 才能相乘；没有就结束）',
        'res[i][p] +=': '`res[{i}][{p}]` += `{v1} × {v2}` → =={res[i][p]}==',
        'return res': '乘积矩阵 `{res}`',
    },
    cards=dict(
        one_liner='零不影响乘积，只拿非零元素两两相乘',
        complexity='时间 `O(mk + kn + 非零对数)`，空间 `O(非零个数)`',
        problem=['给两个稀疏矩阵 `mat1`（m×k）、`mat2`（k×n），求 `mat1 × mat2`',
                 '稀疏 = 大部分元素是 0',
                 '示例：`[[1,0,0],[-1,0,3]]` × `[[7,0,0],[0,0,0],[0,0,1]]` → `[[7,0,0],[-7,0,3]]`'],
        quote='对于mat1中的(i, j)这个位置上的数，其只会与mat2中第j行上的数进行乘法，而mat1[i][j]与mat2[j][p]的乘积将被累加到答案数组的(i, p)这个位置上。',
        quote_src='—— yiduobo 题解原文',
        idea=['`mat1[i][j]` 只会和 `mat2` 的第 `j` 行相乘，结果累加到 `res[i][p]`',
              '先把 mat1 每一列、mat2 每一行的==非零值==收集进哈希表',
              '再按相同的 `j` 两两相乘，零根本不参与'],
        summary=['时间 `O(mk + kn + 非零对数)`，空间 `O(非零个数)`',
                 '`h2.get(j, [])`：mat2 的第 j 行可能全是 0，没有这个键',
                 '乘积要累加 `+=`，不是赋值',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码无需其他改动',
                 '本题库里没有题面，题意按题名与代码整理'],
    ),
)
