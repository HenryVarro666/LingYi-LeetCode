def _sorted(S):
    return S.get('sorted_intervals') or S['intervals']


class _Var:
    def __call__(self, S):
        return _sorted(S)

    def __str__(self):
        return '区间'


class _Out:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, S):
        return self.fn(S)

    def __str__(self):
        return '没被覆盖（保留）'


def _kept(S, n):
    out, mx = [], 0
    for a, b in _sorted(S):
        if b > mx:
            out.append([a, b])
            mx = b
    return out[:n]


def _cur(S):
    if 'x' in S and 'y' in S and [S['x'], S['y']] in _sorted(S):
        return _sorted(S).index([S['x'], S['y']])
    return None


def _txt(S):
    if 'sorted_intervals' not in S:
        return '先按左端从小到大排序（左端相同时右端大的在前）'
    if 'last_y' not in S:
        return '已排序，第一个区间一定保留'
    return f"上一个保留的区间 `({S['last_x']}, {S['last_y']})`，当前 `({S.get('x', '-')}, {S.get('y', '-')})`，已保留 =={S['res']}== 个"


CONFIG = dict(
    num=1288, title='删除被覆盖区间', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='按左端排序 · 对比上一个区间',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def removeCoveredIntervals(self, intervals):

        sorted_intervals = sorted(intervals, key=lambda d:(d[0], -d[1]))
        res = 1
        last_x, last_y = sorted_intervals[0]
        for x, y in sorted_intervals[1:]:
            if y > last_y:
                last_y = y
                if x != last_x:
                    last_x = x
                    res += 1

        return res
''',
    call='Solution().removeCoveredIntervals([[1,4],[2,5],[2,8],[3,6],[7,9]])',
    expect=3,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='intervals', var=_Var(), out=_Out(lambda S: _kept(S, S.get('res', 0))), pointer=_cur,
             label='区间（蓝 = 待看，黄 = 当前，绿 = 保留）', h=420),
    ],
    watch=[('last_x', 'last_x', 'cyan'), ('last_y', 'last_y', 'cyan'), ('x', 'x', 'yellow'), ('y', 'y', 'yellow'), ('res', 'res', 'green')],
    captions={
        'sorted_intervals = sorted': '按左端从小到大排序：之后 `c <= a` 必然成立，只需对比 `b` 和 `d`。左端相同时右端大的在前',
        'res = 1': '第一个区间不可能被前面的覆盖 → `res = 1`',
        'last_x, last_y =': '`(last_x, last_y) = ({last_x}, {last_y})` 是当前「上一个区间」',
        'for x, y in': '扫描到 `(a, b) = ({x}, {y})`',
        'if y > last_y': lambda S, B, ret: (f'`b = {S["y"]} > d = {S["last_y"]}`：没被上一个区间覆盖' if S['y'] > S['last_y']
                                             else f'`b = {S["y"]} <= d = {S["last_y"]}`：被 `({S["last_x"]}, {S["last_y"]})` 覆盖，保留原来的不动'),
        'last_y = y': '以后只需拿 `({x}, {y})` 去检测，它的右端更大：凡是被旧区间盖住的，==也会被它盖住==。`last_y` → {last_y}',
        'if x != last_x': lambda S, B, ret: ('左端不同 → 是一个新区间，计数' if S['x'] != S['last_x'] else '左端相同（排序后不会出现，防御判断）'),
        'last_x = x': '`last_x` → {last_x}',
        'res += 1': '答案加一：`res` → {res}',
        'return res': '剩余区间 `{res}` 个',
    },
    cards=dict(
        one_liner='排序后只对比上一个区间的右端',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`[a,b)` 被 `[c,d)` 覆盖：`c <= a` 且 `b <= d`',
                 '删掉被覆盖的区间，返回剩余个数',
                 '本视频：`[[1,4],[2,5],[2,8],[3,6],[7,9]]` → `3`'],
        quote='若b > d，那么说明(a, b)没有被(c, d)覆盖，应该将答案加上1。……因此对于后续的区间我们只需用(a, b)去检测，那么此时应该将(c, d)置为(a, b)。',
        quote_src='—— yiduobo 题解原文',
        idea=['先按左端排序，条件 `c <= a` 自动满足，只比右端',
              '没被覆盖时，`(a, b)` 比 `(c, d)` 右端更大：以后被 `(c, d)` 覆盖的也必被 `(a, b)` 覆盖',
              '所以把「上一个区间」换成 `(a, b)` 即可'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（`sorted` 拷贝了一份）',
                 '排序键 `(d[0], -d[1])`：左端相同时大区间在前',
                 '对比灵神：灵神只维护最大右端 `max_right`；yiduobo 保留「上一个区间」的两个端点',
                 '原文为 Python 2 写法，只删去了类型说明文档字符串，代码无需其他修改'],
    ),
)
