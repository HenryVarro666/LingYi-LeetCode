def _color(S, i, j, v):
    res = S.get('res') or []
    if res and v == res[-1]:
        return 'yellow'
    if v in res:
        return 'green'
    if 'x1' in S and 'y2' in S:
        x1, y1, x2, y2 = S['x1'], S['y1'], S['x2'], S['y2']
        if x1 <= i <= x2 and y1 <= j <= y2 and (i in (x1, x2) or j in (y1, y2)):
            return 'blue'
    return None


def _layer(S):
    if 'y2' not in S:
        return '从外往内一层一层剥：每层切成==上、右、下、左==四条边'
    return (f'第 `index = {S["index"]}` 层（蓝色）：左上角 `({S["x1"]}, {S["y1"]})`，右下角 `({S["x2"]}, {S["y2"]})`'
            + ('　==只有一行==' if S['x1'] == S['x2'] else ('　==只有一列==' if S['y1'] == S['y2'] else '')))


def _cap_one_row(S, B, ret):
    x1, x2, y1, y2, M = S['x1'], S['x2'], S['y1'], S['y2'], S['matrix']
    if x1 != x2:
        return f'`x1 = {x1}` ≠ `x2 = {x2}`：不止一行'
    top = ', '.join(map(str, M[x1][y1:y2]))
    bot = ', '.join(map(str, M[x2][y2:y1:-1]))
    return f'`x1 == x2`：==只剩一行==。若照常切四条边，上边出 `{top}`，下边又出 `{bot}` → ==重复输出==，所以单独处理'



def _draw_list(name, cell_max=74):
    """数组视图的替代：引擎的 array 视图在空列表时会越界，这里自己画（空列表显示“空”）"""
    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), name, 24, T['muted'], bold=True)
        vals = S.get(name)
        if vals is None:
            cv.text((x0 + 18, y0 + 44), '（尚未创建）', 24, T['dim'])
            return
        if not vals:
            cv.text((x0 + 18, y0 + 44), '[ ]  空', 24, T['dim'], mono=True)
            return
        bvals = B.get(name) or []
        width = x1 - x0 - 40
        cell = min(cell_max, width / len(vals))
        ch = min(cell * 0.92, 68)
        top = y0 + 40
        for i, v in enumerate(vals):
            X = x0 + 20 + i * cell
            new = i >= len(bvals) or bvals[i] != v
            cv.rect((X + 3, top, X + cell - 3, top + ch), fill=T['panel2'], r=8,
                    outline=T['yellow'] if new else T['border'], width=3 if new else 1)
            cv.text((X + cell / 2, top + ch / 2), v, int(min(32, cell * 0.42)), T['text'], anchor='mm', bold=True)
            cv.text((X + cell / 2, top + ch + 6), i, 18, T['dim'], anchor='mt', mono=True)
    return draw

CONFIG = dict(
    num=54, title='螺旋矩阵', difficulty='Medium', category='矩阵',
    author='yiduobo', technique='按层模拟 · 每层切四条边',
    code='''
class Solution(object):
    def spiralOrder(self, matrix):
        if not matrix:
            return []

        res = []

        m = len(matrix)
        n = len(matrix[0])

        for index in range(min((m + 1) // 2, (n + 1) // 2)):
            x1 = y1 = index
            x2 = m - index - 1
            y2 = n - index - 1

            if x1 == x2:
                for pos in range(y1, y2 + 1):
                    res.append(matrix[x1][pos])
            elif y1 == y2:
                for pos in range(x1, x2 + 1):
                    res.append(matrix[pos][y1])
            else:

                for pos in range(y1, y2):
                    res.append(matrix[x1][pos])
                for pos in range(x1, x2):
                    res.append(matrix[pos][y2])
                for pos in range(y2, y1, -1):
                    res.append(matrix[x2][pos])
                for pos in range(x2, x1, -1):
                    res.append(matrix[pos][y1])

        return res
''',
    call='Solution().spiralOrder([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]])',
    expect=[1, 2, 3, 4, 5, 10, 15, 14, 13, 12, 11, 6, 7, 8, 9],
    views=[
        dict(type='text', h=56, size=27, fn=_layer),
        dict(type='grid', var='matrix', cell=110, h=420, color=_color),
        dict(type='custom', h=140, draw=_draw_list('res')),
    ],
    watch=['index', ('x1', 'x1', 'blue'), ('y1', 'y1', 'blue'), ('x2', 'x2', 'blue'), ('y2', 'y2', 'blue'), ('pos', 'pos', 'yellow')],
    skip=['for pos in range'],
    captions={
        'if not matrix': '空矩阵直接返回 `[]`；这里不是空的',
        'res = []': '`res` 按顺序收集答案',
        'm = len': '`m = {m}` 行',
        'n = len': '`n = {n}` 列',
        'for index in range(min(': lambda S, B, ret: (
            '所有层都剥完了' if B.get('index') == S['index']
            else f'层数 `min((m+1)//2, (n+1)//2) = {min((S["m"] + 1) // 2, (S["n"] + 1) // 2)}`；剥第 `index = {S["index"]}` 层'),
        'x1 = y1 = index': '这一层的左上角：`(x1, y1) = ({x1}, {y1})`',
        'x2 = m - index - 1': '下边在第 `x2 = {m} - {index} - 1 = {x2}` 行',
        'y2 = n - index - 1': '右边在第 `y2 = {n} - {index} - 1 = {y2}` 列',
        'if x1 == x2': _cap_one_row,
        'elif y1 == y2': lambda S, B, ret: (f'`y1 == y2`：这一层只剩一列' if S['y1'] == S['y2']
                                            else f'`y1 = {S["y1"]}` ≠ `y2 = {S["y2"]}`：也不止一列 → 正常切四条边'),
        18: '单行：第 `{x1}` 行从左到右==全部==输出（闭区间 `[y1, y2]`）：加入 `{matrix[x1][pos]}`',
        21: '单列：第 `{y1}` 列从上到下全部输出：加入 `{matrix[pos][y1]}`',
        25: lambda S, B, ret: f'上边 `[y1, y2)`：`matrix[{S["x1"]}][{S["pos"]}] = {S["matrix"][S["x1"]][S["pos"]]}`' + ('，==右上角留给右边==' if S['pos'] == S['y2'] - 1 else ''),
        27: lambda S, B, ret: f'右边 `[x1, x2)`：`matrix[{S["pos"]}][{S["y2"]}] = {S["matrix"][S["pos"]][S["y2"]]}`' + ('，==右下角留给下边==' if S['pos'] == S['x2'] - 1 else ''),
        29: lambda S, B, ret: f'下边从右往左 `(y1, y2]`：`matrix[{S["x2"]}][{S["pos"]}] = {S["matrix"][S["x2"]][S["pos"]]}`' + ('，==左下角留给左边==' if S['pos'] == S['y1'] + 1 else ''),
        31: lambda S, B, ret: f'左边从下往上 `(x1, x2]`：`matrix[{S["pos"]}][{S["y1"]}] = {S["matrix"][S["pos"]][S["y1"]]}`' + ('，左上角已在上边输出过，这一层结束' if S['pos'] == S['x1'] + 1 else ''),
        'return res': '返回 `res`',
    },
    max_steps=60,
    cards=dict(
        one_liner='从外往内一层层剥，每层切成上、右、下、左四条边依次输出',
        complexity='时间 `O(mn)`，空间 `O(1)`（返回值不计）',
        problem=['给你 `m` 行 `n` 列的矩阵，按==顺时针螺旋顺序==返回所有元素',
                 '例：`[[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15]]`',
                 '→ `[1,2,3,4,5,10,15,14,13,12,11,6,7,8,9]`'],
        quote='同样是从外往内一层一层切分成上边、右边、下边、左边，然后依次输出。……可能出现切分到某一层的长为一或者宽为一的情况，此时上边与下边或者左边与右边是重叠的，只能输出一次。',
        quote_src='—— yiduobo 题解',
        idea=['第 `index` 层：左上角 `(index, index)`，右下角与它对称',
              '四条边都==不含自己的终点==：终点正好是下一条边的起点，每个角只输出一次',
              '只剩一行或一列时四条边会重叠 → ==单独整段输出一次=='],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '层数 = `min((m+1)//2, (n+1)//2)`',
                 '易错：长方形里层可能退化成一行/一列，不特判会重复输出',
                 '原文为 Python 2：`(m + 1) / 2` 改为 `//`，删去 docstring'],
    ),
)
