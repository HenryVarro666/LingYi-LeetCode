class _Out:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, S):
        return self.fn(S)

    def __str__(self):
        return '没被覆盖（保留）'


def _kept(S, n):
    out, mx = [], 0
    for a, b in S['intervals']:
        if b > mx:
            out.append([a, b])
            mx = b
    return out[:n]


def _cur(S):
    if '_' in S and 'r' in S and [S['_'], S['r']] in S['intervals']:
        return S['intervals'].index([S['_'], S['r']])
    return None


def _txt(S):
    if 'max_right' not in S:
        return '先排序：左端点升序，==左端点相同时右端点降序==，大区间排在小区间前面'
    if 'r' not in S:
        return '`max_right = 0`：还没有遍历过任何区间'
    return f"当前 `[{S['_']}, {S['r']}]`，已遍历区间的最大右端点 `max_right = {S['max_right']}`，保留 =={S['ans']}== 个"


CONFIG = dict(
    num=1288, title='删除被覆盖区间', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='左端点升序 · 维护最大右端点',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution:
    def removeCoveredIntervals(self, intervals: list[list[int]]) -> int:
        # 按区间左端点从小到大排序
        # 区间左端点相同时，按区间右端点从大到小排序，这样会先遍历大区间，再遍历被大区间覆盖的小区间
        intervals.sort(key=lambda a: (a[0], -a[1]))

        ans = 0
        max_right = 0  # 已遍历区间中的最大右端点
        for _, r in intervals:
            # 由于区间左端点是从小到大排序的，已遍历区间的左端点都 <= 当前区间的左端点
            # 如果当前区间右端点 <= max_right，说明当前区间被另一个区间覆盖，否则没被覆盖
            if r > max_right:
                max_right = r
                ans += 1  # 当前区间没被覆盖
        return ans
''',
    call='Solution().removeCoveredIntervals([[1,4],[2,5],[2,8],[3,6],[7,9]])',
    expect=3,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='intervals', var='intervals', out=_Out(lambda S: _kept(S, S.get('ans', 0))), pointer=_cur,
             label='intervals（蓝 = 待看，黄 = 当前，绿 = 保留）', h=420),
    ],
    watch=[('max_right', 'max_right', 'cyan'), ('r', 'r', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'intervals.sort': '排序：左端点小的在前；左端点相同，==右端点大的在前==。`[2,8]` 排在 `[2,5]` 前面',
        'ans = 0': '`ans` 统计没被覆盖的区间数',
        'max_right = 0': '`max_right` 记录已遍历区间的最大右端点，初始 `0`',
        'for _, r in intervals': '遍历到区间 `[{_}, {r}]`：左端点只升不降，只需比较右端点',
        'if r > max_right': lambda S, B, ret: (f'`r = {S["r"]} > max_right = {S["max_right"]}`：没有更靠前的区间能盖住它 → ==保留==' if S['r'] > S['max_right']
                                                else f'`r = {S["r"]} <= max_right = {S["max_right"]}`：被前面某个区间盖住 → ==删除==，不计数'),
        'max_right = r': '右端点更靠右了：`max_right` → {max_right}',
        'ans += 1': '保留数 `ans` → {ans}',
        'return ans': '剩余区间 `{ans}` 个',
    },
    cards=dict(
        one_liner='左端点升序扫描，只需比右端点',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['`[a,b)` 被 `[c,d)` 覆盖：`c <= a` 且 `b <= d`',
                 '删掉所有被覆盖的区间，返回剩余个数',
                 '本视频：`[[1,4],[2,5],[2,8],[3,6],[7,9]]` → `3`'],
        quote='如果按照区间左端点从小到大的顺序遍历 intervals，那么遍历过的区间的左端点都 <= 当前区间的左端点，这样就只需比较区间右端点的大小。',
        quote_src='—— 灵茶山艾府题解',
        idea=['两个约束不好处理：排序先把 `c <= a` 变成自动成立',
              '维护遍历过的最大右端点 `max_right`，当前 `r <= max_right` 就是被覆盖',
              '左端点相同时要==先大后小==，否则小区间会被误判为没被覆盖'],
        summary=['时间 `O(n log n)`（瓶颈在排序），空间 `O(1)`',
                 '易错点：左端点相同时右端点要降序，否则 `[2,5]` 排在 `[2,8]` 前会多算一个',
                 '题目保证区间互不相同，所以不会有完全重复的区间',
                 '同类：区间贪心题单（合并区间、最长数对链等）'],
    ),
)
