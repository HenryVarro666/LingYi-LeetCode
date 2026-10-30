POINTS = [[10, 16], [2, 8], [1, 6], [7, 12], [6, 7]]
LO, HI = 0, 17
ARROW_COLORS = ['pink', 'cyan', 'purple', 'orange']


def _cur_idx(S):
    pts = S.get('points') or []
    if 'start' not in S:
        return None
    for k, p in enumerate(pts):
        if p[0] == S['start'] and p[1] == S['end']:
            return k
    return None


def _arrows(S):
    """已经放下的点（箭）：当前区间之前的贪心结果 + 当前 pre"""
    pts = S.get('points') or []
    idx = _cur_idx(S)
    if idx is None:
        idx = 0
    out, pre = [], float('-inf')
    for a, b in pts[:idx]:
        if a > pre:
            pre = b
            out.append(b)
    p = S.get('pre')
    if isinstance(p, int) and p not in out:
        out.append(p)
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    L, R = x0 + 170, x1 - 50

    def X(v):
        return L + (v - LO) / (HI - LO) * (R - L)
    pts = S.get('points') or POINTS
    cv.text((x0 + 18, y0 + 4), 'points（已按右端点排序；颜色 = 被哪个点射中）', 24, T['muted'], bold=True)
    idx = _cur_idx(S)
    arrows = _arrows(S) if 'pre' in S else []
    top = y0 + 56
    rowh = min(80, (y1 - top - 110) / max(1, len(pts)))
    bottom = top + rowh * len(pts)
    # 箭（竖直虚线）
    for k, p in enumerate(arrows):
        c = T[ARROW_COLORS[k % len(ARROW_COLORS)]]
        cv.dashed((X(p), top - 10), (X(p), bottom + 6), c, 3, 10, 6)
        cv.text((X(p), bottom + 12), f'点{k + 1}：x={p}', 20, c, anchor='mt', bold=True)
    for k, (a, b) in enumerate(pts):
        y = top + k * rowh
        hit = next((j for j, p in enumerate(arrows) if a <= p <= b), None)
        ended = S.get('_line') == 6 and (B.get('start'), B.get('end')) == (S.get('start'), S.get('end'))
        done = idx is not None and (k < idx or (k == idx and (S.get('_line') != 6 or ended)))
        if hit is not None and done:
            c = T[ARROW_COLORS[hit % len(ARROW_COLORS)]]
        else:
            c = (95, 105, 118)
        cv.rect((X(a), y + 8, X(b), y + rowh - 12), fill=c, r=10)
        if k == idx:
            cv.rect((X(a) - 4, y + 4, X(b) + 4, y + rowh - 8), outline=T['yellow'], width=4, r=12)
        cv.text((x0 + 30, y + rowh / 2 - 2), f'[{a},{b}]', 22, T['yellow'] if k == idx else T['text'], anchor='lm', mono=True)
    ay = y1 - 34
    cv.line([(L, ay), (R, ay)], T['border'], 2)
    for v in range(LO, HI + 1):
        if v % 2 == 0:
            cv.line([(X(v), ay - 4), (X(v), ay + 4)], T['dim'], 2)
            cv.text((X(v), ay + 8), str(v), 18, T['dim'], anchor='mt')


def _info(S):
    if 'pre' not in S:
        return '先排序：==按右端点==从小到大'
    p = S['pre']
    ps = '-∞' if p == float('-inf') else str(p)
    if 'start' in S and S.get('_line') in (6, 7, 8, 9):
        return f"当前区间 `[{S['start']},{S['end']}]`，上一个点 `pre = {ps}`，已放 `ans = {S['ans']}` 个点"
    return f"上一个点 `pre = {ps}`，已放 `ans = {S['ans']}` 个点"


def _if_cap(S, B, ret):
    st, pre = S.start, B.pre
    ps = '-∞' if pre == float('-inf') else pre
    if st > pre:
        return f'`start = {st} > pre = {ps}`：上一个点在区间==左边==，射不中它 → 必须新放一个点'
    return f'`start = {st} ≤ pre = {ps} ≤ end = {S.end}`（右端点有序）→ 已被点 `{ps}` 射中，==跳过=='


def _for_cap(S, B, ret):
    if 'start' in S and (B.get('start'), B.get('end')) != (S.start, S.end):
        return f'下一个区间 `[{S.start}, {S.end}]`'
    return '所有区间都处理完了'


CONFIG = dict(
    num=452, title='用最少数量的箭引爆气球', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='区间选点 · 按右端点排序',
    tags=['面试经典150'],
    code='''
class Solution:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        points.sort(key=lambda p: p[1])  # 按照右端点从小到大排序
        ans = 0
        pre = -inf
        for start, end in points:
            if start > pre:  # 上一个点在区间左边
                ans += 1
                pre = end  # 在区间的最右边放一个点
        return ans
''',
    call=f'Solution().findMinArrowShots({POINTS})',
    expect=2,
    views=[
        dict(type='text', h=56, fn=_info, size=26),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('start', 'start', 'yellow'), ('end', 'end', 'yellow'), ('pre', 'pre', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'points.sort': '按照右端点从小到大排序：`{points}`',
        'ans = 0': '`ans` 统计放了几个点（几支箭）',
        'pre = -inf': '`pre` 是上一个点的位置，一开始没有点：`pre = -∞`',
        'for start, end': _for_cap,
        'if start > pre': _if_cap,
        'ans += 1': '放一个新点：`ans = {ans}`',
        'pre = end': '点放在==当前区间的右端点== `x = {pre}`：在不漏掉它的前提下尽量靠右，能顺带射中更多区间',
        'return ans': '最少需要 =={ret}== 个点（支箭）',
    },
    cards=dict(
        one_liner='按右端点排序，每个点都放在第一个没被射中的区间的右端点',
        complexity='时间 `O(n log n)`（排序），空间 `O(1)`',
        problem=['气球 `points[i] = [x_start, x_end]` 是数轴上的区间',
                 '在 `x` 处竖直射箭，能引爆所有 `x_start ≤ x ≤ x_end` 的气球，求==最少箭数==',
                 '示例：`[[10,16],[2,8],[1,6],[7,12]]` → `2`；本视频再加一个 `[6,7]`'],
        before=[dict(heading='题意转化：区间选点', lines=[
            '把区间画在数轴上，==最少放多少个点==，使每个区间都至少包含一个点？',
            '先想：==第一个点（最左边的点）放在哪最好？==',
            '例如 `[[1,6],[6,7],[2,8],[7,10]]`：放在 `x=6` 能满足三个区间，放 `x=7` 就漏掉 `[1,6]`'])],
        quote='把区间按照右端点从小到大排序，这样==第一个点就放在第一个区间的右端点处==。去掉包含第一个点的区间后，第二个点就放在剩余区间的第一个区间的右端点处。依此类推。',
        quote_src='—— 灵茶山艾府题解',
        idea=['右端点最小的区间必须被射中，点越靠右越好 → 就放在它的右端点',
              '之后 `start ≤ pre` 的区间都已包含这个点（因为 `pre ≤ end`），跳过',
              '遇到 `start > pre` 时，问题变成==规模更小的同一个问题==，重复即可'],
        result='运行结束，返回 `2`：点 `x=6` 射中前三个，点 `x=12` 射中后两个',
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`（忽略排序栈）',
                 '==按右端点排序==，不是左端点；端点相等（`start == pre`）也算射中',
                 'C++ 等语言注意 `start` 可能是 32 位最小值，`pre` 用 64 位或取第一个区间右端点',
                 '同类：区间选点 / 无重叠区间（435）都是按右端点贪心'],
    ),
)
