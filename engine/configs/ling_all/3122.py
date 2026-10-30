def _cnt_text(S):
    if 'col' not in S or S.get('f0') is None:
        return '`f0` = 前面各列的最优解（保留元素个数最多），`f1` = 次优解（保留的元素与最优解不同）'
    c = {}
    for v in S['col']:
        c[v] = c.get(v, 0) + 1
    return '本列各数出现次数：' + '，'.join(f'`{v}`×{k}' for v, k in c.items()) + f'；上一列最优保留的数 `pre = {S["pre"]}`'


CONFIG = dict(
    num=3122, title='使矩阵满足条件的最少操作次数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='逐列递推 · 最优解 + 次优解',
    tags=['灵神题单', '其他线性 DP', '难度分 1905'],
    code='''
class Solution:
    def minimumOperations(self, grid: List[List[int]]) -> int:
        f0, f1, pre = 0, 0, -1
        for col in zip(*grid):
            mx, mx2, x = f0, 0, -1  # 不保留任何数字
            for v, c in Counter(col).items():
                res = (f0 if v != pre else f1) + c  # 保留元素 v
                if res > mx:  # 更新最优解和次优解
                    mx, mx2, x = res, mx, v
                elif res > mx2:  # 更新次优解
                    mx2 = res
            f0, f1, pre = mx, mx2, x
        return len(grid) * len(grid[0]) - f0
''',
    call='Solution().minimumOperations([[1, 1, 2, 1], [0, 1, 2, 2], [1, 1, 0, 2]])',
    expect=5,
    views=[
        dict(type='grid', var='grid', label='grid（同一列最终要变成同一个数，相邻列不能相同）', h=270, cell=80,
             color=lambda S, i, j, v: 'green' if v == S.get('x') and S.get('col') is not None and S['col'][i] == v and S.get('_line') in (10, 11) and False else None),
        dict(type='array', var='col', label='col：当前这一列', h=200, cell=80,
             color=lambda S, k, v: 'yellow' if v == S.get('v') and S.get('_line') in (6, 7, 8, 9) else None),
        dict(type='text', fn=_cnt_text, size=24, h=70),
    ],
    watch=[('f0 最优', 'f0', 'green'), ('f1 次优', 'f1', 'cyan'), ('pre', 'pre', 'pink'),
           ('mx', 'mx', 'blue'), ('mx2', 'mx2', 'blue'), ('v', 'v', 'yellow')],
    captions={
        'f0, f1, pre = 0, 0, -1': '反向思考：算==最多保留==多少个数不变。`f0` 最优、`f1` 次优，`pre = -1` 表示还没有上一列',
        'for col in zip': '逐列处理：`col = {col}`，同一列要变成同一个数',
        'mx, mx2, x = f0, 0, -1': '先假设本列==什么都不保留==（变成 -1）：最优 `mx = {f0}` 直接继承，所以不会因 `v == pre` 丢掉最优解',
        'for v, c in Counter': lambda S, B, r: f'枚举本列保留元素 `{S.v}`，它出现 `{S.c}` 次' if S.get('v') is not None and S.get('c') is not None else '本列的元素都试完了',
        'res = (f0 if v': lambda S, B, r: (f'`v = {S.v}` ≠ 上一列的 `pre = {S.pre}` → 接在最优解后：`{S.f0} + {S.c}` = =={S.res}=='
                                           if S.v != S.pre else
                                           f'`v = {S.v}` = `pre` → 相邻列相同不允许，只能接次优解：`{S.f1} + {S.c}` = =={S.res}=='),
        'if res > mx:': lambda S, B, r: (f'`{S.res} > mx = {S.mx2 if False else B.mx}` → 成为新的最优，原最优降为次优' if S.res > B.mx
                                         else f'`{S.res} ≤ mx = {B.mx}`，不是最优，再看能否当次优'),
        'mx, mx2, x = res, mx, v': '最优 `mx = {mx}`（保留 `{x}`），次优 `mx2 = {mx2}`',
        'elif res > mx2': lambda S, B, r: (f'`{S.res} > mx2 = {B.mx2}` → 更新次优解' if S.res > B.mx2 else f'`{S.res} ≤ mx2 = {B.mx2}`，不更新'),
        'mx2 = res': '次优 `mx2 = {mx2}`',
        'f0, f1, pre = mx, mx2, x': '本列算完：最优 `f0 = {f0}`（保留 `{pre}`），次优 `f1 = {f1}`',
        'return len(grid)': '总共 `{len(grid) * len(grid[0])}` 个格子，最多保留 `{f0}` 个 → 最少修改 =={ret}==',
    },
    max_steps=80,
    cards=dict(
        one_liner='反向思考：最多保留多少个数不变；只记最优和次优',
        complexity='时间 `O(mn)`，空间 `O(U)`（U 为元素种类数）',
        problem=['`m × n` 矩阵，每次可把任一格改成任意非负整数',
                 '要求：同一列上下相等，同一行左右相邻不相等',
                 '示例：`[[1,1,1],[0,0,0]]` → `3`；本视频：`3×4` 的矩阵 → `5`'],
        quote='对于 Python，在代码实现时，考虑到第 i 列可能只有一种元素 v，如果 v=pre 那么我们只会从次优解 f1 转移过来，忽略了最优解。我们可以选择不保留任何数字（都变成 -1）。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['同一列必须变成同一个数，所以反过来算：每列选一个数保留，其余改掉',
              '相邻列选的数不能相同：只需知道「上一列最优解」和「不用同一个数的次优解」',
              '本列选 `v`：若 `v ≠ pre` 接最优 `f0`，若 `v = pre` 只能接次优 `f1`，并同步更新新的最优和次优'],
        summary=['时间 `O(mn)`；空间 `O(U)`，U ≤ 10',
                 '易错：次优解必须来自「保留元素不同」的选择，否则相邻列会冲突',
                 '易错：只有一种元素且等于 pre 时，要靠「不保留」（-1）继承最优解',
                 '方法一（记忆化搜索）`dfs(i, j)` 枚举 `k ≠ j`，复杂度 `O(nU^2)`，本视频演示方法二',
                 '同类：枚举「不同于上一个」的选择都可以用最优/次优解优化'],
    ),
)
