SQ = [[0, 0, 2], [1, 1, 1], [3, 3, 1]]
TOT = sum(l * l for _, _, l in SQ)


def _plane(box):
    x0, y0, x1, y1 = box
    s = min((x1 - x0 - 140) / 4.6, (y1 - y0 - 120) / 4.4)
    ox, oy = x0 + 70, y1 - 50
    return s, ox, oy


def _draw(cv, S, B, box, T):
    s, ox, oy = _plane(box)
    cur = (S.get('y') if S.get('_line') == 12 else S.get('y2')) if 'area' in S and 'y2' in S else None
    sweep = S.get('y') if 'area' in S else None
    hit = cur is not None and 'sum_l' in S and S['area'] * 2 >= TOT and S.get('_line') in (14, 15)
    cv.text((box[0] + 18, box[1] + 4), '正方形（绿 = 扫描线下方已累计的部分，橙线 = 扫描线，黄线 = 答案水平线）', 22, T['muted'], bold=True)
    cv.line([(ox - 10, oy), (ox + 4.4 * s, oy)], T['border'], 2)
    for t in range(5):
        cv.text((ox - 18, oy - t * s), t, 20, T['dim'], anchor='rm', mono=True)
    for (x, y, l) in SQ:
        X0, X1 = ox + x * s, ox + (x + l) * s
        cv.rect((X0, oy - (y + l) * s, X1, oy - y * s), fill=T['panel2'], outline=T['border'], width=3)
        if cur is not None and cur > y:
            top = min(cur, y + l)
            cv.rect((X0 + 2, oy - top * s, X1 - 2, oy - y * s - 2), fill=T['green'], alpha=120)
        cv.text((X0 + 6, oy - (y + l) * s + 4), f'l={l}', 20, T['text'], anchor='la', bold=True)
    if cur is not None:
        cv.line([(ox - 10, oy - cur * s), (ox + 4.4 * s, oy - cur * s)], T['orange'], 4)
        cv.text((ox + 4.4 * s + 8, oy - cur * s), f'扫描线 y={cur}', 22, T['orange'], anchor='lm', bold=True)
    if hit:
        ay = S['y2'] - (S['area'] * 2 - TOT) / (S['sum_l'] * 2)
        cv.line([(ox - 10, oy - ay * s), (ox + 4.4 * s, oy - ay * s)], T['yellow'], 5)
        cv.text((ox + 4.4 * s + 8, oy - ay * s + 22), f'答案 {ay:.4f}', 22, T['yellow'], anchor='lm', bold=True)


def _top(S):
    if 'area' not in S:
        return '扫描线从下往上扫，线下面积一到总面积 `tot_area` 的一半，就找到答案'
    return f'扫过 `[{S["y"]}, {S["y2"]}]`：底边总长 `sum_l = {S["sum_l"]}`，累计面积 `area = {S["area"]}`，一半是 `{TOT / 2}`'


def _hit(S, B, ret):
    ok = S.area * 2 >= S.tot_area
    return (f'`area * 2 = {S.area * 2}` {">=" if ok else "<"} `tot_area = {S.tot_area}`：' +
            ('线下面积已超过一半 → 答案就在 `[y, y2]` 里，按线性关系解出来' if ok else '还不到一半 → 继续往上扫'))


CONFIG = dict(
    num=3453, title='分割正方形 I', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='差分 + 扫描线',
    tags=['灵神题单·二分算法', '灵神题单·常用数据结构', '难度分 1735'],
    code='''
class Solution:
    def separateSquares(self, squares: List[List[int]]) -> float:
        tot_area = 0
        diff = defaultdict(int)
        for _, y, l in squares:
            tot_area += l * l
            diff[y] += l
            diff[y + l] -= l

        area = sum_l = 0
        for y, y2 in pairwise(sorted(diff)):
            sum_l += diff[y]  # 矩形底边长度之和
            area += sum_l * (y2 - y)  # 底边长 * 高 = 新增面积
            if area * 2 >= tot_area:
                return y2 - (area * 2 - tot_area) / (sum_l * 2)
''',
    call=f'Solution().separateSquares({SQ})',
    expect=2 - (10 - 6) / 6,
    views=[
        dict(type='text', fn=_top, size=24, h=100),
        dict(type='custom', draw=_draw, h=470),
        dict(type='map', var='diff', label='diff：y → 底边长度的变化（下边 +l，上边 −l）', fmt=lambda k, v: f'y={k}: {v:+d}', h=130),
    ],
    watch=[('tot_area', 'tot_area', 'cyan'), ('y', 'y', 'blue'), ('y2', 'y2', 'orange'), ('sum_l', 'sum_l', 'pink'), ('area', 'area', 'green')],
    captions={
        'tot_area = 0': '`tot_area` 累计所有正方形面积之和（重叠要多次计算）',
        'diff = defaultdict': '`diff[y]`：扫描线越过高度 y 时，底边长度之和的变化量（差分）',
        'for _, y, l in squares': lambda S, B, r: (f'`tot_area = {S.tot_area}`，差分记录完毕' if B.get('y') == S.y and B.get('l') == S.l and 'l' in B
                                                   else f'正方形 `y = {S.y}`，边长 `l = {S.l}`'),
        'tot_area += l * l': '累加面积：`tot_area = {tot_area}`',
        'diff[y] += l': '扫描线到达这个正方形的下边 `y = {y}`：底边长度 `+{l}`',
        'diff[y + l] -= l': '扫到上边 `y + l = {y + l}`：底边长度 `-{l}`，所以==差分==记录',
        'area = sum_l = 0': '`area` 累计线下面积，`sum_l` 是当前扫描线处所有正方形的底边长度之和',
        'for y, y2 in pairwise': lambda S, B, r: (f'扫描线从 `y = {S.y}` 扫到下一个关键高度 `y2 = {S.y2}`' if B.get('y') != S.y or 'y' not in B else '所有关键高度都扫完了'),
        'sum_l += diff[y]': '`diff[{y}] = {diff[y]}`：到了 `y = {y}`，底边总长变为 `sum_l = {sum_l}`',
        'area += sum_l * (y2 - y)': '`y` 到 `y2` 之间底边长度不变 → 新增面积 `{sum_l} × ({y2} - {y}) = {sum_l * (y2 - y)}`，累计 `area = {area}`',
        'if area * 2 >= tot_area': _hit,
        'return y2 - (area': lambda S, B, r: f'线下面积在 `[y, y2]` 里是线性增加的，从 `y2` 往回退 `(area×2 − tot) / (sum_l×2) = {(S.area * 2 - S.tot_area)}/{S.sum_l * 2}`，答案 ==`{r:.5f}`==',
    },
    cards=dict(
        one_liner='水平扫描线从下往上扫，线下面积刚过一半时按线性关系解出答案',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`squares[i] = [x, y, l]` 是平行于坐标轴的正方形（左下角和边长），可以重叠，重叠处面积重复计算',
                 '求最小的水平线 `y`，使线上方的总面积等于线下方的总面积；误差 `1e-5` 内算对',
                 f'本视频：`squares = {SQ}` → `1.33333`'],
        quote='想象有一根水平扫描线在从下往上扫描……扫描的过程中，维护面积之和 area，底边长之和 sumL。设当前 y 与下一个 y\' 之差为 y\'-y，则新增面积为 sumL·(y\'-y)。',
        quote_src='—— 灵茶山艾府题解（方法三）',
        idea=['用差分记录每个高度处“底边长度之和”的变化：下边 `+l`，上边 `-l`',
              '排序后相邻两个高度之间，底边总长不变 → 新增面积 = 底边总长 × 高度差',
              '一旦 `area * 2 >= tot_area`，答案就在这一段，线性回推：`y2 - (area*2 - tot)/(sum_l*2)`'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '答案不一定落在某个关键高度上，要在最后一段里线性插值',
                 '重叠的正方形底边长度要累加，差分正好处理',
                 '题解还有方法一（浮点二分）和方法二（整数二分，乘 `M = 1e5`），复杂度 `O(n log(U/ε))`',
                 '同类：一维差分、扫描线（如天际线、矩形面积并）'],
    ),
)
