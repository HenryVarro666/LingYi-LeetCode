RECTS = [[1, 2], [2, 3], [2, 5]]
POINTS = [[2, 1], [1, 4]]


def _nz(S):
    f = S.get('f')
    return {i: v for i, v in enumerate(f) if v} if f else {}


def _txt(S):
    if 'x' not in S or 'p' not in S:
        return '矩形和点都按横坐标从大到小排；`p` = 已经满足 `l >= x` 的矩形个数；树状数组按高度 `h` 计数'
    return f"点 `({S['x']}, {S['y']})`：`p = {S['p']}` 个矩形长 `>= {S['x']}`，其中高度 `< {S['y']}` 的要扣掉"


CONFIG = dict(
    num=2250, title='统计包含每个点的矩形数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='按横坐标排序 + 高度树状数组',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution(object):
    def countRectangles(self, rectangles, points):

        m = len(rectangles)
        n = len(points)

        sorted_rectangles = sorted(rectangles, key=lambda d:d[0], reverse=True)
        sorted_points = sorted([[x, y, index] for index, [x, y] in enumerate(points)], key=lambda d:d[0], reverse=True)

        res = [0] * n
        f = [0] * 101
        p = 0
        for x, y, index in sorted_points:
            while p < m and sorted_rectangles[p][0] >= x:
                now = sorted_rectangles[p][1]
                while now <= 100:
                    f[now] += 1
                    now += now & -now
                p += 1

            res[index] = p
            now = y - 1
            while now > 0:
                res[index] -= f[now]
                now -= now & -now
        
        return res
''',
    call=f'Solution().countRectangles({RECTS}, {POINTS})',
    expect=[2, 1],
    views=[
        dict(type='text', fn=_txt, h=90, size=27),
        dict(type='grid', var='sorted_rectangles', label='sorted_rectangles（按长 l 从大到小；绿 = 前 p 个）', cols=['长 l', '高 h'],
             rows=lambda S: list(range(len(S['sorted_rectangles']))), cell=70, h=280,
             cursors=[('p', 0, 'yellow', 'p')],
             color=lambda S, r, c, v: 'green' if 'p' in S and r < S['p'] else None),
        dict(type='map', var=_nz, label='树状数组 f（按高度；只显示非 0 节点）', fmt=lambda k, v: f'[{k}] = {v}', h=190, font=26),
        dict(type='array', var='res', label='res（按点的原下标填）', cell=84, h=170, pointers={'index': 'pink'}),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('index', 'index', 'purple'), ('p', 'p', 'orange'), ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    skip=['m = len', 'n = len', 'res = [0] * n', 'f = [0] * 101', 'p = 0', 'while now', 'now += now & -now', 'now -= now & -now', 'now = sorted_rectangles'],
    max_steps=80,
    captions={
        'sorted_rectangles = sorted': '矩形右上角 `(l, h)` 按横坐标 `l` ==从大到小==排序',
        'sorted_points = sorted': '点也按横坐标从大到小排；先记下原下标 `index`，排完才能把答案放回原位',
        'for x, y, index in sorted_points': lambda S, B, r: ('点都处理完了' if 'index' in B and B.index == S.index else f'处理点 `({S.x}, {S.y})`（原下标 `{S.index}`），把 `l >= {S.x}` 的矩形都计入'),
        'while p < m': lambda S, B, r: (f'`sorted_rectangles[{B.p}][0] = {B.sorted_rectangles[B.p][0]} >= x = {B.x}` → ==成立==，这个矩形长度够，把它的高度记进树状数组'
                                       if B.p < B.m and B.sorted_rectangles[B.p][0] >= B.x else '没有更多长度够的矩形了'),
        'f[now] += 1': '高度 `{B.now}` 对应的树状数组节点 `[{B.now}]` 加一 → {f[B.now]}，下一个节点是 `now + lowbit(now)`',
        'p += 1': '这个矩形处理完，`p` → {p}',
        'res[index] = p': '先假设这 `{p}` 个矩形都包含点，再扣掉高度不够的：`res[{index}] = {p}`',
        'now = y - 1': '再扣掉高度 `< y = {y}` 的矩形：查询树状数组前缀 `[1..{y-1}]`，`now = {now}`',
        'res[index] -= f[now]': '扣掉节点 `[{B.now}]` 管的 `{f[B.now]}` 个高度不足的矩形 → `res[{index}] = {res[index]}`，然后 `now` 去掉最低位',
        'return res': '每个点的答案：`{res}`',
    },
    cards=dict(
        one_liner='横坐标靠排序双指针，纵坐标靠树状数组数“不够高”的',
        complexity='时间 `O(n log n + m log m + (n+m) log H)`，空间 `O(H + n + m)`',
        problem=['`rectangles[i] = [l, h]` 是左下角在原点的矩形；`points[j] = [x, y]`',
                 '数每个点被多少个矩形包含（边上也算）',
                 '示例：`rectangles = [[1,2],[2,3],[2,5]]`，`points = [[2,1],[1,4]]` → `[2,1]`'],
        quote='判断某个点是否在矩形内就只需要考虑矩形右上角的点，也就是说问题转化成了判断对于点(x, y)，有多少个矩形右上角的点(l, h)满足l >= x且h >= y。',
        quote_src='—— yiduobo 题解原文',
        idea=['矩形和点都按横坐标从大到小排序，双指针 `p`：前 `p` 个矩形的长都 `>= x`',
              '再数这 `p` 个里高度 `>= y` 的：用树状数组数出高度 `< y` 的个数 `k`',
              '包含点的矩形数 = `p - k`；注意排序打乱了点的顺序，答案要按原下标写回'],
        summary=['时间 `O(n log n + m log m + (n+m) log H)`，`H = 100`；空间 `O(H + n + m)`',
                 '易错：树状数组查询的是 `y - 1`（严格小于 `y`），高度等于 `y` 的矩形仍然包含点',
                 '易错：排序后要靠 `index` 把答案放回原位置',
                 '对比灵神：灵神按纵坐标排序后对 xs 二分；yiduobo 按横坐标排序，用树状数组管高度'],
    ),
)
