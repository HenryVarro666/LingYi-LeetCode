def _cur(S):
    try:
        return S['ranges'].index([S['x'], S['y']])
    except Exception:
        return None


def _txt(S):
    n = S.get('n')
    if 'nowy' in S:
        return f'数组 `[0, {n - 1}]`　已覆盖到 `nowy = {S["nowy"]}`　未覆盖 `res = {S.get("res")}`'
    return f'数组下标 `[0, {n - 1}]`，把覆盖区间合并，空隙就是未覆盖区间（含两头）'


def _if(S, B, ret):
    x, ny = B.x, B.nowy
    if x <= ny + 1:
        return f'`x = {x} ≤ nowy + 1 = {ny + 1}`：重叠或紧挨着 → ==合并==，更新终点'
    return f'`x = {x} > nowy + 1 = {ny + 1}`：中间有空隙 `[{ny + 1}, {x - 1}]` 没被覆盖'


CONFIG = dict(
    num=2655, title='寻找最大长度的未覆盖区间', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='排序合并区间 + 记录空隙（含两端）',
    tags=['灵神题单', '贪心算法'],
    code='''
class Solution(object):
    def findMaximalUncoveredRanges(self, n, ranges):

        if not ranges:
            return [[0, n - 1]]

        ranges.sort()
        res = []
        if ranges[0][0] > 0:
            res.append([0, ranges[0][0] - 1])
        
        nowx, nowy = ranges[0]
        for x, y in ranges[1:]:
            if x <= nowy + 1:
                nowy = max(nowy, y)
            else:
                res.append([nowy + 1, x - 1])
                nowx, nowy = x, y
        
        if nowy + 1 < n:
            res.append([nowy + 1, n - 1])
        
        return res
''',
    call='Solution().findMaximalUncoveredRanges(12, [[3,5],[7,8],[4,6],[10,10]])',
    expect=[[0, 2], [9, 9], [11, 11]],
    views=[
        dict(type='text', fn=_txt, size=24),
        dict(type='intervals', var='ranges', out='res', pointer=_cur, label='数轴：蓝 = 覆盖区间（黄 = 当前），绿 = 未覆盖区间 res', h=440),
    ],
    watch=[('nowx', 'nowx', 'blue'), ('nowy', 'nowy', 'pink'), ('res', 'res', 'green')],
    captions={
        'if not ranges': '没有任何覆盖区间 → 整段都未覆盖；本例有 `{len(ranges)}` 个，继续',
        'ranges.sort()': '按起点排序：`{ranges}`',
        'res = []': '`res` 存未覆盖区间',
        'if ranges[0][0] > 0': lambda S, B, rt: '首个区间起点 `{}`：{}'.format(S.ranges[0][0], '> 0，开头 `[0, {}]` 没被覆盖'.format(S.ranges[0][0] - 1) if S.ranges[0][0] > 0 else '就是 0，开头没有空隙'),
        'res.append([0, ranges[0][0] - 1])': '开头空隙加入：`res = {res}`',
        'nowx, nowy = ranges[0]': '合并区间从第一个开始：`[{nowx}, {nowy}]`',
        'for x, y in ranges[1:]': lambda S, B, rt: ('看下一个区间 `[{}, {}]`'.format(S.x, S.y) if 'x' not in B or B.x != S.x or B.y != S.y else '区间都看完了，接着看末尾'),
        'if x <= nowy + 1': _if,
        'nowy = max': '`nowy = max({B.nowy}, {y}) = {nowy}`：只更新终点',
        'res.append([nowy + 1, x - 1])': '中间空隙 `[{nowy + 1}, {x - 1}]` 加入 `res`',
        'nowx, nowy = x, y': '从当前区间重新开始合并：`[{nowx}, {nowy}]`',
        'if nowy + 1 < n': lambda S, B, rt: '末尾：`nowy + 1 = {}` 与 `n = {}`：{}'.format(S.nowy + 1, S.n, '后面还有空隙 `[{}, {}]`'.format(S.nowy + 1, S.n - 1) if S.nowy + 1 < S.n else '已覆盖到末尾'),
        'res.append([nowy + 1, n - 1])': '末尾空隙加入：`res = {res}`',
        'return res': '未覆盖区间：`{ret}`',
    },
    cards=dict(
        one_liner='先合并覆盖区间，区间之间和两端的空隙就是答案',
        complexity='时间 `O(n log n)`，空间 `O(1)`（不计返回值）',
        problem=['长度为 `n` 的数组（下标 `0..n-1`），`ranges` 给出若干已覆盖的子区间（可重叠）',
                 '返回所有==最大的未覆盖区间==，按起点升序，互不相邻',
                 '示例：`n=10`，`[[3,5],[7,8]]` → `[[0,2],[6,6],[9,9]]`',
                 '本视频：`n=12`，`[[3,5],[7,8],[4,6],[10,10]]`'],
        quote='若当前遍历到的区间起点在上一个区间的终点之前，或者紧挨着上一个区间的终点，那么就将这两个区间合并；反过来，说明两段区间之前存在未覆盖区域，起点是上一个区间的终点加1，终点是本区间的起点减1。',
        quote_src='—— yiduobo 题解原文',
        idea=['经典区间合并：排序后一趟遍历，`x <= nowy + 1`（含紧挨）就并入',
              '断开时，中间空隙 `[nowy + 1, x - 1]` 就是一个未覆盖区间',
              '还要处理两头：首区间起点 `> 0`、末区间终点 `+ 1 < n`'],
        summary=['时间 `O(n log n)`，排序是瓶颈',
                 '紧挨也要合并：`x <= nowy + 1`，否则会产生空的「未覆盖区间」',
                 '易漏：开头空隙、末尾空隙；`ranges` 为空时整段都未覆盖',
                 '原文代码本身就是 Python 3 可运行的，未做修改（会员题，题意按 LeetCode 原题）'],
    ),
)
