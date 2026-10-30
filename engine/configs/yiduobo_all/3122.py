CONFIG = dict(
    num=3122, title='使矩阵满足条件的最少操作次数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='按列 DP · 维护最优与次优',
    tags=['灵神题单', '其他线性 DP', '难度分 1905'],
    code='''
class Solution(object):
    def minimumOperations(self, grid):

        m = len(grid)
        n = len(grid[0])

        first_f = 0
        first_v = 0
        second_f = 0
        second_v = 1

        for j in range(n):
            pre_first_f, pre_first_v = first_f, first_v
            pre_second_f, pre_second_v = second_f, second_v
            first_f = second_f = -1

            freq = Counter()
            for i in range(m):
                freq[grid[i][j]] += 1
            
            for v in range(10):
                cost = m - freq[v]
                if v != pre_first_v:
                    f = pre_first_f + cost
                else:
                    f = pre_second_f + cost
                
                if first_f == -1 or f < first_f:
                    first_f, second_f = f, first_f
                    first_v, second_v = v, first_v
                elif second_f == -1 or f < second_f:
                    second_f = f
                    second_v = v
        
        return first_f
''',
    call='Solution().minimumOperations([[1, 1], [0, 1], [1, 2]])',
    expect=3,
    views=[
        dict(type='grid', var='grid', label='grid（黄框 = 当前处理的第 j 列）', h=270, cell=80,
             cursors=[], color=lambda S, i, j, v: 'yellow' if j == S.get('j') else None),
        dict(type='array', var='freq', label='', h=10, cell=10) if False else dict(type='text', size=24, h=60,
             fn=lambda S: (f'第 `{S["j"]}` 列各数出现次数 `freq`：' + '，'.join(f'`{k}`×{c}' for k, c in sorted(S['freq'].items()) if c)
                           if S.get('j') is not None and 'freq' in S else '`f[j][v]` = 前 j 列、第 j 列全改成 v 的最少操作数')),
        dict(type='text', size=24, h=60,
             fn=lambda S: (f'最优：改成 `{S["first_v"]}` 花 `{S["first_f"]}`；次优：改成 `{S["second_v"]}` 花 `{S["second_f"]}`'
                           if S.get('first_v') is not None and S.get('first_f', -1) >= 0 else '')),
    ],
    watch=[('j（列）', 'j', 'blue'), ('v（改成）', 'v', 'pink'), ('cost', 'cost', 'orange'), ('f', 'f', 'green'),
           ('first_f', 'first_f', 'green'), ('second_f', 'second_f', 'cyan')],
    captions={
        'm = len(grid)': '`m = {m}` 行',
        'n = len(grid[0])': '`n = {n}` 列',
        'first_f = 0': '`first_f`：到上一列为止的==最小==操作数（最优）',
        'first_v = 0': '`first_v`：最优方案中上一列变成的值',
        'second_f = 0': '`second_f`：==次小==操作数（次优），第 0 列之前都是 0',
        'second_v = 1': '`second_v`：次优方案中上一列变成的值（和 first_v 不同）',
        'for j in range(n)': '处理第 `{j}` 列',
        'pre_first_f, pre_first_v': '把上一列的最优 `({first_f}, 改成 {first_v})` 存成 `pre_first`',
        'pre_second_f, pre_second_v': '把上一列的次优 `({second_f}, 改成 {second_v})` 存成 `pre_second`',
        'first_f = second_f = -1': '清空，开始统计本列：`-1` 表示还没有候选',
        'freq = Counter()': '`freq`：本列各数出现次数',
        'freq[grid[i][j]] += 1': '`grid[{i}][{j}] = {grid[i][j]}` → `freq[{grid[i][j]}]` = {freq[grid[i][j]]}',
        'for v in range(10)': '枚举本列变成 `{v}`',
        'cost = m - freq[v]': '本列全改成 `{v}` 要改 `{m} − {freq[v]}` = ==`{cost}`== 个',
        'if v != pre_first_v': lambda S, B, r: (f'`v = {S.v}` ≠ 上一列最优的值 `{S.pre_first_v}` → 可以接最优' if S.v != S.pre_first_v
                                                else f'`v = {S.v}` = 上一列最优的值 → 相邻列不能相同，只能接次优'),
        'f = pre_first_f + cost': '`f = {pre_first_f} + {cost}` = =={f}==',
        'f = pre_second_f + cost': '`f = {pre_second_f} + {cost}` = =={f}==',
        'if first_f == -1 or f < first_f': lambda S, B, r: (f'`f = {S.f}` 比当前最优 `{S.first_f}` 小（或还没有候选）→ 成为最优，原最优降为次优'
                                                            if S.first_f == -1 or S.f < S.first_f else f'`f = {S.f}` 不比最优 `{S.first_f}` 小，再看能否当次优'),
        'first_f, second_f = f, first_f': '最优 `{first_f}`（改成 {v}），次优 `{second_f}`',
        'first_v, second_v = v, first_v': '值同步：最优改成 `{first_v}`，次优改成 `{second_v}`',
        'elif second_f == -1 or f < second_f': lambda S, B, r: (f'`f = {S.f}` 比次优 `{S.second_f}` 小（或还没有）→ 更新次优' if S.second_f == -1 or S.f < S.second_f
                                                                else f'`f = {S.f}` 不比次优小，不更新'),
        'second_f = f': '次优 `second_f = {second_f}`',
        'second_v = v': '次优改成 `{second_v}`',
        'return first_f': '最小操作数 = 最后一列的最优 =={ret}==',
    },
    skip=['cost = m - freq[v]', 'if v != pre_first_v', 'for i in range(m)', 'freq[grid[i][j]] += 1', 'for v in range(10)', 'second_v = v', 'first_v, second_v = v, first_v', 'pre_second_f, pre_second_v', 'm = len', 'n = len'],
    max_steps=130,
    cards=dict(
        one_liner='f[i][j] 只会从上一列「值不同」的最小值转移：留最优、次优两个就够',
        complexity='时间 `O(10 · mn)`，空间 `O(1)`',
        problem=['0~9 组成的 `m × n` 矩阵，每次可把一个格子改成任意整数',
                 '要求每个格子与上下相邻相等，与左右相邻不同，求最少操作数',
                 '本视频：`3×4` 矩阵 → `5`'],
        quote='每个元素都与上下相邻的元素相等，就意味着最终矩阵中的同一列的值都相同，而矩阵中数值的取值范围在0到9之间，那么最终修改的目的也必然在0到9之间。',
        quote_src='—— yiduobo 题解原文',
        idea=['同一列同值、取值只有 0~9：`f[i][j]` = 前 i 列、第 i 列全变成 j 的最小代价',
              '`f[i][j] = min(f[i-1][p]) + m - freq[i][j]`，其中 `p ≠ j`',
              '这个 min 只和上一列的最优、次优两个值有关：`j` 等于最优的值就改用次优'],
        summary=['时间 `O(10 · mn)`，空间 `O(1)`（只存最优和次优两对值）',
                 '易错：`v` 等于上一列最优的值时，必须用次优，不能再用最优',
                 '这里算「最少修改数」（`m - freq`），灵神是算「最多保留数」，方向相反',
                 '`-1` 表示本列还没有候选，用来初始化最优、次优',
                 '原文为 Python 2 风格，除删去类型说明外无改动'],
    ),
)
