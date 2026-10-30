INTERVALS = [[1, 3], [2, 4], [3, 5], [1, 2], [4, 7], [5, 6]]   # 互不相同，便于从 (x, y) 反查下标
LO, HI = 1, 7


def _state(S, B):
    """按 yiduobo 的扫描过程复原每个区间的状态：keep（当前考察的保留区间）/ done（确认不冲突，不用再管）/ del / cur / clash / todo"""
    iv = S['sorted_intervals']
    n, line = len(iv), S['_line']
    st = ['todo'] * n
    if 'right' not in S:
        return st
    if 'x' not in S:
        k = 0          # 还没进循环
    elif line == 16 or (line == 9 and 'x' in B and (B['x'], B['y']) == (S['x'], S['y'])):
        k = n          # 扫描结束
    else:
        k = iv.index([S['x'], S['y']])
    right, keep = iv[0][1], 0
    st[0] = 'keep'
    for j in range(1, n):
        if j > k:
            break
        if j == k and line not in (11, 13, 14):
            st[j] = 'cur'
            break
        x, y = iv[j]
        if x >= right:
            st[keep] = 'done'
            keep, right = j, y
            st[j] = 'keep'
        elif j == k and line == 13:
            st[j] = 'clash'
        elif y < right:
            st[keep] = 'del'
            keep, right = j, y
            st[j] = 'keep'
        else:
            st[j] = 'del'
    return st


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    iv = S.get('sorted_intervals')
    cv.text((x0 + 18, y0 + 4), 'sorted_intervals（按左端点排序；绿 = 正在考察的保留区间，红 = 删去）', 22, T['muted'], bold=True)
    if iv is None:
        cv.text((x0 + 18, y0 + 50), '（尚未排序）', 24, T['dim'])
        return
    st = _state(S, B)
    L, R = x0 + 150, x1 - 60
    unit = (R - L) / (HI - LO)

    def X(v):
        return L + (v - LO) * unit

    top, rowh = y0 + 56, min(70, (y1 - y0 - 190) / len(iv))
    axis_y = top + rowh * len(iv) + 16
    for v in range(LO, HI + 1):
        cv.line([(X(v), top - 10), (X(v), axis_y)], (36, 42, 52), 1)
        cv.text((X(v), axis_y + 8), v, 20, T['dim'], anchor='mt', mono=True)
    colors = {'keep': T['green'], 'done': (46, 98, 62), 'del': (90, 52, 52), 'cur': T['yellow'],
              'clash': T['orange'], 'todo': (70, 78, 90)}
    tags = {'keep': '保留', 'done': '保留', 'del': '删', 'cur': '?', 'clash': '重叠', 'todo': ''}
    tcol = {'keep': T['green'], 'done': T['green'], 'del': T['red'], 'cur': T['yellow'], 'clash': T['orange']}
    for j, (a, b) in enumerate(iv):
        y = top + j * rowh
        s = st[j]
        cv.rect((X(a), y + 8, X(b), y + rowh - 10), fill=colors[s], r=10)
        cv.text((X(a) + 10, y + rowh / 2 - 1), f'[{a},{b}]', 20, T['bg'] if s in ('keep', 'cur', 'clash') else T['text'],
                anchor='lm', bold=True, mono=True)
        cv.text((x0 + 60, y + rowh / 2 - 1), j, 18, T['dim'], anchor='rm', mono=True)
        if tags[s]:
            cv.text((x0 + 104, y + rowh / 2 - 1), tags[s], 21, tcol[s], anchor='mm', bold=True)
        if s == 'del':
            cv.line([(X(a) - 6, y + rowh / 2), (X(b) + 6, y + rowh / 2)], T['red'], 3)
        cv.rect((X(a) - 5, y + 4, X(a) + 5, y + rowh - 6), fill=T['cyan'], r=3)   # 排序关键字：左端点
    right = S.get('right')
    if isinstance(right, int):
        cv.dashed((X(right), top - 6), (X(right), axis_y + 34), T['pink'], 3)
        cv.text((X(right), axis_y + 38), f'right = {right}', 22, T['pink'], anchor='mt', bold=True)
    if 'res' in S:
        cv.text((x0 + 18, y1 - 34), f"已删除 res = {S['res']} 个", 24, T['red'], anchor='lm', bold=True)


def _cap_for(S, B, ret):
    if 'x' in B and (B.x, B.y) == (S.x, S.y):
        return '扫描结束'
    return f'考察下一个区间 `[{S.x}, {S.y}]`，和当前保留区间（右端点 `right = {S.right}`）比较'


def _cap_if(S, B, ret):
    if S.x >= S.right:
        touch = '（端点相接不算重叠）' if S.x == S.right else ''
        return (f'`x = {S.x} ≥ right = {S.right}`{touch}：不重叠；后面的起点只会更大，也不会和旧区间重叠'
                f' → ==不用再管它==')
    return f'`x = {S.x} < right = {S.right}`：两个区间重叠 → ==必须删一个=='


def _cap_min(S, B, ret):
    if S.y < B.right:
        return f'`min({B.right}, {S.y}) = {S.right}`：删掉右边界较大的==旧区间==，保留 `[{S.x}, {S.y}]`'
    return f'`min({B.right}, {S.y}) = {S.right}`：删掉右边界较大的==新区间== `[{S.x}, {S.y}]`，旧的继续保留'


CONFIG = dict(
    num=435, title='无重叠区间', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='按起点排序 · 重叠时删右边界大的',
    tags=['字节30天'],
    code='''
class Solution(object):
    def eraseOverlapIntervals(self, intervals):
        if not intervals:
            return 0

        sorted_intervals = sorted(intervals, key=lambda d:(d[0], d[1]))
        left, right = sorted_intervals[0]
        res = 0
        for x, y in sorted_intervals[1:]:
            if x >= right:
                left, right = x, y
            else:
                res += 1
                right = min(right, y)

        return res
''',
    call=f'Solution().eraseOverlapIntervals({INTERVALS})',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=620),
    ],
    watch=[('x', 'x', 'yellow'), ('y', 'y', 'yellow'), ('right', 'right', 'pink'), ('res', 'res', 'red')],
    captions={
        'if not intervals': '空列表直接返回 0；这里有 {len(intervals)} 个区间',
        'sorted_intervals = sorted': '按==起点==从小到大排序（起点相同再比终点）：青色小块 = 排序关键字',
        'left, right = sorted_intervals[0]': '先考察第一个区间 `[{left}, {right}]`',
        'res = 0': '`res`：删掉的区间个数',
        'for x, y in': _cap_for,
        'if x >= right': _cap_if,
        'left, right = x, y': '考察对象换成 `[{x}, {y}]`',
        'res += 1': '删一个：`res = {res}`',
        'right = min(right, y)': _cap_min,
        'return res': '一共删掉 =={ret}== 个区间',
    },
    cards=dict(
        one_liner='按起点排序扫描，两两重叠就删掉右边界较大的那个',
        complexity='时间 `O(n log n)`（排序），空间 `O(n)`（`sorted` 复制一份）',
        problem=['给一组区间 `intervals[i] = [start, end]`，求==最少移除几个==，使剩下的互不重叠',
                 '只在端点接触（如 `[1,2]` 和 `[2,3]`）==不算重叠==',
                 '示例：`[[1,2],[2,3],[3,4],[1,3]]` → `1`（移除 `[1,3]`）'],
        quote='若x[index + 1] < y[index]，说明两个区间重叠，必须删去其中某一个。为了尽量少删除区间，很明显应该==删去右边界较大的那一个区间==，保留另一个。',
        quote_src='—— yiduobo 题解原文',
        idea=['按起点排序，维护当前考察的区间（只需记右端点 `right`）',
              '下一个区间起点 `≥ right`：不重叠，后面的起点更大，旧区间可以扔掉不管',
              '起点 `< right`：重叠，删掉右边界大的，留下的那个对后面==威胁更小=='],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：重叠时只更新 `right = min(right, y)`，`left` 用不到，不用改',
                 '易错：端点相接不算重叠，判断用 `x >= right`',
                 '对比灵神：灵神按右端点排序，直接数最多能选几个；yiduobo 按起点排序，边扫边删',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
