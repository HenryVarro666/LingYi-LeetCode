def _cur(S):
    if 'l' in S and 'r' in S and [S['l'], S['r']] in S['ranges']:
        return S['ranges'].index([S['l'], S['r']])
    return None


def _txt(S):
    if 'max_r' not in S:
        return '先按左端点排序，再扫描：每个「大区间」有 2 种分组方案 → 答案是 ==2^m=='
    if 'l' not in S:
        return f'`m = {S["m"]}`，`max_r = {S["max_r"]}`（还没有任何大区间）'
    return f'已有大区间 `m = {S["m"]}` 个，当前大区间右端点 `max_r = {S["max_r"]}`；看区间 `[{S["l"]}, {S["r"]}]`'


def _if(S, B, ret):
    l, mr = B.l, B.max_r
    if l > mr:
        return f'`l = {l} > max_r = {mr}`：==不相交==。左端点已排序，后面也碰不到之前的区间 → 产生新大区间'
    return f'`l = {l} ≤ max_r = {mr}`：==有交集==，必须和当前大区间同组 → 合并'


CONFIG = dict(
    num=2580, title='统计将重叠区间合并成组的方案数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='排序 + 合并区间 + 乘法原理',
    tags=['灵神题单', '贪心算法', '难度分 1632'],
    code='''
class Solution:
    def countWays(self, ranges: List[List[int]]) -> int:
        ranges.sort(key=lambda p: p[0])
        m, max_r = 0, -1
        for l, r in ranges:
            if l > max_r:  # 无法合并
                m += 1  # 新区间
            max_r = max(max_r, r)  # 合并
        return pow(2, m, 1_000_000_007)
''',
    call='Solution().countWays([[1,3],[10,20],[2,5],[4,8],[25,26]])',
    expect=8,
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='intervals', var='ranges', pointer=_cur, label='数轴：蓝 = ranges（黄 = 当前区间）', h=430),
    ],
    watch=[('m', 'm', 'green'), ('max_r', 'max_r', 'orange'), ('l', 'l', 'blue'), ('r', 'r', 'pink')],
    captions={
        'ranges.sort': '按左端点从小到大排序：`{ranges}`。有交集的区间会挨在一起',
        'm, max_r = 0, -1': '`m` = 大区间个数，`max_r` = 当前大区间右端点。初始 `-1`，保证第一个区间一定开新区间',
        'for l, r in ranges': lambda S, B, rt: ('看下一个区间 `[{}, {}]`'.format(S.l, S.r) if 'l' not in B or B.l != S.l or B.r != S.r else '所有区间都看完了'),
        'if l > max_r': _if,
        'm += 1': '新大区间：`m` → =={m}==',
        'max_r = max': '`max_r = max({B.max_r}, {r}) = {max_r}`：右端点取最大，被包含时不变',
        'return pow': '共 `m = {m}` 个大区间，各 2 种选法 → `2^{m} = {ret}`（对 10^9+7 取模）',
    },
    cards=dict(
        one_liner='有交集的必须同组：先合并成 m 个大区间，答案 2^m',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['把 `ranges` 分成两个组（可为空），==有交集的区间必须同组==',
                 '返回分组方案数，对 `10^9 + 7` 取模',
                 '示例：`[[1,3],[10,20],[2,5],[4,8]]` → `4`',
                 '演示用 `[[1,3],[10,20],[2,5],[4,8],[25,26]]` → `8`'],
        quote='设合并后有 m 个大区间，那么每个大区间都可以分到第一个组或者第二个组，每个大区间都有 2 个方案。由于不同的大区间之间互相独立，根据乘法原理，方案数为 2^m。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先把有交集的区间合并，每个大区间整体选一组：`2` 种',
              '按左端点排序后维护 `max_r`：`l > max_r` 就是新大区间，`m += 1`',
              '否则并入当前大区间，`max_r` 取最大值'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`',
                 '`max_r` 初值 `-1`，因为区间端点可以是 `0`',
                 '判断用 `l > max_r`：端点相同（共用一个整数）也算有交集',
                 '`max_r` 要取 `max`，不能直接赋成 `r`（会被包含的小区间拉回去）',
                 '题解另一种写法：遍历时直接 `ans *= 2` 并取模'],
    ),
)
