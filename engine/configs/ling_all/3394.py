def _cur(S):
    try:
        return S['intervals'].index((S['l'], S['r']))
    except Exception:
        return None


def _axis(S):
    rs = S.get('rectangles')
    iv = S.get('intervals')
    if rs is None or iv is None:
        return ''
    if sorted(iv) == sorted((a[0], a[2]) for a in rs):
        return '竖切：矩形看成 x 区间 [start_x, end_x]'
    return '横切：矩形看成 y 区间 [start_y, end_y]'


def _txt(S):
    if 'cnt' not in S:
        return '竖切只看横坐标、横切只看纵坐标 → 各自变成「合并区间」，数合并后有几段'
    base = f'{_axis(S)}　`cnt = {S["cnt"]}`，`max_r = {S["max_r"]}`'
    if 'l' in S and S['l'] is not None and _cur(S) is not None:
        base += f'　当前 `[{S["l"]}, {S["r"]}]`'
    return base


def _if(S, B, ret):
    l, mr = B.l, B.max_r
    if l >= mr:
        return f'`l = {l} ≥ max_r = {mr}`：和前面的区间不重叠（贴着也行）→ ==新区间==，`cnt` 加一'
    return f'`l = {l} < max_r = {mr}`：和当前合并区间重叠，不能在这里切 → 并入'


def _upd(S, B, ret):
    if B.r > B.max_r:
        return f'`r = {B.r} > max_r = {B.max_r}`：更新右端点最大值 → =={S.max_r}=='
    return f'`r = {B.r} ≤ max_r = {B.max_r}`：被包含，右端点不变'


CONFIG = dict(
    num=3394, title='判断网格图能否被切割成块', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='投影成区间 + 合并区间计数',
    tags=['灵神题单', '贪心算法', '难度分 1916'],
    code='''
class Solution:
    def check(self, intervals: List[Tuple[int, int]]) -> bool:
        intervals.sort(key=lambda p: p[0])  # 按照左端点从小到大排序
        cnt = max_r = 0
        for l, r in intervals:
            if l >= max_r:  # 新区间
                cnt += 1
            if r > max_r:
                max_r = r  # 更新右端点最大值（手写 if 效率更高）
        return cnt >= 3  # 也可以在循环中提前退出，但是慢一些

    def checkValidCuts(self, _: int, rectangles: List[List[int]]) -> bool:
        return self.check([(sx, ex) for sx, _, ex, _ in rectangles]) or \\
               self.check([(sy, ey) for _, sy, _, ey in rectangles])
''',
    call='Solution().checkValidCuts(5, [[1,0,5,2],[0,2,2,4],[3,2,5,3],[0,4,4,5]])',
    expect=True,
    views=[
        dict(type='text', fn=_txt, size=24),
        dict(type='intervals', var='intervals', pointer=_cur, label='数轴：矩形在这个方向上的投影（黄 = 当前）', h=430),
    ],
    watch=[('cnt', 'cnt', 'green'), ('max_r', 'max_r', 'orange'), ('l', 'l', 'blue'), ('r', 'r', 'pink')],
    captions={
        'intervals.sort': '按左端点排序：`{intervals}`',
        'cnt = max_r = 0': '`cnt` = 合并后的区间数，`max_r` = 已见区间的最大右端点',
        'for l, r in intervals': lambda S, B, rt: ('看下一个投影 `[{}, {}]`'.format(S.l, S.r) if 'l' not in B or B.l != S.l or B.r != S.r else '全部看完'),
        'if l >= max_r': _if,
        'cnt += 1': '`cnt` → =={cnt}==',
        'if r > max_r': lambda S, B, rt: '`r = {}` 与 `max_r = {}` 比较 → {}'.format(S.r, S.max_r, '更大，要更新' if S.r > S.max_r else '不更大，不用更新'),
        'max_r = r': '`max_r` → =={max_r}==',
        'return cnt >= 3': '合并后有 `cnt = {cnt}` 段，`≥ 3` → ==' + '{ret}' + '==（至少 3 段才能切出 3 块）',
        'self.check([(sx': lambda S, B, rt: ('先试竖切：只取每个矩形的 `(start_x, end_x)`' if rt is None else '竖切或横切有一个能切成 3 块就行 → 返回 =={}=='.format(rt)),
        'self.check([(sy': '竖切不行，再试横切：只取 `(start_y, end_y)`',
    },
    cards=dict(
        one_liner='竖切只看 x、横切只看 y：投影成区间，合并后 ≥ 3 段就能切',
        complexity='时间 `O(m log m)`，空间 `O(m)`',
        problem=['`n×n` 网格里有若干不重叠的矩形，判断能否用==两条同向的线==切成 3 块',
                 '每块至少含一个矩形，且每个矩形只属于一块（不能被线穿过）',
                 '示例 1：`n=5`，4 个矩形 → `true`（在 `y=2` 和 `y=4` 横切）',
                 '本视频就用示例 1：竖切不行，横切可以'],
        quote='竖切的时候，答案与纵坐标，也就是矩形的高无关，我们可以把每个矩形视作一个区间。问题变成把这 n 个区间合并后，区间的个数是否 ≥ 3。',
        quote_src='—— 灵茶山艾府题解',
        idea=['线不能穿过矩形 → 投影区间有重叠的必须在同一块',
              '先合并区间（模板：56 题），数一数合并后有 `cnt` 段',
              '`cnt >= 3` 就能在段与段之间切两刀；竖切、横切各做一次'],
        summary=['时间 `O(m log m)`，瓶颈在排序',
                 '判断是 `l >= max_r`（不是 `>`）：矩形边贴着边，切线可以落在共同边上',
                 '`max_r` 从 `0` 开始，所以第一个区间（`l ≥ 0`）一定算新区间',
                 '返回 `cnt >= 3`；题解说可以提前退出，但更慢',
                 '与 56 题的区别：这里端点相接不合并（按坐标线切，不是整数点）'],
    ),
)
