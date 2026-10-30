def _out(name):
    def f(S, B, r):
        t, c = S['trees'][S[name]], S['center']
        d = ((t[0] - c[0]) ** 2 + (t[1] - c[1]) ** 2) ** 0.5
        return (f"树 {name} 到圆心距离 `{d:.2f}`，半径 `{S['radius']:.2f}` → " +
                ('==在圆外==，圆必须扩大' if d > S['radius'] else '在圆内（或圆上），跳过'))
    return f


def _col(S, B, r):
    a, b, c, d = S['a'], S['b'], S['c'], S['d']
    return f"判断三点是否共线：`b*c = {b*c}`，`a*d = {a*d}` → " + ('==共线==，取最远两点的中点' if b * c == a * d else '==不共线==，解 i、j、k 三点的外接圆')


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    tr = S['trees']
    n = len(tr)
    xs = [p[0] for p in tr]
    ys = [p[1] for p in tr]
    lo_x, hi_x, lo_y, hi_y = min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1
    span = max(hi_x - lo_x, hi_y - lo_y)
    u = min((x1 - x0 - 80) / span, (y1 - y0 - 200) / span)
    cx0 = x0 + 40 + ((x1 - x0 - 80) - u * span) / 2
    cy0 = y1 - 110
    P = lambda x, y: (cx0 + (x - lo_x) * u, cy0 - (y - lo_y) * u)
    cv.text((x0 + 18, y0 + 4), '树的位置（已打乱）· 黄圈 = 当前最小圆 · 橙 = i，青 = j，粉 = k', 22, T['muted'], bold=True)
    for k in range(int(lo_x), int(hi_x) + 1):
        cv.line([P(k, lo_y), P(k, lo_y + span)], T['border'], 1)
        cv.text((P(k, lo_y)[0], cy0 + 8), k, 18, T['dim'], anchor='mt', mono=True)
    for k in range(int(lo_y), int(hi_y) + 1):
        cv.line([P(lo_x, k), P(lo_x + span, k)], T['border'], 1)
        cv.text((P(lo_x, k)[0] - 8, P(lo_x, k)[1]), k, 18, T['dim'], anchor='rm', mono=True)
    ln = S.get('_line')
    c = S.get('center')
    r = S.get('radius')
    if c is not None and r is not None and r > 0:
        X, Y = P(c[0], c[1])
        cv.d.ellipse((X - r * u, Y - r * u, X + r * u, Y + r * u), outline=T['yellow'], width=4)
        cv.d.ellipse((X - 5, Y - 5, X + 5, Y + 5), fill=T['yellow'])
    elif c is not None:
        X, Y = P(c[0], c[1])
        cv.d.ellipse((X - 5, Y - 5, X + 5, Y + 5), fill=T['yellow'])
    I, J, K = S.get('i'), S.get('j'), S.get('k')
    act = {}
    if ln is not None and ln >= 21 and K is not None:
        act[K] = ('k', T['pink'])
    if ln is not None and ln >= 16 and J is not None:
        act[J] = ('j', T['cyan'])
    if ln is not None and ln >= 12 and I is not None:
        act[I] = ('i', T['orange'])
    for idx, p in enumerate(tr):
        X, Y = P(p[0], p[1])
        col = T['text']
        tag = ''
        if idx in act:
            tag, col = act[idx]
        cv.d.ellipse((X - 10, Y - 10, X + 10, Y + 10), fill=col if tag else (125, 133, 145))
        cv.text((X + 14, Y - 14), f'{idx}' + (f'={tag}' if tag else '') + f'({p[0]},{p[1]})', 19, col, anchor='lb', bold=bool(tag))
    if c is not None and r is not None:
        cv.text((x0 + 18, y1 - 60), f'圆心 ({c[0]:.2f}, {c[1]:.2f})  半径 {r:.2f}', 26, T['yellow'], bold=True)


CONFIG = dict(
    num=1924, title='安装栅栏 II', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='Welzl 最小圆覆盖',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution(object):
    def outerTrees(self, trees):

        random.shuffle(trees)
        center = trees[0][:]
        radius = 0.0
        n = len(trees)

        def dis(p1, p2):
            return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

        for i in range(n):
            if dis(trees[i], center) > radius:
                center = trees[i][:]
                radius = 0.0
                for j in range(i):
                    if dis(trees[j], center) > radius:
                        center[0] = (trees[i][0] + trees[j][0]) * 0.5
                        center[1] = (trees[i][1] + trees[j][1]) * 0.5
                        radius = dis(center, trees[i])
                        for k in range(j):
                            if dis(trees[k], center) > radius:
                                a = trees[i][0] - trees[j][0]
                                b = trees[i][1] - trees[j][1]
                                c = trees[i][0] - trees[k][0]
                                d = trees[i][1] - trees[k][1]
                                if b * c == a * d:
                                    di = dis(trees[i], trees[k])
                                    dj = dis(trees[j], trees[k])
                                    if di > dj:
                                        p = trees[i]
                                    else:
                                        p = trees[j]
                                    
                                    center[0] = (p[0] + trees[k][0]) * 0.5
                                    center[1] = (p[1] + trees[k][1]) * 0.5
                                else:
                                    e = ((trees[i][0] ** 2 - trees[j][0] ** 2) - (trees[j][1] ** 2 - trees[i][1] ** 2)) * 0.5
                                    f = ((trees[i][0] ** 2 - trees[k][0] ** 2) - (trees[k][1] ** 2 - trees[i][1] ** 2)) * 0.5
                                    center[0] = -(d * e - b *f) / (b * c - a * d)
                                    center[1] = -(a * f - c *e) / (b * c - a * d)

                                radius = dis(center, trees[i])
        
        return [center[0], center[1], radius]
''',
    setup='import random\nrandom.seed(0)',
    call='Solution().outerTrees([[0,0],[4,0],[2,3],[2,1]])',
    expect=[2.0, 0.833333, 2.166667],
    result_fn=lambda r: [round(v, 6) for v in r],
    views=[dict(type='custom', draw=_draw, h=600)],
    watch=['i', 'j', 'k', ('radius', lambda S: round(S['radius'], 3) if 'radius' in S else '-', 'yellow')],
    skip=['a = trees', 'b = trees', 'c = trees', 'd = trees', 'e = ((', 'f = (('],
    captions={
        'random.shuffle': '先随机打乱顺序：这是期望 `O(n)` 的前提，否则最坏 `O(n^3)`',
        'center = trees[0][:]': '初始圆：圆心取第一棵树，半径 0',
        'for i in range': lambda S, B, r: ('依次处理第 `{}` 棵树'.format(S['i']) if S['i'] != B.get('i') or B.get('i') is None else '树都处理完了，最小圆就是当前的圆'),
        'if dis(trees[i], center) > radius': _out('i'),
        'center = trees[i][:]': '定理：圆外的点一定在新圆的边上 → 新圆过树 `i`，先以它为圆心，回头扫前面的树',
        'for j in range': lambda S, B, r: ('回头检查第 `{}` 棵树'.format(S['j']) if S['j'] != B.get('j') or B.get('j') is None else '前面的树都检查完，回到外层'),
        'if dis(trees[j], center) > radius': _out('j'),
        'center[0] = (trees[i][0] + trees[j][0]) * 0.5': '新圆过 i、j 两点：圆心横坐标取 i、j 的中点 `{center[0]}`',
        'center[1] = (trees[i][1] + trees[j][1]) * 0.5': '圆心取 i、j 的中点 `({center[0]}, {center[1]})`',
        'radius = dis(center, trees[i])': lambda S, B, r: '半径 = 圆心到树 i 的距离（圆过 i 点）',
        'for k in range': lambda S, B, r: ('再回头检查第 `{}` 棵树'.format(S['k']) if S['k'] != B.get('k') or B.get('k') is None else '检查完毕，回到外层'),
        'if dis(trees[k], center) > radius': _out('k'),
        'if b * c == a * d': _col,
        'center[0] = -(d * e': '外接圆：解线性方程得圆心横坐标 `{center[0]:.3f}`',
        'center[1] = -(a * f': '圆心 = `({center[0]:.3f}, {center[1]:.3f})`，到 i、j、k 三点等距',
        'return [center': '最小覆盖圆：圆心 `({center[0]:.3f}, {center[1]:.3f})`，半径 `{radius:.3f}`',
    },
    cards=dict(
        one_liner='先随机打乱，再逐点增量维护最小覆盖圆',
        complexity='期望时间 `O(n)`，空间 `O(1)`',
        problem=['平面上有一些树，用一个最小的圆把所有树围起来',
                 '返回圆心坐标和半径 `[x, y, r]`',
                 '示例：`[[1,1],[2,2],[2,0],[2,4],[3,3]]` → `[2, 2, 2]`','本视频：`[[0,0],[4,0],[2,3],[2,1]]`，需要三点定圆'],
        quote='对于当前遍历到的点，若其在已经得到的最小圆中，那么就跳过该点，否则就以新遍历到的点作为新圆的圆心，然后回过头去遍历之前已经遍历过的点。',
        quote_src='—— yiduobo 题解原文',
        idea=['定理：圆外一点 p，覆盖「原来的点 + p」的最小圆一定经过 p',
              '第 i 个点在圆外 → 新圆过 i；回头扫 j，j 在圆外 → 新圆过 i、j',
              '再回头扫 k，k 还在圆外 → 新圆过 i、j、k 三点（外接圆）'],
        summary=['期望 `O(n)`，最坏 `O(n^3)`，所以==必须先 shuffle==',
                 '三点共线时不能解外接圆，取最远两点的中点为圆心',
                 '原文为 Python 2 风格，本视频只补了 `random.seed(0)`，保证打乱结果固定',
                 '半径是浮点数，对拍时要允许误差'],
    ),
)
