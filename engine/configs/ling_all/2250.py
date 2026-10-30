RECTS = [[1, 2], [2, 3], [2, 5]]
POINTS = [[2, 1], [1, 4]]


def _pt(S):
    if 'x' not in S or 'y' not in S:
        return '先把矩形、点都按纵坐标从大到小排序；高度只有 `1..100`，排序最多 100 次'
    n = len(S['rectangles'])
    got = S['i']
    ok = sum(1 for k in range(got) if S['rectangles'][k][0] >= S['x'])
    return f"点 `({S['x']}, {S['y']})`：已入 xs 的 `{got}` 个矩形高度都 `>= {S['y']}`，其中长 `>= {S['x']}` 的有 =={ok}== 个"


CONFIG = dict(
    num=2250, title='统计包含每个点的矩形数目', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='按纵坐标排序 + 二分',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution:
    def countRectangles(self, rectangles: List[List[int]], points: List[List[int]]) -> List[int]:
        rectangles.sort(key=lambda r: -r[1])
        n = len(points)
        ans = [0] * n
        i, xs = 0, []
        for (x, y), id in sorted(zip(points, range(n)), key=lambda x: -x[0][1]):
            start = i
            while i < len(rectangles) and rectangles[i][1] >= y:
                xs.append(rectangles[i][0])
                i += 1
            if start < i:
                xs.sort()  # 只有在 xs 插入了新元素时才排序
            ans[id] = i - bisect_left(xs, x)
        return ans
''',
    call=f'Solution().countRectangles({RECTS}, {POINTS})',
    expect=[2, 1],
    views=[
        dict(type='text', fn=_pt, h=90, size=27),
        dict(type='grid', var='rectangles', label='rectangles（按高度从大到小；绿 = 已加入 xs）', cols=['长 l', '高 h'],
             rows=lambda S: list(range(len(S['rectangles']))), cell=70, h=290,
             cursors=[('i', 0, 'yellow', 'i')],
             color=lambda S, r, c, v: 'green' if 'i' in S and r < S['i'] else None),
        dict(type='array', var='xs', label='xs（已满足“高度 >= y”的矩形的长，排序后二分）', cell=84, h=190,
             color=lambda S, i, v: 'cyan' if 'x' in S and v >= S['x'] else None, dim=lambda S, i, v: 'x' in S and v < S['x']),
        dict(type='array', var='ans', label='ans（按原来的点序号填）', cell=84, h=170,
             pointers={'id': 'pink'}),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('id', 'id', 'purple'), ('i', 'i', 'orange'), ('ans', 'ans', 'green')],
    skip=['n = len(points)', 'ans = [0] * n', 'start = i'],
    max_steps=80,
    captions={
        'rectangles.sort': '矩形按==高度从大到小==排序：后面处理纵坐标 `y` 时，前缀里的矩形高度都 `>= y`',
        'i, xs = 0, []': '`i` 是还没加入的第一个矩形，`xs` 保存已加入矩形的长',
        'for (x, y), id in sorted': lambda S, B, r: ('所有点都处理完了' if 'id' in B and B.id == S.id else f'点也按纵坐标从大到小处理：现在是点 `({S.x}, {S.y})`，它在原数组的下标 `id = {S.id}`'),
        'while i < len(rectangles)': lambda S, B, r: (f'矩形 `{B.rectangles[B.i]}` 高 `{B.rectangles[B.i][1]} >= y = {B.y}` → ==成立==，它一定盖得住纵坐标，加入 xs'
                                                        if B.i < len(B.rectangles) and B.rectangles[B.i][1] >= B.y
                                                        else ('矩形都加完了，结束' if B.i >= len(B.rectangles) else f'矩形 `{B.rectangles[B.i]}` 高 `{B.rectangles[B.i][1]} < y = {B.y}` → 不成立，先不加')),
        'xs.append': '把这个矩形的长 `{rectangles[i][0]}` 放进 `xs`，只剩横坐标要比较',
        'i += 1': '`i` → {i}，看下一个矩形',
        'if start < i': lambda S, B, r: ('这个点有新矩形加入 → `xs` 要重新排序' if B.start < B.i else '没有新矩形加入，`xs` 仍有序，不用再排'),
        'xs.sort()': '`xs` 排好序：{xs}（高度只有 100 种，最多排 100 次）',
        'ans[id] = i - bisect_left': lambda S, B, r: (lambda k: f'`xs` 里共 `{S.i}` 个矩形；长 `< {S.x}` 的有 `{k}` 个（`bisect_left`），剩下 `{S.i} − {k}` = =={S.ans[S.id]}== 个包含点 `({S.x}, {S.y})`')(sum(1 for v in S.xs if v < S.x)),
        'return ans': '每个点的答案：`{ans}`',
    },
    cards=dict(
        one_liner='按高度从大到小加矩形，横坐标交给二分',
        complexity='时间 `O(H·n log n + m log m + m log n)`，空间 `O(n+m)`',
        problem=['`rectangles[i] = [l, h]` 是左下角在原点的矩形；`points[j] = [x, y]`',
                 '求每个点被多少个矩形包含（边上也算）：`x <= l` 且 `y <= h`',
                 '示例：`rectangles = [[1,2],[2,3],[2,5]]`，`points = [[2,1],[1,4]]` → `[2,1]`'],
        quote='由于纵坐标的范围只有 [1,100]，我们可以暴力地在每次插入完横坐标后对 xs 排序，排序的次数不会超过 100 次。',
        quote_src='—— 灵茶山艾府题解',
        idea=['点和矩形都按纵坐标从大到小：处理点 `y` 时，已加入的矩形高度都 `>= y`',
              '只需再数其中长 `>= x` 的个数：`xs` 排序后 `i - bisect_left(xs, x)`',
              '纵坐标只有 100 种，每次有新矩形才排序，最多排 100 次'],
        summary=['时间 `O(H·n log n + m log m + m log n)`，`H = 100`；空间 `O(n+m)`',
                 '易错：排序会打乱点的顺序，答案要按原下标 `id` 写回',
                 '易错：用 `bisect_left` 求“长 `< x`”的个数，等于也算包含',
                 '原文还给了按横坐标排序 + 高度计数、按行统计 + 二分两种写法'],
    ),
)
