def _tri(x, y, n, cx, top, w, h):
    """row x (1-based), index y (1-based) -> 3 vertices"""
    L = cx - x * w / 2
    t, b = top + (x - 1) * h, top + x * h
    if y % 2 == 1:
        k = (y - 1) // 2
        return [(L + w / 2 + k * w, t), (L + k * w, b), (L + (k + 1) * w, b)]
    j = y // 2
    return [(L + w / 2 + (j - 1) * w, t), (L + w / 2 + j * w, t), (L + j * w, b)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = 4
    w = min((x1 - x0 - 60) / n, (y1 - y0 - 150) / (n * 0.866))
    h = w * 0.866
    cx = (x0 + x1) / 2
    top = y0 + 46
    cv.text((x0 + 18, y0 + 4), '三角形网格：红 = 已种树（res），黄框 = 当前位置 [nowx, nowy]', 22, T['muted'], bold=True)
    res = S.get('res') or []
    red = {(a, b) for a, b in res}
    for x in range(1, n + 1):
        for y in range(1, 2 * x):
            pts = _tri(x, y, n, cx, top, w, h)
            isr = (x, y) in red
            cv.poly(pts, T['red'] if isr else T['panel2'])
            cv.line(pts + [pts[0]], T['border'], 3)
            gx = sum(p[0] for p in pts) / 3
            gy = sum(p[1] for p in pts) / 3
            cv.text((gx, gy + (6 if y % 2 else -6)), f'{x},{y}', 20, T['bg'] if isr else T['dim'], anchor='mm', bold=True, mono=True)
    if 'nowx' in S and S.get('nowy') and 1 <= S['nowx'] <= n and 1 <= S['nowy'] <= 2 * S['nowx'] - 1:
        pts = _tri(S['nowx'], S['nowy'], n, cx, top, w, h)
        cv.line(pts + [pts[0]], T['yellow'], 8)
    yb = y1 - 80
    cv.text((x0 + 18, yb), f"已种树 {len(res)} 棵", 28, T['red'], bold=True)


CONFIG = dict(
    num=2647, title='把三角形染成红色', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='构造：底边全染 + 蛇形隔格',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution(object):
    def colorRed(self, n):

        res = [[1, 1]]
        if n == 1:
            return res
        
        for index in range(1, n * 2, 2):
            res.append([n, index])
        
        nowx = n - 1
        nowy = 1
        d = 1
        bound = (n - 1) * 2
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
    call='Solution().colorRed(4)',
    expect=[[1, 1], [4, 1], [4, 3], [4, 5], [4, 7], [3, 2], [2, 3]],
    views=[
        dict(type='custom', draw=_draw, h=620),
    ],
    watch=['nowx', 'nowy', 'd', 'bound', 'near_flag'],
    captions={
        'res = [[1, 1]]': '顶点 `[1,1]` 只有一个小三角，没有邻居可以感染它 → ==必须自己种树==',
        'if n == 1': '`n = {n}`，不是 1，还要处理更多行',
        'res.append([n, index])': '最底下一行：每个正三角（奇数 `y`）都种树 `[{n},{index}]`，中间的倒三角被两边感染，不用种',
        'nowx = n - 1': '从倒数第二行 `nowx = {nowx}` 开始往上，一行一行处理',
        'd = 1': '`d` 是行内扫描方向：`1` 向右，`-1` 向左，每换一行翻转（蛇形）',
        'bound = (n - 1) * 2': '`bound = {bound}`：本行扫描的边界，走到它就该换行',
        'near_flag = False': '`near_flag`：上一个位置是否刚种过树',
        'while nowx != 1': lambda S, B, r: (f'还在第 `{S.nowx}` 行，继续往上处理' if S.nowx != 1 else '`nowx = 1`：顶部已经处理完，结束'),
        'if nowy % 2 == 1': lambda S, B, r: (f'`nowy = {B.nowy}` 是奇数 → 当前是==正三角==，不种树，直接往 `d` 方向走' if B.nowy % 2 == 1 else f'`nowy = {B.nowy}` 是偶数 → 当前是==倒三角=='),
        'nowy += d': '沿方向 `d = {d}` 走一格：`nowy = {nowy}`',
        'if nowy == bound': lambda S, B, r: (f'`nowy = {S.nowy}` 到达 `bound = {S.bound}`：本行走到头' if S.nowy == S.bound else f'`nowy = {S.nowy}` 还没到 `bound = {S.bound}`，继续'),
        'elif near_flag': lambda S, B, r: ('`near_flag` 为真：上一格刚种了树，这个倒三角会被感染 → 不种' if S.near_flag else '`near_flag` 为假：上一格没种树，这个倒三角要自己种'),
        'if nowy + d + d == bound': lambda S, B, r: (f'再走两格就碰到 `bound = {S.bound}`：这是本行最后一个倒三角 → 换行' if S.nowy + S.d + S.d == S.bound else '本行还没走完，继续'),
        'd = -d': '换行：方向翻转，`d = {d}`（蛇形）',
        'nowx -= 1': '往上一行：`nowx = {nowx}`',
        39: '向右扫描：从本行最左的正三角开始，`nowy = {nowy}`',
        12: '`nowy = 1`：行内从最左的正三角开始',
        'nowy = nowx * 2 - 1': '向左扫描：从本行最右的正三角开始，`nowy = {nowy}`',
        'bound = 0': '向左扫描的边界是 0',
        'bound = nowx * 2': '向右扫描的边界是本行右端 `bound = {bound}`',
        'if nowx > 1': lambda S, B, r: (f'上一行还没到顶 → 先把新行起点 `[{S.nowx},{S.nowy}]` 种上树' if S.nowx > 1 else '已经到顶（第 1 行），不需要再种'),
        'res.append([nowx, nowy])': '种树 `[{nowx},{nowy}]`，已种 {len(res)} 棵',
        'near_flag = True': '记下：刚种过树，下一个倒三角会被感染',
        'near_flag = False': '`near_flag = False`',
        'return res': '一共种 `{len(res)}` 棵树，全部感染完成',
    },
    max_steps=70,
    cards=dict(
        one_liner='底边先染满，再一行一行蛇形往上，隔格种树',
        complexity='时间 `O(n²)`，空间 `O(n²)`（输出本身）',
        problem=['边长为 `n` 的三角形网格，第 `x` 行有 `2x−1` 个小三角，坐标 `[x, y]`',
                 '初始染一些红色；白色三角只要有 ≥ 2 个相邻的红色，就会变红',
                 '求最少的初始红色集合，使最终全部变红。示例：`n = 4` → 7 个'],
        quote='本题与之前遇到过的LCP70题完全相同，直接照搬当时的处理方法即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`[1,1]` 与最底下一行所有正三角（奇数 `y`）先染红',
              '之后每一行从下往上，用 `nowx, nowy` 和方向 `d` 蛇形扫描，`near_flag` 控制隔一个种一个',
              '每行走到头就 `d = -d`、上一行，奇偶位置交替，保证红色能逐层蔓延'],
        summary=['时间 `O(n²)`，空间 `O(n²)`',
                 '`nowy` 奇数是正三角，偶数是倒三角；`bound` 是本行的边界，到边界就换行换方向',
                 '`near_flag` 为真时说明刚种过树，下一个倒三角会被感染，直接跳过',
                 '原文本就是 Python 3 可运行的写法，未修改；与 LCP 70 沙地治理是同一题']
    ),
)
