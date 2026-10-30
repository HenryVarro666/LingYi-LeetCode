PTS = [[0, 0], [2, 0], [3, 1], [1, 1]]


def _plot(cv, S, B, box, T):
    x0, y0, x1_, y1_ = box
    cv.text((x0 + 18, y0 + 4), '点与当前枚举的点对（黄线 = 当前点对，灰线 = 已处理的点对）', 22, T['muted'], bold=True)
    gx0, gy0, gx1, gy1 = x0 + 60, y0 + 60, x1_ - 60, y1_ - 50
    maxx = max(p[0] for p in PTS) + 1
    maxy = max(p[1] for p in PTS) + 1
    s = min((gx1 - gx0) / maxx, (gy1 - gy0) / maxy)

    def P(x, y):
        return gx0 + x * s, gy1 - y * s
    for xx in range(maxx + 1):
        cv.line([P(xx, 0), P(xx, maxy)], T['border'], 1)
        cv.text((P(xx, 0)[0], gy1 + 6), xx, 18, T['dim'], anchor='mt', mono=True)
    for yy in range(maxy + 1):
        cv.line([P(0, yy), P(maxx, yy)], T['border'], 1)
        cv.text((gx0 - 10, P(0, yy)[1]), yy, 18, T['dim'], anchor='rm', mono=True)
    pts = S['points']
    i = S.get('i')
    cur = None
    if i is not None and 'x2' in S and 9 <= S.get('_line', 0) <= 40:
        cur = ((S['x1'], S['y1']), (S['x2'], S['y2']))
    if i is not None:
        for a in range(i + 1):
            for b in range(a + 1, len(pts)):
                if a < i or (cur and b < pts.index(list(cur[1]))):
                    cv.line([P(*pts[a]), P(*pts[b])], (90, 98, 110), 2)
    if cur:
        cv.line([P(*cur[0]), P(*cur[1])], T['yellow'], 5)
    for px_, py_ in pts:
        px, py = P(px_, py_)
        col, r = T['text'], 13
        if cur and (px_, py_) in cur:
            col, r = T['yellow'], 17
        cv.rect((px - r, py - r, px + r, py + r), fill=col, r=r)
        cv.text((px + 20, py - 28), f'({px_},{py_})', 18, T['muted'], mono=True)


def _fmt(k, v):
    return f'{k}: ' + ' '.join(f'({c},{g},{d})' for c, g, d in v)


def _txt(S):
    if 'A' in S and 'B' in S and 'C' in S and 9 <= S.get('_line', 0) <= 40 and 'x2' in S:
        return f"直线 {S['A']}x + {S['B']}y + {S['C']} = 0；(A,B) = ({S['A']},{S['B']}) 相同就平行或共线"
    if 'pair' in S and S.get('_line', 0) >= 45:
        return f"pair = {S['pair']}，同距离对 = {S.get('same_dis_pair', 0)}，共线且同距离对 = {S.get('same_line_same_dis_pair', 0)}"
    return '每个点对 → 直线 Ax+By+C=0，约成 (A,B,C/g) 后按 (A,B) 分组'


CONFIG = dict(
    num=3625, title='统计梯形的数目 II', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='标准式分组 · 容斥原理',
    tags=['灵神题单', '难度分 2643'],
    code='''
class Solution(object):
    def countTrapezoids(self, points):
        
        def gcd(x, y):
            while y > 0:
                x, y = y, x % y
            return x

        lines = {}
        for i, (x1, y1) in enumerate(points):
            for j, (x2, y2) in enumerate(points[i + 1:]):
                A = y1 - y2
                B = x2 - x1
                C = x1 * y2 - x2 * y1
                if A == 0 or B == 0:
                    g = max(abs(A), abs(B))
                else:
                    g = gcd(abs(A), abs(B))
                
                A //= g
                B //= g
                if A < 0:
                    A = -A
                    B = -B
                    C = -C
                elif A == 0 and B < 0:
                    B = -B
                    C = -C
                
                if C != 0:
                    t = gcd(g, abs(C))
                    g //= t
                    C //= t
                else:
                    g = 0
                
                key = (A, B)
                if key not in lines:
                    lines[key] = []
                lines[key].append((C, g, (x1 - x2) ** 2 + (y1 - y2) ** 2))

        pair = 0
        same_dis_pair = 0
        same_line_same_dis_pair = 0
        for key in lines:
            tot = len(lines[key])
            pair += tot * (tot - 1) // 2
            c_dict = {}
            dis_dict = {}
            all_dict = {}
            for C, g, dis in lines[key]:
                key_c = (C, g)
                c_dict[key_c] = c_dict.get(key_c, 0) + 1
                key_all = (C, g, dis)
                all_dict[key_all] = all_dict.get(key_all, 0) + 1 
                dis_dict[dis] = dis_dict.get(dis, 0) + 1
            
            for key_c in c_dict:
                same_line = c_dict[key_c]
                pair -= same_line * (same_line - 1) // 2
            
            for dis in dis_dict:
                same_dis = dis_dict[dis]
                same_dis_pair += same_dis * (same_dis - 1) // 2

            for key_all in all_dict:
                same_line_same_dis = all_dict[key_all]
                same_line_same_dis_pair += same_line_same_dis * (same_line_same_dis - 1) // 2

        return pair - same_dis_pair // 2 + same_line_same_dis_pair // 2
''',
    call='Solution().countTrapezoids(%r)' % PTS,
    expect=1,
    views=[
        dict(type='custom', draw=_plot, h=300),
        dict(type='text', h=70, fn=_txt),
        dict(type='map', var='lines', h=190, fmt=_fmt, font=20),
    ],
    watch=['i', 'A', 'B', 'C', ('pair', 'pair', 'green'), 'same_dis_pair', 'same_line_same_dis_pair'],
    captions={
        14: lambda S, B, r: f"点对 `({S.x1},{S.y1})`-`({S.x2},{S.y2})`：`{S['A']}x + {S['B']}y + {S['C']} = 0`",
        21: lambda S, B, r: f"`A`、`B` 同除 gcd `{S.g}` → `({S.A}, {S.B})`，平行线的 (A, B) 就会相同",
        37: lambda S, B, r: f"A 取正后 `({S.A}, {S.B})`；" + ('`C = 0` 过原点，记 `C/g = 0`' if S.C == 0 else f'`C/g = {S.C}/{S.g}` 用分数存'),
        40: '`(C, g, 距离平方 = {(x1 - x2) ** 2 + (y1 - y2) ** 2})` 记进 `lines[{key}]`：C/g 同 = 共线',
        47: '`key = {key}` 有 `{tot}` 条线段，任取两条：`pair` → =={pair}==（还含共线的）',
        60: '直线 `{key_c}` 上有 `{same_line}` 条：共线的对不是梯形，`pair` → =={pair}==',
        64: '长度平方 `{dis}` 的线段 `{same_dis}` 条，平行等长 → 平行四边形候选：`same_dis_pair` → =={same_dis_pair}==',
        68: '共线又等长的 `{same_line_same_dis}` 条被减了两次，加回：`same_line_same_dis_pair` → =={same_line_same_dis_pair}==',
        70: '`{pair} − {same_dis_pair}//2 + {same_line_same_dis_pair}//2` = =={ret}==：平行四边形数了两次，减一半',
    },
    skip=[5, 6, 7, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 30, 31, 32, 33, 34, 35, 38, 39,
          42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 53, 54, 55, 56, 58, 59, 62, 63, 66, 67],
    max_steps=80,
    cards=dict(
        one_liner='直线标准式分组，容斥减去平行四边形',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['给出平面上的点，求任选四个点能组成的==梯形==个数',
                 '梯形：凸四边形，至少有一对平行边',
                 '本视频：`[[0,0],[2,0],[3,1],[1,1]]`（平行四边形）→ `1`'],
        quote='对于所有(A, B)相同的直线对，如果二者不共线，那么就可以形成一个梯形，因此在这里可以使用直线对的总数，减去共线直线对的总数来进行计算。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个点对写成 `Ax + By + C = 0`，==(A, B) 约成互质==，C 用 `C/g` 的分数表示',
              '(A, B) 相同：要么平行要么共线；用直线对总数减去共线对数',
              '平行四边形、矩形被数了两次：减去「平行且长度相等」的对数的一半，再把共线重复减掉的加回'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`',
                 '易错点：C 不一定被 g 整除，所以存 `(C/t, g/t)` 作为分数',
                 '标准化符号：保证 `A > 0`，或 `A = 0` 时 `B > 0`',
                 '共线且等长的对被减了两次，最后要加回来',
                 '原文已是 Python 3 兼容写法（用的是 `//`），无需修改'],
    ),
)
