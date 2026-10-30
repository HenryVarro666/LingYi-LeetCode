SIZE = 4


def _nbrs(r, j, n):
    out = []
    if j % 2 == 1:
        k = (j + 1) // 2
        if k > 1:
            out.append((r, j - 1))
        if k < r:
            out.append((r, j + 1))
        if r < n:
            out.append((r + 1, j + 1))
    else:
        out += [(r, j - 1), (r, j + 1)]
        out.append((r - 1, j - 1))
    return out


def _oasis(trees, n):
    oa = set(trees)
    changed = True
    while changed:
        changed = False
        for r in range(1, n + 1):
            for j in range(1, 2 * r):
                if (r, j) not in oa and sum((a in oa) for a in _nbrs(r, j, n)) >= 2:
                    oa.add((r, j))
                    changed = True
    return oa


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = SIZE
    cv.text((x0 + 18, y0 + 4), '沙地三角形（绿 = 已种树，浅绿 = 被相邻绿洲带成绿洲，粉框 = 当前位置）', 22, T['muted'], bold=True)
    h = min((y1 - y0 - 175) / n, (x1 - x0 - 80) / n * 0.866)
    w = h / 0.866
    cx = (x0 + x1) / 2
    ty = y0 + 80
    trees = {tuple(p) for p in S.get('res', [])}
    oa = _oasis(trees, n) if trees else set()

    def pts(r, j):
        top = ty + (r - 1) * h
        bot = top + h
        if j % 2 == 1:
            k = (j + 1) // 2
            ax = cx - (r - 1) * w / 2 + (k - 1) * w
            return [(ax, top), (ax + w / 2, bot), (ax - w / 2, bot)], (ax, top + h * 0.62)
        m = j // 2
        lx = cx - (r - 1) * w / 2 + (m - 1) * w
        return [(lx, top), (lx + w, top), (lx + w / 2, bot)], (lx + w / 2, top + h * 0.35)

    for r in range(1, n + 1):
        for j in range(1, 2 * r):
            p, c = pts(r, j)
            fill = T['green'] if (r, j) in trees else (T['cyan'] if (r, j) in oa else T['panel2'])
            cv.poly(p, fill)
            cv.line(p + [p[0]], T['border'], 2)
            cv.text(c, f'{r},{j}', 17, T['bg'] if (r, j) in oa else T['dim'], anchor='mm', mono=True)
    if 'nowx' in S and S.get('_line', 0) >= 10:
        r, j = S['nowx'], S['nowy']
        if 1 <= r <= n and 1 <= j < 2 * r:
            p, c = pts(r, j)
            cv.line(p + [p[0]], T['pink'], 6)
    cv.text((x0 + 18, y0 + 36), f"已种 {len(trees)} 棵树；整张图被覆盖：{'是' if len(oa) == n * n else '否'}（{len(oa)}/{n * n}）", 24, T['text'], bold=True)


CONFIG = dict(
    num='LCP 70', title='沙地治理', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='贪心构造 · 之字形逐行种树',
    tags=[],
    code='''
class Solution(object):
    def sandyLandManagement(self, size):

        res = [[1, 1]]
        if size == 1:
            return res
        
        for index in range(1, size * 2, 2):
            res.append([size, index])
        
        nowx = size - 1
        nowy = 1
        d = 1
        bound = (size - 1) * 2
        near_flag = False
        while nowx != 1:
            #nowy为奇数表示当前位于正三角
            if nowy % 2 == 1:
                nowy += d
                #若nowy是当前行处理的最后一个正三角，那么就往上移动一行，同时之前的near_flag会因此而失效
                if nowy == bound:
                    d = -d
                    nowx -= 1
                    near_flag = False
                    if d > 0:
                        nowy = 2
                        bound = nowx * 2
                    else:
                        nowy = (nowx - 1) * 2
                        bound = 0

            #若当前位置是倒三角，且触发了near_flag
            elif near_flag:
                #特殊情况，即当前倒三角是本行的最后处理的倒三角
                if nowy + d + d == bound:
                    d = -d
                    nowx -= 1
                    if d > 0:
                        nowy = 1
                        bound = nowx * 2
                    else:
                        nowy = nowx * 2 - 1
                        bound = 0
                    
                    #将上一行的第一个处理的正三角种上树
                    if nowx > 1:
                        res.append([nowx, nowy])
                    nowy += d
                else:
                    nowy += d
                    near_flag = False
            
            #没有触发near_flag，那么就种树，并将near_flag置为true
            else:
                res.append([nowx, nowy])
                near_flag = True
                nowy += d
        
        return res
''',
    call='Solution().sandyLandManagement(4)',
    expect=[[1, 1], [4, 1], [4, 3], [4, 5], [4, 7], [3, 2], [2, 3]],
    skip=[13, 15, 22, 24],
    max_steps=90,
    views=[
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=[('nowx', lambda S: S.get('nowx'), 'blue'), ('nowy', lambda S: S.get('nowy'), 'pink'),
           ('d', lambda S: S.get('d')), ('bound', lambda S: S.get('bound')), ('near_flag', lambda S: S.get('near_flag'), 'orange'),
           ('树数', lambda S: len(S['res']), 'green')],
    captions={
        4: '先在顶角种一棵：`[1, 1]`。三个角只和一个三角形相邻，必须种树',
        5: '`size = {size}`，不是 1，继续',
        9: '最底下一行：隔一个种一棵，种在所有==正三角== `[{size}, {index}]`，倒三角会被左右两棵树带成绿洲',
        11: '从倒数第二行开始，自下而上之字形处理：`nowx = {nowx}`',
        12: '`nowy` 是行内编号，==奇数 = 正三角，偶数 = 倒三角==，从 1 开始',
        14: '`bound` 是本行处理的边界：走到它就要换行，初始 `{bound}`',
        27: '边界 `bound` → {bound}',
        30: '边界 `bound` → {bound}',
        40: '边界 `bound` → {bound}',
        43: '边界 `bound` → {bound}',
        16: lambda S, B, r: (f'还没处理到第 1 行：`nowx = {S.nowx}`，继续' if S.nowx != 1 else '`nowx = 1`：已回到顶端，结束'),
        18: lambda S, B, r: (f'`nowy = {S.nowy}` 是==正三角==：这里不种树（它的底边挨着下一行的绿洲倒三角），直接跳过' if S.nowy % 2 == 1
                              else f'`nowy = {S.nowy}` 是==倒三角==：看看有没有被相邻正三角影响（`near_flag`）'),
        19: '正三角不种，沿方向 `d = {d}` 走到下一个格子：`nowy` → {nowy}',
        21: lambda S, B, r: (f'`nowy = {S.nowy}` 等于 `bound = {S.bound}`：走到本行末端了 → 换到上一行' if S.nowy == S.bound
                              else f'`nowy = {S.nowy}` 还没到边界 `{S.bound}`，继续'),
        23: '往上一行：`nowx` → {nowx}，方向反转 `d` → {d}（之字形）',
        25: lambda S, B, r: ('新的一行从左往右（`d > 0`）：从倒三角 2 开始' if S.d > 0 else '新的一行从右往左（`d < 0`）：从最右边的倒三角开始'),
        26: '起点 `nowy` → {nowy}，边界 `bound` → {bound}',
        29: '起点 `nowy` → {nowy}，边界 `bound` → {bound}',
        33: lambda S, B, r: ('倒三角，而且 `near_flag = True`：它已被相邻的正三角影响到一条边，==这一格不种，留给下一个==' if S.near_flag
                              else '倒三角，`near_flag = False`：没被影响，==要种树=='),
        35: lambda S, B, r: (f'`nowy + d + d = {S.nowy + S.d + S.d}` 等于 `bound = {S.bound}`：这是本行最后处理的倒三角，没有下一个可以种了'
                              if S.nowy + S.d + S.d == S.bound else f'`nowy + d + d = {S.nowy + S.d + S.d}` ≠ `bound`：还有下一个倒三角可种，继续'),
        36: '特殊情况：换到上一行',
        37: '上一行：`nowx` → {nowx}',
        38: lambda S, B, r: ('新的一行从左往右' if S.d > 0 else '新的一行从右往左'),
        39: '`nowy` → {nowy}（行首的正三角），`bound` → {bound}',
        42: '`nowy` → {nowy}（行尾的正三角），`bound` → {bound}',
        46: '新一行里第一个处理的是正三角：到了顶行 `nowx = 1` 就不用补了（顶角已种）→ {"要补" if nowx > 1 else "不用补"}',
        47: '把新一行第一个处理的==正三角==种上，避免浪费：种 `[{nowx}, {nowy}]`',
        48: '继续沿方向走：`nowy` → {nowy}',
        50: '没种，往前走一格，并清掉标记：`nowy` → {nowy}，`near_flag = False`',
        55: '倒三角没被影响：==种树== `[{nowx}, {nowy}]`',
        56: '`near_flag = True`：这棵树把相邻两个正三角连起来了，下一个倒三角不用种',
        57: '往前走一格：`nowy` → {nowy}',
        59: '共种 `{len(res)}` 棵树',
    },
    cards=dict(
        one_liner='三个角必种；其余每隔一个种，不浪费相邻的那条边',
        complexity='时间 `O(size^2)`，空间 `O(1)`（不含输出）',
        problem=['边长为 `size` 的正三角形沙地，被分成 `size^2` 个小正三角形，行内编号从 1 开始',
                 '种树的三角形变成绿洲；==与至少两个绿洲三角形相邻（共边）的三角形也会变成绿洲==',
                 '求最少种多少棵树，让整片沙地都变成绿洲；返回任意一种种法。本视频：`size = 4`'],
        quote='首先，三角形的三个角都必须要种树，因为这三个位置只与另外一个三角形相邻。',
        quote_src='—— yiduobo 题解原文',
        idea=['贪心：三个角必种；已和绿洲相邻的三角形，不到万不得已不种，免得浪费共边',
              '底边先在所有正三角种树，倒三角自然变绿洲；再从倒数第二行起之字形往上',
              '用 `near_flag` 标记当前倒三角是否已被相邻正三角影响：被影响就跳过，否则种树'],
        summary=['时间 `O(size^2)`，空间 `O(1)`（不含输出）',
                 '作者说明：这是找规律的贪心构造，没有证明一定是最优',
                 '易错点：换行时 `near_flag` 要重置，行末触发时要在上一行补种一棵正三角',
                 '易错点：奇数 = 正三角，偶数 = 倒三角；之字形换行方向 `d` 要取反',
                 '原文为 Python 2 风格，Python 3 无需修改；答案不唯一，视频里 `expect` 用该代码的真实输出'],
    ),
)
