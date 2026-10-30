def _color(S, i, j, v):
    if v and v == max(max(r) for r in S['res']):
        return 'yellow'
    if v:
        return 'green'
    if 'x1' in S and 'y2' in S:
        x1, y1, x2, y2 = S['x1'], S['y1'], S['x2'], S['y2']
        if x1 <= i <= x2 and y1 <= j <= y2 and (i in (x1, x2) or j in (y1, y2)):
            return 'blue'
    return None


def _layer(S):
    if 'y2' not in S:
        return '从外往内一层一层处理：每层是一个正方形的==外框=='
    x1, y1, x2, y2 = S['x1'], S['y1'], S['x2'], S['y2']
    tail = '　==只剩中心一格==' if x1 == x2 else f'　每条边 `{y2 - y1}` 格'
    return f'第 `index = {S["index"]}` 层（蓝色外框）：左上 `({x1}, {y1})`，右下 `({x2}, {y2})`{tail}'


def _cap_center(S, B, ret):
    if S.x1 == S.x2:
        return f'`x1 == x2 = {S.x1}`：n 为奇数，最中心只有一个点，==四条边重叠成一格==，只填一次'
    return f'`x1 = {S.x1}` ≠ `x2 = {S.x2}`：正常切成上、右、下、左四条边'


CONFIG = dict(
    num=59, title='螺旋矩阵 II', difficulty='Medium', category='矩阵',
    author='yiduobo', technique='按层模拟 · 每层四条边',
    tags=['字节30天', '热题173'],
    code='''
class Solution(object):
    def generateMatrix(self, n):
        res = [[0 for index in range(n)] for index in range(n)]

        now = 1
        for index in range((n + 1) // 2):
            x1 = y1 = index
            x2 = y2 = n - index - 1

            if x1 == x2:
                res[x1][y1] = now
            else:
                for pos in range(y1, y2):
                    res[x1][pos] = now
                    now += 1
                for pos in range(x1, x2):
                    res[pos][y2] = now
                    now += 1
                for pos in range(y2, y1, -1):
                    res[x2][pos] = now
                    now += 1
                for pos in range(x2, x1, -1):
                    res[pos][y1] = now
                    now += 1
        return res
''',
    call='Solution().generateMatrix(5)',
    expect=[[1, 2, 3, 4, 5], [16, 17, 18, 19, 6], [15, 24, 25, 20, 7], [14, 23, 22, 21, 8], [13, 12, 11, 10, 9]],
    skip=['now += 1', 'for pos in range'],
    views=[
        dict(type='text', h=60, size=27, fn=_layer),
        dict(type='grid', var='res', cell=104, h=560, color=_color,
             label='res（蓝 = 当前层还没填的格子，绿 = 已填，黄 = 刚填）'),
    ],
    watch=['index', ('x1', 'x1', 'blue'), ('y1', 'y1', 'blue'), ('x2', 'x2', 'blue'), ('y2', 'y2', 'blue'),
           ('pos', 'pos', 'yellow'), ('now', 'now', 'green')],
    captions={
        'res = [[0': '`{n} × {n}` 的矩阵，先全填 0',
        'now = 1': '`now`：下一个要填的数，从 `1` 开始',
        'for index in range(': lambda S, B, ret: (
            '所有层都处理完了' if B.get('index') == S['index']
            else f'层数 `(n + 1) // 2 = {(S.n + 1) // 2}`；处理第 `index = {S.index}` 层'),
        'x1 = y1 = index': '这一层左上角：`(x1, y1) = ({x1}, {y1})`',
        'x2 = y2 = n - index - 1': '正方形，右下角对称：`x2 = y2 = {n} - {index} - 1 = {x2}`',
        'if x1 == x2': _cap_center,
        'res[x1][y1] = now': '中心点 `({x1}, {y1})` 填 `{now}`',
        14: lambda S, B, ret: f'上边 `[y1, y2)` 从左往右：`res[{S.x1}][{S.pos}] = {B.now}`' + ('，==右上角留给右边==' if S.pos == S.y2 - 1 else ''),
        17: lambda S, B, ret: f'右边 `[x1, x2)` 从上往下：`res[{S.pos}][{S.y2}] = {B.now}`' + ('，==右下角留给下边==' if S.pos == S.x2 - 1 else ''),
        20: lambda S, B, ret: f'下边 `(y1, y2]` 从右往左：`res[{S.x2}][{S.pos}] = {B.now}`' + ('，==左下角留给左边==' if S.pos == S.y1 + 1 else ''),
        23: lambda S, B, ret: f'左边 `(x1, x2]` 从下往上：`res[{S.pos}][{S.y1}] = {B.now}`' + ('，左上角早已填过，这一层结束' if S.pos == S.x1 + 1 else ''),
        'return res': '返回 `res`',
    },
    max_steps=60,
    cards=dict(
        one_liner='从外往内一圈一圈填，每圈按上、右、下、左四条边',
        complexity='时间 `O(n²)`，空间 `O(1)`（返回值不计）',
        problem=['给你正整数 `n`，生成 `n × n` 的矩阵',
                 '按==顺时针螺旋==顺序依次填入 `1` 到 `n²`',
                 '示例：`n = 3` → `[[1,2,3],[8,9,4],[7,6,5]]`；本视频用 `n = 5`'],
        quote='都是从外往内每次处理一个矩形，然后对于每个矩形同样是分为上边、右边、下边、左边依次进行处理。……当n为奇数时，中心点的四边都是重叠的，只需要处理一次。',
        quote_src='—— yiduobo 题解',
        idea=['第 `index` 层：左上角 `(index, index)`，右下角 `(n-1-index, n-1-index)`',
              '四条边都==左闭右开==：每条边不含自己的终点，终点是下一条边的起点',
              '`n` 为奇数时最里层只有一个点，单独填一次'],
        summary=['时间 `O(n²)`，空间 `O(1)`',
                 '层数 `(n + 1) // 2`：奇数 `n` 多出中心这一“层”',
                 '易错：中心点不特判的话，四个 `range` 都为空，中心会漏填（仍是 0）',
                 '原文为 Python 2：`(n + 1) / 2` 已改为 `(n + 1) // 2`，删去 docstring',
                 '对比灵神：灵神用方向数组 + 撞墙右转，yiduobo 直接按层切边'],
    ),
)
