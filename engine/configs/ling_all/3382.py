XS = [1, 1, 3, 3, 1, 3]
YS = [1, 3, 1, 3, 2, 2]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = S.get('points')
    if not pts:
        return
    ux = sorted(set(p[0] for p in pts))
    uy = sorted(set(p[1] for p in pts))
    W, H = x1 - x0 - 120, y1 - y0 - 160
    gx = lambda x: x0 + 70 + (ux.index(x) / max(1, len(ux) - 1)) * W
    gy = lambda y: y1 - 50 - (uy.index(y) / max(1, len(uy) - 1)) * H
    cv.text((x0 + 18, y0 + 4), '点按 (x, y) 排序后依次加入树状数组（填色 = 已加入；黄 = 左点，粉 = 右点）', 22, T['muted'], bold=True)
    tree = S.get('tree')
    ys = S.get('ys')
    added = 0
    if tree is not None and ys:
        added = tree.pre(len(ys))
    cur = None
    if 'x2' in S and 'y2' in S:
        cur = ((S['x1'], S['y1']), (S['x2'], S['y2']))
    pre = S.get('pre') or {}
    if cur and 'cur' in S and S['x1'] == S['x2'] and S['y2'] in pre and pre[S['y2']][1] == S['y1']:
        lx = pre[S['y2']][0]
        ok = pre[S['y2']][2] + 2 == S['cur']
        c = T['green'] if ok else T['red']
        cv.rect((gx(lx), gy(S['y2']), gx(S['x2']), gy(S['y1'])), fill=c, alpha=45, outline=c, width=3)
    for x in ux:
        cv.text((gx(x), y1 - 28), x, 20, T['dim'], anchor='mt', mono=True)
    for y in uy:
        cv.text((x0 + 50, gy(y)), y, 20, T['dim'], anchor='rm', mono=True)
    for k, p in enumerate(pts):
        X, Y = gx(p[0]), gy(p[1])
        fill = T['blue'] if k < added else (46, 52, 62)
        ring = None
        if cur and p == cur[0]:
            ring = T['yellow']
        elif cur and p == cur[1]:
            ring = T['pink']
        cv.rect((X - 20, Y - 20, X + 20, Y + 20), fill=fill, r=20, outline=ring or T['border'], width=5 if ring else 1)
        cv.text((X, Y), k, 18, T['bg'] if k < added else T['dim'], anchor='mm', bold=True, mono=True)


def _cap_pair(S, B, ret):
    if B.get('y2') == S.y2 and B.get('x2') == S.x2:
        return '所有相邻点对都看完了 → 结束循环'
    if S.x1 == S.x2:
        return f'相邻两点 `({S.x1},{S.y1})`、`({S.x2},{S.y2})` ==同一列==：可能是矩形的一条竖边'
    return f'相邻两点 `({S.x1},{S.y1})`、`({S.x2},{S.y2})` 不在同一列'


def _cap_if(S, B, ret):
    y2 = S.y2
    if y2 not in S.pre:
        return f'`pre` 里还没有纵坐标 `{y2}` 的左边竖边：这条竖边先当“左边”存起来'
    lx, ly, c1 = S.pre[y2]
    if ly != S.y1:
        return f'左边竖边下端是 `{ly}`，和当前 `y1 = {S.y1}` 不一样：对不上'
    need = c1 + 2
    if need == S.cur:
        return f'左边竖边 `x = {lx}`：`C1 + 2 = {c1} + 2 = {need}` ==等于== `C2 = {S.cur}` → 新增的只有这两个角，==合法=='
    return f'左边竖边 `x = {lx}`：`C1 + 2 = {need}` ≠ `C2 = {S.cur}`，中间还夹着别的点 → ==不合法=='


CONFIG = dict(
    num=3382, title='用点构造面积最大的矩形 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='扫描线 + 树状数组数点（思路一）',
    tags=['常用数据结构', '难度分 2723'],
    code='''
# 树状数组模板
class Fenwick:
    def __init__(self, n: int):
        self.tree = [0] * (n + 1)

    def add(self, i: int) -> None:
        while i < len(self.tree):
            self.tree[i] += 1
            i += i & -i

    # [1,i] 中的元素和
    def pre(self, i: int) -> int:
        res = 0
        while i > 0:
            res += self.tree[i]
            i &= i - 1
        return res

    # [l,r] 中的元素和
    def query(self, l: int, r: int) -> int:
        return self.pre(r) - self.pre(l - 1)

class Solution:
    def maxRectangleArea(self, xCoord: List[int], yCoord: List[int]) -> int:
        points = sorted(zip(xCoord, yCoord))
        ys = sorted(set(yCoord))  # 离散化用

        ans = -1
        tree = Fenwick(len(ys))
        tree.add(bisect_left(ys, points[0][1]) + 1)  # 离散化
        pre = {}

        for (x1, y1), (x2, y2) in pairwise(points):  # 枚举矩形的右下角和右上角
            y = bisect_left(ys, y2) + 1  # 离散化
            tree.add(y)
            if x1 != x2:  # 两点不在同一列
                continue

            cur = tree.query(bisect_left(ys, y1) + 1, y)
            # 左下角为 pre[y2]
            if y2 in pre and pre[y2][1] == y1 and pre[y2][2] + 2 == cur:
                ans = max(ans, (x2 - pre[y2][0]) * (y2 - y1))
            pre[y2] = (x1, y1, cur)

        return ans
''',
    call=f'Solution().maxRectangleArea({XS}, {YS})',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='tree.tree', label='树状数组 tree.tree（下标 1..len(ys) 对应离散化后的纵坐标）', h=150, cell=80),
        dict(type='map', var='pre', label='pre：纵坐标 y2 → (左下角 x, y1, C1)', fmt=lambda k, v: f'{k}: {v}', h=130, font=26),
    ],
    watch=[('ys', 'ys', 'cyan'), ('cur', 'cur', 'orange'), ('ans', 'ans', 'green')],
    skip=['self.tree[i] += 1', 'i += i & -i', 'while i', 'res += self.tree[i]', 'i &= i - 1',
          'return res', 'res = 0', 'return self.pre', 'self.tree = [0]', 'y = bisect_left'],
    captions={
        'points = sorted': '按横坐标、再按纵坐标排序：同一列的点相邻，竖边就是相邻两点',
        'ys = sorted': '纵坐标离散化：`ys = {ys}`',
        'ans = -1': '`ans = -1`：找不到合法矩形就返回 -1',
        'tree = Fenwick': '树状数组==只存纵坐标==：`tree` 里的点已按横坐标 ≤ 当前 x 加入',
        'tree.add(bisect_left(ys, points[0][1])': '先加入第一个点 `{points[0]}`',
        'pre = {}': '`pre[y2]`：以 y2 为上端的“左边竖边”：`(x, y1, C1)`',
        'for (x1, y1), (x2, y2)': _cap_pair,
        'tree.add(y)': '把右点 `({x2},{y2})` 的纵坐标加进树状数组',
        'if x1 != x2': lambda S, B, r: ('两点不在同一列 → 不是竖边，`continue`' if S.x1 != S.x2
                                         else '同一列 → 它是一条竖边，往下算它夹住多少点'),
        'cur = tree.query': '`cur`：横坐标 ≤ `{x2}` 且纵坐标在 `[{y1}, {y2}]` 的点数 = `{cur}`',
        'if y2 in pre': _cap_if,
        'ans = max': '面积 `({x2} − {pre[y2][0]}) × ({y2} − {y1})` → `ans = {ans}`',
        'pre[y2] = (x1, y1, cur)': '记下这条竖边：它可能是后面某个矩形的==左边==',
        'return ans': '最大面积 = =={ret}==',
    },
    max_steps=80,
    cards=dict(
        one_liner='竖边夹住的点数，增加量刚好是 2，矩形里就没有别的点',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['平面上有 `n` 个点，选 4 个点作为轴平行矩形的顶点',
                 '矩形内部和边界上==不能有其他点==，求最大面积，没有则 `-1`',
                 '本视频：`x=[1,1,3,3,1,3]`，`y=[1,3,1,3,2,2]` → `2`'],
        quote='计算横坐标 ≤ x1 且纵坐标在 [y1,y2] 中的点的个数，记作 pre。然后计算横坐标 ≤ x2 且纵坐标在 [y1,y2] 中的点的个数，记作 cur。如果 pre+2 = cur，说明新增的 2 个点是矩形的右下角和右上角。',
        quote_src='—— 灵茶山艾府题解（思路一）',
        idea=['排序后遍历，把纵坐标加进树状数组；同一列相邻两点就是一条竖边',
              '先遇到左边竖边，记下它夹住的点数 `C1`；再遇到右边竖边，数出 `C2`',
              '`C1 + 2 = C2` ⇒ 两条竖边之间没有别的点，更新面积'],
        summary=['时间 `O(n log n)`（排序 + 树状数组），空间 `O(n)`',
                 '易错：相邻两点既可能是某个矩形的右边，也可能是另一个矩形的左边，==两件事都要做==',
                 '易错：必须检查 `pre[y2][1] == y1`，左右两条竖边的上下端要对齐',
                 '题解还有思路二：预处理每点正下/正左的点，再离线二维数点；本视频演示思路一',
                 '原题 3380（数据小）同理，数点用暴力即可'],
    ),
)
