INTERVALS = [[1, 3], [2, 4], [3, 5], [1, 2], [4, 7], [5, 6]]   # 互不相同，便于从 (l, r) 反查下标
LO, HI = 1, 7


def _state(S, B):
    """返回 (当前下标 k 或 None, 每个区间的状态列表)；状态：chosen / skip / cur / todo"""
    iv = S.get('intervals') or INTERVALS
    line = S.get('_line')
    n = len(iv)
    if 'l' not in S or line == 10:
        k = n if 'l' in S else 0
    elif line == 6 and 'l' in B and (B['l'], B['r']) == (S['l'], S['r']):
        k = n          # 循环结束
    else:
        k = iv.index([S['l'], S['r']])
    st, pre = [], float('-inf')
    for j in range(n):
        if j < k:
            ok = iv[j][0] >= pre
            st.append('chosen' if ok else 'skip')
            if ok:
                pre = iv[j][1]
        elif j == k:
            st.append('chosen' if line in (8, 9) else 'cur')
        else:
            st.append('todo')
    return (k if k < n else None), st


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    iv = S.get('intervals') or INTERVALS
    k, st = _state(S, B)
    L, R = x0 + 150, x1 - 60
    unit = (R - L) / (HI - LO)

    def X(v):
        return L + (v - LO) * unit

    sorted_now = True   # 第一步就是排序，之后一直是排好序的
    cv.text((x0 + 18, y0 + 4), 'intervals（已按右端点排序；绿 = 选，红 = 删，黄 = 正在看）', 22, T['muted'], bold=True)
    top, rowh = y0 + 56, min(70, (y1 - y0 - 190) / len(iv))
    axis_y = top + rowh * len(iv) + 16
    for v in range(LO, HI + 1):
        cv.line([(X(v), top - 10), (X(v), axis_y)], (36, 42, 52), 1)
        cv.text((X(v), axis_y + 8), v, 20, T['dim'], anchor='mt', mono=True)
    colors = {'chosen': T['green'], 'skip': (90, 52, 52), 'cur': T['yellow'], 'todo': (70, 78, 90)}
    tags = {'chosen': '选', 'skip': '删', 'cur': '?', 'todo': ''}
    for j, (a, b) in enumerate(iv):
        y = top + j * rowh
        c = colors[st[j]]
        cv.rect((X(a), y + 8, X(b), y + rowh - 10), fill=c, r=10)
        cv.text((X(a) + 10, y + rowh / 2 - 1), f'[{a},{b}]', 20, T['bg'] if st[j] in ('chosen', 'cur') else T['text'],
                anchor='lm', bold=True, mono=True)
        cv.text((x0 + 70, y + rowh / 2 - 1), j, 18, T['dim'], anchor='rm', mono=True)
        if tags[st[j]]:
            cv.text((x0 + 108, y + rowh / 2 - 1), tags[st[j]], 22,
                    {'chosen': T['green'], 'skip': T['red'], 'cur': T['yellow']}[st[j]], anchor='mm', bold=True)
        if st[j] == 'skip':
            cv.line([(X(a) - 6, y + rowh / 2), (X(b) + 6, y + rowh / 2)], T['red'], 3)
        if sorted_now:
            cv.rect((X(b) - 5, y + 4, X(b) + 5, y + rowh - 6), fill=T['orange'], r=3)   # 排序关键字：右端点
    pre = S.get('pre_r')
    if isinstance(pre, (int, float)) and pre != float('-inf'):
        cv.dashed((X(pre), top - 6), (X(pre), axis_y + 34), T['pink'], 3)
        cv.text((X(pre), axis_y + 38), f'pre_r = {pre}', 22, T['pink'], anchor='mt', bold=True)
    elif 'pre_r' in S:
        cv.text((L, axis_y + 38), 'pre_r = -∞', 22, T['pink'], anchor='mt', bold=True)
    if 'ans' in S:
        cv.text((x0 + 18, y1 - 34), f"已选 ans = {S['ans']} 个互不重叠的区间", 24, T['green'], anchor='lm', bold=True)


def _cap_for(S, B, ret):
    if 'l' in B and (B.l, B.r) == (S.l, S.r):
        return '所有区间看完'
    return f'下一个区间 `[{S.l}, {S.r}]`（右端点从小到大）'


def _cap_if(S, B, ret):
    if S.l >= S.pre_r:
        pre = '-∞' if S.pre_r == float('-inf') else S.pre_r
        touch = '（只在端点接触，==不算重叠==）' if S.l == S.pre_r else ''
        return f'`l = {S.l} ≥ pre_r = {pre}`：和已选的不相交{touch} → ==选它=='
    return f'`l = {S.l} < pre_r = {S.pre_r}`：和上一个选的区间重叠 → 不选（要移除）'


CONFIG = dict(
    num=435, title='无重叠区间', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='按右端点排序 · 选最多不相交区间',
    tags=['字节30天'],
    code='''
class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda x: x[1])
        ans = 0
        pre_r = -inf
        for l, r in intervals:
            if l >= pre_r:
                ans += 1
                pre_r = r
        return len(intervals) - ans
''',
    call=f'Solution().eraseOverlapIntervals({INTERVALS})',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=620),
    ],
    watch=[('l', 'l', 'yellow'), ('r', 'r', 'yellow'), ('pre_r', 'pre_r', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'intervals.sort': '按==右端点==从小到大排序：最先结束的区间排最前（橙色小块 = 排序关键字）',
        'ans = 0': '`ans`：最多能选几个互不重叠的区间',
        'pre_r = -inf': '`pre_r`：上一个选的区间的右端点，初始 `-∞`（第一个区间一定能选）',
        'for l, r in': _cap_for,
        'if l >= pre_r': _cap_if,
        'ans += 1': '`ans = {ans}`',
        'pre_r = r': '`pre_r = {pre_r}`：后面的区间左端点 `≥ {pre_r}` 才能选',
        'return len': '最多选 `{ans}` 个 → 至少移除 `{len(intervals)} − {ans}` = =={ret}== 个',
    },
    cards=dict(
        one_liner='反过来求最多能留多少个不相交区间；每次选右端点最小的',
        complexity='时间 `O(n log n)`（排序），空间 `O(1)`',
        problem=['给一组区间 `intervals[i] = [start, end]`，求==最少移除几个==，使剩下的互不重叠',
                 '只在端点接触（如 `[1,2]` 和 `[2,3]`）==不算重叠==',
                 '示例：`[[1,2],[2,3],[3,4],[1,3]]` → `1`（移除 `[1,3]`）'],
        quote='我们可以选所有区间中右端点最小的区间（记作 A）。为什么？因为==在任意一种选法中，都可以把最左边的区间，替换成 A==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['改为计算最多能选多少个互不重叠的区间，没选的就是要移除的',
              'A 结束得最早，换上它不会和其他已选区间相交 → 选 A 不亏',
              '按右端点排序后，下一个能选的是第一个 `左端点 ≥ pre_r` 的区间'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`（不计排序栈）',
                 '易错：端点相接不算重叠，判断用 `l >= pre_r`（不是 `>`）',
                 '为什么按右端点排序：选完 A 后，左端点 `< A 的右端点` 的区间都与 A 相交',
                 '同类：452 用最少数量的箭引爆气球、646 最长数对链'],
    ),
)
