CONFIG = dict(
    num=1914, title='循环轮转矩阵', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='模拟 · 每圈展开成数组再循环左移',
    code='''
DIRS = (0, 1), (1, 0), (0, -1), (-1, 0)  # 右下左上

class Solution:
    def rotateGrid(self, grid: List[List[int]], k: int) -> List[List[int]]:
        m0, n0 = len(grid), len(grid[0])

        # 从外到内枚举圈
        for i in range(min(m0, n0) // 2):
            m, n = m0 - i * 2, n0 - i * 2  # 这一圈的行数和列数
            x, y = i, i  # 这一圈的左上角
            a = []
            for dx, dy in DIRS:
                for _ in range(n - 1):
                    a.append(grid[x][y])
                    x += dx
                    y += dy
                m, n = n, m  # 见 54. 螺旋矩阵 我的题解

            shift = k % len(a)
            a = a[shift:] + a[:shift]

            # 注意此时 (x, y) 又回到了左上角
            j = 0
            for dx, dy in DIRS:
                for _ in range(n - 1):
                    grid[x][y] = a[j]
                    j += 1
                    x += dx
                    y += dy
                m, n = n, m

        return grid
''',
    call='Solution().rotateGrid([[1,2,3,4],[5,6,7,8]], 3)',
    expect=[[4,8,7,6],[3,2,1,5]],
    views=[
        dict(type='grid', var='grid', h=240, cell=70,
             cursors=[('x', 'y', 'blue', '(x,y)')],
             color=lambda S, i, j, v: (None if 'i' not in S else
                                       'cyan' if min(i, j, len(S['grid']) - 1 - i, len(S['grid'][0]) - 1 - j) == S['i'] and S['_line'] >= 8 and not (i == S.get('x') and j == S.get('y')) else None)),
        dict(type='array', var='a', h=200, label='a（这一圈顺时针展开）', pointers={'j': 'orange'}),
        dict(type='text', fn=lambda S: (f"这一圈共 `{len(S['a'])}` 个元素，向左移 `k % {len(S['a'])} = {S['k'] % len(S['a'])}` 位" if S.get('a') and 'shift' in S else ''), size=28),
    ],
    skip=['for _ in range(n - 1)', 'x += dx', 'j += 1'],
    max_steps=80,
    watch=['i', ('x', 'x', 'blue'), ('y', 'y', 'blue'), 'shift', ('j', 'j', 'orange')],
    captions={
        'for i in range(min(m0, n0) // 2)': lambda S, B, r: ('所有圈都处理完了' if 'i' in B and B.i == S.i else f'处理第 `{S.i}` 圈（从外到内，每圈互相独立）'),
        'm, n = m0 - i * 2': '这一圈是 `{m} × {n}`',
        'x, y = i, i': '从这一圈的左上角 `({x},{y})` 出发',
        'a = []': '`a` 用来按顺时针记下这一圈的元素',
        'a.append': '记下 `grid[{x}][{y}] = {a[-1]}`，`a = {a}`',
        'y += dy': '朝 `({dx},{dy})` 走一格 → `({x},{y})`',
        'm, n = n, m': '换方向后，要走的步数在 `n-1` 与 `m-1` 之间交替（见 54 题）',
        'for dx, dy in DIRS': lambda S, B, r: ('四个方向都走完，这一步结束' if 'dx' in B and (B.dx, B.dy) == (S.dx, S.dy) else f'换方向：`(dx,dy) = ({S.dx},{S.dy})`（右、下、左、上）'),
        'shift = k % len(a)': '循环左移 `N` 次等于没移 → 只需移 `k % N = {k} % {len(a)} = {shift}` 位',
        'a = a[shift:] + a[:shift]': '循环左移：`a` 变为 `{a}`',
        'j = 0': '回到左上角，按同样的顺时针顺序把 `a` 填回 `grid`',
        'grid[x][y] = a[j]': '`grid[{x}][{y}] = a[{j}] = {a[j]}`',
                'return grid': '所有圈都轮转完，返回 `grid`',
    },
    cards=dict(
        one_liner='每一圈互相独立：展开成数组，循环左移 k mod N，再填回去',
        complexity='时间 `O(mn)`，空间 `O(m+n)`',
        problem=['矩阵由若干圈组成，每次轮转，圈上每个元素取代其逆时针方向的相邻元素',
                 '返回轮转 `k` 次后的矩阵（`m`、`n` 均为偶数，`k` 最大 10^9）',
                 '本视频：`2×4` 矩阵 `[[1,2,3,4],[5,6,7,8]]`，`k = 3`'],
        quote='对于每一圈：从左上角开始，顺时针遍历这一圈，把遍历到的元素记录到一个数组 a 中。把 a 循环左移 k mod N 次。把 a 中元素按照步骤 1 中的顺序，重新填回 grid。',
        quote_src='—— 灵茶山艾府题解',
        idea=['用方向数组 `DIRS`（右下左上）走一圈，步数是 `n-1, m-1, n-1, m-1`',
              '顺时针展开后，逆时针轮转 = 数组循环左移',
              '`k` 很大，取 `k % N` 即可'],
        summary=['时间 `O(mn)`，空间 `O(m+n)`',
                 '一圈走完后 `(x, y)` 又回到左上角，填回时无需重置',
                 '换方向时交换 `m, n`，与螺旋矩阵的写法一样',
                 '题解还给了 `O(1)` 空间写法：用三次翻转代替切片（见 189 轮转数组）'],
    ),
)
