MAT = [[1, 1, 0], [0, 1, 1], [1, 0, 1]]


def _phase(S):
    ln = S.get('_line', 0)
    if ln <= 16:
        return 0
    if ln <= 25:
        return 1
    if ln <= 35:
        return 2
    return 3


DIRS = [(0, 1), (1, 0), (1, -1), (1, 1)]   # 终点相对于“上一个格子”的方向 (di, dj)
NAMES = ['横向（逐行）', '竖向（逐列）', '反对角线（i+j 相同）', '主对角线（i−j 相同）']
ACTIVE = (11, 12, 13, 14, 15, 20, 21, 22, 23, 24, 30, 31, 32, 33, 34, 40, 41, 42, 43, 44)


def _cur(S):
    return S.get('i') if S.get('_line') in ACTIVE else None


def _color(S, i, j, v):
    if S.get('_line') not in ACTIVE or 'now' not in S:
        return None
    di, dj = DIRS[_phase(S)]
    for k in range(S['now']):
        if (i, j) == (S['i'] - k * di, S['j'] - k * dj):
            return 'green'
    return None


def _txt(S):
    if S.get('_line', 0) < 8 or 'res' not in S:
        return ''
    return f"方向：=={NAMES[_phase(S)]}==　当前连续 `now = {S['now']}`　最长 `res = {S['res']}`"


CONFIG = dict(
    num=562, title='矩阵中最长的连续1线段', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='四个方向各扫一遍 · 计数器 now',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution(object):
    def longestLine(self, mat):
        m = len(mat)
        n = len(mat[0])

        now = 0
        res = 0
        for i in range(m):
            now = 0
            for j in range(n):
                if mat[i][j] == 1:
                    now += 1
                    res = max(res, now)
                else:
                    now = 0
        
        for j in range(n):
            now = 0
            for i in range(m):
                if mat[i][j] == 1:
                    now += 1
                    res = max(res, now)
                else:
                    now = 0
        
        for s in range(m + n - 1):
            now = 0
            for i in range(max(0, s - n + 1), min(m - 1, s) + 1):
                j = s - i
                if mat[i][j] == 1:
                    now += 1
                    res = max(res, now)
                else:
                    now = 0
        
        for s in range(-(n - 1), m):
            now = 0
            for i in range(max(s, 0), min(m - 1, s + n - 1) + 1): 
                j = i - s
                if mat[i][j] == 1:
                    now += 1
                    res = max(res, now)
                else:
                    now = 0

        return res
''',
    call=f'Solution().longestLine({MAT})',
    expect=3,
    skip=['m = len', 'n = len', 'res = 0', 'now += 1', 'now = 0', 'for j in range', 'for i in range', 'for s in range', 'j = s - i', 'j = i - s'],
    max_steps=56,
    views=[
        dict(type='grid', var='mat', label='mat（绿 = 当前这一段连续的 1，黄框 = 正在看的格子）', cell=96, h=330,
             color=_color, cursors=[(lambda S: S.get('i') if S.get('_line') in ACTIVE else None, 'j', 'yellow')]),
        dict(type='text', fn=_txt, size=26, h=60),
    ],
    watch=[('now', 'now', 'blue'), ('res', 'res', 'green')],
    captions={
        'if mat[i][j] == 1': lambda S, B, r: (f'`mat[{S.i}][{S.j}] = 1`：是 1，线段接着延长，`now` 加 1 → =={S.now + 1}=='
                                              if S.mat[S.i][S.j] == 1 else
                                              f'`mat[{S.i}][{S.j}] = 0`：断开了，`now` 清零'),
        'res = max': '连续 `{now}` 个 1：`res = max({B.res}, {now}) = {res}`，记录见过的最长线段',
        'return res': '四个方向都扫完，最长连续 1 线段是 =={res}==',
    },
    cards=dict(
        one_liner='四个方向各扫一遍，用一个计数器数连续的 1',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['给一个只含 `0` 和 `1` 的矩阵 `mat`，求最长的连续 1 线段的长度',
                 '线段可以是==横向、竖向、对角线、反对角线==四种方向',
                 '本视频：`[[1,1,0],[0,1,1],[1,0,1]]` → `3`（主对角线）'],
        quote='如果在指定方向上枚举，则完全不需要数组，只需要使用遍历迭代就行了。以row[i][j]为例，在这里可以只一个变量now而不是数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['先写 DP：四个数组分别表示以 `(i,j)` 结尾的四个方向连续 1 的个数',
              '但每个方向只依赖前一个格子 → ==沿方向枚举，一个 `now` 就够==',
              '遇到 1 就 `now += 1`，遇到 0 或换到新的一条线就清零'],
        summary=['时间 `O(mn)`，空间 `O(1)`：四趟扫描，每趟每格只看一次',
                 '反对角线上 `i + j` 相同，主对角线上 `i - j` 相同，共 `m + n - 1` 条',
                 '易错：换一条线时 `now` 必须清零；对角线的 `i` 范围要用 `max/min` 限制在矩阵内',
                 '原文为 Python 2 风格，只删去了 `:type` 说明文档字符串，代码未改'],
    ),
)
