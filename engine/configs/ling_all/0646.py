def _chosen(S, n):
    """按右端点排序后贪心选出的区间，取前 n 个"""
    out, pre = [], float('-inf')
    for l, r in sorted(S['pairs'], key=lambda x: x[1]):
        if l > pre:
            out.append([l, r])
            pre = r
    return out[:n]


class _Out:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, S):
        return self.fn(S)

    def __str__(self):
        return '已选入链'


def _cur(S):
    if 'l' in S and 'r' in S and [S['l'], S['r']] in S['pairs']:
        return S['pairs'].index([S['l'], S['r']])
    return None


def _txt(S):
    if 'pre_r' not in S:
        return '先排序，再扫描：区间的左端点 `l` 必须 ==大于== 上一个选中区间的右端点 `pre_r`'
    if 'l' not in S:
        return '`pre_r = -inf`：还没选任何区间'
    pre = '-inf' if S['pre_r'] == float('-inf') else S['pre_r']
    return f"当前 `[{S['l']}, {S['r']}]`，`pre_r = {pre}`，已选 =={S['ans']}== 个"


CONFIG = dict(
    num=646, title='最长数对链', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='按右端点排序 · 不相交区间贪心',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution:
    def findLongestChain(self, pairs: List[List[int]]) -> int:
        pairs.sort(key=lambda x: x[1])
        ans = 0
        pre_r = -inf
        for l, r in pairs:
            if l > pre_r:
                ans += 1
                pre_r = r
        return ans
''',
    call='Solution().findLongestChain([[3,4],[1,2],[7,8],[2,3],[4,5]])',
    expect=3,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='intervals', var='pairs', out=_Out(lambda S: _chosen(S, S.get('ans', 0))), pointer=_cur,
             label='pairs（蓝 = 待选，黄 = 当前，绿 = 已选入链）', h=380),
    ],
    watch=['ans', 'pre_r', 'l', 'r'],
    captions={
        'pairs.sort': '按右端点从小到大排序：右端点最小的区间 ==一定可以选==，它给后面留的空间最大',
        'ans = 0': '`ans` 记录选了几个区间',
        'pre_r = -inf': '`pre_r` 是上一个选中区间的右端点，一开始什么都没选 → `-inf`',
        'for l, r in pairs': lambda S, B, r: ('区间都看完了，循环结束' if ('l' in B and (B['l'], B['r']) == (S.l, S.r)) else f'看下一个区间 `[{S.l}, {S.r}]`'),
        'if l > pre_r': lambda S, B, r: (f"`l = {S.l} > pre_r = {S.pre_r}`：不与已选区间相交 → ==可以接在后面==" if S.l > S.pre_r
                                         else f"`l = {S.l} ≤ pre_r = {S.pre_r}`：与已选区间相交（左端点没超过上一个右端点）→ ==跳过=="),
        'ans += 1': '选中 `[{l}, {r}]`，链长 `ans` → =={ans}==',
        'pre_r = r': '更新 `pre_r = {pre_r}`：下一个区间的左端点必须大于它',
        'return ans': '链最长 =={ans}==',
    },
    cards=dict(
        one_liner='右端点最小的区间一定能选：替换进任何方案都不吃亏',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['`[a, b]` 后面可以跟 `[c, d]`，当且仅当 `b < c`',
                 '求能串成的最长数对链长度，数对可任意挑选、任意顺序',
                 '示例：`[[1,2],[2,3],[3,4]]` → `2`；本视频：`[[3,4],[1,2],[7,8],[2,3],[4,5]]` → `3`'],
        quote='在任意一种选法中，都可以把最左边的区间，替换成 A（右端点最小的区间）。由于 A 是一个更靠左的区间，所以 A 不会与其他已选区间相交。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先问：最左边的区间选哪个？答案是==右端点最小==的那个 A',
              '选了 A，左端点不超过 A 右端点的区间全部作废，剩下的是规模更小的子问题',
              '所以按右端点排序，一路扫过去：能接上就选，更新 `pre_r`'],
        summary=['时间 `O(n log n)`（排序），空间 `O(1)`',
                 '按==右==端点排序，不是左端点；比较用严格大于 `l > pre_r`，因为题目要求 `b < c`',
                 '本题是「不相交区间」模板，和 435 无重叠区间、452 射气球同一类'],
    ),
)
