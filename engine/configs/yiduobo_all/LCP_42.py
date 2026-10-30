TOYS = [[3, 3, 1], [1, 1, 2]]
CIRCLES = [[4, 3]]
R = 2


def _caught(i):
    tx, ty, tr = TOYS[i]
    l = R - tr
    return tr <= R and any((cx - tx) ** 2 + (cy - ty) ** 2 <= l * l for cx, cy in CIRCLES)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '玩具（圆）与圈心（蓝点）：玩具被套中 ⇔ 有圈心落在半径 r−tr 的圆里', 22, T['muted'], bold=True)
    wx0, wx1, wy0, wy1 = -1, 6, -1, 5
    top, bot = y0 + 90, y1 - 50
    sc = min((x1 - x0 - 100) / (wx1 - wx0), (bot - top) / (wy1 - wy0))
    ox = x0 + 60 + ((x1 - x0 - 100) - sc * (wx1 - wx0)) / 2
    oy = top + ((bot - top) - sc * (wy1 - wy0)) / 2

    def P(x, y):
        return ox + (x - wx0) * sc, oy + (wy1 - y) * sc

    for gx in range(wx0, wx1 + 1):
        X = P(gx, 0)[0]
        cv.line([(X, P(0, wy1)[1]), (X, P(0, wy0)[1])], T['border'], 1)
        cv.text((X, P(0, wy0)[1] + 6), gx, 18, T['dim'], anchor='mt', mono=True)
    for gy in range(wy0, wy1 + 1):
        Y = P(0, gy)[1]
        cv.line([(P(wx0, 0)[0], Y), (P(wx1, 0)[0], Y)], T['border'], 1)
        cv.text((P(wx0, 0)[0] - 8, Y), gy, 18, T['dim'], anchor='rm', mono=True)
    live = 'tx' in S
    cur = -1
    if live:
        cur = TOYS.index([S['tx'], S['ty'], S['tr']])
    done_line = S.get('_line', 0) >= 24
    for i, (tx, ty, tr) in enumerate(TOYS):
        X, Y = P(tx, ty)
        fin = live and (i < cur or (i == cur and done_line))
        if i == cur:
            col = T['pink']
        elif fin:
            col = T['green'] if _caught(i) else T['red']
        else:
            col = T['muted']
        if fin and _caught(i):
            cv.d.ellipse((X - tr * sc, Y - tr * sc, X + tr * sc, Y + tr * sc), fill=mix2(T['green'], T['bg']))
        cv.d.ellipse((X - tr * sc, Y - tr * sc, X + tr * sc, Y + tr * sc), outline=col, width=4)
        cv.text((X, Y), f'({tx},{ty})', 18, col, anchor='mm', bold=True)
    if live and 'l' in S:
        X, Y = P(S['tx'], S['ty'])
        l = S['l']
        cv.d.ellipse((X - l * sc, Y - l * sc, X + l * sc, Y + l * sc), outline=T['yellow'], width=3)
        cv.text((X + l * sc * 0.72 + 8, Y - l * sc * 0.72 - 4) if l else (X + 16, Y + 14), f'r−tr={l}', 20, T['yellow'], bold=True)
        if 'x' in S and 'y' in S and not done_line:
            px, py = S['x'], S['y']
            Q = P(px, py)
            inside = (px - S['tx']) ** 2 + (py - S['ty']) ** 2 <= l * l
            hit = inside and (px, py) in set(map(tuple, CIRCLES))
            c = T['green'] if hit else (T['cyan'] if inside else T['dim'])
            cv.d.ellipse((Q[0] - 11, Q[1] - 11, Q[0] + 11, Q[1] + 11), outline=c, width=4)
    seen = 'circle_set' in S
    for cx, cy in CIRCLES:
        if seen and (cx, cy) in S['circle_set']:
            Q = P(cx, cy)
            cv.d.ellipse((Q[0] - 9, Q[1] - 9, Q[0] + 9, Q[1] + 9), fill=T['blue'])
            cv.text((Q[0] + 14, Q[1] + 8), f'({cx},{cy})', 18, T['blue'], bold=True)
    if live:
        cv.text(((x0 + x1) / 2, y0 + 44), f"当前玩具 ({S['tx']},{S['ty']}) 半径 {S['tr']}；圈半径 r = {R}，圈心只能在 r−tr = {R - S['tr']} 以内",
                20, T['text'], anchor='mt')


def mix2(c, bg):
    return tuple((a * 35 + b * 65) // 100 for a, b in zip(c, bg))


def _inside(S):
    return (S.x - S.tx) ** 2 + (S.y - S.ty) ** 2 <= S.l ** 2


CONFIG = dict(
    num='LCP 42', title='玩具套圈', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='哈希表 · 枚举整数圈心',
    tags=['计算几何'],
    code='''
class Solution(object):
    def circleGame(self, toys, circles, r):

        res = 0
        circle_set = set()
        for cx, cy in circles:
            circle_set.add((cx, cy))
        
        for tx, ty, tr in toys:
            if tr > r:
                continue
            
            l = r - tr
            flag = False
            for x in range(tx - l, tx + l + 1):
                if flag:
                    break
                for y in range(ty - l, ty + l + 1):
                    if (x - tx) ** 2 + (y - ty) ** 2 <= l ** 2 and (x, y) in circle_set:
                        flag = True
                        break
            
            if flag:
                res += 1
        
        return res
''',
    call='Solution().circleGame([[3,3,1],[1,1,2]], [[4,3]], 2)',
    expect=1,
    views=[dict(type='custom', draw=_draw, h=520), dict(type='set', var='circle_set', h=110,
                                                          fmt=lambda p: f'({p[0]},{p[1]})')],
    watch=[('tx', 'tx if "tx" in S else "-"', 'pink'), ('ty', 'ty if "ty" in S else "-"', 'pink'), ('l', 'l if "l" in S else "-"', 'yellow'),
           ('x', 'x if "x" in S else "-"', 'cyan'), ('y', 'y if "y" in S else "-"', 'cyan'),
           ('flag', 'flag if "flag" in S else "-"', 'orange'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记套中的玩具数',
        'circle_set = set()': '用哈希集合存==所有圈心==，查「某个整数点有没有圈心」是 `O(1)`',
        'for cx, cy': lambda S, B, r_: ('所有圈心都存好了' if 'cx' in B and B.cx == S.cx else f'取下一个圈的圆心 `({S.cx}, {S.cy})`'),
        'circle_set.add': '圈心 `({cx}, {cy})` 入集合',
        'for tx, ty, tr': lambda S, B, r_: ('所有玩具都处理完了' if 'tx' in B and B.tx == S.tx else f'处理玩具 `({S.tx}, {S.ty})`，半径 `{S.tr}`'),
        'if tr > r': lambda S, B, r_: (f'玩具半径 `{S.tr} > {S.r}`：圈比玩具还小，不可能套住' if S.tr > S.r
                                       else f'玩具半径 `{S.tr} ≤ {S.r}`：有可能被套住，继续'),
        'l = r - tr': '圈心离玩具中心不能超过 `r − tr = {r} − {tr}` = =={l}==，否则玩具会露出圈外',
        'flag = False': '`flag` 记录这个玩具有没有找到能套住它的圈心',
        'for x in': lambda S, B, r_: ('横坐标枚举结束' if 'x' in B and B.x == S.x else '') or f'枚举圈心横坐标 `x` = =={S.x}==（范围 `{S.tx - S.l}` 到 `{S.tx + S.l}`）',
        'if flag:': lambda S, B, r_: (('`flag` 为真，这个玩具被套中' if S.flag else '`flag` 为假：没有任何整数圈心能套住它') if S['_line'] == 23 else '已经找到圈心了 → 不用再枚举，跳出' if S.flag else '还没找到，继续枚举下一列'),
        'break': '找到了 → 跳出 `y` 循环',
        'for y in': lambda S, B, r_: ('这一列枚举完了，没有命中' if 'y' in B and B.y == S.y else '') or f'枚举圈心纵坐标 `y` = =={S.y}==，候选圈心 `({S.x}, {S.y})`',
        'if (x - tx)': lambda S, B, r_: (
            f'`({S.x}-{S.tx})² + ({S.y}-{S.ty})² = {(S.x - S.tx) ** 2 + (S.y - S.ty) ** 2}`，'
            + (f'`≤ l² = {S.l ** 2}`：在可套范围内；' if _inside(S) else f'`> l² = {S.l ** 2}`：超出范围，圈会漏掉玩具；')
            + (('`(x, y)` 在圈心集合里 → ==套中==' if (S.x, S.y) in S.circle_set else '但集合里没有这个圈心 → 不行')
               if _inside(S) else '不用查集合')),
        'flag = True': '这个玩具能被套住：`flag = True`',
        'res += 1': '套中数 `res` → =={res}==',
        'return res': '一共套中 `{res}` 个玩具',
    },
    cards=dict(
        one_liner='半径只有 10：枚举每个玩具周围的整数点，在集合里查有没有圈心',
        complexity='时间 `O(n·r²)`，空间 `O(m)`（`m` 为圈数）',
        problem=['平地上有若干玩具 `(x, y, 半径)`，扔了若干半径都为 `r` 的圈，圈心坐标已知',
                 '玩具被某个圈==完整==覆盖才算套中，多个圈套同一个只算一次',
                 '示例：`toys=[[3,3,1],[3,2,1]], circles=[[4,3]], r=2` → `1`',
                 '本视频：`toys=[[3,3,1],[1,1,2]]`，其余同上 → `1`'],
        quote='每个圆的半径都不超过10，同时所有圆的圆心都处在整数点上，那么在这里就可以将所有圈的圆心先加入到哈希表，然后对于每个玩具，枚举所有可以套到这个玩具的整数圆心。',
        quote_src='—— yiduobo 题解原文',
        idea=['大圆 `(x1,y1,r1)` 盖住小圆 `(x2,y2,r2)` ⇔ 圆心距 `≤ r1 − r2`，平方后免开根',
              '于是圈心必须落在以玩具为中心、半径 `r − tr` 的圆里，整数点至多 `O(r²)` 个',
              '枚举这些整数点，查哈希集合；一旦命中就 `break`，该玩具只计一次'],
        summary=['时间 `O(n·r²)`（`r ≤ 10`，每个玩具最多约 400 个点），空间 `O(m)`',
                 '易错：`tr > r` 要直接跳过；双层循环命中后要连同外层一起 `break`',
                 '正方形范围只是枚举上界，必须再用 `≤ l²` 过滤成圆',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需改动',
                 '对比灵神：灵神排序+二分，yiduobo 利用小半径直接哈希'],
    ),
)
