M = [[1, -1], [-1, 1]]


def _cell(S, r, c, v):
    l, rr, idx = S.get('l'), S.get('r'), S.get('index')
    if l is None or rr is None or 'f' not in S:
        return None
    if l <= c <= rr:
        return 'yellow' if idx is not None and r == idx else ('blue' if idx is not None and r < idx else None)
    return None


def _txt(S):
    l, r, idx = S.get('l'), S.get('r'), S.get('index')
    if l is None or r is None or 'f' not in S:
        return '先算每行前缀和 `s_row`，再枚举列区间 `[l, r]`，从上到下累加行的区间和'
    if idx is None:
        return f'列区间 `[{l}, {r}]`：从上往下逐行累加'
    return f'列区间 `[{l}, {r}]`，到第 `{idx}` 行：累计和 `s = {S.get("s")}`'


CONFIG = dict(
    num=1074, title='元素和为目标值的子矩阵数量', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='行前缀和 + 枚举列区间 + 哈希表',
    tags=['前缀和与哈希表', '难度分 2189'],
    code='''
class Solution(object):
    def numSubmatrixSumTarget(self, matrix, target):

        m = len(matrix)
        n = len(matrix[0])
        s_row = []
        for i in range(m):
            s_row.append([matrix[i][0]])
            for j in range(1, n):
                s_row[-1].append(s_row[-1][-1] + matrix[i][j])
        
        res = 0
        for l in range(n):
            for r in range(l, n):
                f = {0:1}
                s = 0
                for index in range(m):
                    if l == 0:
                        now = s_row[index][r]
                    else:
                        now = s_row[index][r] - s_row[index][l - 1]
                    
                    s += now
                    res += f.get(s - target, 0)
                    f[s] = f.get(s, 0) + 1
        
        return res
''',
    call=f'Solution().numSubmatrixSumTarget({M}, 0)',
    expect=5,
    skip=['m = len', 'n = len', 's_row = []', 'for i in range(m)', 's_row.append', 'for j in range(1, n)',
          's_row[-1].append', 'res = 0', 'if l == 0', 'else:'],
    views=[
        dict(type='grid', var='matrix', label='matrix（蓝 = 已累加的行，黄 = 当前行；只看列区间 l..r）', cell=90, h=230, color=_cell),
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='table', var='s_row', label='s_row（每行的前缀和）', cell=80, h=190),
        dict(type='map', var='f', label='f（前缀和 → 出现次数，一开始 {0:1}）', fmt=lambda k, v: f'{k}: {v}', h=170, font=30),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('index', 'index'), ('s', 's', 'orange'), ('res', 'res', 'green')],
    captions={
        'for l in range(n)': lambda S, B, r: (f'枚举列区间的起点 `l = {S.l}`' if 'l' not in B or S.l != B.l else '所有列区间都枚举完了'),
        'for r in range(l, n)': '`r` 取下一个终点（取完则换起点 `l`）：列区间 `[{l}, {r}]`',
        'f = {0:1}': '`f` 记录“上方各行累计和”出现的次数，空前缀 `0` 先放一个',
        's = 0': '`s` 从上往下累加每行在 `[l, r]` 的和',
        'for index in range(m)': lambda S, B, r: (f'处理第 `{S.index}` 行' if 'index' not in B or S.index != B.index else '所有行处理完，换下一个终点'),
        'now = s_row[index][r] - s_row[index][l - 1]': '行区间和 = `s_row[{index}][{r}] − s_row[{index}][{l - 1}]` = =={now}==',
        'now = s_row[index][r]': '`l = 0`，行区间和直接是 `s_row[{index}][{r}]` = =={now}==',
        's += now': '`s` → {s}：从第 0 行到第 {index} 行的累计和',
        'res += f.get': '找以前出现过几次 `s - target = {s - target}`：每次出现就对应一个和为 `{target}` 的子矩阵 → `res = {res}`',
        'f[s] =': '把当前累计和 `{s}` 记入 `f`（次数 {f[s]}）',
        'return res': '一共 `{res}` 个子矩阵',
    },
    cards=dict(
        one_liner='先枚举列区间，再把每行的和当一维数组做前缀和',
        complexity='时间 `O(n²m)`，空间 `O(mn)`',
        problem=['给矩阵 `matrix` 和 `target`，数元素和等于 `target` 的非空子矩阵个数',
                 '示例：`[[1,-1],[-1,1]]`，`target = 0` → `5`',
                 '本视频用这个例子'],
        quote='如果我们优先枚举每一行的起始与结束，那么通过行的前缀和，我们就可以高效地计算出当前行在这个列区间之内的和，接下来问题就转化成了给出一个数组，求这个数组区间和等于target的区间数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['先算每行的前缀和 `s_row`，任意列区间的行和 O(1)',
              '枚举 `(l, r)`，从上往下累加成 `s`：行区间 = 一维数组的元素',
              '`f` 里存 `s` 出现的次数，查 `s − target`，再放入 `s`'],
        summary=['时间 `O(n²m)`，空间 `O(mn)`',
                 '`f = {0:1}` 表示空前缀；先查 `f` 再放当前 `s`',
                 '`l == 0` 时没有 `s_row[index][l-1]`，要单独处理',
                 '对比灵神：灵神枚举上下边界压列和；yiduobo 枚举列区间对行累加，思路对称',
                 '原文本身可直接运行，代码未改'],
    ),
)
