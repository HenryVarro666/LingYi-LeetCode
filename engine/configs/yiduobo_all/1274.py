W, H = 4, 2
SHIPS = {(0, 1), (2, 0), (3, 1)}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    tr, bl = S.get('topRight'), S.get('bottomLeft')
    cv.text((x0 + 18, y0 + 4), '海域（黄点 = 船，粉框 = 当前递归的矩形，灰 = 已排除）', 22, T['muted'], bold=True)
    cell = min(130, (x1 - x0 - 480) / W, (y1 - y0 - 80) / H)
    sx = x0 + 40
    sy = y0 + 60
    sea = S.get('sea')
    log = sea.log if sea else []
    empty = [r for r, ok in log if not ok]
    for yy in range(H):
        for xx in range(W):
            X = sx + xx * cell
            Y = sy + (H - 1 - yy) * cell
            dead = any(b.x <= xx <= t.x and b.y <= yy <= t.y for (t, b) in empty)
            cv.rect((X + 4, Y + 4, X + cell - 4, Y + cell - 4), fill=(44, 50, 60) if dead else T['panel2'], r=10, outline=T['border'])
            cv.text((X + 10, Y + 8), f'{xx},{yy}', 16, T['dim'], mono=True)
            if (xx, yy) in SHIPS:
                cv.rect((X + cell * 0.3, Y + cell * 0.3, X + cell * 0.7, Y + cell * 0.7), fill=T['yellow'], r=int(cell * 0.2))
    if tr is not None and bl is not None:
        cv.rect((sx + bl.x * cell + 1, sy + (H - 1 - tr.y) * cell + 1, sx + (tr.x + 1) * cell - 1, sy + (H - bl.y) * cell - 1),
                outline=T['pink'], width=6, r=12)
    xr = sx + W * cell + 40
    cv.text((xr, sy), f"hasShips 已调用 {len(log)} 次", 26, T['text'], bold=True)
    cv.text((xr, sy + 44), '最近 4 次：', 22, T['muted'])
    for k, ((t, b), ok) in enumerate(log[-4:]):
        cv.text((xr, sy + 80 + k * 34), f"({b.x},{b.y})~({t.x},{t.y})  →  {'有船' if ok else '没有'}", 24,
                T['green'] if ok else T['red'], mono=True)
    if tr is not None and bl is not None:
        cv.text((xr, sy + 235), f"当前矩形 宽 {tr.x-bl.x+1} × 高 {tr.y-bl.y+1}", 26, T['pink'], bold=True)
        if 'flag' in S:
            cv.text((xr, sy + 275), f"flag = {S['flag']}", 22, T['cyan'])


CONFIG = dict(
    num=1274, title='矩形内船只的数目', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='二分递归 + hasShips', tags=[],
    code='''
class Solution(object):
    def countShips(self, sea, topRight, bottomLeft):

        def check(sea, topRight, bottomLeft, flag):
            if topRight.x < bottomLeft.x or topRight.y < bottomLeft.y:
                return 0
            
            if not flag and not sea.hasShips(topRight, bottomLeft):
                return 0
            
            if topRight.x == bottomLeft.x and topRight.y == bottomLeft.y:
                return 1
            
            if topRight.x - bottomLeft.x <= topRight.y - bottomLeft.y:
                mid_y = (topRight.y + bottomLeft.y) // 2
                top_cnt = check(sea, topRight, Point(bottomLeft.x, mid_y + 1), False)
                bottom_cnt = check(sea, Point(topRight.x, mid_y), bottomLeft, top_cnt == 0)
                return top_cnt + bottom_cnt
            
            else:
                mid_x = (topRight.x + bottomLeft.x) // 2
                right_cnt = check(sea, topRight, Point(mid_x + 1, bottomLeft.y), False)
                left_cnt = check(sea, Point(mid_x, topRight.y), bottomLeft, right_cnt == 0)
                return left_cnt + right_cnt
        
        return check(sea, topRight, bottomLeft, False)
''',
    setup='''
class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x},{self.y})"

class Sea(object):
    def __init__(self, ships):
        self.ships = ships
        self.log = []
    def hasShips(self, topRight, bottomLeft):
        ok = any(bottomLeft.x <= x <= topRight.x and bottomLeft.y <= y <= topRight.y for x, y in self.ships)
        self.log.append(((topRight, bottomLeft), ok))
        return ok
sea = Sea({(0, 1), (2, 0), (3, 1)})
''',
    call='Solution().countShips(sea, Point(3, 1), Point(0, 0))',
    expect=3,
    views=[
        dict(type='custom', h=400, draw=_draw),
        dict(type='calls', h=230, hide=('sea',)),
    ],
    watch=[('topRight', 'topRight'), ('bottomLeft', 'bottomLeft'), ('flag', 'flag', 'cyan'),
           ('top/right', 'top_cnt if "top_cnt" in S else right_cnt if "right_cnt" in S else None', 'green')],
    captions={
        'not flag and not sea.hasShips': lambda S, B, ret: (
            f"矩形 `{S['bottomLeft']}~{S['topRight']}`：`flag = True`，已知有船，==省掉这次 hasShips=="
            if S['flag'] else
            f"问 `hasShips({S['bottomLeft']}~{S['topRight']})` → " +
            ('==有船==，继续往下' if S['sea'].log[-1][1] else '==没有船==，整块剪掉，返回 0')),
        'topRight.x - bottomLeft.x <=': '宽 `{topRight.x - bottomLeft.x + 1}`、高 `{topRight.y - bottomLeft.y + 1}`：宽 ≤ 高就==横着切==（上半 / 下半），否则竖着切',
        'mid_y =': '横切线 `mid_y = {mid_y}`：上半区 `y ≥ {mid_y + 1}`，下半区 `y ≤ {mid_y}`',
        'mid_x =': '竖切线 `mid_x = {mid_x}`：右半区 `x ≥ {mid_x + 1}`，左半区 `x ≤ {mid_x}`',
        9: '这块没有船，返回 `0`，不用再往下切',
        12: '矩形缩成一个点且有船（上一步已问过）→ ==恰好 1 艘==，返回 `1`',
        16: '先递归上半区（还不知道有没有船，`flag = False`）',
        17: '`top_cnt = {top_cnt}`：' + '{"上半区没船 → 下半区必有船，传 ==flag=True== 省一次询问" if top_cnt == 0 else "上半区有船，再递归下半区，仍要询问"}',
        22: '先递归右半区（`flag = False`）',
        23: '`right_cnt = {right_cnt}`：' + '{"右半区没船 → 左半区必有船，传 ==flag=True== 省一次询问" if right_cnt == 0 else "右半区有船，再递归左半区，仍要询问"}',
        'return top_cnt': '两个半区的船数相加：`{top_cnt} + {bottom_cnt}` = =={ret}==',
        'return left_cnt': '两个半区的船数相加：`{left_cnt} + {right_cnt}` = =={ret}==',
        'return check(sea': '从整片海域开始递归',
    },
    skip=['topRight.x < bottomLeft.x or', 'topRight.x == bottomLeft.x and'],
    max_steps=110,
    cards=dict(
        one_liner='问一次 hasShips：没有就剪掉，有就切两半再问',
        complexity='询问次数约 `O(船数 × log(边长))`，空间 `O(log)`',
        problem=['给定一片海域和 `hasShips(右上, 左下)`：矩形里有船返回真',
                 '每个格子至多一艘船，`hasShips` 的调用次数有上限（≤ 400）',
                 '求海域内船的总数。示例：4×2 的海里 3 艘船 → `3`'],
        quote='非常标准的二分查找问题。对于一个给定区间，通过hasShips检测其中是否存在船只。若不存在，那么就不需要继续向下查找了，反之若存在，则可以根据区间的长宽将其分为上半区和下半区，或者左半区和右半区。',
        quote_src='—— yiduobo 题解',
        idea=['没船整块丢掉，有船就沿较长的边切成两半，分别递归求和',
              '面积为 0 返回 0；面积为 1 且有船，一定刚好一艘；1000×1000 在约 20 层内能定位一艘船',
              '优化：已知某半区没船，另一半必有船，直接传 `flag=True`，省一次询问'],
        summary=['询问次数 `O(k log n)`（k 为船数），递归栈深 `O(log n)`',
                 '易错：矩形宽/高为 0 要先返回 0；`mid` 是闭区间边界，另一半从 `mid+1` 开始',
                 '原文用 `/` 取中点（Python 2 整数除法），已改为 `//`',
                 '本题为 VIP 题，这里自己写了 `Point`、`Sea` 来模拟交互接口，原文头部的接口注释已删去'],
    ),
)
