MAT = [[1, 2, 2], [3, 2, 4]]


def _color(S, i, j, v):
    if 'fa' not in S:
        return None
    n = len(S['matrix'][0])
    k = i * n + j
    r = k
    while S['fa'][r] != r:
        r = S['fa'][r]
    if r != k or S['size'][k] > 1:
        return 'purple'
    return None


def _rank(S):
    if 'order' not in S:
        return ''
    m, n = len(S['matrix']), len(S['matrix'][0])
    root = lambda k: k if S['fa'][k] == k else root(S['fa'][k])
    if 'res' in S and S.get('_line', 0) >= 87:
        return '最终秩 `res` = ==' + str(S['res']) + '=='
    cur = [['·' if S['order'][root(i * n + j)] is None else S['order'][root(i * n + j)] for j in range(n)] for i in range(m)]
    return '已定的秩（·=未定）：==' + str(cur) + '=='


CONFIG = dict(
    num=1632, title='矩阵转换后的秩', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='并查集缩点 + 拓扑排序',
    tags=['图论算法', '常用数据结构', '难度分 2471'][:2],
    code='''
class Solution(object):
    def matrixRankTransform(self, matrix):

        m = len(matrix)
        n = len(matrix[0])
        fa = list(range(m * n))
        size = [1] * (m * n)
        row = [[] for _ in range(m)]
        column = [[] for _ in range(n)]
        for i in range(m):
            for j in range(n):
                row[i].append((matrix[i][j], i * n + j))
                column[j].append((matrix[i][j], i * n + j))
        
        for i in range(m):
            row[i].sort()
            for j in range(1, n):
                if row[i][j][0] == row[i][j - 1][0]:
                    fa_l = self.find(row[i][j - 1][1], fa)
                    fa_r = self.find(row[i][j][1], fa)
                    if fa_l != fa_r:
                        if size[fa_l] < size[fa_r]:
                            fa[fa_l] = fa_r
                            size[fa_r] += size[fa_l]
                        else:
                            fa[fa_r] = fa_l
                            size[fa_l] += size[fa_r]
        
        for j in range(n):
            column[j].sort()
            for i in range(1, m):
                if column[j][i][0] == column[j][i - 1][0]:
                    fa_l = self.find(column[j][i - 1][1], fa)
                    fa_r = self.find(column[j][i][1], fa)
                    if fa_l != fa_r:
                        if size[fa_l] < size[fa_r]:
                            fa[fa_l] = fa_r
                            size[fa_r] += size[fa_l]
                        else:
                            fa[fa_r] = fa_l
                            size[fa_l] += size[fa_r]
        
        ind = [0] * (m * n)
        next = [set() for _ in range(m * n)]

        for i in range(m):
            for j in range(1, n):
                if row[i][j][0] > row[i][j - 1][0]:
                    fa_l = self.find(row[i][j - 1][1], fa)
                    fa_r = self.find(row[i][j][1], fa)
                    if fa_r not in next[fa_l]:
                        next[fa_l].add(fa_r)
                        ind[fa_r] += 1
        
        for j in range(n):
            for i in range(1, m):
                if column[j][i][0] > column[j][i - 1][0]:
                    fa_l = self.find(column[j][i - 1][1], fa)
                    fa_r = self.find(column[j][i][1], fa)
                    if fa_r not in next[fa_l]:
                        next[fa_l].add(fa_r)
                        ind[fa_r] += 1
    
        q = []
        l = r = 0
        for num in range(m * n):
            if self.find(num, fa) == num and ind[num] == 0:
                q.append(num)
                r += 1
        
        step = 0
        order = [None] * (m * n)
        while l < r:
            new_r = r
            step += 1
            for num in q[l : r]:
                order[num] = step
                for next_num in next[num]:
                    ind[next_num] -= 1
                    if ind[next_num] == 0:
                        q.append(next_num)
                        new_r += 1

            l, r = r, new_r
        
        res = [[None] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                res[i][j] = order[self.find(i * n + j, fa)]
        
        return res

    def find(self, now, fa):
        if now != fa[now]:
            fa[now] = self.find(fa[now], fa)
        return fa[now]
''',
    call=f'Solution().matrixRankTransform({MAT})',
    expect=[[1, 2, 2], [3, 2, 4]],
    views=[
        dict(type='grid', var='matrix', h=190, cell=90, label='matrix（紫 = 同行同列相等、已并成一个点）',
             color=_color),
        dict(type='array', var='fa', h=150, label='fa[k]（并查集父亲，编号 k = i*n+j）'),
        dict(type='array', var='ind', h=150, label='ind[k]（缩点后的入度）',
             color=lambda S, i, v: 'green' if v == 0 and S.get('_line', 0) >= 78 else None),
        dict(type='array', var='order', h=150, label='order[k]（拓扑轮次 = 秩）', pointers={'num': 'blue'}),
        dict(type='text', fn=_rank, size=26, h=70),
    ],
    watch=['fa_l', 'fa_r', 'step', ('q', 'q', 'cyan')],
    captions={
        'fa = list(range': '并查集 `fa`：每个位置先是自己的父亲，编号 `i*n+j`',
        'row[i].sort()': '第 `{i}` 行按值排序：`{row[i]}`（值，编号）',
        'column[j].sort()': '第 `{j}` 列按值排序：`{column[j]}`',
        'fa_l = self.find(row[i][j - 1][1], fa)': lambda S, B, r: f'同行相邻两个值相等 `{S.row[S.i][S.j][0]}`：找它们的根 `{S.fa_l}` 和 `{S.fa_r}`' if 'fa_l' in S else '找根',
        'fa[fa_l] = fa_r': '小的并到大的下面：`fa[{fa_l}] = {fa_r}`，==相等的数合成一个点==',
        'fa[fa_r] = fa_l': '`fa[{fa_r}] = {fa_l}`，把 `{fa_r}` 并到 `{fa_l}`，==相等的数合成一个点==',
        52: '同行相邻且前小后大：根 `{fa_l}` → `{fa_r}` 连一条有向边',
        61: '同列相邻且前小后大：根 `{fa_l}` → `{fa_r}` 连一条有向边',
        53: '`{fa_r}` 的入度 +1 → `{ind[fa_r]}`（又多一个更小的点要先算）',
        62: '`{fa_r}` 的入度 +1 → `{ind[fa_r]}`（又多一个更小的点要先算）',
        'q.append(num)': '`{num}` 是根且入度为 0：==没有更小的前驱==，第一轮就能确定，入队',
        'step += 1': '新一轮：`step = {step}`，这一轮的点秩都是 `{step}`',
        'order[num] = step': '点 `{num}` 的秩 = 轮次 `{step}`，即 `order[{num}] = {step}`',
        'ind[next_num] -= 1': '后继 `{next_num}` 少一个前驱：入度 → `{ind[next_num]}`',
        'q.append(next_num)': '`{next_num}` 的所有前驱都算完了，进下一轮队列',
        'res[i][j] = order[': '位置 `({i},{j})` 的秩 = 它所在缩点的轮次 = =={order[fa[i*n+j]]}==',
        'return res': '返回每个位置的秩 `{res}`',
    },
    skip=['m = len', 'n = len', 'size = [1]', 'row = [[]', 'column = [[]', 'for i in range', 'for j in range',
          'row[i].append', 'column[j].append', 'ind = [0]', 'next = [set', 'l = r = 0', 'q = []', 'r += 1', 'step = 0', 'order = [None]',
          'new_r = r', 'new_r += 1', 'size[fa_', 'if row[i][j][0]', 'if column[j][i][0]', 'if fa_l != fa_r',
          'if size[fa_l]', 'else:', 'fa_r = self.find', 'if fa_r not in', 'for num in', 'for next_num', 'res = [[None]',
          'if ind[next_num]', 'if self.find(num', 'while l < r', 'l, r = r, new_r', 'column[j][i - 1][1], fa)', 'row[i][j - 1][1], fa)',
          'if now != fa[now]', 'fa[now] = self.find', 'return fa[now]', 'def find', 'row[i][j][1], fa)', 'column[j][i][1], fa)'],
    max_steps=100,
    cards=dict(
        one_liner='相等的数缩成一个点，再按「小→大」拓扑排序，轮次就是秩',
        complexity='时间 `O(mn log(mn))`，空间 `O(mn)`',
        problem=['给整数矩阵，求每个元素的「秩」：比同行同列别的元素大，秩就更大',
                 '==同行或同列相等的元素，秩必须相同==；秩尽量小',
                 '本视频：`[[1,2,2],[3,2,4]]` → `[[1,2,2],[3,2,4]]`'],
        quote='一个自然的想法就是将所有行列相连的x缩成一个节点，在这里可以使用bfs或者并查集来做。',
        quote_src='—— yiduobo 题解原文',
        idea=['不考虑相等：每个数只需看行、列里「刚好比它小」的那个数',
              '相等的数会让边数爆炸 → 用并查集把同行同列相等的合成一个点',
              '行、列里相邻且不等的点连边 小→大，再拓扑排序，轮次就是秩'],
        summary=['时间 `O(mn log(mn))`（排序），空间 `O(mn)`',
                 '易错：==先合并相等的数，再建边==；边要用并查集的根去连',
                 '拓扑起点：必须是根且入度为 0',
                 '原文为 Python 2 写法，`fa = range(m * n)` 已改为 `list(range(m * n))`（Python 3 的 range 不能改元素）'],
    ),
)
