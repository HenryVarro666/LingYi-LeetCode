IV = [[1, 2], [2, 3], [2, 4], [4, 5]]
LO, HI = 0, 6


def _cur(S):
    if 'start' not in S or 'intervals' not in S:
        return None
    for k, t in enumerate(S['intervals']):
        if t[0] == S['start'] and t[1] == S['end']:
            return k
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '数轴：黄 = 当前区间，绿 = 栈里已选的时间点（合并后的区间）', 22, T['muted'], bold=True)
    L, R = x0 + 60, x1 - 60
    unit = (R - L) / (HI - LO + 1)

    def X(v):
        return L + (v - LO) * unit
    top = y0 + 56
    axis = y1 - 50
    for v in range(LO, HI + 1):
        cv.line([(X(v) + unit / 2, top), (X(v) + unit / 2, axis)], (36, 42, 52), 1)
        cv.text((X(v) + unit / 2, axis + 8), v, 22, T['dim'], anchor='mt', mono=True)
    # 已处理 / 当前区间
    iv = S.get('intervals') or IV
    k = _cur(S)
    rowh = 34
    for j, (a, b) in enumerate(iv):
        y = top + j * rowh
        if k is None or j > k:
            col = (70, 78, 90)
        elif j == k:
            col = T['yellow']
        else:
            col = (96, 110, 130)
        cv.rect((X(a) + 4, y, X(b) + unit - 4, y + 22), fill=col, r=11)
        cv.text((X(a) - 2, y + 11), f'[{a},{b}]', 17, T['muted'], anchor='rm', mono=True)
    # 栈中区间
    y = top + len(iv) * rowh + 18
    cv.text((L - 52, y + 24), 'st', 24, T['green'], anchor='rm', bold=True, mono=True)
    for (l, r, s) in S.get('st', []):
        if r < 0:
            continue
        cv.rect((X(l) + 4, y, X(r) + unit - 4, y + 48), fill=T['green'], r=10, alpha=200)
        cv.text(((X(l) + X(r) + unit) / 2, y + 24), f'[{l},{r}]', 24, T['bg'], anchor='mm', bold=True, mono=True)
    if k is not None and 'd' in S and S['_line'] not in (8,):
        pass


CONFIG = dict(
    num=757, title='设置交集大小至少为2', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='右端点排序 + 栈维护已选点 + 二分',
    tags=['灵神题单·贪心与思维', '贪心算法', '难度分 2379'],
    code='''
class Solution:
    def intersectionSizeTwo(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda interval: interval[1])
        # 栈中保存闭区间左右端点，栈底到栈顶的区间长度的和
        st = [(-2, -2, 0)]  # 哨兵，保证不和任何区间相交
        for start, end in intervals:
            _, r, s = st[bisect_left(st, (start,)) - 1]
            d = 2 - (st[-1][2] - s)  # 去掉运行中的时间点
            if start <= r:  # start 在区间 st[i] 内
                d -= r - start + 1  # 去掉运行中的时间点
            if d <= 0:
                continue
            while end - st[-1][1] <= d:  # 剩余的 d 填充区间后缀
                l, r, _ = st.pop()
                d += r - l + 1  # 合并区间
            st.append((end - d + 1, end, st[-1][2] + d))
        return st[-1][2]
''',
    call=f'Solution().intersectionSizeTwo({IV})',
    expect=5,
    views=[
        dict(type='stack', var='st', label='st：(左端点, 右端点, 前缀长度和)', h=150, fmt=lambda x: str(x)),
        dict(type='custom', draw=_draw, h=420),
    ],
    watch=[('start', 'start', 'blue'), ('end', 'end', 'cyan'), ('d', 'd', 'orange'), ('选点数', 'st[-1][2]', 'green')],
    captions={
        'intervals.sort': '==按右端点从小到大排序==：后面的区间要么和当前不相交，要么只盖住它的==后缀==',
        'st = [': '栈里放已选时间点合并成的闭区间，每项带「到此为止一共选了几个点」；哨兵 `(-2,-2,0)` 不和任何区间相交',
        'for start, end': '取出区间 `[{start}, {end}]`，它至少要含 2 个已选点',
        '_, r, s =': '二分栈：找到包含/最靠近 `start` 左侧的那一项，`r = {r}`，`s = {s}`（`start` 之前已选点数）',
        'd = 2 - (': '区间 `[{start}, {end}]` 里已有 `{st[-1][2] - s}` 个已选点，还差 ==d = {d}== 个',
        'd -= r - start + 1': '`start` 落在栈中区间内，要减去区间内 `[{start}, {r}]` 这 `{r - start + 1}` 个点 → `d = {d}`',
        'if start <= r': lambda S, B, ret: (f'`start = {S.start} <= r = {S.r}` → start 落在已选区间里，里面的点也算' if S.start <= S.r
                                            else f'`start = {S.start} > r = {S.r}` → 已选区间都在 start 左边，不用再减'),
        'if d <= 0': lambda S, B, ret: (f'`d = {S.d} <= 0`：已有点够了，不用新增，`continue`' if S.d <= 0
                                        else f'`d = {S.d} > 0`：还差 {S.d} 个点，要在区间右边补'),
        'while end - st[-1][1] <= d': lambda S, B, ret: (
            f'`end - st[-1][1] = {S.end - S.st[-1][1]} <= d = {S.d}`：补的 {S.d} 个点会和栈顶连成一片区间 → ==合并=='
            if S.end - S.st[-1][1] <= S.d else f'`end - st[-1][1] = {S.end - S.st[-1][1]} > d = {S.d}`：补的点和栈顶接不上 → 不用合并'),
        'l, r, _ = st.pop()': '弹出栈顶 `[{l}, {r}]`',
        'd += r - l + 1': '栈顶 `{r - l + 1}` 个点并入新区间：`d` 加上它 → ==d = {d}==',
        'st.append': '把 `[{end - d + 1}, {end}]` 这 `{d}` 个点放在区间==最右边==入栈；累计选点 `{st[-1][2]}`',
        'return st[-1][2]': '栈顶记录的前缀和就是最少选点数：=={ret}==',
    },
    cards=dict(
        one_liner='右端点排序，缺的点补在区间最右边，用栈合并成大区间',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每个区间 `[start, end]` 至少要有 ==2 个整数== 属于集合 `nums`',
                 '求集合最小大小',
                 '本视频：`[[1,2],[2,3],[2,4],[4,5]]` → `5`'],
        quote='把 2 改成 k 怎么做？更一般地，每个区间要包含的数字个数各有不同，怎么做？这题是 2589. 完成所有任务的最少时间。',
        quote_src='—— 灵茶山艾府题解',
        idea=['这题就是 2589 的特例：每个区间的 `d` 恒为 2',
              '右端点排序后，缺的点==尽量放在区间后缀==，后面的区间更容易蹭到',
              '补点总是从右往左，所以已选点可合并成区间，用栈保存，并存==前缀长度和==',
              '栈中二分 `start`，前缀和相减就能 `O(log n)` 数出区间内已选点数'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '栈顶记录的前缀和 `st[-1][2]` 就是已选点总数',
                 '`d` 先减区间里已有的点，再减 `start` 所在区间的部分，小心不要重复数',
                 '合并条件 `end - st[-1][1] <= d`：补的后缀会碰到栈顶就并起来',
                 '换成 `2 → k`，或每个区间需求不同，这份代码稍改即可（即 2589 / LCP 32）'],
    ),
)
