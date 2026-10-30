MAT = [[1, 2, 3], [4, 5, 6]]
_PAL = ['blue', 'pink', 'green', 'purple', 'cyan', 'orange']


def _grid_color(S, i, j, v):
    rl = S.get('res_list')
    if rl is None:
        return None
    n = len(S['matrix'][0])
    done = sum(len(x) for x in rl)
    if 'res' in S or i * n + j < done:
        return _PAL[(i + j) % len(_PAL)]
    return None


def _draw_lists(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    rl = S.get('res_list')
    cv.text((x0 + 18, y0 + 4), 'res_list[k]：第 k 条对角线（i + j = k）上的数，按行优先顺序放入', 23, T['muted'], bold=True)
    if rl is None:
        cv.text((x0 + 18, y0 + 44), '（尚未创建）', 24, T['dim'])
        return
    brl = B.get('res_list') or []
    cur = S.get('index') if 'res' in S else None
    line = S.get('_line')
    rh = min(46, (y1 - y0 - 44) / max(1, len(rl)))
    for k, lst in enumerate(rl):
        Y = y0 + 40 + k * rh
        c = T[_PAL[k % len(_PAL)]]
        is_cur = cur == k
        if is_cur:
            cv.rect((x0 + 14, Y - 2, x1 - 14, Y + rh - 4), fill=(60, 52, 30), r=8)
        cv.text((x0 + 30, Y + rh / 2 - 3), f'[{k}]', 22, c, anchor='lm', mono=True, bold=True)
        X = x0 + 90
        for t, v in enumerate(lst):
            cv.rect((X, Y + 2, X + 50, Y + rh - 8), fill=c, r=6)
            cv.text((X + 25, Y + rh / 2 - 3), v, 22, T['bg'], anchor='mm', bold=True)
            X += 56
        if not lst:
            cv.text((X, Y + rh / 2 - 3), '[ ]  空', 20, T['dim'], anchor='lm', mono=True)
        tag = ''
        if 'res' in S and k % 2 == 0 and lst:
            if cur is not None and (k < cur or (k == cur and line in (16, 17))):
                tag = '偶数 → 已反转'
            elif cur is not None and k >= cur:
                tag = '偶数 → 要反转'
        elif 'res' in S and k % 2 == 1 and lst:
            tag = '奇数 → 原样'
        if is_cur and line == 16:
            tag = '← 刚反转'
        if tag:
            cv.text((x1 - 30, Y + rh / 2 - 3), tag, 20, T['yellow'] if is_cur else T['muted'], anchor='rm', bold=True)


CONFIG = dict(
    num=498, title='对角线遍历', difficulty='Medium', category='矩阵',
    author='yiduobo', technique='按 i + j 分组 · 偶数条反转后拼接',
    tags=['热题173'],
    code='''
class Solution(object):
    def findDiagonalOrder(self, matrix):
        if not matrix:
            return []

        m = len(matrix)
        n = len(matrix[0])
        res_list = [[] for _ in range(m + n + 1)]
        for i in range(m):
            for j in range(n):
                res_list[i + j].append(matrix[i][j])

        res = []
        for index in range(m + n + 1):
            if index % 2 == 0:
                res_list[index].reverse()
            res.extend(res_list[index])

        return res
''',
    call=f'Solution().findDiagonalOrder({MAT})',
    expect=[1, 2, 4, 5, 3, 6],
    views=[
        dict(type='grid', var='matrix', label='matrix（同色 = 同一条对角线）', h=250, cell=86,
             color=_grid_color, cursors=[("i if 'res' not in vars() else None", 'j', 'yellow')]),
        dict(type='custom', draw=_draw_lists, h=280),
        dict(type='array', var='res', label='res', cell=66, h=110),
    ],
    watch=[('i', lambda S: None if 'res' in S else S.get('i')), ('j', lambda S: None if 'res' in S else S.get('j')),
           ('i + j', lambda S: None if 'res' in S or 'j' not in S else S['i'] + S['j'], 'yellow'),
           ('index', lambda S: S.get('index') if 'res' in S else None, 'cyan'), ('len(res)', 'len(res)', 'green')],
    captions={
        'if not matrix': '矩阵不为空，继续',
        'm = len(matrix)': '`m = {m}` 行',
        'n = len(matrix[0])': '`n = {n}` 列',
        'res_list = [[]': '为每条对角线准备一个列表：开了 `m + n + 1 = {len(res_list)}` 个（实际只用到 `m + n − 1` 个，多的为空）',
        'res_list[i + j].append': '`({i},{j})`：`i + j = {i + j}` → 在第 =={i + j}== 条对角线上，`res_list[{i + j}]` 加入 `{matrix[i][j]}`',
        'res = []': '一次遍历后，每条对角线上的数都按「从右上到左下」的顺序放好了',
        'for index in range': lambda S, B, ret: (f'处理第 `{S.index}` 条对角线' if S.get('index') != B.get('index')
                                                 else '所有对角线都拼好了'),
        'if index % 2 == 0': lambda S, B, ret: (
            (f'`{S.index}` 是偶数 → 反转（不过这是多开的空列表）' if not S.res_list[S.index]
             else f'`{S.index}` 是偶数：这条要==从左下往右上==走 → 反转') if S.index % 2 == 0
            else (f'`{S.index}` 是奇数，不用反转（空列表）' if not S.res_list[S.index]
                  else f'`{S.index}` 是奇数：本来就是从右上往左下 → 不用反转')),
        'res_list[index].reverse()': '反转：`res_list[{index}] = {res_list[index]}`',
        'res.extend': lambda S, B, ret: (f'拼到答案后面：`res = {S.res}`' if S.res_list[S.index]
                                         else f'`res_list[{S.index}]` 是空的（多开的），拼了也不变'),
        'return res': '返回 `{ret}`',
    },
    skip=['for i in range(m)', 'for j in range(n)', 'return []'],
    cards=dict(
        one_liner='先按 i + j 把数分到各条对角线，偶数条反转，再依次拼起来',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['按对角线==之字形==的顺序，返回 `m × n` 矩阵的所有元素',
                 '示例：`[[1,2,3],[4,5,6],[7,8,9]]` → `[1,2,4,7,5,3,6,8,9]`',
                 '本视频：`[[1,2,3],[4,5,6]]` → `[1,2,4,5,3,6]`'],
        quote='如果将左上角视为第0条对角线，那么对于第i行第j个元素，其所在的==对角线编号为i + j==，于是可以先通过一次遍历计算出每条对角线上有哪些元素。接下来，对于==编号为偶数的对角线，我们应当将其反转==。',
        quote_src='—— yiduobo 题解原文',
        idea=['按行遍历：同一条对角线上，行号小的先放 → 列表里是==右上 → 左下==的顺序',
              '题目要求偶数条对角线==左下 → 右上==，所以偶数条反转',
              '最后把所有对角线按编号拼起来即为答案'],
        result='返回 `[1,2,4,5,3,6]` ✓',
        summary=['时间 `O(mn)`；空间 `O(mn)`：额外存了一份按对角线分组的数',
                 '列表开了 `m + n + 1` 个，比需要的 `m + n − 1` 多两个空列表，不影响结果',
                 '原文为 Python 2 写法，只删去了类型说明文档字符串，代码未改',
                 '对比灵神：灵神直接算出每条对角线上 j 的范围，按方向取数，不用额外空间'],
    ),
)
