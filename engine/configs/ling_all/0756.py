def _L(v):
    return chr(64 + v) if v else ''


def _row(S, r):
    """第 r 行已经填好的字母（列表，None = 还没填）"""
    pyr, n = S['pyramid'], S['n']
    i, j = S.get('i'), S.get('j')
    if r == n - 1 or i is None:
        return [_L((pyr[r] >> (3 * k)) & 7) for k in range(r + 1)]
    if r > i:
        return [_L((pyr[r] >> (3 * k)) & 7) for k in range(r + 1)]
    if r == i:
        top = S['_inner'].get('top')
        return [(_L((pyr[r] >> (3 * k)) & 7) if (k < j or (k == j and top is not None and (pyr[r] >> (3 * k)) & 7 == top)) else None) for k in range(r + 1)]
    return [None] * (r + 1)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S['n']
    i, j = S.get('i'), S.get('j')
    cell = min(92, (x1 - x0 - 60) / n, (y1 - y0 - 120) / n - 8)
    top = y0 + 50
    cv.text((x0 + 18, y0 + 4), '金字塔（从下往上、每行从左到右填；黄 = 正在填，蓝 = 它下面的两块）', 22, T['muted'], bold=True)
    for r in range(n):
        letters = _row(S, r)
        y = top + r * (cell + 8)
        sx = (x0 + x1) / 2 - (r + 1) * cell / 2
        for k, ch in enumerate(letters):
            X = sx + k * cell
            fill, tc = T['panel2'], T['dim']
            if ch:
                fill, tc = (70, 78, 90), T['text']
            if r == n - 1:
                fill, tc = T['green'], T['bg']
            if i is not None and i >= 0 and j is not None:
                if r == i + 1 and k in (j, j + 1) and j <= i:
                    fill, tc = T['blue'], T['bg']
                if r == i and k == j:
                    fill = T['yellow'] if ch else T['panel2']
                    tc = T['bg'] if ch else T['dim']
            cv.rect((X + 4, y, X + cell - 4, y + cell), fill=fill, r=10, outline=T['border'])
            cv.text((X + cell / 2, y + cell / 2), ch or '·', 38, tc, anchor='mm', bold=True, mono=True)
    if i is not None and i >= 0 and j is not None and j <= i:
        pyr = S['pyramid']
        a, b = (pyr[i + 1] >> (3 * j)) & 7, (pyr[i + 1] >> (3 * (j + 1))) & 7
        cands = ''.join(_L(c) for c in S['groups'][a][b]) or '（空）'
        cv.text((x0 + 18, y1 - 36), f'底下是 {_L(a)}{_L(b)} → 顶上可填：{cands}', 28, T['yellow'], bold=True)


def _vis_fmt(x):
    return ''.join(_L((x >> (3 * k)) & 7) for k in range(x.bit_length() // 3 + 1) if (x >> (3 * k)) & 7)


def _top(S, B, ret):
    a = (S.pyramid[S.i + 1] >> (S.j * 3)) & 7
    b = (S.pyramid[S.i + 1] >> ((S.j + 1) * 3)) & 7
    return f'`({S.i+1},{S.j})`={_L(a)}、`({S.i+1},{S.j+1})`={_L(b)} → 枚举顶部字母 `{_L(S.top)}`（候选 {len(S.groups[a][b])} 个）'


def _prune(S, B, ret):
    if not S.j:
        return '`j = 0`：第一格左边没有邻居，不用剪枝'
    left = (S.pyramid[S.i] >> ((S.j - 1) * 3)) & 7
    if S.groups[left][S.top]:
        return f'左边已填 `{_L(left)}`，`{_L(left)}{_L(S.top)}` 上面还能放字母 → 可以填 `{_L(S.top)}`'
    return f'左边是 `{_L(left)}`，填 `{_L(S.top)}` 后 `{_L(left)}{_L(S.top)}` 上面放不了任何字母 → ==剪枝 continue=='


CONFIG = dict(
    num=756, title='金字塔转换矩阵', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='回溯填格子 + 位运算 + 记忆化 + 剪枝',
    tags=['动态规划', '链表树与回溯', '难度分 1990'],
    setup='''
from functools import reduce
''',
    code='''
class Solution:
    def pyramidTransition(self, bottom: str, allowed: List[str]) -> bool:
        groups = [[[] for _ in range(7)] for _ in range(7)]
        for a, b, c in allowed:
            # A~F -> 1~6
            groups[ord(a) & 31][ord(b) & 31].append(ord(c) & 31)

        n = len(bottom)
        pyramid = [0] * n
        for i, ch in enumerate(bottom):
            pyramid[-1] |= (ord(ch) & 31) << (i * 3)  # 等价于 pyramid[-1][i] = ord(ch)&31

        vis = set()

        def dfs(i: int, j: int) -> bool:
            if i < 0:
                return True

            if pyramid[i] in vis:
                return False

            if j == i + 1:
                vis.add(pyramid[i])
                return dfs(i - 1, 0)

            for top in groups[pyramid[i + 1] >> (j * 3) & 7][pyramid[i + 1] >> ((j + 1) * 3) & 7]:
                if j and not groups[pyramid[i] >> ((j - 1) * 3) & 7][top]:
                    continue
                pyramid[i] &= ~(7 << (j * 3))  # 清除之前填的字母，等价于 pyramid[i][j] = 0
                pyramid[i] |= top << (j * 3)  # 等价于 pyramid[i][j] = top
                if dfs(i, j + 1):
                    return True
            return False

        return dfs(n - 2, 0)
''',
    call='Solution().pyramidTransition("BCD", ["BCB", "BCC", "CDE", "CEA"])',
    expect=True,
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='set', var='vis', label='vis（填过但没成功的行）', fmt=_vis_fmt, h=90),
        dict(type='calls', h=150),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'blue'), ('j', lambda S: S['_inner'].get('j'), 'pink'),
           ('top', lambda S: _L(S['_inner']['top']) if S['_inner'].get('top') else '-', 'yellow')],
    skip=['pyramid = [0] * n', 'n = len(bottom)', 'vis = set()', 'groups = [[[]', 'for a, b, c in allowed', 'for i, ch in enumerate'],
    captions={
        'groups[ord(a) & 31]': '`{a}{b}` → `{c}`：三角形底下 {a}、{b}，上面可放 {c}（字母映射到 1~6）',
        'pyramid[-1] |=': '每个字母占 3 个比特，把 `{ch}` 压进最底行的第 `{i}` 位',
        'return dfs(n - 2, 0)': '最底行已定，从倒数第二行的左端开始填：`dfs({n-2}, 0)`',
        'if i < 0': lambda S, B, r: ('`i < 0`：所有格子都填完了 → ==True==' if S.i < 0 else f'`i = {S.i}`：还有行没填，继续'),
        'if pyramid[i] in vis': lambda S, B, r: (f'这一行 `{_vis_fmt(S.pyramid[S.i])}` 以前填过且没能到塔顶 → 直接 False' if S.pyramid[S.i] in S.vis
                                                 else '这一行的写法没见过，继续填'),
        'if j == i + 1': lambda S, B, r: (f'`j = {S.j} = i + 1`：第 `{S.i}` 行填满了' if S.j == S.i + 1 else f'`j = {S.j}`：这一行还没填完'),
        'vis.add': lambda S, B, r: f'把这一行 `{_vis_fmt(B.pyramid[B.i])}` 记入 `vis`：下次再填出一样的就不用搜了',
        'return dfs(i - 1, 0)': lambda S, B, r: f'这一行填满，往上一行：`dfs({B.i - 1}, 0)`',
        'if j and not groups': _prune,
        'for top in groups': _top,
        'pyramid[i] &= ': '先清掉 `({i},{j})` 原来的 3 个比特（回溯换字母时要用）',
        'pyramid[i] |= top': lambda S, B, r: f'`({S.i},{S.j})` 填 `{_L(S.top)}`',
        'if dfs(i, j + 1)': lambda S, B, r: f'去填右边一格：`dfs({B.i}, {B.j + 1})`',
        'return True': '一路填到塔顶 → ==True==，层层返回',
        'return False': '这个位置的候选都试完了，==回溯==到上一格换个字母',
        'return dfs(n - 2': '最底行已定，从倒数第二行的左端开始填',
    },
    max_steps=70,
    cards=dict(
        one_liner='按“从下往上、从左到右”回溯填格子，填错就退回换字母',
        complexity='时间 `O(6^n)` 量级（剪枝后），空间 `O(6^n)`',
        problem=['给底行 `bottom`，每个三角形 “左下、右下 → 顶” 必须在 `allowed` 里',
                 '问能否一直垒到塔尖',
                 '本视频：`bottom=BCD`，`allowed=[BCB,BCC,CDE,CEA]` → `True`'],
        quote='考虑枚举金字塔的每个格子填什么字母。写一个类似 17. 电话号码的字母组合 的回溯（搜索）。按照从下往上，从左到右的顺序填字母。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`groups[a][b]`：底下是 a、b 时，顶上能放哪些字母',
              '每个格子==枚举填哪个==，由它下面两块决定候选',
              '`vis` 记住填不出塔尖的行；左边相邻放不下就剪枝'],
        result='填到塔尖，返回 True ✓',
        summary=['时间约 `O(6^n)`，空间 `O(6^n)`（`vis` 存位压缩的行）',
                 '字母映射到 `1~6` 而不是 `0~5`：否则 `AA` 和 `AAA` 都是 0 分不清',
                 '灵神还给了更早的几种写法：直接回溯 → 加 `vis` → 位运算，最终版再加剪枝',
                 '易错点：回溯换字母前要先清掉旧的 3 个比特'],
    ),
)
