def _color2(S, i, j, v):
    """本轮 check 正在走的行或列：dx == 0 时行号 x 不变，dy == 0 时列号 y 不变"""
    if 'dx' not in S or 'x' not in S:
        return None
    if S['dx'] == 0 and i == S['x']:
        return 'blue'
    if S['dy'] == 0 and j == S['y']:
        return 'blue'
    return None


CONFIG = dict(
    num=2133, title='检查是否每一行每一列都包含全部整数', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希集合 · 逐行逐列判重',
    tags=[],
    code='''
class Solution(object):
    def checkValid(self, matrix):

        n = len(matrix)

        def check(x, y, dx, dy):
            num_set = set()
            for index in range(n):
                num_set.add(matrix[x][y])
                x += dx
                y += dy
            
            return len(num_set) == n
        
        for index in range(n):
            if not check(index, 0, 0, 1):
                return False

            if not check(0, index, 1, 0):
                return False
        
        return True
''',
    call='Solution().checkValid([[1,2,3],[3,1,2],[2,2,1]])',
    expect=False,
    views=[
        dict(type='grid', var='matrix', label='matrix（蓝 = 当前检查的行或列，黄 = 刚加入集合的格子）',
             cursors=[('x', 'y', 'yellow', '(x,y)')], color=lambda S, i, j, v: _color2(S, i, j, v), h=300, cell=90),
        dict(type='set', var='num_set', label='num_set（已见过的数）', fmt=lambda x: str(x), h=130),
        dict(type='text', fn=lambda S: ('集合大小必须等于 `n`：重复的数会被集合吃掉，大小就不够了' if 'num_set' not in S else f"`len(num_set) = {len(S['num_set'])}`，`n = {len(S['matrix'])}`"), size=26),
    ],
    watch=[('index', 'index', 'purple'), ('x', 'x', 'blue'), ('y', 'y', 'pink'), ('dx,dy', '(dx, dy)', 'cyan')],
    captions={
        'n = len(matrix)': '`n = {n}`：矩阵是 `n x n`，每行每列应恰好含 `1..n`',
        'def check': '`check(x, y, dx, dy)`：从 `(x, y)` 出发，每步走 `(dx, dy)`，走 `n` 格——`(0,1)` 走一整行，`(1,0)` 走一整列',
        'num_set = set()': '新建空集合 `num_set`，用来看这一行（列）里出现了哪些数',
        8: lambda S, B, ret: ('这一行（列）的 `n` 个格子都走完了' if S.x >= S.n or S.y >= S.n else f'下一个格子：`({S.x}, {S.y})`'),
        15: lambda S, B, ret: (f'`index = {S.index}`：检查第 `{S.index}` 行和第 `{S.index}` 列' if S.index != B.get('index') else '行列都检查完了'),
        'num_set.add': '把 `matrix[{x}][{y}] = {matrix[x][y]}` 加入集合：`num_set` = `{sorted(num_set)}`（重复的数加不进去）',
        'x += dx': '`x` → `{x}`',
        'y += dy': '`y` → `{y}`',
        'return len(num_set) == n': lambda S, B, ret: (f'`len(num_set) = {len(S.num_set)}`，`n = {S.n}` → ' + ('==相等，包含了 1..n 的全部整数==' if ret else '==小于 n，说明有重复，缺了数==')),
        'if not check(index, 0, 0, 1)': lambda S, B, ret: (f'检查第 `{S.index}` 行（从 `({S.index}, 0)` 向右走）' if 'index' in S else ''),
        'if not check(0, index, 1, 0)': lambda S, B, ret: f'检查第 `{S.index}` 列（从 `(0, {S.index})` 向下走）',
        'return False': '某一行或某一列不全：矩阵无效，返回 `False`',
        'return True': '所有行和列都通过 → `True`',
    },
    skip=['x += dx', 'y += dy'],
    max_steps=90,
    cards=dict(
        one_liner='用集合给每行每列去重，大小等于 n 才算齐全',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`n x n` 矩阵，==每一行和每一列==都要包含 `1` 到 `n` 的全部整数才是有效矩阵',
                 '示例：`[[1,2,3],[3,1,2],[2,3,1]]` → `true`',
                 '本视频：`[[1,2,3],[3,1,2],[2,2,1]]` → `false`（第 1 列有两个 2）'],
        quote='由于题目保证了矩阵中的数都在1到n直接，那么对于任意行或者列，如果用哈希表来储存其中的数，只要出现了相同的数哈希表的大小就必然小于n，反之若哈希表的大小等于n，那么说明当前行或者列包含了1到n直接的所有数。',
        quote_src='—— yiduobo 题解原文',
        idea=['数值都在 `1..n` 之间，所以只要==没有重复==，`n` 个数就恰好是 `1..n`',
              '集合自动去重：`len(num_set) == n` 就说明没有重复',
              '`check` 用起点和方向统一处理：`(0,1)` 扫行，`(1,0)` 扫列'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '依赖题目保证 `1 <= matrix[i][j] <= n`，否则光看集合大小不够',
                 '行和列一起检查，任何一个失败就立刻返回 `False`',
                 '原文已是 Python 3 可运行写法，仅删去类型说明文档字符串，代码未改'],
    ),
)
