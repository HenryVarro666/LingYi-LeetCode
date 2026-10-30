H, W = 5, 7
TREE, SQ, NUTS = [2, 2], [4, 4], [[3, 0], [2, 5]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cell = min(92, (x1 - x0 - 40) / W, (y1 - y0 - 50) / H)
    sx = x0 + ((x1 - x0) - cell * W) / 2
    sy = y0 + 20
    cur = (S['x'], S['y']) if 'x' in S and 'y' in S and 'res' in S else None
    for i in range(H):
        for j in range(W):
            cv.rect((sx + j * cell + 2, sy + i * cell + 2, sx + (j + 1) * cell - 2, sy + (i + 1) * cell - 2), fill=(36, 42, 52), r=6)
    tx, ty = sx + TREE[1] * cell + cell / 2, sy + TREE[0] * cell + cell / 2
    for n in NUTS:
        nx, ny = sx + n[1] * cell + cell / 2, sy + n[0] * cell + cell / 2
        hot = cur == (n[0], n[1])
        cv.line([(tx, ty), (nx, ny)], T['yellow'] if hot else T['border'], 3 if hot else 2)
        cv.rect((nx - cell * .3, ny - cell * .3, nx + cell * .3, ny + cell * .3), fill=T['yellow'] if hot else T['orange'], r=10)
        cv.text((nx, ny), '果', 30, T['bg'], anchor='mm', bold=True)
    cv.rect((tx - cell * .3, ty - cell * .3, tx + cell * .3, ty + cell * .3), fill=T['green'], r=10)
    cv.text((tx, ty), '树', 30, T['bg'], anchor='mm', bold=True)
    qx, qy = sx + SQ[1] * cell + cell / 2, sy + SQ[0] * cell + cell / 2
    cv.rect((qx - cell * .3, qy - cell * .3, qx + cell * .3, qy + cell * .3), fill=T['blue'], r=10)
    cv.text((qx, qy), '鼠', 30, T['bg'], anchor='mm', bold=True)
    if cur:
        nx, ny = sx + cur[1] * cell + cell / 2, sy + cur[0] * cell + cell / 2
        cv.dashed((qx, qy), (nx, ny), T['blue'], 3)


def _fn(S):
    if 'now' in S and 's' in S and 'x' in S:
        return (f"首颗是 ({S['x']},{S['y']})：`s − 树到它 + 鼠到它` = `{S['s']} − "
                f"{abs(TREE[0]-S['x'])+abs(TREE[1]-S['y'])} + {abs(SQ[0]-S['x'])+abs(SQ[1]-S['y'])}` = =={S['now']}==")
    if 's' in S:
        return f"`s` = 当前累计的距离 = =={S['s']}=="
    return ''


CONFIG = dict(
    num=573, title='松鼠模拟', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='枚举第一颗松果 · 通分式化简',
    code='''
class Solution(object):
    def minDistance(self, height, width, tree, squirrel, nuts):

        s = 0
        for x, y in nuts:
            s += abs(tree[0] - x) + abs(tree[1] - y)
        
        s += s
        res = None
        for x, y in nuts:
            now = s - abs(tree[0] - x) - abs(tree[1] - y) + abs(squirrel[0] - x) + abs(squirrel[1] - y)
            if res is None or res > now:
                res = now
        
        return res
''',
    call='Solution().minDistance(5, 7, [2,2], [4,4], [[3,0],[2,5]])',
    expect=12,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', fn=_fn, h=70),
    ],
    watch=[('s', 's', 'orange'), ('x', 'x'), ('y', 'y'), ('now', 'now', 'blue'), ('res', 'res', 'green')],
    captions={
        's = 0': '`s` 先累计「树到每颗松果」的单程距离',
        's += abs': '树到 `({x},{y})` 的曼哈顿距离 `{abs(tree[0]-x)+abs(tree[1]-y)}`，`s` = {s}',
        's += s': '除首颗外每颗都是「树→果→树」，要走两趟 → 先乘 2：`s` = =={s}==',
        'res = None': '`res` 记录最小总路程，先置空',
        'now = s': '假设首颗是 `({x},{y})`：`now = {s} − {abs(tree[0]-x)+abs(tree[1]-y)} + {abs(squirrel[0]-x)+abs(squirrel[1]-y)}` = =={now}==（少走一趟树→果，改成鼠→果）',
        'if res is None': lambda S, B, r: (f'`res` 为空 → 直接记下 {S.now}' if B.res is None else f'比较 `res = {B.res}` 与 `now = {S.now}`：' + ('==now 更小，更新答案==' if B.res > S.now else '不更小，保留')),
        'res = now': '更新答案：`res = {res}`',
        'return res': '最优首颗松果对应的最短路程：=={res}==',
    },
    cards=dict(
        one_liner='除首颗松果外，每颗都是树到果再回树，走两趟',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['网格里有一棵树、一只松鼠和若干松果，松鼠一次只能带一颗松果回树',
                 '松鼠可从任意位置出发，每步走上下左右一格',
                 '求把所有松果送回树的最短步数',
                 '示例：树 `[2,2]`，松鼠 `[4,4]`，松果 `[[3,0],[2,5]]` → `12`'],
        quote='因此最终答案就是 松鼠到某颗松果的距离 + 这颗松果到树的距离 + 树到其他所有松果的距离 * 2',
        quote_src='—— yiduobo 题解原文',
        idea=['先给每颗松果都按「树往返」算两趟，总和为常数 `C`',
              '首颗松果那趟是「鼠到果 + 果到树」，比往返少 `树到果`，多 `鼠到果`',
              '所以总路程 = `C − 树到首颗 + 鼠到首颗`，枚举首颗取最小'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`s += s` 后 `s` 已是两倍，再减去的是「单程」距离',
                 '距离用曼哈顿距离，不涉及障碍',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
