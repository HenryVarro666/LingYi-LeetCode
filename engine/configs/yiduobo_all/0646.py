def _chosen(S, n):
    out, pre = [], None
    for a, b in sorted(S['pairs'], key=lambda d: d[1]):
        if pre is None or pre < a:
            out.append([a, b])
            pre = b
    return out[:n]


class _Out:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, S):
        return self.fn(S)

    def __str__(self):
        return '已选入链'


def _cur(S):
    p = S.get('pair')
    return S['pairs'].index(p) if p is not None and p in S['pairs'] else None


def _txt(S):
    if 'now' not in S:
        return '把数对看成区间，问题是「最多选几个互不相交的区间」'
    pair = S.get('pair')
    if pair is None:
        return '`now = None`：还没选任何区间'
    return f"当前 `{pair}`，`now = {S['now']}`，`res = {S['res']}`"


CONFIG = dict(
    num=646, title='最长数对链', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='按右边界排序 · 一趟扫描',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def findLongestChain(self, pairs):

        now = None
        res = 0
        for pair in sorted(pairs, key=lambda d:d[1]):
            if now is None or now < pair[0]:
                now = pair[1]
                res += 1
        
        return res
''',
    call='Solution().findLongestChain([[3,4],[1,2],[7,8],[2,3],[4,5]])',
    expect=3,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='intervals', var='pairs', out=_Out(lambda S: _chosen(S, S.get('res', 0))), pointer=_cur,
             label='pairs（蓝 = 原数对，黄 = 当前，绿 = 已加入答案）', h=380),
    ],
    watch=['now', 'res', 'pair'],
    captions={
        'now = None': '`now` 是答案里最后一个区间的右边界，还没有区间 → `None`',
        'res = 0': '`res` 统计选了几个',
        'for pair in sorted': lambda S, B, r: ('区间都看完了，循环结束' if ('pair' in B and B['pair'] == S.pair) else f'按右边界从小到大排好，取下一个 `{S.pair}`'),
        'if now is None': lambda S, B, r: ('答案里还没有区间 → ==直接加入==' if S.now is None
                                           else (f"`now = {S.now} < pair[0] = {S.pair[0]}`：左边界在答案右边界之后 → ==加入==" if S.now < S.pair[0]
                                                 else f"`now = {S.now} ≥ pair[0] = {S.pair[0]}`：与答案相交，右边界更小的那个已经在答案里 → ==舍弃==")),
        'now = pair[1]': '答案的右边界更新为 `now = {now}`',
        'res += 1': '`{pair}` 成为链的一环，`res` → =={res}==',
        'return res': '最多选出 =={res}== 个不相交区间',
    },
    cards=dict(
        one_liner='相交的两个区间留右边界小的，给后面留空间',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['数对 `[a, b]` 后面可以跟 `[c, d]`，条件是 `b < c`',
                 '求最长的数对链',
                 '本视频：`[[3,4],[1,2],[7,8],[2,3],[4,5]]` → `3`'],
        quote='对于两个相交的区间，我们应当选择右边界较小的那一个，这样的话可以留出更多选择的空间给后面的区间。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目名叫数对链，其实就是标准的区间问题：选最多的不相交区间',
              '按右边界排序后一趟扫描，用 `now` 记住答案的右边界',
              '当前区间左边界比 `now` 大就加入，否则舍弃'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '`now is None` 单独判断，处理第一个区间',
                 '对比灵神：灵神用 `-inf` 作初值省掉判断，并先对 `pairs` 原地排序'],
    ),
)
