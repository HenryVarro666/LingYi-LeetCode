TOYS = [[3, 3, 1], [5, 5, 3]]
CIRCLES = [[4, 3]]
R0 = 2


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '平面图（橙 = 玩具，白点 = 圈心，青环 = 圈心可以落的范围，粉点 = 正在试的整数点）', 22, T['muted'], bold=True)
    gx0, gy0, gx1, gy1 = x0 + 50, y0 + 60, x1 - 30, y1 - 40
    W = H = 9.0
    sc = min((gx1 - gx0) / W, (gy1 - gy0) / H)
    ox = gx0 + ((gx1 - gx0) - sc * W) / 2
    oy = gy1 - ((gy1 - gy0) - sc * H) / 2

    def P(x, y):
        return ox + x * sc, oy - y * sc

    for k in range(0, 10):
        cv.line([P(k, 0), P(k, 9)], T['border'], 1)
        cv.line([P(0, k), P(9, k)], T['border'], 1)
        cv.text((P(k, 0)[0], P(k, 0)[1] + 8), k, 20, T['dim'], anchor='mt', mono=True)
        cv.text((P(0, k)[0] - 10, P(0, k)[1]), k, 20, T['dim'], anchor='rm', mono=True)
    for t in TOYS:
        px, py = P(t[0], t[1])
        rr = t[2] * sc
        cur = 'tx' in S and 'ty' in S and (t[0], t[1]) == (S['tx'], S['ty'])
        cv.rect((px - rr, py - rr, px + rr, py + rr), fill=T['yellow'] if cur else T['orange'], alpha=150 if cur else 70,
                outline=T['yellow'] if cur else T['orange'], width=3, r=rr)
    if 'tx' in S and 'l' in S:
        px, py = P(S['tx'], S['ty'])
        rr = S['l'] * sc
        cv.rect((px - rr, py - rr, px + rr, py + rr), outline=T['cyan'], width=4, r=rr)
    for c in CIRCLES:
        px, py = P(c[0], c[1])
        cv.rect((px - 8, py - 8, px + 8, py + 8), fill=T['text'], r=8)
    if 'x' in S and 'y' in S and 'l' in S and S.get('_line') in (18, 19):
        px, py = P(S['x'], S['y'])
        cv.rect((px - 11, py - 11, px + 11, py + 11), outline=T['pink'], width=5, r=11)


CONFIG = dict(
    num='LCP 42', title='玩具套圈', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='圆心哈希集合 枚举整数点',
    tags=[],
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
    call='Solution().circleGame([[3,3,1],[5,5,3]], [[4,3]], 2)',
    expect=1,
    views=[
        dict(type='text', fn=lambda S: (f"`l = r − tr = {S['l']}`：圈心必须落在以玩具为中心、半径 `{S['l']}` 的圆内（再看是不是整数点）" if 'l' in S else '圈心都是整数点，玩具半径又小 → 枚举整数点')),
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=[('r', 'r', 'pink'), ('l', 'l', 'cyan'), ('x', 'x', 'yellow'), ('y', 'y', 'yellow'), ('flag', 'flag', 'blue'), ('res', 'res', 'green')],
    captions={
        'circle_set.add': '圈心 `({cx}, {cy})` 放进集合 → `circle_set = {circle_set}`',
        'for cx, cy in circles': lambda S, B, r_: ('圈心都放进集合了' if 'cx' in B and B['cx'] == S.cx and B['cy'] == S.cy else '先把所有圈心放进哈希集合，之后查一个点是不是圈心只要 `O(1)`'),
        'for tx, ty, tr in toys': lambda S, B, r_: ('所有玩具都枚举完了' if 'tx' in B and B['tx'] == S.tx and B['tr'] == S.tr else f'枚举玩具：圆心 `({S.tx}, {S.ty})`，半径 `{S.tr}`'),
        'if tr > r': lambda S, B, r_: (f'玩具半径 `{S.tr}` > 圈半径 `{S.r}`：怎么也套不住，跳过' if S.tr > S.r else f'玩具半径 `{S.tr}` <= 圈半径 `{S.r}`：有可能套住'),
        'l = r - tr': '套住的条件是 `圆心距 <= r - tr`：圈心得落在半径 `l = {l}` 的圆里',
        'flag = False': '`flag` 记这个玩具有没有被套中',
        'for x in range': lambda S, B, r_: ('这个玩具的所有列都枚举完了' if B.get('x') == S.x and 'x' in B else f'把圆外接成正方形，枚举横坐标 `x` 从 `{S.tx - S.l}` 到 `{S.tx + S.l}`：当前 `x = {S.x}`'),
        16: lambda S, B, r_: ('已经找到圈了，不用再枚举其他列' if S.flag else f'还没找到：继续看 `x = {S.x}` 这一列'),
        'for y in range': lambda S, B, r_: ('这一列的纵坐标枚举完了' if B.get('y') == S.y and 'y' in B and B.get('x') == S.x else f'枚举纵坐标：当前点 `({S.x}, {S.y})`'),
        'if (x - tx)': lambda S, B, r_: (f'点 `({S.x}, {S.y})` 离玩具 `{(S.x - S.tx) ** 2 + (S.y - S.ty) ** 2}` ' + ('<=' if (S.x - S.tx) ** 2 + (S.y - S.ty) ** 2 <= S.l ** 2 else '>') + f' `l^2 = {S.l ** 2}`，且' + ('在' if (S.x, S.y) in S.circle_set else '不在') + '集合里 → ' + ('==这里有圈，套中了==' if (S.x - S.tx) ** 2 + (S.y - S.ty) ** 2 <= S.l ** 2 and (S.x, S.y) in S.circle_set else '不行')),
        'flag = True': '找到可用的圈心，`flag = True`',
        'break': '这个玩具已经确定被套中，跳出',
        23: lambda S, B, r_: ('玩具被套中 → `res` 加一' if S.flag else '这个玩具没有被任何圈套中'),
        'res += 1': '`res` → {res}',
        'return res': '所有玩具都判断完，套中 `{res}` 个',
    },
    cards=dict(
        one_liner='半径只有 10：把圈心放进哈希表，只枚举玩具附近的整数点',
        complexity='时间 `O(n * r^2 + m)`，空间 `O(m)`',
        problem=['玩具 `[x, y, r]`，圈的半径都是 `r`，圈心 `[x, y]`',
                 '玩具被某个圈完整盖住就算套中，多个圈只算一个',
                 '本视频：玩具 `[3,3,1]`、`[5,5,3]`，圈心 `[4,3]`，`r = 2`，答案 `1`'],
        quote='每个圆的半径都不超过10，同时所有圆的圆心都处在整数点上，那么在这里就可以将所有圈的圆心先加入到哈希表，然后对于每个玩具，枚举所有可以套到这个玩具的整数圆心。',
        quote_src='—— yiduobo 题解原文',
        idea=['圈 `(xc, yc)` 套住玩具 `(xt, yt, rt)`：`(xc−xt)^2 + (yc−yt)^2 <= (r−rt)^2`',
              '等价于圈心落在以玩具为圆心、半径 `r − rt` 的圆里',
              '枚举外接正方形里的整数点，既在圆内又在哈希集合中就是套中'],
        summary=['时间 `O(n * r^2 + m)`，`r <= 10` 所以每个玩具只枚举至多 `21 × 21` 个点',
                 '用平方比较，避免开根号',
                 '找到一个圈就要同时跳出两层循环（`flag` + `break`）',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码无需改动'],
    ),
)
