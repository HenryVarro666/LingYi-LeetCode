CODE = '''
class Solution(object):
    def amountPainted(self, paint):

        def get(now, left, right, start, end):
            if s[now] == right - left + 1:
                return end - start + 1
            
            if left == start and right == end:
                return s[now]
            
            mid = (left + right) >> 1
            if end <= mid:
                return get(now + now + 1, left, mid, start, end)
            elif start > mid:
                return get(now + now + 2, mid + 1, right, start, end)
            else:
                return get(now + now + 1, left, mid, start, mid) + get(now + now + 2, mid + 1, right, mid + 1, end)
        
        def add(now, left, right, start, end):
            if s[now] == right - left + 1:
                return

            if left == start and right == end:
                s[now] = right - left + 1
                return
            
            mid = (left + right) >> 1
            if end <= mid:
                add(now + now + 1, left, mid, start, end)
            elif start > mid:
                add(now + now + 2, mid + 1, right, start, end)
            else:
                add(now + now + 1, left, mid, start, mid)
                add(now + now + 2, mid + 1, right, mid + 1, end)
            
            s[now] = s[now + now + 1] + s[now + now + 2]

        s = [0] * 131072
        res = []
        for start, end in paint:
            res.append(end - start - get(0, 0, 65535, start, end - 1))
            add(0, 0, 65535, start, end - 1)

        return res
'''
_LINES = CODE.strip('\n').split('\n')
_ADD0 = next(i for i, l in enumerate(_LINES) if 'def add' in l) + 1   # 1-based 行号
PAINT = [[1, 3], [2, 4]]
W = 9   # 画出 0..8


def _phase(S):
    return 'add' if (S.get('_line') or 0) >= _ADD0 else 'get'


def _op(S):
    if 'res' not in S or 'paint' not in S:
        return None
    k = len(S['res']) - (1 if _phase(S) == 'add' else 0)
    if not 0 <= k < len(S['paint']):
        return None
    return k


def _painted(S):
    k = _op(S)
    if k is None:
        k = len(S.get('res', []))
        base = S['paint'][:k] if 'paint' in S else []
    else:
        base = S['paint'][:k]
    cells = set()
    for a, b in base:
        cells.update(range(a, b))
    return cells


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cell = min(100, (x1 - x0 - 60) / W)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * W) / 2
    ys = y0 + 110
    ch = cell * 0.9
    cv.text((x0 + 18, y0 + 4), '数轴格子 0..8（蓝 = 之前已填充，黄框 = 本次区间，绿 = 本次新填）', 22, T['muted'], bold=True)
    painted = _painted(S)
    k = _op(S)
    cur = None
    if k is not None:
        a, b = S['paint'][k]
        cur = (a, b - 1)
    ph = _phase(S)
    for i in range(W):
        X = sx + i * cell
        old = i in painted
        inq = cur is not None and cur[0] <= i <= cur[1]
        fill = T['blue'] if old else T['panel2']
        if inq and ph == 'add' and S.get('_line', 0) >= _ADD0 + 6 and not old:
            fill = T['green']
        cv.rect((X + 4, ys, X + cell - 4, ys + ch), fill=fill, r=8, outline=T['border'])
        cv.text((X + cell / 2, ys + ch / 2), '■' if old else '', 28, T['bg'], anchor='mm')
        cv.text((X + cell / 2, ys + ch + 8), i, 20, T['dim'], anchor='mt', mono=True)
    if cur is not None:
        cv.rect((sx + cur[0] * cell + 1, ys - 8, sx + (cur[1] + 1) * cell - 1, ys + ch + 8), outline=T['yellow'], width=5, r=12)
        new = sum(1 for i in range(cur[0], cur[1] + 1) if i not in painted)
        cv.text((x0 + 30, ys + ch + 70),
                f"第 {k + 1} 次：paint = [{cur[0]}, {cur[1] + 1})，区间长 {cur[1] + 1 - cur[0]}，其中已填充 {cur[1] + 1 - cur[0] - new}，新区域 {new}",
                26, T['text'], bold=True)
    # 当前线段树结点
    if 'now' in S and 'left' in S and 'right' in S and S['right'] - S['left'] < 70000:
        l, r = S['left'], S['right']
        full = S['s'][S['now']] == r - l + 1
        cv.text((x0 + 30, ys + ch + 120), f"当前线段树结点 now={S['now']}：管 [{l}, {r}]，s[now]={S['s'][S['now']]}"
                + ('（整段已满）' if full else ''), 24, T['orange'], bold=True)
        if r - l + 1 <= W + 100:
            pass
    cv.text((x0 + 30, ys + ch + 170), f"已得到 res = {S.get('res')}", 26, T['green'], bold=True)


CONFIG = dict(
    num=2158, title='每天绘制新区域的数量', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='线段树 · 区间和 + 区间填充',
    tags=['灵神题单', '常用数据结构'],
    code=CODE,
    call=f'Solution().amountPainted({PAINT})',
    expect=[2, 1],
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='calls', h=260, hide=('amountPainted',)),
    ],
    watch=['start', 'end', ('res', 'res', 'green')],
    captions={
        'def get': '`get`：查询 `[start, end]` 里已经被填充的格子数',
        'def add': '`add`：把 `[start, end]` 全部填充',
        's = [0]': '`s[now]` 是线段树结点 now 区间里已填充的格子数，线段树管 `0..65535`',
        'res = []': '`res` 保存每天新绘制的数量',
        'for start, end in paint': '这一天画 `[{start}, {end})`，转成闭区间 `[{start}, {end - 1}]`',
        'res.append': '`res.append(区间长 − get(...))`：先用 `get` 查区间里已填充的格子数，新区域 = 区间长 − 已填充数',
        'add(0, 0, 65535': '查完了，再用 `add` 把这段区间填满',
        'if s[now] == right - left + 1': lambda S, B, r: ((f'结点 `[{S.left}, {S.right}]` 已经==全满==' if S.s[S.now] == S.right - S.left + 1
                                                         else f'结点 `[{S.left}, {S.right}]` 还没全满（`s = {S.s[S.now]}`），继续')),
        'return end - start + 1': '整段已填充 → 查询区间也全是已填充，直接返回区间长 `{ret}`',
        'if left == start and right == end': lambda S, B, r: (f'结点区间恰好等于查询区间 `[{S.start}, {S.end}]`' if (S.left == S.start and S.right == S.end)
                                                              else f'结点 `[{S.left}, {S.right}]` 比查询 `[{S.start}, {S.end}]` 大，需要往下分'),
        'return s[now]': '区间正好对上，已填充数就是 `s[now] = {ret}`',
        21: '这段本来就整段已满：不用再填，直接返回',
        25: '这段填满了，返回上一层',
        's[now] = right - left + 1': '区间正好对上：整段填满，`s[now]` = =={s[now]}==。以后这段再不会变',
        'mid = ': '中点 `mid = {mid}`',
        'if end <= mid': lambda S, B, r: (f'`end = {S.end} <= mid = {S.mid}`：整个区间在左半边' if S.end <= S.mid else f'`end = {S.end} > mid = {S.mid}`：不全在左半边'),
        'elif start > mid': lambda S, B, r: (f'`start = {S.start} > mid = {S.mid}`：整个区间在右半边' if S.start > S.mid else f'`start = {S.start} <= mid = {S.mid}`：跨过中点，要拆成两段'),
        'return get(now + now + 1, left, mid, start, end)': '只用查左孩子',
        'return get(now + now + 2': '只用查右孩子',
        'return get(now + now + 1, left, mid, start, mid) +': '跨过中点：左右各查一段，==相加==',
        'add(now + now + 1, left, mid, start, end)': '只往左孩子填充',
        'add(now + now + 2, mid + 1, right, start, end)': '只往右孩子填充',
        'add(now + now + 1, left, mid, start, mid)': '跨过中点：左半边填 `[{start}, {mid}]`',
        'add(now + now + 2, mid + 1, right, mid + 1, end)': '右半边填 `[{mid + 1}, {end}]`',
        's[now] = s[now + now + 1]': '回溯更新：`s[now]` = 左孩子 + 右孩子 = =={s[now]}==',
        'return res': '每天的新区域数：`{res}`',
    },
    skip=['mid = (left + right)', 'if end <= mid', 'elif start > mid', 'return get(now + now + 1, left, mid, start, end)',
          'return get(now + now + 2', 'add(now + now + 1, left, mid, start, end)', 'add(now + now + 2, mid + 1, right, start, end)',
          's[now] = s[now + now + 1]', 'if left == start and right == end'],
    max_steps=66,
    cards=dict(
        one_liner='线段树记录每段已填充数，整段满了就不再下探',
        complexity='时间 `O(n log C)`，空间 `O(C)`（C = 值域）',
        problem=['依次给出一天一个区间 `[start, end)`，每天要把区间涂满',
                 '每天返回这个区间里==新涂的格子数==（已涂过的不算）',
                 '示例：`[[1,4],[4,7],[5,8]]` → `[3,3,1]`',
                 '本视频：`[[1,3],[2,4]]` → `[2,1]`',
                 '题面库里没有，题意按 LeetCode 2158 整理'],
        quote='题目中的两种操作实际上就是区间和以及区间赋值操作，另外，由于一旦某个区间被填充后，后续的所有操作都无法影响到该区间，因此在具体处理时可以利用区间和以及区间长度很方便地实现区间填充。',
        quote_src='—— yiduobo 题解原文',
        idea=['`s[now]` = 结点区间内已填充的格子数；`s[now] == 区间长` 说明整段已满',
              '`get` 先查询区间内已填充的数量，新区域 = 区间长 − 已填充数',
              '`add` 填充：整段满了就停止下探；回溯时 `s[now] = 左孩子 + 右孩子`'],
        summary=['时间 `O(n log C)`，空间 `O(C)`，`C = 65536`，开 `131072` 的数组',
                 '区间是 `[start, end)`，传给线段树时要用 `end - 1`',
                 '因为只填不擦，所以不需要懒标记，用 `s[now] == 区间长` 就够了',
                 '原文代码在 Python 3 可直接运行；本视频示例 2 天、坐标 0..8，线段树仍管 `0..65535`，只画出前 9 格'],
    ),
)
