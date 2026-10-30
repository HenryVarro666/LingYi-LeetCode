def _txt(S):
    if 'index' not in S:
        return '`left[c-1]`：c 左侧最近出现的位置；`right[c-1]`：右侧最近的位置（`-n` / `2n` 表示没有）'
    L = S.get('_line')
    if L and L >= 20 and 'c' in S and 'mi' not in S:
        return f'查询：位置 `{S["index"]}`、颜色 `{S["c"]}`，看两张表的黄格'
    if 'mi' in S and L and L >= 20:
        return f'查询：到左边 `{S["index"] - S["left_list"][S["index"]][S["c"] - 1]}`，到右边 `{S["right_list"][S["index"]][S["c"] - 1] - S["index"]}`，取小 `mi = {S["mi"]}`'
    return f'扫描位置 `index = {S["index"]}`，颜色 `{S["colors"][S["index"]]}`'

COLS = {1: 'pink', 2: 'cyan', 3: 'orange'}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    colors = S['colors']
    n = len(colors)
    live = 'index' in S
    L = S.get('_line', 0)
    cv.text((x0 + 18, y0 + 4), 'colors（粉 1 / 青 2 / 橙 3）', 22, T['muted'], bold=True)
    cell = 70
    sx = x0 + (x1 - x0 - cell * n) / 2
    for i, v in enumerate(colors):
        X = sx + i * cell
        cv.rect((X + 3, y0 + 40, X + cell - 3, y0 + 40 + 56), fill=T[COLS[v]], r=8)
        cv.text((X + cell / 2, y0 + 68), v, 30, T['bg'], anchor='mm', bold=True)
        cv.text((X + cell / 2, y0 + 100), i, 16, T['dim'], anchor='mt', mono=True)
    if live and 0 <= S['index'] < n:
        X = sx + S['index'] * cell + cell / 2
        cv.tri_down(X, y0 + 38, 9, T['blue'])
    ty = y0 + 150
    rh = min(38, (y1 - ty - 40) / n)
    cw = 62
    q = live and L >= 21 and 'c' in S and L != 27
    tabs = [('left_list', 'left_list[i]：i 及其左边最近的下标', x0 + 30),
            ('right_list', 'right_list[i]：i 及其右边最近的下标', x0 + 30 + (x1 - x0) / 2)]
    for name, title, tx in tabs:
        cv.text((tx, ty - 8), title, 20, T['muted'], anchor='lb', bold=True)
        rows = S[name]
        k = len(rows)
        built = name == 'left_list' or L >= 18
        for j in range(3):
            cv.text((tx + 50 + j * cw + cw / 2, ty + 14), f'颜色{j + 1}', 16, T[COLS[j + 1]], anchor='mm', bold=True)
        for r in range(n):
            Y = ty + 30 + r * rh
            cv.text((tx + 20, Y + rh / 2), r, 18, T['dim'], anchor='mm', mono=True)
            if name == 'left_list':
                vals = rows[r] if r < k else None
            elif built:
                vals = rows[r] if r < k else None
            else:
                kk = n - 1 - r
                vals = rows[kk] if 0 <= kk < k else None
            for j in range(3):
                X = tx + 50 + j * cw
                hit = q and r == S['index'] and j == S['c'] - 1 and (name != 'right_list' or True)
                fill = T['yellow'] if hit else None
                cv.rect((X + 2, Y + 2, X + cw - 2, Y + rh - 2), fill=fill or (36, 42, 52), r=5)
                if vals is not None:
                    v = vals[j]
                    cv.text((X + cw / 2, Y + rh / 2), v, 20, T['bg'] if hit else (T['dim'] if abs(v) >= n else T['text']),
                            anchor='mm', bold=True, mono=True)
        if live and not q and L in (9, 10, 15, 16) and ((name == 'left_list') == (L in (9, 10))):
            pass
    if q:
        cv.text((x0 + 18, y1 - 6), '黄格：查询用到的两个值（灰色 = 占位，表示这种颜色不存在）', 20, T['yellow'], anchor='lb')


CONFIG = dict(
    num=1182, title='与目标颜色间的最短距离', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='正反两趟预处理 · 最近位置表',
    tags=['题单·二分算法'],
    code='''
class Solution(object):
    def shortestDistanceColor(self, colors, queries):

        n = len(colors)

        left = [-n, -n, -n]
        left_list = []
        for index in range(n):
            left[colors[index] - 1] = index
            left_list.append(left[:])
        
        right = [n + n, n + n, n + n]
        right_list = []
        for index in range(n - 1, -1, -1):
            right[colors[index] - 1] = index
            right_list.append(right[:])
        
        right_list.reverse()

        res = []
        for index, c in queries:
            mi = min(index - left_list[index][c - 1], right_list[index][c - 1] - index)
            if mi >= n:
                mi = -1
            res.append(mi)
        
        return res
''',
    call='Solution().shortestDistanceColor([1,1,2,1,3,2,3], [[1,3],[2,2],[6,1]])',
    expect=[3, 0, 3],
    views=[
        dict(type='custom', draw=_draw, h=560),
        dict(type='text', h=70, size=26, fn=_txt),
    ],
    watch=[('n', 'n'), ('index', 'index', 'blue'), ('c', 'c', 'orange'), ('mi', 'mi', 'green'), ('res', 'res', 'green')],
    captions={
        'n = len(colors)': '`n = {n}`。没有出现的颜色用 `-n` 或 `2n` 占位，距离一定 ≥ n',
        'left = [-n': '`left[c-1]`：颜色 c 左侧最近出现的下标，一开始都没见过 → `-n`',
        'left_list = []': '`left_list[i]` 保存扫到 i 时的 `left` 快照',
        'left[colors[index] - 1] = index': '位置 `{index}` 是颜色 `{colors[index]}` → 它自己就是左侧最近的：`left = {left}`，同时把快照 `left[:]` 存进 `left_list`',
        'left_list.append': '把当前 `left` 拷贝一份记到 `left_list[{index}]`（要用 `left[:]` 拷贝）',
        'right = [n + n': '反向再来一趟：`right[c-1]` 是右侧最近的下标，没见过 → `2n`',
        'right_list = []': '`right_list` 先按倒序存，最后翻转',
        'for index in range(n - 1': lambda S, B, r: (f'从右往左：`index = {S.index}`' if len(S.right_list) == 0 or S.index != B.index
                                                     else '反向扫描结束'),
        'right[colors[index] - 1] = index': '从右往左，位置 `{index}` 是颜色 `{colors[index]}` → `right = {right}`，快照存进 `right_list`（倒序）',
        'right_list.append': '记下快照（倒序存放）',
        'right_list.reverse': '翻转后 `right_list[i]` 就对应位置 `i`',
        'res = []': '预处理完毕，每个查询 `O(1)` 回答',
        'for index, c in queries': lambda S, B, r: (f'查询：从位置 `{S.index}` 找颜色 `{S.c}`' if 'c' not in B or (S.index, S.c) != (B.index, B.c)
                                                    else '查询全部回答完了'),
        'mi = min': '左边 `{index} − {left_list[index][c-1]}`，右边 `{right_list[index][c-1]} − {index}`，取小 → `mi = {mi}`',
        'if mi >= n': lambda S, B, r: (f'`mi = {S.mi} ≥ n = {S.n}`：占位值被选中，说明颜色不存在 → 答案 -1' if S.mi >= S.n
                                       else f'`mi = {S.mi} < n`：真的找到了这个颜色，保留'),
        'mi = -1': '改成 `-1`',
        'res.append': '这个查询的答案 `{mi}` 加入 `res = {res}`',
        'return res': '返回 `{res}`',
    },
    skip=['left_list.append', 'right_list.append'],
    max_steps=75,
    cards=dict(
        one_liner='正反各扫一遍，查询直接查表',
        complexity='时间 `O(n + q)`，空间 `O(n)`',
        problem=['`colors[i]` 取 1/2/3，每个查询 `(i, c)`：从下标 `i` 到最近的颜色 `c` 的距离，没有则 `-1`',
                 '示例：`colors=[1,1,2,1,3,2,2,3,3]`，`queries=[[1,3],[2,2],[6,1]]` → `[3,0,3]`',
                 '本视频：`colors=[1,1,2,1,3,2,3]`，同样的查询 → `[3,0,3]`'],
        quote='首先正反两趟遍历，预处理出两个数组left和right，其含义为对于每个位置，其左侧和右侧最近的1、2、3所在的下标。',
        quote_src='—— yiduobo 题解原文',
        idea=['`left_list[i][c-1]`：位置 i 及其左边最近的颜色 c；`right_list` 同理看右边',
              '一个查询的答案 = `min(i − 左最近, 右最近 − i)`',
              '没出现的颜色用 `-n` / `2n` 占位，距离 ≥ n 就判为 `-1`'],
        summary=['时间 `O(n + q)`，空间 `O(n)`（两个 n×3 的表）',
                 '易错：下标要 `c - 1`；快照必须 `left[:]` 拷贝，否则全部指向同一个列表',
                 '右侧表倒序生成，别忘了 `reverse()`',
                 '原文为 Python 2 风格，本题代码无需改动，直接可运行',
                 '题单归在二分，但这个写法不用二分，预处理就够了'],
    ),
)
