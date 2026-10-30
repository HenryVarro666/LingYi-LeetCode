def _cell_color(name):
    def f(S, i, j, v):
        if 'res' in S and S['_line'] >= 49:
            m = min(S['left'][i][j], S['right'][i][j], S['up'][i][j], S['down'][i][j])
            if m == S['res'] and m > 0:
                return 'green'
        if (i, j) in S.get('mine_set', ()):
            return 'red'
        return None
    return f


def _view(name, label, cur):
    return dict(type='grid', var=name, label=label, h=135, cell=46,
                cursors=[('i', 'j', cur, '')], color=_cell_color(name))


CONFIG = dict(
    num=764, title='最大加号标志', difficulty='Medium', category='网格图',
    author='yiduobo', technique='四方向连续 1 的个数（四张 DP 表）', tags=[],
    code='''
class Solution(object):
    def orderOfLargestPlusSign(self, N, mines):

        left = [[0] * N for _ in range(N)]
        right = [[0] * N for _ in range(N)]
        up = [[0] * N for _ in range(N)]
        down = [[0] * N for _ in range(N)]

        mine_set = set()
        for x, y in mines:
            mine_set.add((x, y))
        
        for i in range(N):
            for j in range(N):
                if (i, j) in mine_set:
                    left[i][j] = 0
                elif j == 0:
                    left[i][j] = 1
                else:
                    left[i][j] = left[i][j - 1] + 1
        
        for i in range(N):
            for j in range(N - 1, -1, -1):
                if (i, j) in mine_set:
                    right[i][j] = 0
                elif j == N - 1:
                    right[i][j] = 1
                else:
                    right[i][j] = right[i][j + 1] +1
        
        for j in range(N):
            for i in range(N):
                if (i, j) in mine_set:
                    up[i][j] = 0
                elif i == 0:
                    up[i][j] = 1
                else:
                    up[i][j] = up[i - 1][j] + 1
        
        for j in range(N):
            for i in range(N - 1, -1, -1):
                if (i, j) in mine_set:
                    down[i][j] = 0
                elif i == N - 1:
                    down[i][j] = 1
                else:
                    down[i][j] = down[i + 1][j] + 1

        res = 0
        for i in range(N):
            for j in range(N):
                res = max(res, min(left[i][j], right[i][j], up[i][j], down[i][j]))
        
        return res
''',
    call='Solution().orderOfLargestPlusSign(3, [[0, 0], [2, 2]])',
    expect=2,
    views=[
        _view('left', 'left：向左连续 1 的个数（红 = 0）', 'blue'),
        _view('right', 'right：向右', 'pink'),
        _view('up', 'up：向上', 'cyan'),
        _view('down', 'down：向下（最后一轮绿色 = 当前最大加号中心）', 'orange'),
    ],
    watch=['i', 'j', ('res', 'res', 'green')],
    skip=['mine_set.add', 'for x, y in mines', 'for i in range', 'for j in range', 'if (i, j) in mine_set', 'elif j ==', 'elif i =='],
    max_steps=120,
    captions={
        'left = [[0]': '四张 N×N 表，分别存各方向连续 1 的个数',
        'mine_set = set()': '`mines` 里的点放进集合，方便 O(1) 判断',
        'left[i][j] = 0': '`({i},{j})` 是 0 → 向左连续 1 的个数为 `0`',
        'left[i][j] = 1': '`j == 0`，左边没有格子 → `left[{i}][{j}] = 1`',
        'left[i][j] = left': '`left[{i}][{j}] = left[{i}][{j-1}] + 1` = =={left[i][j]}==：从左向右扫，继承左邻居',
        'right[i][j] = 0': '`({i},{j})` 是 0 → `right = 0`',
        'right[i][j] = 1': '`j == N-1`，右边没有格子 → `right[{i}][{j}] = 1`',
        'right[i][j] = right': '`right[{i}][{j}] = right[{i}][{j+1}] + 1` = =={right[i][j]}==：==从右向左==扫，继承右邻居',
        'up[i][j] = 0': '`({i},{j})` 是 0 → `up = 0`',
        'up[i][j] = 1': '`i == 0`，上边没有格子 → `up[{i}][{j}] = 1`',
        'up[i][j] = up': '`up[{i}][{j}] = up[{i-1}][{j}] + 1` = =={up[i][j]}==：外层列、内层行，从上向下',
        'down[i][j] = 0': '`({i},{j})` 是 0 → `down = 0`',
        'down[i][j] = 1': '`i == N-1`，下边没有格子 → `down[{i}][{j}] = 1`',
        'down[i][j] = down': '`down[{i}][{j}] = down[{i+1}][{j}] + 1` = =={down[i][j]}==：==从下向上==扫',
        'res = 0': '四张表都填好了，开始枚举每个点作为加号中心',
        'res = max': '`({i},{j})` 加号长度 = min(`{left[i][j]}`, `{right[i][j]}`, `{up[i][j]}`, `{down[i][j]}`) = =={min(left[i][j], right[i][j], up[i][j], down[i][j])}==，`res` → =={res}==',
        'return res': '最大加号的阶数 `{res}`',
    },
    cards=dict(
        one_liner='每个点四个方向各数连续 1，加号长度取最短的那个方向',
        complexity='时间 `O(N^2)`，空间 `O(N^2)`',
        problem=['`N×N` 的 01 网格，初始全是 1，`mines` 里的位置是 0',
                 '求由 1 组成的最大「加号」的阶数（中心向四个方向延伸的臂长，含中心）',
                 '本视频：`N=3, mines=[[0,0],[2,2]]` → `2`'],
        quote='那么以这个点为中心的加号长度就是这四个方向中最短的那一个。',
        quote_src='—— yiduobo 题解原文',
        idea=['`left`、`right`、`up`、`down` 四张表：当前是 1 就 `= 邻居 + 1`，是 0 就清零',
              '扫描方向要合理：求 `up` 必须从上往下，求 `down` 必须从下往上',
              '最后枚举每个点，取 `min` 更新答案'],
        summary=['时间、空间都是 `O(N^2)`，常数是 4 张表',
                 '边界要单独处理：第一列/行/最后一列/行直接记 1',
                 '全是 0 时答案是 0；有一个 1 答案至少为 1',
                 '原文 Python 2 风格，本题代码无需修改即可在 Python 3 运行'],
    ),
)
