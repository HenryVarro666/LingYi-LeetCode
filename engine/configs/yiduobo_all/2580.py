class _V:
    def __init__(self, fn, name):
        self.fn, self.name = fn, name

    def __call__(self, S):
        return self.fn(S)

    def __str__(self):
        return self.name


def _srt0(S):
    return sorted(S['ranges'])


_srt = _V(_srt0, 'sorted(ranges)')


def _cur(S):
    if 'x' in S and 'y' in S and [S['x'], S['y']] in S['ranges']:
        return sorted(S['ranges']).index([S['x'], S['y']])
    return None


def _merging0(S):
    if S.get('lastx') is None:
        return []
    return [[S['lastx'], S['lasty']]]


_merging = _V(_merging0, '合并中的区间 [lastx, lasty]')


def _txt(S):
    if 'res' in S and 'mod' in S:
        return f'共 `cnt = {S["cnt"]}` 个合并区间 → 每个区间 ×2：`res = {S["res"]}`'
    if 'cnt' not in S:
        return '合并相交区间，得到 cnt 个互不相交的区间 → 答案 ==2^cnt=='
    if S.get('lastx') is None:
        return f'`cnt = {S["cnt"]}`，还没有合并中的区间'
    return f'已定型 `cnt = {S["cnt"]}` 个，正在合并的区间 `[{S["lastx"]}, {S["lasty"]}]`（绿色）'


def _elif(S, B, ret):
    x, ly = B.x, B.lasty
    if ly < x:
        return f'`lasty = {ly} < x = {x}`：==不相交==，上一个区间不会再碰到后面的了 → 定型'
    return f'`lasty = {ly} ≥ x = {x}`：==相交==，合并，只需更新终点'


CONFIG = dict(
    num=2580, title='统计将重叠区间合并成组的方案数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='排序合并区间 + 2^cnt（循环翻倍）',
    tags=['灵神题单', '贪心算法', '难度分 1632'],
    code='''
class Solution(object):
    def countWays(self, ranges):

        cnt = 0
        lastx, lasty = None, None
        for x, y in sorted(ranges):
            if lastx is None:
                lastx, lasty = x, y
            elif lasty < x:
                cnt += 1
                lastx, lasty = x, y
            else:
                lasty = max(lasty, y)
        
        cnt += 1
        res = 1
        mod = 10 ** 9 + 7
        for _ in range(cnt):
            res += res
            if res >= mod:
                res -= mod
        
        return res
''',
    call='Solution().countWays([[1,3],[10,20],[2,5],[4,8],[25,26]])',
    expect=8,
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='intervals', var=_srt, out=_merging, pointer=_cur, label='排序后的区间（蓝，黄 = 当前）与正在合并的区间（绿）', h=430),
    ],
    watch=[('cnt', 'cnt', 'green'), ('lastx', 'lastx', 'blue'), ('lasty', 'lasty', 'pink'), ('res', 'res', 'orange')],
    captions={
        'cnt = 0': '`cnt` 统计合并后区间的个数（先不算最后一个）',
        'for x, y in sorted': lambda S, B, r: ('按起点排序后一趟遍历，看区间 `[{}, {}]`'.format(S.x, S.y) if 'x' not in B or B.x != S.x or B.y != S.y else '区间都看完了'),
        'if lastx is None': lambda S, B, r: ('`lastx is None`：这是第一个区间，直接作为「上一个区间」`[{}, {}]`'.format(S.x, S.y)
                                             if B.lastx is None else '`lastx` 已有值，不是第一个区间 → 看和上一个区间是否相交'),
        'elif lasty < x': _elif,
        10: '上一个区间定型，`cnt` → =={cnt}==',
        'lastx, lasty = x, y': '当前区间 `[{x}, {y}]` 成为新的「上一个区间」',
        15: '遍历结束后，最后一个合并区间还没被计数：`cnt` → =={cnt}==',
        'lasty = max': '起点已排序，只需用终点更新：`lasty = max({B.lasty}, {y}) = {lasty}`',
        'res = 1': '`res` 从 1 开始，每轮翻一倍 → 最后是 2^cnt',
        'res += res': '`res` 翻倍：`{B.res} + {B.res} = {res}`',
        'res -= mod': '超过 `mod` 就减掉，保持在取模范围内',
        'return res': '`cnt = {cnt}` 个合并区间 → 方案数 `2^{cnt} = {ret}`',
    },
    cards=dict(
        one_liner='相交区间必须同组：合并后有 cnt 个区间，答案就是 2^cnt',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['把 `ranges` 分成两个组（可为空），==相交的区间必须在同一组==',
                 '返回总方案数，对 `10^9 + 7` 取模',
                 '示例：`[[1,3],[10,20],[2,5],[4,8]]` → `4`',
                 '演示用 `[[1,3],[10,20],[2,5],[4,8],[25,26]]` → `8`'],
        quote='需要先将相交区间全部合并，得到最终的不重叠区间列表。不妨设其中有cnt个区间，那么对于这cnt个区间而言，既可以加入到第一个组也可以加入到第二个组，因此最终答案就是2^cnt。',
        quote_src='—— yiduobo 题解原文',
        idea=['按起点排序，一趟遍历维护「上一个区间」`[lastx, lasty]`',
              '`lasty < x`：不相交，上一个区间定型，`cnt += 1`',
              '遍历结束后，最后一个区间还没被计数，所以 `cnt` 要再加 1'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（sorted 复制了一份）',
                 '易错：循环里只在「断开」时 `cnt += 1`，结束后要补最后一个区间',
                 '用循环翻倍代替 `pow`：`res += res`，超过 `mod` 就减 `mod`',
                 '对比灵神：灵神把 `max_r` 初值设 `-1`，第一个区间也当作断开，不用补 1'],
    ),
)
