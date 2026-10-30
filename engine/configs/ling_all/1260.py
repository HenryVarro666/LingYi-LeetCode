CONFIG = dict(
    num=1260, title='二维网格迁移', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='三次反转（轮转数组）',
    tags=[],
    code='''
class Solution:
    def shiftGrid(self, grid: List[List[int]], k: int) -> List[List[int]]:
        m, n = len(grid), len(grid[0])

        def reverse(l: int, r: int) -> None:
            while l < r:
                x1, y1 = divmod(l, n)
                x2, y2 = divmod(r, n)
                grid[x1][y1], grid[x2][y2] = grid[x2][y2], grid[x1][y1]
                l += 1
                r -= 1

        # 189. 轮转数组
        size = m * n
        k %= size  # 轮转 k 次等同于轮转 k % size 次
        reverse(0, size - 1)
        reverse(0, k - 1)
        reverse(k, size - 1)
        return grid
''',
    call='Solution().shiftGrid([[1,2,3],[4,5,6]], 2)',
    expect=[[5, 6, 1], [2, 3, 4]],
    views=[
        dict(type='text', size=30, h=64, fn=lambda S: (f"正在反转一维下标区间 `[{S['l']}, {S['r']}]`" if 'l' in S and 'r' in S and S.get('_inner') is not None and 'x1' in S else '把网格按行拼成一维数组，做三次反转')),
        dict(type='grid', var='grid', h=300, cell=110,
             cursors=[('x1', 'y1', 'blue', 'l'), ('x2', 'y2', 'pink', 'r')]),
    ],
    watch=[('k', 'k', 'yellow'), ('l', 'l', 'blue'), ('r', 'r', 'pink')],
    skip=['m, n = len'],
    captions={
        'size = m * n': '网格共 `size` = `{m} × {n}` = =={size}== 个格子，按行拼成一维数组',
        'k %= size': '轮转 `size` 次等于没动，所以 `k %= size` → =={k}==',
        'reverse(0, size - 1)': '第 1 次：整体反转，后面的 k 个数被换到前面',
        'reverse(0, k - 1)': '第 2 次：把前 `k` 个数再反转回正序',
        'reverse(k, size - 1)': '第 3 次：把剩下的数也反转回正序',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`：两端还没相遇，继续交换' if S.l < S.r else f'`l = {S.l} ≥ r = {S.r}`：相遇，这一段反转完成'),
        'x1, y1 = divmod': '下标 `l = {l}` 换算成网格坐标：`({x1}, {y1})`',
        'x2, y2 = divmod': '下标 `r = {r}` 换算成网格坐标：`({x2}, {y2})`',
        'grid[x1][y1], grid[x2][y2]': '交换 `grid[{x1}][{y1}]` 和 `grid[{x2}][{y2}]` → {grid}',
        'l += 1': '`l` 右移 → {l}',
        'r -= 1': '`r` 左移 → {r}',
        'return grid': lambda S, B, r: f'三次反转完成，原地得到 {S.grid}',
    },
    max_steps=110,
    cards=dict(
        one_liner='网格按行拼成一维数组，循环右移 k 位 = 三次反转',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['每次迁移：每个元素右移一格，行末元素跳到下一行行首，最后一格跳回左上角',
                 '求迁移 `k` 次后的网格',
                 '示例：`[[1,2,3],[4,5,6]]`，`k = 2` → `[[5,6,1],[2,3,4]]`'],
        quote='把二维矩阵的每一行拼在一起，可以得到一个一维数组，方便我们处理。',
        quote_src='—— 灵茶山艾府题解',
        idea=['行末的「下一个」是下一行行首，所以网格就是一个首尾相接的一维数组',
              '一维数组循环右移 `k` 位：反转整体、反转前 `k` 个、反转后面剩下的',
              '下标 `l` 用 `divmod(l, n)` 换算成行列，不用真的建一维数组'],
        summary=['时间 `O(mn)`，空间 `O(1)`（原地）',
                 '易错：先 `k %= size`；`k = 0` 时 `reverse(0, -1)` 什么也不做，正好',
                 '方法一：新建 `ans`，元素 `(i*n+j+k) % size` 直接放到新位置，空间 `O(mn)`'],
    ),
)
