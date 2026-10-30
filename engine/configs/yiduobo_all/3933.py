MAT = [[1, 2, 0], [0, 0, 1]]


def _col(S, a, b, v):
    if 'x' not in S or v is None:
        return None
    if 'filled' not in S:
        return None
    if (a, b) == (S['x'], S['y']) and S['_inner'].get('x1') is not None:
        return 'yellow'
    if (a, b) in S['filled']:
        return 'green'
    inn = S['_inner']
    if inn.get('x1') is not None and 'y2' in inn and inn['x1'] <= a <= inn['x2'] and inn['y1'] <= b <= inn['y2']:
        return 'cyan'
    return None


def _txt(S):
    if 'filled' not in S:
        return '按数值从大到小分批处理：更大的数先放进树状数组'
    inn = S['_inner']
    if inn.get('x1') is None or 'x' not in S:
        return '绿色 = 已放进树状数组的（更大的）数'
    return (f'检查 `({S["x"]},{S["y"]})`：值 `{S["v"]}`，范围 `[{inn["x1"]},{inn["x2"]}] × [{inn["y1"]},{inn["y2"]}]`（青色）'
            + (f'，里面有 `{inn["s"]}` 个更大的数' if 's' in inn else ''))


CONFIG = dict(
    num=3933, title='矩阵中的局部最大值 II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='值从大到小分批 + 二维树状数组',
    tags=['灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def countLocalMaximums(self, matrix):
        
        pos = {}

        m = len(matrix)
        n = len(matrix[0])

        for i in range(m):
            for j in range(n):
                if matrix[i][j] > 0:
                    if matrix[i][j] not in pos:
                        pos[matrix[i][j]] = []
                    pos[matrix[i][j]].append((i, j))
        
        f = [[0] * (n + 1) for _ in range(m + 1)]
        res = 0
        filled = set()

        def add(x, y):
            tmp = y
            while x <= m:
                y = tmp
                while y <= n:
                    f[x][y] += 1
                    y += y & -y
                x += x & -x
        
        def get(x, y):
            tmp = y
            s = 0
            while x > 0:
                y = tmp
                while y > 0:
                    s += f[x][y]
                    y -= y & -y
                x -= x & -x
            return s

        for v in sorted(pos.keys(), reverse=True):
            for x, y in pos[v]:
                x1 = max(x - v, 0)
                y1 = max(y - v, 0)
                x2 = min(x + v, m - 1)
                y2 = min(y + v, n - 1)

                s = get(x2 + 1, y2 + 1) - get(x2 + 1, y1) - get(x1, y2 + 1) + get(x1, y1)
                if x1 == x - v and y1 == y - v and (x1, y1) in filled:
                    s -= 1
                if x1 == x - v and y2 == y + v and (x1, y2) in filled:
                    s -= 1
                if x2 == x + v and y1 == y - v and (x2, y1) in filled:
                    s -= 1
                if x2 == x + v and y2 == y + v and (x2, y2) in filled:
                    s -= 1
                
                if s == 0:
                    res += 1
            
            for x, y in pos[v]:
                add(x + 1, y + 1)
                filled.add((x, y))
        
        return res
''',
    call=f'Solution().countLocalMaximums({MAT})',
    expect=2,
    max_steps=64,
    skip=['x1 = max(x - v', 'y1 = max(y - v', 'x2 = min(x + v', 'tmp = y', 'y = tmp', 'while x <= m', 'while y <= n', 'f[x][y] += 1', 'y += y & -y', 'x += x & -x', 'while x > 0', 'while y > 0',
          's += f[x][y]', 'y -= y & -y', 'x -= x & -x', 's = 0', 'return s', 'm = len', 'n = len', 'for i in range(m)', 'for j in range(n)',
          'if matrix[i][j] > 0', 'if matrix[i][j] not in pos', 'pos[matrix[i][j]] = []', 'pos[matrix[i][j]].append', 'f = [[0]', 'filled = set()'],
    views=[
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='grid', var='matrix', label='matrix（绿 = 已加入树状数组的更大数，黄 = 当前格，青 = 检查范围）', cell=100, h=290, color=_col),
        dict(type='grid', var=lambda S: S.get('f'), label='f（二维树状数组，计数）', cell=64, h=240),
    ],
    watch=[('v', "S.get('v')", 'blue'), ('s', "S['_inner'].get('s')", 'pink'), ('res', 'res', 'green')],
    captions={
        'pos = {}': '`pos[值]` = 这个值出现的所有位置；0 不用管',
        'res = 0': '`res` 计数；`f` 是二维树状数组，`filled` 记录已经放进去的位置',
        'for v in sorted': lambda S, B, r: (f'下一批：值 `{S.v}` 的格子 {S.pos[S.v]}；树状数组里放的都是比它更大的数' if not ('v' in B and B.v == S.v) else '所有批次处理完了'),
        41: lambda S, B, r: (f'检查 `({S.x},{S.y})`，值 `{S.v}`' if not ('x' in B and 'x1' in B and (B.x, B.y) == (S.x, S.y)) else '这一批的格子都检查完了'),
        60: '再把这一批的格子逐个放进树状数组',
        'y2 = min(y + v, n - 1)': '“x 行 x 列”的范围，裁到矩阵内：`[{x1},{x2}] × [{y1},{y2}]`（青色）',
        's = get(': '用二维树状数组数范围内已放入的（更大的）数：4 个前缀和容斥',
        'if x1 == x - v and y1 == y - v': lambda S, B, r: ('左上角 `({},{})` 是行、列距离都恰好等于 v 的角，且它里面放过更大的数 → 不算，`s` 减 1'.format(S.x1, S.y1) if (S.x1 == S.x - S.v and S.y1 == S.y - S.v and (S.x1, S.y1) in S.filled) else '左上角不是“被忽略的角”，或里面没有更大的数 → 不用减'),
        'if x1 == x - v and y2 == y + v': lambda S, B, r: ('右上角 `({},{})` 是被忽略的角且里面放过更大的数 → `s` 减 1'.format(S.x1, S.y2) if (S.x1 == S.x - S.v and S.y2 == S.y + S.v and (S.x1, S.y2) in S.filled) else '右上角不是“被忽略的角”，或里面没有更大的数 → 不用减'),
        'if x2 == x + v and y1 == y - v': lambda S, B, r: ('左下角 `({},{})` 是被忽略的角且里面放过更大的数 → `s` 减 1'.format(S.x2, S.y1) if (S.x2 == S.x + S.v and S.y1 == S.y - S.v and (S.x2, S.y1) in S.filled) else '左下角不是“被忽略的角”，或里面没有更大的数 → 不用减'),
        'if x2 == x + v and y2 == y + v': lambda S, B, r: ('右下角 `({},{})` 是被忽略的角且里面放过更大的数 → `s` 减 1'.format(S.x2, S.y2) if (S.x2 == S.x + S.v and S.y2 == S.y + S.v and (S.x2, S.y2) in S.filled) else '右下角不是“被忽略的角”，或里面没有更大的数 → 不用减'),
        'if s == 0': lambda S, B, r: (f'`s = {S.s}`：范围里没有更大的数 → ==局部最大值==' if S.s == 0 else f'`s = {S.s} > 0`：范围里还有更大的数 → 不是局部最大值'),
        'res += 1': '`res` = {res}',
        'add(x + 1, y + 1)': '检查完这一批才加入：把 `({B.x},{B.y})` 放进树状数组（同值的互不影响）',
        'filled.add': '`filled` 记下 `({B.x},{B.y})`，之后判断角上是否放过更大的数',
        'return res': '全部批次处理完，局部最大值共 =={ret}== 个',
    },
    cards=dict(
        one_liner='先放大的、后查小的：范围里放过的数个数为 0，就是局部最大值',
        complexity='时间 `O(nm log n log m)`，空间 `O(nm)`',
        problem=['非零格 `(row, col)`，`x = matrix[row][col]`，看周围 `x` 行 `x` 列范围内的格子',
                 '行距、列距都恰好等于 `x` 的四个角要忽略',
                 '范围内没有更大的值，就是局部最大值，数出个数',
                 '本视频：`[[1,2,0],[0,0,1]]` → `2`'],
        quote='对于矩阵中的所有元素，其能否成为局部最大值，只取决于那些大于该元素的其他元素是否出现在以matrix[row][col]为中心的子矩阵中。',
        quote_src='—— yiduobo 题解原文',
        idea=['按数值从大到小分批：处理某一批时，树状数组里放的正好是“比它大”的数',
              '用二维树状数组数出子矩阵里已放入的个数（4 个前缀容斥）',
              '四个角本来就要忽略：角上若放过更大的数，要把它再减掉',
              '整批查完才把这一批放进树状数组，同值的数不互相影响'],
        summary=['时间 `O(nm log n log m)`，空间 `O(nm)`',
                 '易错：同一批（相等的值）必须先全部检查、再统一加入，相等不算“更大”',
                 '易错：角只有在 `x1 == x - v` 且 `y1 == y - v` 这类没被裁剪时才存在',
                 '原文可直接在 Python 3 运行，代码未改',
                 '对比灵神：灵神用二维 ST 表直接查最大值，yiduobo 换了“从大到小 + 计数”的角度'],
    ),
)
