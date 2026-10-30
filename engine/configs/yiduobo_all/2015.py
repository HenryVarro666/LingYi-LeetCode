def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    bs = S.get('buildings') or []
    cv.text((x0 + 18, y0 + 4), '建筑物（宽 = 区间，高 = 高度；竖线 = 扫到的位置）', 24, T['muted'], bold=True)
    if not bs:
        return
    lo, hi = min(b[0] for b in bs), max(b[1] for b in bs)
    hm = max(b[2] for b in bs)
    L, R = x0 + 50, x1 - 50
    base, top = y1 - 50, y0 + 60

    def X(v):
        return L + (v - lo) / max(1, hi - lo) * (R - L)
    sweep = None
    if 'last' in S and 'cnt' in S:
        sweep = S['last']
    cols = [T['blue'], T['pink'], T['cyan'], T['orange']]
    for k, (a, b, h) in enumerate(bs):
        yh = base - h / hm * (base - top)
        cv.rect((X(a), yh, X(b), base), fill=cols[k % 4], alpha=150, r=4)
        cv.text(((X(a) + X(b)) / 2, yh + 8), f'h={h}', 22, T['text'], anchor='mt', bold=True)
    res = S.get('res') or []
    for a, b, h in res:
        cv.rect((X(a) + 2, base + 6, X(b) - 2, base + 22), fill=T['green'], r=6)
        cv.text(((X(a) + X(b)) / 2, base + 14), f'avg {h}', 16, T['bg'], anchor='mm', bold=True)
    cv.line([(L, base), (R, base)], T['border'], 2)
    for v in range(lo, hi + 1):
        cv.text((X(v), base + 28), str(v), 18, T['dim'], anchor='mt', mono=True)
    if sweep is not None and lo <= sweep <= hi:
        cv.line([(X(sweep), top - 10), (X(sweep), base)], T['yellow'], 3)


def _txt(S):
    if 'cnt' not in S:
        return '把每栋楼拆成两个事件：左端 `left×2` 加高度，右端 `right×2−1` 减高度'
    return f'当前位置 `{S["last"]}`：覆盖 ==`{S["cnt"]}`== 栋，高度和 `{S["s"]}`' + (f'，平均 ==`{S["s"] // S["cnt"]}`==' if S['cnt'] else '，没有楼')


CONFIG = dict(
    num=2015, title='每段建筑物的平均高度', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='差分 · 事件排序扫描',
    tags=['常用数据结构'],
    code='''
class Solution(object):
    def averageHeightOfBuildings(self, buildings):

        points = []
        for left, right, avg in buildings:
            points.append([left * 2, avg])
            points.append([right * 2 - 1, avg])
        
        cnt = 0
        last = 0
        s = 0
        res = []
        for p, v in sorted(points):
            t = p % 2
            p = (p + 1) // 2
            if cnt > 0 and last != p:
                if res and last == res[-1][1] and s // cnt == res[-1][2]:
                    res[-1][1] = p
                else:
                    res.append([last, p, s // cnt])
            
            last = p
            if t == 0:
                cnt += 1
                s += v
            else:
                cnt -= 1
                s -= v

        return res
''',
    call='Solution().averageHeightOfBuildings([[1,4,2],[3,9,4]])',
    expect=[[1, 3, 2], [3, 4, 3], [4, 9, 4]],
    views=[
        dict(type='text', fn=_txt, size=24, h=80),
        dict(type='custom', draw=_draw, h=300),
        dict(type='text', fn=lambda S: ('已得到的区间 `res = ' + str(S['res']) + '`') if 'res' in S else '', size=22, h=60),
    ],
    watch=[('p', 'p', 'yellow'), ('last', 'last', 'blue'), ('cnt', 'cnt', 'orange'), ('s', 's', 'pink')],
    captions={
        'points.append([left': '左端点：位置 `{left}` 编码成 `{left*2}`（偶数），这里开始多一栋高 `{avg}` 的楼',
        'points.append([right': '右端点：位置 `{right}` 编码成 `{right*2-1}`（奇数），这里结束一栋楼',
        'cnt = 0': '`cnt` 当前覆盖的楼数，`s` 是高度之和',
        'for p, v in sorted': '按位置从小到大取下一个事件：`p = {p}`，`v = {v}`',
        't = p % 2': lambda S, B, r: ('`p` 是偶数 → 楼的左端（开始）' if S.t == 0 else '`p` 是奇数 → 楼的右端（结束）'),
        'p = (p + 1)': '还原真实位置：`p = {p}`',
        'if cnt > 0 and last': lambda S, B, r: (f'`cnt = {S.cnt} > 0` 且 `last = {S.last} != p = {S.p}`：区间 `[{S.last}, {S.p}]` 内楼的状态没变，可以结算' if S.cnt > 0 and S.last != S.p else f'`last = {S.last}`，`p = {S.p}`，`cnt = {S.cnt}`：没有要结算的区间（无楼，或位置相同）'),
        'if res and last': lambda S, B, r: ('和上一段首尾相接且平均高度相同 → 合并' if (S.res and S.last == S.res[-1][1] and S.s // S.cnt == S.res[-1][2]) else '不能合并（不相接或平均高度不同）→ 新开一段'),
        'res[-1][1] = p': '合并：上一段右端延长到 `{p}`',
        'res.append': '结算一段 `[{last}, {p}]`，平均高度 `{s} // {cnt} = {s//cnt}`（向下取整）',
        'last = p': '`last` 移到 `{last}`，从这里开始下一段',
        'cnt += 1': '一栋楼开始：`cnt` → {cnt}',
        's += v': '高度和 `s` → =={s}==',
        'cnt -= 1': '一栋楼结束：`cnt` → {cnt}',
        's -= v': '高度和 `s` → =={s}==',
        'return res': '得到所有区间 `{res}`',
    },
    cards=dict(
        one_liner='排序左右边界，扫一遍维护楼数和高度和',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`buildings[i] = [start, end, height]`：街道上的建筑，覆盖 `[start, end)`',
                 '把街道分成最少的段，每段内楼的==平均高度相同==（向下取整），没有楼的段不输出',
                 '示例：`[[1,4,2],[3,9,4]]` → `[[1,3,2],[3,4,3],[4,9,4]]`'],
        quote='一趟排序，接下来一趟遍历，计算前缀的高度和以及建筑数目，然后计算平均高度即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['街道是数组，一栋楼 = 区间 `[l, r]` 加高度 `h`，离线用差分处理',
              '每栋楼两个事件，位置乘 2 做编码：左端偶数、右端奇数，一次排序搞定',
              '每经过一个位置，把 `[last, p]` 结算成一段；与上一段首尾相接且平均相同就合并'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '平均高度是整数除法：`s // cnt`；合并时要同时判断相接和平均值相同',
                 '`cnt = 0` 的空隙不能输出，所以结算条件里有 `cnt > 0`',
                 '原文为 Python 2 写法，`/` 整数除法已改为 `//`（共 2 处）'],
    ),
)
