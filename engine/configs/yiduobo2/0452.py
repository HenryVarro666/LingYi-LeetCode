POINTS = [[5, 9], [1, 6], [10, 16], [3, 4], [7, 12], [2, 8]]
LO, HI = 0, 17
GROUP_COLORS = ['pink', 'cyan', 'purple', 'blue']


def _cur_idx(S):
    pts = S.get('sorted_points')
    if not pts:
        return None
    if 'x' not in S:
        return 0
    for k, p in enumerate(pts):
        if k > 0 and p[0] == S['x'] and p[1] == S['y']:
            return k
    return None


def _groups(S, B):
    """每个气球属于第几组（只算已经处理过的）"""
    pts = S.get('sorted_points') or []
    idx = _cur_idx(S)
    if idx is None:
        return {}
    line = S.get('_line')
    ended = line == 9 and (B.get('x'), B.get('y')) == (S.get('x'), S.get('y'))
    upto = idx + 1 if (line in (7, 8, 10, 11, 12, 14, 16) or ended or idx == 0) else idx
    g, right, out = 0, None, {}
    for k, (a, b) in enumerate(pts[:upto]):
        if k == 0:
            right = b
        elif a > right:
            if not (k == idx and line == 10):  # 刚判断完，还没开新组
                g += 1
                right = b
            else:
                continue
        else:
            right = min(right, b)
        out[k] = g
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    L, R = x0 + 170, x1 - 50

    def X(v):
        return L + (v - LO) / (HI - LO) * (R - L)
    pts = S.get('sorted_points')
    title = 'sorted_points（按左端点排序）' if pts else 'points（尚未排序）'
    pts = pts or S.get('points') or POINTS
    cv.text((x0 + 18, y0 + 4), title + '：橙 = 当前这一组，其他颜色 = 已结束的组', 24, T['muted'], bold=True)
    idx = _cur_idx(S) if S.get('sorted_points') else None
    grp = _groups(S, B) if S.get('sorted_points') else {}
    cur_g = max(grp.values()) if grp else None
    top = y0 + 74
    rowh = min(68, (y1 - top - 80) / max(1, len(pts)))
    for k, (a, b) in enumerate(pts):
        y = top + k * rowh
        g = grp.get(k)
        if g is None:
            c = (95, 105, 118)
        elif g == cur_g:
            c = T['orange']
        else:
            c = T[GROUP_COLORS[g % len(GROUP_COLORS)]]
        cv.rect((X(a), y + 10, X(b), y + rowh - 14), fill=c, r=10)
        if k == idx:
            cv.rect((X(a) - 4, y + 6, X(b) + 4, y + rowh - 10), outline=T['yellow'], width=4, r=12)
        cv.text((x0 + 30, y + rowh / 2 - 2), f'[{a},{b}]', 22, T['yellow'] if k == idx else T['text'], anchor='lm', mono=True)
    # 当前组的公共部分 [max(start), right]：一支箭射在这里就能引爆这一组
    if cur_g is not None and 'right' in S:
        mem = [k for k, g in grp.items() if g == cur_g]
        lo = max(pts[k][0] for k in mem)
        r = S['right']
        ya, yb = top + min(mem) * rowh + 2, top + (max(mem) + 1) * rowh - 6
        if lo <= r:
            cv.rect((X(lo), ya, X(r), yb), fill=T['text'], alpha=55, r=6)
            cv.rect((X(lo), ya, X(r), yb), outline=T['yellow'], width=2, r=6)
        cv.dashed((X(r), ya - 10), (X(r), yb + 2), T['orange'], 3, 10, 6)
        cv.text((X(r) + 6, ya - 4), f'right={r}', 20, T['orange'], anchor='lb', bold=True)
    ay = y1 - 34
    cv.line([(L, ay), (R, ay)], T['border'], 2)
    for v in range(LO, HI + 1):
        if v % 2 == 0:
            cv.line([(X(v), ay - 4), (X(v), ay + 4)], T['dim'], 2)
            cv.text((X(v), ay + 8), str(v), 18, T['dim'], anchor='mt')


def _info(S):
    if 'res' not in S:
        return '先==按左端点==排序，再从左往右把能重叠的气球分到同一组'
    return f"已结束 `res = {S['res']}` 组；当前组的最小右端点 `right = {S['right']}`（一支箭射在公共部分里）"


def _if_cap(S, B, ret):
    if S.x > B.right:
        return f'`x = {S.x} > right = {B.right}`：和这一组==重叠不上== → 这一组结束，需要再来一支箭'
    return f'`x = {S.x} ≤ right = {B.right}`：能和这一组的公共部分重叠 → 放进这一组'


def _min_cap(S, B, ret):
    if S.right != B.right:
        return f'`right = min({B.right}, {S.y}) = {S.right}`：公共部分==缩小==，箭只能射在 `≤ {S.right}` 的位置'
    return f'`right = min({B.right}, {S.y}) = {S.right}`：右端点更远，公共部分不变'


def _for_cap(S, B, ret):
    if 'x' in S and (B.get('x'), B.get('y')) != (S.x, S.y):
        return f'下一个气球 `[{S.x}, {S.y}]`'
    return '所有气球都分好组了'


CONFIG = dict(
    num=452, title='用最少数量的箭引爆气球', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='按左端点排序 · 统计重叠不上的区间',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def findMinArrowShots(self, points):
        if not points:
            return 0

        sorted_points = sorted(points, key=lambda d:(d[0], d[1]))
        left, right = sorted_points[0]
        res = 0
        for x, y in sorted_points[1:]:
            if x > right:
                left, right = x, y
                res += 1
            else:
                right = min(right, y)

        return res + 1
''',
    call=f'Solution().findMinArrowShots({POINTS})',
    expect=3,
    views=[
        dict(type='text', h=56, fn=_info, size=25),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('x', 'x', 'yellow'), ('y', 'y', 'yellow'), ('left', 'left'), ('right', 'right', 'orange'), ('res', 'res', 'green')],
    captions={
        'if not points': '`points` 非空，继续',
        'sorted_points = sorted': '按==左端点==排序（相同再比右端点）：`{sorted_points}`',
        'left, right = sorted_points[0]': '第一组从 `[{left}, {right}]` 开始：`right` 记录这一组的==最小右端点==',
        'res = 0': '`res` 统计==已经结束==的组（重叠不上的次数）',
        'for x, y in': _for_cap,
        'if x > right': _if_cap,
        'left, right = x, y': '新的一组从 `[{x}, {y}]` 开始：`right = {right}`',
        'res += 1': '结束的组数 `res = {res}`',
        'else:': '前面的条件不成立 → 走 `else`：重叠上了',
        'right = min': _min_cap,
        'return res + 1': '最后一组还没计数，所以 `res + 1` → 至少 =={ret}== 支箭',
    },
    cards=dict(
        one_liner='排好序后，能和当前组重叠就并进去，重叠不上就多一支箭',
        complexity='时间 `O(n log n)`（排序），空间 `O(n)`（`sorted` 新列表）',
        problem=['气球 `points[i] = [x_start, x_end]`，在 `x` 处竖直射箭',
                 '能引爆所有 `x_start ≤ x ≤ x_end` 的气球，求引爆全部气球的==最少箭数==',
                 '示例：`[[10,16],[2,8],[1,6],[7,12]]` → `2`；本视频用 6 个气球'],
        quote='题目说的是气球，但是实际上可以抽象从一维区间，寻找重叠的区间……435题是对于重叠上的区间不进行计数，而这一题则是==对重叠不上的区间进行计数==。',
        quote_src='—— yiduobo 题解原文',
        idea=['按左端点排序后，从左往右把气球分组：==同一组共用一支箭==',
              '`right` 是当前组的最小右端点；新气球 `x ≤ right` 就能并进来，并把 `right` 缩成 `min`',
              '`x > right` 就重叠不上：开新组、`res += 1`；最后一组在 `return` 时补上 `+1`'],
        result='运行结束，返回 `3`：三组 `[1,6][2,8][3,4]`、`[5,9][7,12]`、`[10,16]`',
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：并入一组后要 `right = min(right, y)`，否则 `[3,4]` 这种短气球会被漏掉',
                 '返回 `res + 1`：`res` 只数了“重叠不上”的次数，最后一组要补上',
                 '对比灵神：按右端点排序就不用维护 `min`，`pre = end` 即可',
                 '原文为 Python 2 风格，只删去了 docstring，代码未改'],
    ),
)
