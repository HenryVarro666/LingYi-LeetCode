_SC = [5, 2, 9, 8, 4]
_POS = {0: (0.08, 0.55), 1: (0.33, 0.0), 2: (0.5, 0.6), 3: (0.92, 0.15), 4: (0.85, 1.0)}
_E = [(0, 1), (1, 2), (2, 3), (0, 2), (2, 4)]


def _gdraw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 2), '黄 = 中间边 x-y　粉 = p（x 的邻居）　青 = q（y 的邻居）　节点下方 = 分数', 21, T['muted'], bold=True)
    W, Hh = x1 - x0 - 140, y1 - y0 - 190
    pt = {k: (x0 + 70 + p[0] * W, y0 + 70 + p[1] * Hh) for k, p in _POS.items()}
    inn = S.get('_inner', {})
    search = 'res' in S
    x, y = (inn.get('x'), inn.get('y')) if search else (None, None)
    ln = S.get('_line', 0)
    p = inn.get('p', inn.get('p1')) if search and ln > 30 else None
    q = inn.get('q', inn.get('q1')) if search and ln > 36 else None
    for u, v in _E:
        hot = search and x is not None and {u, v} == {x, y}
        cv.line([pt[u], pt[v]], T['yellow'] if hot else T['dim'], 6 if hot else 3)
    for a, b, col in ((p, x, 'pink'), (y, q, 'cyan')):
        if a is not None and b is not None and a != b:
            cv.line([pt[a], pt[b]], T[col], 5)
    for k, (px, py) in pt.items():
        ol, fill, tc = T['border'], T['panel2'], T['text']
        if search and k in (x, y):
            ol = T['yellow']
        if search and k == p:
            ol, fill, tc = T['pink'], T['pink'], T['bg']
        if search and k == q and k != p:
            ol, fill, tc = T['cyan'], T['cyan'], T['bg']
        cv.d.ellipse((px - 32, py - 32, px + 32, py + 32), fill=fill, outline=ol, width=5)
        cv.text((px, py), k, 32, tc, anchor='mm', bold=True)
        cv.text((px, py + 50), f'分 {_SC[k]}', 22, T['muted'], anchor='mm')


def _tab(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 2), '每个点分数最大的三个邻居（None = 没有）', 22, T['muted'], bold=True)
    f, s, t = S.get('first'), S.get('second'), S.get('third')
    if f is None:
        return
    inn = S.get('_inner', {})
    search = 'res' in S
    hx, hy = (inn.get('x'), inn.get('y')) if search else (None, None)
    cur = None
    cw = (x1 - x0 - 150) / 3
    for j, nm in enumerate(('first', 'second', 'third')):
        cv.text((x0 + 150 + j * cw + cw / 2, y0 + 52), nm, 24, T['muted'], anchor='mm', mono=True)
    rh = min(44, (y1 - y0 - 80) / len(f))
    for i in range(len(f)):
        yy = y0 + 70 + i * rh
        hot = i in (hx, hy)
        if hot:
            cv.rect((x0 + 10, yy, x1 - 10, yy + rh - 4), fill=T['panel2'], r=8)
        cv.text((x0 + 24, yy + rh / 2 - 2), f'点 {i}', 26, T['yellow'] if hot else T['text'], anchor='lm', bold=True)
        for j, arr in enumerate((f, s, t)):
            v = arr[i]
            txt = 'None' if v is None else f'{v}（分{_SC[v]}）'
            cv.text((x0 + 150 + j * cw + cw / 2, yy + rh / 2 - 2), txt, 24, T['dim'] if v is None else T['text'], anchor='mm')


def _first(U, W):
    def fn(S, B, ret):
        u, w = S[U], S[W]
        f = S['first'][u]
        if B['first'][u] is None:
            return f'`{u}` 还没有任何邻居 → `{w}`（分 {S["scores"][w]}）直接当第一名'
        o = B['first'][u]
        if S['scores'][o] < S['scores'][w]:
            return f'`{w}` 分 {S["scores"][w]} > 第一名 `{o}` 分 {S["scores"][o]} → ==成立==，抢走第一名'
        return f'`{w}` 分 {S["scores"][w]} 不比第一名 `{o}` 分 {S["scores"][o]} 大 → 去和第二名比'
    return fn


def _second(U, W):
    def fn(S, B, ret):
        u, w = S[U], S[W]
        o = S['second'][u]
        if o is None:
            return f'`{u}` 还没有第二名 → `{w}` 当第二名'
        if S['scores'][o] < S['scores'][w]:
            return f'`{w}` 分 {S["scores"][w]} > 第二名 `{o}` 分 {S["scores"][o]} → ==成立==，抢第二名'
        return f'`{w}` 分 {S["scores"][w]} 不比第二名 `{o}` 分 {S["scores"][o]} 大 → 去和第三名比'
    return fn


def _third(U, W):
    def fn(S, B, ret):
        u, w = S[U], S[W]
        o = S['third'][u]
        if o is None:
            return f'`{u}` 还没有第三名 → `{w}` 当第三名'
        if S['scores'][o] < S['scores'][w]:
            return f'`{w}` 分 {S["scores"][w]} > 第三名 `{o}` 分 {S["scores"][o]} → 顶掉第三名'
        return f'`{w}` 分 {S["scores"][w]} 连第三名 `{o}` 都不如 → 不收'
    return fn


CONFIG = dict(
    num=2242, title='节点序列的最大得分', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='枚举中间边 + 前三大邻居分类讨论',
    tags=['灵神题单·图论算法', '灵神题单·常用数据结构', '难度分 2304'],
    code='''
class Solution(object):
    def maximumScore(self, scores, edges):

        n = len(scores)
        first = [None] * n
        second = [None] * n
        third = [None] * n

        for x, y in edges:
            if first[x] is None or scores[first[x]] < scores[y]:
                first[x], second[x], third[x] = y, first[x], second[x]
            elif second[x] is None or scores[second[x]] < scores[y]:
                second[x], third[x] = y, second[x]
            elif third[x] is None or scores[third[x]] < scores[y]:
                third[x] = y
            
            if first[y] is None or scores[first[y]] < scores[x]:
                first[y], second[y], third[y] = x, first[y], second[y]
            elif second[y] is None or scores[second[y]] < scores[x]:
                second[y], third[y] = x, second[y]
            elif third[y] is None or scores[third[y]] < scores[x]:
                third[y] = x
        
        res = -1
        for x, y in edges:
            if second[x] is None or second[y] is None:
                continue
            
            if third[x] is None:
                if first[x] == y:
                    p = second[x]
                else:
                    p = first[x]

                if third[y] is None:
                    if first[y] == x:
                        q = second[y]
                    else:
                        q = first[y]
                    
                    if p == q:
                        continue
                    else:
                        res = max(res, scores[x] + scores[y] + scores[p] + scores[q])
                else:
                    if first[y] == x:
                        if second[y] == p:
                            q = third[y]
                        else:
                            q = second[y]
                    elif first[y] == p:
                        if second[y] == x:
                            q = third[y]
                        else:
                            q = second[y]
                    else:
                        q = first[y]
                    
                    res = max(res, scores[x] + scores[y] + scores[p] + scores[q])
            
            elif third[y] is None:
                if first[y] == x:
                    q = second[y]
                else:
                    q = first[y]
                
                if first[x] == y:
                    if second[x] == q:
                        p = third[x]
                    else:
                        p = second[x]
                elif first[x] == q:
                    if second[x] == y:
                        p = third[x]
                    else:
                        p = second[x]
                else:
                    p = first[x]
                
                res = max(res, scores[x] + scores[y] + scores[p] + scores[q])
            
            else:
                if first[x] == y:
                    p1, p2 = second[x], third[x]
                elif second[x] == y:
                    p1, p2 = first[x], third[x]
                else:
                    p1, p2 = first[x], second[x]
                
                if first[y] == x:
                    q1, q2 = second[y], third[y]
                elif second[y] == x:
                    q1, q2 = first[y], third[y]
                else:
                    q1, q2 = first[y], second[y]
                
                if p1 != q1:
                    res = max(res, scores[x] + scores[y] + scores[p1] + scores[q1])
                else:
                    res = max(res, scores[x] + scores[y] + scores[p1] + scores[q2], scores[x] + scores[y] + scores[p2] + scores[q1])
        
        return res
''',
    call='Solution().maximumScore([5, 2, 9, 8, 4], [[0, 1], [1, 2], [2, 3], [0, 2], [2, 4]])',
    expect=24,
    views=[
        dict(type='custom', draw=_gdraw, h=330),
        dict(type='custom', draw=_tab, h=260),
    ],
    watch=[('x-y', lambda S: f"{S['_inner']['x']}-{S['_inner']['y']}" if 'res' in S and 'x' in S['_inner'] else None, 'yellow'),
           ('p', lambda S: S['_inner'].get('p', S['_inner'].get('p1')) if 'res' in S else None, 'pink'),
           ('q', lambda S: S['_inner'].get('q', S['_inner'].get('q1')) if 'res' in S else None, 'cyan'),
           ('res', 'res', 'green')],
    skip=['for x, y in edges', 'n = len(scores)', 'first = [None]', 'second = [None]', 'third = [None]'],
    captions={
        'first[x] is None': _first('x', 'y'),
        'first[y] is None': _first('y', 'x'),
        'second[x] is None or scores': _second('x', 'y'),
        'second[y] is None or scores': _second('y', 'x'),
        'third[x] is None or scores': _third('x', 'y'),
        'third[y] is None or scores': _third('y', 'x'),
        'first[x], second[x], third[x] = y': '`{y}` 当第一名，原来的第一、第二名各降一位：`{first[x]}, {second[x]}, {third[x]}`',
        'first[y], second[y], third[y] = x': '`{x}` 当第一名，原来的第一、第二名各降一位：`{first[y]}, {second[y]}, {third[y]}`',
        'second[x], third[x] = y': '`{y}` 当第二名，原第二名降为第三：`{first[x]}, {second[x]}, {third[x]}`',
        'second[y], third[y] = x': '`{x}` 当第二名，原第二名降为第三：`{first[y]}, {second[y]}, {third[y]}`',
        'third[x] = y': '`{y}` 当 `{x}` 的第三名',
        'third[y] = x': '`{x}` 当 `{y}` 的第三名',
        'res = -1': '预处理完毕；`res = -1`，凑不出序列就返回 -1。下面枚举中间边 `x-y`',
        'second[x] is None or second[y] is None': lambda S, B, r: (
            f'边 `{S.x}-{S.y}`：`{S.x}` 或 `{S.y}` 只有一个邻居，凑不出 p-x-y-q → ==跳过==' if S.second[S.x] is None or S.second[S.y] is None
            else f'边 `{S.x}-{S.y}` 作中间：两端至少各有两个邻居，才可能凑出长度 4'),
        'continue': lambda S, B, r: ('p 和 q 是同一个点，序列长度不到 4 → 跳过这条边' if S.get('p') is not None and S.get('p') == S.get('q')
                                     else '跳过这条边'),
        'if third[x] is None': lambda S, B, r: (
            f'`third[{S.x}]` 为空 → `{S.x}` 除 y 外只剩一个 p 可选' if S.third[S.x] is None
            else f'`{S.x}` 有三个邻居，p 有备选'),
        'if first[x] == y': lambda S, B, r: (
            f'`first[{S.x}] = {S.first[S.x]}` 就是 `{S.y}` → p 只能取第二名' if S.first[S.x] == S.y
            else f'`first[{S.x}] = {S.first[S.x]}` 不是 `{S.y}` → p 取第一名'),
        'p = second[x]': '`p = second[{x}] = {p}`',
        'p = first[x]': '`p = first[{x}] = {p}`',
        'if third[y] is None': lambda S, B, r: (
            f'`third[{S.y}]` 也为空 → q 也只有一种选择' if S.third[S.y] is None else f'`{S.y}` 有三个邻居，q 有备选，p、q 撞了还能换'),
        'if first[y] == x': lambda S, B, r: (
            f'`first[{S.y}] = {S.first[S.y]}` 就是 x → q 不能取它' if S.first[S.y] == S.x
            else f'`first[{S.y}] = {S.first[S.y]}` 不是 x → 先看它是不是 p'),
        'elif first[y] == p': lambda S, B, r: (
            f'`first[{S.y}] = {S.first[S.y]}` 恰好是 p → 要避开' if S.first[S.y] == S.p
            else f'`first[{S.y}] = {S.first[S.y]}` 不是 p，也不是 x → 放心取它'),
        'q = first[y]': '`q = first[{y}] = {q}`',
        'q = second[y]': '`q = second[{y}] = {q}`',
        'if p == q': lambda S, B, r: (f'p = `{S.p}`，q = `{S.q}`：==同一个点==，凑不出长度 4' if S.p == S.q
                                      else f'p = `{S.p}`，q = `{S.q}`，不同 → 可以更新答案'),
        'res = max(res, scores[x] + scores[y] + scores[p] + scores[q])': '序列 `{p}-{x}-{y}-{q}`：`{scores[p]} + {scores[x]} + {scores[y]} + {scores[q]}` = {scores[p] + scores[x] + scores[y] + scores[q]} → `res = {res}`',
        'return res': '全部中间边枚举完，最大得分 =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='拉直成 p-x-y-q，枚举中间边，两端取最大且不重复',
        complexity='时间 `O(n+m)`，空间 `O(n)`',
        problem=['无向图，每点有分数；找长度为 4 的合法节点序列（相邻有边、点不重复）',
                 '返回序列分数和的最大值，没有则返回 `-1`',
                 '示例：`scores=[5,2,9,8,4]`，5 条边 → `24`'],
        quote='长度为4的序列拉直，就可以写成 p - x - y - q ……通常的做法就是枚举中间这一项，然后想办法求出在这种情况下两边的最优解。',
        quote_src='—— yiduobo 题解',
        idea=['数据大，只有一次枚举的机会：枚举中间的边 `x-y`，问题变成挑 p、q',
              'p、q 不能和 x、y 或彼此重复 → 预处理每个点分数最大的==前三个==邻居',
              '再按「第三名是否存在、第一名是不是 y」分类讨论，挑出合法的最优 p、q'],
        result='最大得分 24',
        summary=['时间 `O(n+m)`，空间 `O(n)`',
                 '只需前三大：p 要躲开 y 和 q，最多占掉两个名额',
                 '`second[x]` 或 `second[y]` 为空时，这条边凑不出长度 4，直接跳过',
                 '分类很多，易错：first/second 恰好是 y 或 x 时要往后顺延一位',
                 '原文本身可直接在 Python 3 运行，未作修改'],
    ),
)
