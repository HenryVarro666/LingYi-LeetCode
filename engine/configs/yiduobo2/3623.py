PTS = [[0, 0], [2, 0], [1, 1], [3, 1], [4, 1], [0, 2], [3, 2]]
MOD = 10 ** 9 + 7


def _phase(S):
    ln = S.get('_line', 0)
    if ln in (7, 8):
        return 'count'
    if 11 <= ln <= 15:
        return 'row'
    if ln >= 17:
        return 'end'
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ph = _phase(S)
    cv.text((x0 + 18, y0 + 4), '点按 y 分组（黄 = 当前，绿 = 已处理）', 22, T['muted'], bold=True)
    xs = [p[0] for p in PTS]
    ys = sorted({p[1] for p in PTS})
    gx0, gx1 = x0 + 150, x1 - 300
    gy0, gy1 = y0 + 70, y1 - 45
    xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)

    def X(v):
        return gx0 + (v - xmin) / max(1, xmax - xmin) * (gx1 - gx0)

    def Y(v):
        return gy1 - (v - ymin) / max(1, ymax - ymin) * (gy1 - gy0)

    cnt = S.get('cnt') or {}
    cur_row = S.get('y') if ph == 'row' else None
    done = set()
    if ph == 'row':
        for k in cnt:
            if k == cur_row:
                break
            done.add(k)
    elif ph == 'end':
        done = set(cnt)
    cur_pt = (S.get('x'), S.get('y')) if ph == 'count' else None
    counted = set()
    if ph == 'count':
        for p in PTS:
            counted.add(tuple(p))
            if tuple(p) == cur_pt:
                break
    elif ph in ('row', 'end'):
        counted = {tuple(p) for p in PTS}

    for yv in ys:
        c = T['yellow'] if yv == cur_row else T['green'] if yv in done else T['border']
        cv.line([(gx0 - 40, Y(yv)), (gx1 + 40, Y(yv))], c, 3 if c != T['border'] else 2)
        cv.text((x0 + 30, Y(yv)), f'y = {yv}', 24, c if c != T['border'] else T['muted'], anchor='lm', bold=True)
        if ph in ('row', 'end') and yv in cnt:
            n = cnt[yv]
            ly = n * (n - 1) // 2
            cv.text((gx1 + 60, Y(yv)), f'line_y = {ly}，共线对 {ly * (ly - 1) // 2}', 22,
                    c if c != T['border'] else T['muted'], anchor='lm', bold=True)
    for px, py in PTS:
        if (px, py) == cur_pt:
            c = T['yellow']
        elif py == cur_row:
            c = T['yellow']
        elif py in done:
            c = T['green']
        elif (px, py) in counted:
            c = T['blue']
        else:
            c = T['dim']
        r = 13
        cv.d.ellipse((X(px) - r, Y(py) - r, X(px) + r, Y(py) + r), fill=c)


def _formula(S):
    ph = _phase(S)
    if ph in ('row', 'end') and 'line' in S:
        r = S['res']
        neg = r - MOD if r > MOD // 2 else r
        return f"`res` 当前为 `{r}` ≡ =={neg}== (mod 10^9+7)；`line = {S['line']}`"
    return '答案 = C(line, 2) − Σ C(line_y, 2)：任选两条边，再减去==共线==的'


CONFIG = dict(
    num=3623, title='统计梯形的数目 I', difficulty='Medium', category='哈希',
    author='yiduobo', technique='哈希计数 + 容斥原理',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def countTrapezoids(self, points):

        cnt = {}
        res = 0
        line = 0
        for x, y in points:
            cnt[y] = cnt.get(y, 0) + 1

        mod = 10 ** 9 + 7
        for y in cnt:
            line_y = cnt[y] * (cnt[y] - 1) // 2
            line += line_y
            res += (mod - line_y * (line_y - 1) // 2 % mod)
            res %= mod

        res += line * (line - 1) // 2 % mod
        return res % mod
''',
    call=f'Solution().countTrapezoids({PTS})',
    expect=7,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='map', var='cnt', label='cnt：y → 这条水平线上的点数', h=130, fmt=lambda k, v: f'y={k}: {v}'),
    ],
    watch=['y', ('line_y', 'line_y', 'yellow'), ('line', 'line', 'green'), ('res', 'res', 'pink')],
    captions={
        'cnt = {}': '以 y 作为 key，用哈希表收集==同一水平线==上的点数',
        'res = 0': '`res` 存最终答案（会先减后加）',
        'line = 0': '`line` = 所有水平线上的==可用边总数==',
        'for x, y in points': lambda S, B, r: ('所有点都收集完了' if B.get('x') == S.x and B.get('y') == S.y
                                               else f'点 `({S.x}, {S.y})`'),
        'cnt[y] = cnt.get': '`cnt[{y}]` = {cnt[y]}',
        'mod = 10 ** 9 + 7': '准备容斥：总边数 `line` 和要减掉的共线方案',
        'for y in cnt': lambda S, B, r: ('所有水平线处理完毕' if S.y == list(S.cnt)[-1] and S.get('line_y') is not None and S.line == sum(v * (v - 1) // 2 for v in S.cnt.values())
                                         else f'处理水平线 `y = {S.y}`：上面有 `{S.cnt[S.y]}` 个点'),
        'line_y = cnt[y]': '任选两点成一条水平边：`line_y = {cnt[y]}×{cnt[y]-1}/2` = =={line_y}==',
        'line += line_y': '累加到总可用边数：`line` = {line}',
        'res += (mod - line_y': lambda S, B, r: (f'减去同一条线上选两条边的 `C({S.line_y}, 2) = {S.line_y * (S.line_y - 1) // 2}` 种（==共线不能成梯形==）；加 `mod` 保证非负'),
        'res %= mod': lambda S, B, r: f'`res %= mod` → `{S.res}`' + (f'，即 ==−{MOD - S.res}==（模意义下的负数）' if S.res > MOD // 2 else ''),
        'res += line * (line - 1)': '再加上任选两条边的 `C({line}, 2) = {line * (line - 1) // 2}` 种',
        'return res % mod': lambda S, B, r: f'取模：`{S.line * (S.line - 1) // 2}` − 共线 `{sum((v*(v-1)//2)*((v*(v-1)//2)-1)//2 for v in S.cnt.values())}` → 返回 =={r}==',
    },
    cards=dict(
        one_liner='任选两条水平边，减去两条边共线的方案（容斥）',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给 `n` 个互不相同的点 `points[i] = [x, y]`',
                 '==水平梯形==：至少有一对边平行于 x 轴的凸四边形',
                 '统计任选 4 点能组成多少个水平梯形，对 `10^9+7` 取模',
                 '示例：`[[0,0],[1,0],[0,1],[2,1]]` → `1`；本视频 7 个点 → `7`'],
        quote='平行四边形和矩形也算是水平梯形，也就是说这里只需要满足有两组不共线的水平边就行了。基于这一点，就可以==通过容斥原理来计算==。',
        quote_src='—— yiduobo 题解原文',
        idea=['同一 y 上 `cnt[y]` 个点 → `line_y = C(cnt[y], 2)` 条水平边，累加成 `line`',
              '任选两条边 `C(line, 2)`，==减去共线的== `Σ C(line_y, 2)`',
              '减法在模意义下做：`res += mod - x % mod` 保证不出现负数'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：两条边==在同一条水平线上==时组不成四边形，必须减掉',
                 '模意义减法要先加 `mod`；Python 虽不溢出，但这样写更通用',
                 '原文为 Python 2 写法，仅删去了类型注释的文档字符串'],
    ),
)
