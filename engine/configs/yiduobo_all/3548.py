def _t(S):
    if 'now' in S and 's' in S:
        return "上半部分 now = ==%d==，下半部分 s − now = %d，差 now − (s − now) = ==%d==" % (S['now'], S['s'] - S['now'], 2 * S['now'] - S['s'])
    return ''


CONFIG = dict(
    num=3548, title='等和矩阵分割 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='四个方向扫描 · removeable 集合', tags=['灵神题单', '难度分 2245'],
    code='''
class Solution(object):
    def canPartitionGrid(self, grid):
        
        m = len(grid)
        n = len(grid[0])
        s = 0

        for i in range(m):
            for j in range(n):
                s += grid[i][j]
        
        removeable = set()
        now = 0
        for i in range(m - 1):
            for j in range(n):
                now += grid[i][j]
                if i == 0:
                    if j == 0 or j == n - 1:
                        removeable.add(grid[i][j])
                elif n > 1:
                    removeable.add(grid[i][j])
                elif now - grid[i][j] == s - now:
                    return True
            
            if i == 1:
                for j in range(1, n - 1):
                    removeable.add(grid[i - 1][j])

            if now + now == s:
                return True
            if now - (s - now) in removeable:
                return True
        
        removeable = set()
        now = 0
        for i in range(m - 1, 0, -1):
            for j in range(n):
                now += grid[i][j]
                if i == m - 1:
                    if j == 0 or j == n - 1:
                        removeable.add(grid[i][j])
                elif n > 1:
                    removeable.add(grid[i][j])
                elif now - grid[i][j] == s - now:
                    return True
            
            if i == m - 2:
                for j in range(1, n - 1):
                    removeable.add(grid[i + 1][j])
            
            if now + now == s:
                return True
            if now - (s - now) in removeable:
                return True
        
        removeable = set()
        now = 0
        for j in range(n - 1):
            for i in range(m):
                now += grid[i][j]
                if j == 0:
                    if i == 0 or i == m - 1:
                        removeable.add(grid[i][j])
                elif m > 1:
                    removeable.add(grid[i][j])
                elif now - grid[i][j] == s - now:
                    return True
            
            if j == 1:
                for i in range(1, m - 1):
                    removeable.add(grid[i][j - 1])
            
            if now + now == s:
                return True
            if now - (s - now) in removeable:
                return True
        
        removeable = set()
        now = 0
        for j in range(n - 1, 0, -1):
            for i in range(m):
                now += grid[i][j]
                if j == n - 1:
                    if i == 0 or i == m - 1:
                        removeable.add(grid[i][j])
                elif m > 1:
                    removeable.add(grid[i][j])
                elif now - grid[i][j] == s - now:
                    return True
            
            if j == n - 2:
                for i in range(1, m - 1):
                    removeable.add(grid[i][j + 1])
            
            if now + now == s:
                return True
            if now - (s - now) in removeable:
                return True
        
        return False
''',
    call='Solution().canPartitionGrid([[1,2],[3,4]])',
    expect=True,
    views=[
        dict(type='grid', var='grid', h=170, cursors=[('i', 'j', 'yellow', '')]),
        dict(type='set', var='removeable', h=110, label='removeable：能删的数'),
        dict(type='text', fn=_t, h=60),
    ],
    watch=['s', 'now', ('i', 'i', 'yellow'), ('j', 'j', 'yellow')],
    captions={
        's += grid[i][j]': '先求总和 `s`：加上 `{grid[i][j]}` → =={s}==',
        'now += grid[i][j]': '`now` 累加：已扫过的那一部分的和 → =={now}==',
        'if i == 0': lambda S, B, r: ('`i = 0`：扫描的第一行，此时这部分只有一行' if S.i == 0 else '`i = 0`？不是 → 已经不是第一行了'),
        'if j == 0 or j == n - 1': '只有一行时，删中间的数会让这行断开，所以只有两端能删：`j={j}`，`n={n}` → ' + '两端才记入',
        'removeable.add(grid[i][j])': '`{grid[i][j]}` 可以删 → 记入 `removeable`',
        'elif n > 1': '宽度大于 1：这一行任何元素删掉都不影响连通，全部可删',
        'elif now - grid[i][j] == s - now': '宽度是 1 的长条：只有当前这个端点能删，直接判断',
        'if i == 1': lambda S, B, r: ('扫到第二行了：第一行被第二行连住，它的中间元素现在也能删' if S.i == 1 else '`i == 1` 吗？不是，不用补第一行'),
        'if i == m - 2': lambda S, B, r: ('自下而上扫到倒数第二行：最后一行被连住，补进它的中间元素' if S.i == S.m - 2 else '倒数第二行吗？不是'),
        'if now + now == s': lambda S, B, r: f'不删：上半 `{S.now}` ×2 = `{S.now*2}`，总和 `{S.s}` → ' + ('==相等，可分割==' if S.now*2 == S.s else '不等'),
        'if now - (s - now) in removeable': lambda S, B, r: f'差值 `{S.now} − ({S.s} − {S.now}) = {S.now*2-S.s}`，能删的数里有它吗？→ ' + ('==有，删掉它两边相等==' if S.now*2-S.s in S.removeable else '没有'),
        'return True': '找到可行的分割 → `True`',
        'return False': '四个方向都不行 → `False`',
    },
    skip=['m = len(grid)', 'n = len(grid[0])', 'removeable = set()', 'now = 0'],
    cards=dict(
        one_liner='从四个方向扫描，用集合记下“还能删掉的数”',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['给一个 `m×n` 的正整数矩阵，切一刀（横或竖），分成两个非空矩阵',
                 '两部分和相等，或各自删掉至多一个数后相等，删完要保持连通',
                 '示例：`[[1,2],[3,4]]` → `true`，从下半部分删去 `4`，`3 = 3`'],
        quote='首先对于 i = 0 这一行，在一开始只能移除掉 j = 0 或者 j = n - 1 这两个位置上的元素，因为一开始这个矩阵只有 i = 0 这一行，如果移除掉中间的元素就会将矩阵切分成两个部分。',
        quote_src='—— yiduobo 题解原文',
        idea=['`now` 是扫过部分的和，差值 `now − (s − now)` 就是要删掉的那个数',
              '先算总和 `s`，再从上到下、从下到上、从左到右、从右到左各扫一遍',
              '`removeable` 只存删了不会断开的数：单行只有两端，宽为 1 的长条只有端点',
              '扫到第二行时，再把第一行的中间元素补进去'],
        summary=['时间 `O(mn)`：总和一遍，四个方向各一遍；空间 `O(mn)`',
                 '易错：第一行的中间元素，到 `i == 1` 才能补进 `removeable`',
                 '易错：宽（或高）为 1 时，每个数只在当前这条分割线才能删',
                 '原文是 Python 3 可直接运行的写法，没有改动',
                 '对比灵神：灵神把表翻转、转置后复用一段代码；yiduobo 把四个方向各写一遍'],
    ),
)
