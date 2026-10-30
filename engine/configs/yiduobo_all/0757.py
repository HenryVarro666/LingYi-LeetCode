IV = [[1, 3], [1, 4], [3, 5], [4, 5], [7, 8], [6, 9]]
LO, HI = 0, 9


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '数轴：黄 = 当前区间，绿点 = 已选的最大两个数 min / max', 22, T['muted'], bold=True)
    L, R = x0 + 90, x1 - 40
    unit = (R - L) / (HI - LO + 1)

    def X(v):
        return L + (v - LO) * unit + unit / 2
    top, axis = y0 + 56, y1 - 50
    for v in range(LO, HI + 1):
        cv.line([(X(v), top), (X(v), axis)], (36, 42, 52), 1)
        cv.text((X(v), axis + 8), v, 22, T['dim'], anchor='mt', mono=True)
    iv = S.get('intervals') or IV
    if 'x' in S:
        k = None
        if S['x'] == iv[0][0] and S['y'] == iv[0][1] and S.get('res', 2) == 2 and S['_line'] <= 11:
            k = 0
        for j, (a, b) in enumerate(iv):
            if (a, b) == (S['x'], S['y']):
                k = j
        k = 0 if k is None else k
    else:
        k = None
    rowh = min(40, (axis - top - 40) / len(iv))
    for j, (a, b) in enumerate(iv):
        y = top + j * rowh
        col = T['yellow'] if j == k else ((96, 110, 130) if (k is not None and j < k) else (70, 78, 90))
        cv.rect((X(a) - unit / 2 + 5, y, X(b) + unit / 2 - 5, y + 24), fill=col, r=12)
        cv.text((X(a) - unit / 2, y + 12), f'[{a},{b}]', 17, T['muted'], anchor='rm', mono=True)
    if 'min_num' in S:
        yy = axis - 24
        for name, v, c in (('min', S['min_num'], T['cyan']), ('max', S['max_num'], T['green'])):
            if LO <= v <= HI:
                cv.rect((X(v) - 14, yy - 14, X(v) + 14, yy + 14), fill=c, r=14)
                cv.text((X(v), yy - 22), name, 20, c, anchor='mb', bold=True)


CONFIG = dict(
    num=757, title='设置交集大小至少为2', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='按末尾排序 + 维护最大的两个数',
    tags=['灵神题单·贪心与思维', '贪心算法', '难度分 2379'],
    code='''
class Solution(object):
    def intersectionSizeTwo(self, intervals):

        intervals = sorted(intervals, key=lambda d:d[1])
        min_num = intervals[0][1] - 1
        max_num = intervals[0][1]
        res = 2
        for (x, y) in intervals[1:]:
            if x <= min_num:
                continue
            elif x <= max_num:
                if y == max_num:
                    min_num = max_num - 1
                else:
                    min_num = max_num
                    max_num = y

                res += 1
            else:
                min_num = y - 1
                max_num = y
                res += 2
        
        return res
''',
    call=f'Solution().intersectionSizeTwo({IV})',
    expect=6,
    views=[
        dict(type='text', fn=lambda S: (f"已选集合中最大的两个数：`min = {S['min_num']}`，`max = {S['max_num']}`，共 =={S['res']}== 个数" if 'min_num' in S else ''), size=26, h=70),
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'cyan'), ('min_num', 'min_num', 'orange'), ('max_num', 'max_num', 'pink'), ('res', 'res', 'green')],
    captions={
        4: '==按区间末尾从小到大排序==：后面的区间末尾都不小于前面的',
        5: '第 0 个区间选==最右侧两个数==：`min_num = {min_num}`（次大），末尾更靠右、更可能出现在后续区间里',
        6: '`max_num = {max_num}`（最大）',
        7: '已经选了 2 个数，`res = 2`',
        8: lambda S, B, ret: ('所有区间都看完了' if B.get('x') == S.x and B.get('y') == S.y and 'res' in B and S.x == 6 else f'看后面的区间 `[{S.x}, {S.y}]`：起点 x，终点 y'),
        9: lambda S, B, ret: (f'`x = {S.x} <= min_num = {S.min_num}`：因为 y 不小于之前的终点，区间含 min 和 max 两个数 → ==已满足=='
                                              if S.x <= S.min_num else f'`x = {S.x} > min_num = {S.min_num}`：min 不在区间里，往下看'),
        10: '这个区间已满足，不用加数，看下一个',
        11: lambda S, B, ret: (f'`x = {S.x} <= max_num = {S.max_num}`：区间里==只有 max 一个数==在 S 中，还差 1 个'
                                                if S.x <= S.max_num else f'`x = {S.x} > max_num = {S.max_num}`：区间里一个已选数都没有，要加 2 个'),
        12: lambda S, B, ret: (f'`y = {S.y} == max_num`：终点就是 max，只能再选 `y - 1`' if S.y == S.max_num
                                              else f'`y = {S.y} > max_num = {S.max_num}`：再选终点 y，它最靠右'),
        13: '新数选 `y - 1 = {min_num}`，它成为次大的数：`min_num = {min_num}`',
        15: '`min_num` 变成老的 max = `{min_num}`',
        16: '新选的 y 成为最大的数：`max_num = {max_num}`',
        18: '这种情况加了 1 个数：`res = {res}`',
        20: '区间里没有已选数：选最右的两个数 `y - 1` 和 `y`：先 `min_num = {min_num}`',
        21: '再 `max_num = {max_num}`',
        22: '这种情况加了 2 个数：`res = {res}`',
        24: '最少需要 =={ret}== 个数',
    },
    cards=dict(
        one_liner='按末尾排序，每次只保留最大的两个已选数',
        complexity='时间 `O(n log n)`，空间 `O(1)`（不计排序）',
        problem=['每个区间 `[start, end]` 都要有至少 ==2 个整数== 在集合 S 里',
                 '求 S 的最小大小',
                 '本视频：`[[1,3],[1,4],[3,5],[4,5],[7,8],[6,9]]` → `6`'],
        quote='对于第0个区间，我们需要从中间选择两个数加入到S中。由于我们已经按末尾从小到大进行了排序，那么在这里我们很明显应该选择第0个区间中最右侧的两个数加入到S中。',
        quote_src='—— yiduobo 题解原文',
        idea=['末尾从小到大排序后，选区间==最右两个数==最可能被后续区间用到',
              '记已选的最大两个数 `min_num < max_num`，对新区间 `[x, y]` 分三种情况',
              '`x <= min_num`：已含两个数；`min_num < x <= max_num`：只含一个，补 1 个；`x > max_num`：补 2 个',
              '补的数总是取区间末尾 `y`（和 `y-1`）'],
        summary=['时间 `O(n log n)`，空间 `O(1)`（不计排序）',
                 '三种情况：已满足 / 补 1 个 / 补 2 个，第二种要看 `y` 是否等于 `max_num`',
                 '`y == max_num` 时补的是 `y - 1`，且 `min_num` 变为 `max_num - 1`',
                 '用到“后面区间末尾不小于前面”这个性质，所以必须按末尾排序',
                 '对比灵神：灵神把它看作 2589 的特例，用栈和二分一般化；yiduobo 针对 k = 2 只记两个数'],
    ),
)
