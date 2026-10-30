PIC = [['W', 'B', 'W', 'W'],
       ['W', 'W', 'B', 'B'],
       ['B', 'W', 'W', 'W']]


def _lonely(S, i, j, v):
    if 'res' not in S or 'row' not in S:
        return None
    if v == 'B' and S['row'][i] == 1 and S['col'][j] == 1:
        return 'green'
    return None


def _top(S):
    if 'res' in S:
        return f"第二遍：黑像素所在行、列的黑像素数都为 1 才算孤独像素，`res = {S['res']}`"
    if 'row' in S:
        return '第一遍：`row[i]` 数第 i 行的黑像素，`col[j]` 数第 j 列的黑像素'
    return '孤独像素 = 所在行和所在列里==唯一==的黑像素 `B`'


CONFIG = dict(
    num=531, title='孤独像素 I', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='行列计数 · 两次遍历',
    code='''
class Solution(object):
    def findLonelyPixel(self, picture):

        m = len(picture)
        n = len(picture[0])
        row = [0] * m
        col = [0] * n

        for i in range(m):
            for j in range(n):
                if picture[i][j] == 'B':
                    row[i] += 1
                    col[j] += 1
        
        res = 0
        for i in range(m):
            for j in range(n):
                if picture[i][j] == 'B' and row[i] == 1 and col[j] == 1:
                    res += 1
        
        return res
''',
    call=f'Solution().findLonelyPixel({PIC})',
    expect=2,
    skip=['m = len', 'n = len', 'for i in range', 'for j in range'],
    views=[
        dict(type='text', size=26, fn=_top, h=70),
        dict(type='grid', var='picture', label='picture（黑 B / 白 W；绿 = 孤独像素，蓝框 = 当前格子）', cell=100, h=330,
             color=_lonely, cursors=[('i', 'j', 'blue')]),
        dict(type='array', var='row', label='row（每行黑像素数）', cell=90, h=130),
        dict(type='array', var='col', label='col（每列黑像素数）', cell=90, h=130),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('res', 'res', 'green')],
    captions={
        'row = [0] * m': '`row[i]` 记录第 i 行有几个黑像素，共 `{m}` 行',
        'col = [0] * n': '`col[j]` 记录第 j 列有几个黑像素，共 `{n}` 列',
        "if picture[i][j] == 'B':": lambda S, B, r: (f"`picture[{S.i}][{S.j}] = 'B'` 是黑像素，要计入行列" if S.picture[S.i][S.j] == 'B'
                                                      else f"`picture[{S.i}][{S.j}] = 'W'` 白像素，不计数"),
        'row[i] += 1': '第 `{i}` 行又多一个黑像素：`row[{i}] = {row[i]}`',
        'col[j] += 1': '第 `{j}` 列又多一个黑像素：`col[{j}] = {col[j]}`',
        'res = 0': '行列统计完了，第二遍遍历来找孤独像素，`res = 0`',
        "row[i] == 1 and col[j] == 1": lambda S, B, r: (
            f"`({S.i},{S.j})` 是黑像素，`row[{S.i}] = {S.row[S.i]}`，`col[{S.j}] = {S.col[S.j]}`"
            + ('：行列都==只有它一个== → 孤独像素' if S.row[S.i] == 1 and S.col[S.j] == 1 else '：行或列里还有别的黑像素 → 不孤独')
            if S.picture[S.i][S.j] == 'B' else f"`({S.i},{S.j})` 是白像素，直接跳过"),
        'res += 1': '找到一个孤独像素，`res` → {res}',
        'return res': '一共 `{res}` 个孤独像素',
    },
    cards=dict(
        one_liner='先数每行每列的黑像素，再找行列都只有一个的格子',
        complexity='时间 `O(mn)`，空间 `O(m+n)`',
        problem=['`m × n` 的图片，`B` 是黑像素，`W` 是白像素',
                 '孤独像素：所在==行和列==中==唯一==的黑像素',
                 '返回黑色孤独像素的数量',
                 '本视频：3×4 的图片，答案是 `2`'],
        quote='可以先遍历整个图片，使用两个数组统计每一行和每一列中黑色像素的数量，接下来再遍历整个图片，对于每个单元格，若其为黑色像素，且其所在行和所在列都只有一个黑色像素，那么该单元格上就是一个孤独像素。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一遍：`row[i]`、`col[j]` 分别累计每行每列的黑像素数',
              '第二遍：格子是 `B` 且 `row[i] == 1` 且 `col[j] == 1` 就是孤独像素',
              '不用在原图上反复扫行扫列，两遍就够'],
        summary=['时间 `O(mn)`，空间 `O(m+n)`',
                 '易错：必须是黑像素才计数，白像素的行列计数也可能为 1',
                 '这是会员题，题面按 LeetCode 原题整理',
                 '原文代码已是 Python 3 写法，未改动'],
    ),
)
