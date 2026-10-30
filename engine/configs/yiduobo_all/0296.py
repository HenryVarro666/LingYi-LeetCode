CONFIG = dict(
    num=296, title='最佳的碰头地点', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='行列分开 · 取中位数',
    tags=['贪心与思维'],
    code='''
class Solution(object):
    def minTotalDistance(self, grid):

        x_list = []
        y_list = []
        
        m = len(grid)
        n = len(grid[0])
        for x in range(m):
            for y in range(n):
                if grid[x][y] == 1:
                    x_list.append(x)
                    y_list.append(y)
        
        def calc(arr):
            arr.sort()
            target = arr[len(arr) // 2]
            res = 0
            for v in arr:
                res += abs(v - target)
            return res

        return calc(x_list) + calc(y_list)
''',
    call='Solution().minTotalDistance([[1,0,0,0,0],[0,0,0,1,0],[0,1,0,0,0],[0,0,0,0,1]])',
    expect=10,
    setup='',
    views=[
        dict(type='grid', var='grid', h=240, label='grid（1 = 住户）', cell=64,
             cursors=[('x', 'y', 'yellow', '(x,y)')],
             color=lambda S, i, j, v: 'green' if v == 1 else None),
        dict(type='array', var=lambda S: S.get('x_list'), h=170, label='x_list（行坐标）',
             pointers={}, color=lambda S, i, v: 'blue' if 'target' in S and S.get('arr') is S.get('x_list') and i == len(S['arr']) // 2 else None),
        dict(type='array', var=lambda S: S.get('y_list'), h=170, label='y_list（列坐标）',
             pointers={}, color=lambda S, i, v: 'pink' if 'target' in S and S.get('arr') is S.get('y_list') and i == len(S['arr']) // 2 else None),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), 'target', ('v', 'v', 'yellow'), ('res', 'res', 'green')],
    captions={
        'x_list = []': '准备两个列表，分别收集所有住户的==行坐标==',
        'y_list = []': '和==列坐标==：行和列互不影响，可以分开求解',
        'if grid[x][y] == 1': '`grid[{x}][{y}] = {grid[x][y]}`：{"是住户，记下坐标" if grid[x][y] == 1 else "空地，跳过"}',
        'x_list.append': '行坐标 `{x}` 入 `x_list` → `{x_list}`',
        'y_list.append': '列坐标 `{y}` 入 `y_list` → `{y_list}`',
        'arr.sort()': '排序：`arr = {arr}`',
        'target =': '中位数 `arr[{len(arr)} // 2] = {target}`：碰头点在这一维上取它，总距离最短',
        'res += abs': '`|{v} − {target}| = {abs(v - target)}`，`res` → {res}',
        'return res': '这一维总距离 =={res}==',
        'return calc': '先后算 `x_list`（行）和 `y_list`（列）两个一维问题，相加',
    },
    cards=dict(
        one_liner='曼哈顿距离的行、列互不相干，各取中位数',
        complexity='时间 `O(mn + k log k)`，空间 `O(k)`（k 为住户数）',
        problem=['`m×n` 网格里 `1` 表示住户，选一个点让所有住户到它的曼哈顿距离之和最小',
                 '距离 `|x1−x2| + |y1−y2|`，返回最小总距离',
                 '本视频：`[[1,0,0,0,0],[0,0,0,1,0],[0,1,0,0,0],[0,0,0,0,1]]` → `10`',
                 '（题面来自 LeetCode 296 原题，库里无题面）'],
        quote='行和列互相之间不会产生影响，因此在这里可以分开求解最佳的行和最佳的列。单独考虑行或者列，这是经典的最优位置问题，最终答案就是取中位数的位置最佳。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历网格，把住户的行坐标、列坐标分别收集起来',
              '各自排序，取中位数当碰头点的行 / 列',
              '再累加每个坐标到中位数的差值，两维相加就是答案'],
        summary=['时间 `O(mn + k log k)`，空间 `O(k)`',
                 '行坐标靠遍历顺序天然有序，列坐标需要排序',
                 '偶数个住户时，中间两个数取哪个都一样',
                 '原文为 Python 2 写法，`len(arr) / 2` 已改为 `//`',
                 '同类题：2033、462、2448'],
    ),
)
