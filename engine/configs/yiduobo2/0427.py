import collections
import views as V

GRID = [[1, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 1, 1, 1],
        [1, 1, 0, 1]]

CODE = '''
class Solution(object):
    def construct(self, grid):
        if not grid:
            return None

        n = len(grid)
        sum_matrix = grid[:]
        for i in range(n):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        continue
                    else:
                        sum_matrix[i][j] += sum_matrix[i][j - 1]
                elif j == 0:
                    sum_matrix[i][j] += sum_matrix[i - 1][j]
                else:
                    sum_matrix[i][j] += sum_matrix[i - 1][j] + sum_matrix[i][j - 1] - sum_matrix[i - 1][j - 1]

        return self.build(0, 0, n - 1, n - 1, sum_matrix)

    def build(self, x1, y1, x2, y2, sum_matrix):
        if x1 == 0:
            if y1 == 0:
                s = sum_matrix[x2][y2]
            else:
                s = sum_matrix[x2][y2] - sum_matrix[x2][y1 - 1]
        elif y1 == 0:
            s = sum_matrix[x2][y2] - sum_matrix[x1 - 1][y2]
        else:
            s = sum_matrix[x2][y2] - sum_matrix[x1 - 1][y2] - sum_matrix[x2][y1 - 1] + sum_matrix[x1 - 1][y1 - 1]

        if s == 0 or s == (x2 - x1 + 1) * (y2 - y1 + 1):
            if s == 0:
                val = 0
            else:
                val = 1
            return Node(val, True, None, None, None, None)

        midx = (x1 + x2) // 2
        midy = (y1 + y2) // 2
        topLeft = self.build(x1, y1, midx, midy, sum_matrix)
        topRight = self.build(x1, midy + 1, midx, y2, sum_matrix)
        bottomLeft = self.build(midx + 1, y1, x2, midy, sum_matrix)
        bottomRight = self.build(midx + 1, midy + 1, x2, y2, sum_matrix)
        return Node(0, False, topLeft, topRight, bottomLeft, bottomRight)
'''

SETUP = '''
class Node(object):
    def __init__(self, val, isLeaf, topLeft, topRight, bottomLeft, bottomRight):
        self.val = val
        self.isLeaf = isLeaf
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
'''

_LINES = CODE.strip('\n').split('\n')
L_RET_LEAF = [k + 1 for k, t in enumerate(_LINES) if 'return Node(val, True' in t][0]
L_RET_IN = [k + 1 for k, t in enumerate(_LINES) if 'return Node(0, False' in t][0]
L_S = {k + 1 for k, t in enumerate(_LINES) if 's = sum_matrix' in t}
KIDS = ('topLeft', 'topRight', 'bottomLeft', 'bottomRight')
KID_CN = {'topLeft': '左上', 'topRight': '右上', 'bottomLeft': '左下', 'bottomRight': '右下'}


def _ref(x1, y1, x2, y2):
    """参考结构：区域 -> 叶子值 / 四个孩子区域（只用于画图的布局）"""
    vals = {GRID[i][j] for i in range(x1, x2 + 1) for j in range(y1, y2 + 1)}
    if len(vals) == 1:
        return dict(r=(x1, y1, x2, y2), leaf=True, val=vals.pop(), kids=[])
    mx, my = (x1 + x2) // 2, (y1 + y2) // 2
    return dict(r=(x1, y1, x2, y2), leaf=False, val=0,
                kids=[_ref(x1, y1, mx, my), _ref(x1, my + 1, mx, y2), _ref(mx + 1, y1, x2, my), _ref(mx + 1, my + 1, x2, y2)])


REF = _ref(0, 0, len(GRID) - 1, len(GRID) - 1)


def _child_regions(x1, y1, x2, y2):
    mx, my = (x1 + x2) // 2, (y1 + y2) // 2
    return dict(topLeft=(x1, y1, mx, my), topRight=(x1, my + 1, mx, y2),
                bottomLeft=(mx + 1, y1, x2, my), bottomRight=(mx + 1, my + 1, x2, y2))


def _state(st):
    """从调用栈里读出：已经建好的区域、当前区域、祖先区域"""
    frames = [fr for fr in st.get('_frames', []) if fr['name'] == 'build']
    done, path = set(), []
    for fr in frames:
        L = fr['locals']
        r = tuple(L.get(k) for k in ('x1', 'y1', 'x2', 'y2'))
        path.append(r)
        if 'midx' in L:
            reg = _child_regions(*r)
            for k in KIDS:
                if L.get(k) is not None:
                    done.add(reg[k])
    line = st['_S'].get('_line')
    if frames and line in (L_RET_LEAF, L_RET_IN):
        done.add(path[-1])
    return done, path


def _all_done(ref, done):
    out = set()

    def walk(nd, inherited):
        d = inherited or nd['r'] in done
        if d:
            out.add(nd['r'])
        for k in nd['kids']:
            walk(k, d)
    walk(ref, False)
    return out


def _draw(cv, spec, st, box, vi, ctx):
    T = V.T
    x0, y0, x1, y1 = box
    V.label(cv, box, 'grid（黄框 = 当前区域）  四叉树（绿 = 叶子 1，灰 = 叶子 0，· = 内部）')
    done, path = _state(st)
    fin = _all_done(REF, done)
    n = len(GRID)
    cell = min(66, (y1 - y0 - 70) / n)
    gx, gy = x0 + 30, y0 + 52
    leaves = []

    def collect(nd):
        if nd['leaf']:
            leaves.append(nd)
        for k in nd['kids']:
            collect(k)
    collect(REF)
    for lf in leaves:
        a, b, c, d = lf['r']
        if lf['r'] in fin:
            fill = (40, 120, 70) if lf['val'] == 1 else (55, 62, 75)
            cv.rect((gx + b * cell + 2, gy + a * cell + 2, gx + (d + 1) * cell - 2, gy + (c + 1) * cell - 2), fill=fill, r=6)
    for i in range(n):
        for j in range(n):
            X, Y = gx + j * cell, gy + i * cell
            cv.rect((X + 1, Y + 1, X + cell - 1, Y + cell - 1), outline=T['border'], width=1, r=4)
            cv.text((X + cell / 2, Y + cell / 2), GRID[i][j], int(cell * 0.42), T['text'], anchor='mm', bold=True)
    for k, r in enumerate(path):
        a, b, c, d = r
        last = k == len(path) - 1
        cv.rect((gx + b * cell - 1, gy + a * cell - 1, gx + (d + 1) * cell + 1, gy + (c + 1) * cell + 1),
                outline=T['yellow'] if last else T['purple'], width=5 if last else 2, r=6)
    # quad tree on the right
    tx0 = gx + n * cell + 50
    tw = x1 - 20 - tx0
    levels = collections.defaultdict(list)

    def lay(nd, dep):
        levels[dep].append(nd)
        for k in nd['kids']:
            lay(k, dep + 1)
    lay(REF, 0)
    pos = {}
    nleaf = [0]

    def place(nd, dep):
        if not nd['kids']:
            pos[nd['r']] = (nleaf[0], dep)
            nleaf[0] += 1
        else:
            for k in nd['kids']:
                place(k, dep + 1)
            xs = [pos[k['r']][0] for k in nd['kids']]
            pos[nd['r']] = ((xs[0] + xs[-1]) / 2, dep)
    place(REF, 0)
    sp = tw / max(1, nleaf[0])
    dy = min(110, (y1 - y0 - 100) / max(1, max(levels)))
    rad = min(22, sp * 0.42)

    def P(r):
        xi, dep = pos[r]
        return tx0 + sp * (xi + 0.5), y0 + 80 + dep * dy

    def edges(nd):
        for k in nd['kids']:
            if k['r'] in fin or nd['r'] in fin:
                cv.line([P(nd['r']), P(k['r'])], T['muted'], 3)
            else:
                cv.dashed(P(nd['r']), P(k['r']), T['border'], 2)
            edges(k)
    edges(REF)

    def nodes(nd):
        X, Y = P(nd['r'])
        cur = path and nd['r'] == path[-1]
        if nd['r'] in fin:
            fill = ((40, 120, 70) if nd['val'] == 1 else (55, 62, 75)) if nd['leaf'] else T['panel2']
            txt = str(nd['val']) if nd['leaf'] else '·'
            cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill,
                         outline=T['yellow'] if cur else T['muted'], width=4 if cur else 2)
            cv.text((X, Y), txt, int(rad * 0.95), T['text'], anchor='mm', bold=True)
        else:
            cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=T['bg'],
                         outline=T['yellow'] if cur else (T['purple'] if nd['r'] in path else T['border']), width=4 if cur else 2)
        for k in nd['kids']:
            nodes(k)
    nodes(REF)


V.VIEWS.setdefault('quad_0427', (_draw, lambda spec: spec.get('h', 360)))


def _corner(S, i, j, v):
    # 子矩阵和 = S[x2][y2] − S[x1−1][y2] − S[x2][y1−1] + S[x1−1][y1−1]
    if S.get('_line') not in L_S:
        return None
    x1, y1, x2, y2 = S['x1'], S['y1'], S['x2'], S['y2']
    if (i, j) == (x2, y2):
        return 'yellow'
    if (i, j) in ((x1 - 1, y2), (x2, y1 - 1)):
        return 'pink'
    if (i, j) == (x1 - 1, y1 - 1):
        return 'green'
    return None


def _ser(root):
    out, q = [], collections.deque([root])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None)
            continue
        out.append([1 if nd.isLeaf else 0, nd.val])
        q.extend([nd.topLeft, nd.topRight, nd.bottomLeft, nd.bottomRight])
    while out and out[-1] is None:
        out.pop()
    return out


def _s(S, B, r):
    x1, y1, x2, y2, M = S.x1, S.y1, S.x2, S.y2, S.sum_matrix
    parts = [str(M[x2][y2])]
    if x1 > 0:
        parts.append(f'− {M[x1 - 1][y2]}')
    if y1 > 0:
        parts.append(f'− {M[x2][y1 - 1]}')
    if x1 > 0 and y1 > 0:
        parts.append(f'+ {M[x1 - 1][y1 - 1]}')
    if len(parts) == 1:
        return f'区域从 (0,0) 开始：和就是 `sum_matrix[{x2}][{y2}] = {S.s}`'
    return f'区域 `({x1},{y1})~({x2},{y2})` 的和，用前缀和 O(1) 算：`{" ".join(parts)} = {S.s}`'


def _area(S):
    return (S.x2 - S.x1 + 1) * (S.y2 - S.y1 + 1)


def _test(S, B, r):
    s, a = B.s, (B.x2 - B.x1 + 1) * (B.y2 - B.y1 + 1)
    if s == 0:
        return f'区域和 `s = 0`：==全是 0== → 叶子'
    if s == a:
        return f'区域和 `s = {s}` = 面积 `{a}`：==全是 1== → 叶子'
    return f'`0 < s = {s} < 面积 {a}`：有 0 也有 1 → 需要切成四块'


def _call(which):
    def f(S, B, r):
        return f'递归建==「{KID_CN[which]}」==：`build({S.x1}, {S.y1}, {S.x2}, {S.y2})`'
    return f


CONFIG = dict(
    num=427, title='建立四叉树', difficulty='Medium', category='矩阵',
    author='yiduobo', technique='二维前缀和 + 分治递归',
    tags=['面试经典150'],
    code=CODE,
    setup=SETUP,
    call=f'Solution().construct({GRID})',
    result_fn=_ser,
    expect=[[0, 0], [1, 1], [1, 0], [1, 1], [0, 0], None, None, None, None, None, None, None, None, None, None, None, None,
            [1, 1], [1, 1], [1, 0], [1, 1]],
    skip=['if not grid', 'for j in range(n)', 'if i == 0', 'if j == 0', 'continue', 'else:', 'elif j == 0',
          'sum_matrix[i][j] +=', 'if x1 == 0', 'if y1 == 0', 'elif y1 == 0', 'if s == 0:', 'val = 0', 'val = 1', 'n = len'],
    views=[
        dict(type='quad_0427', h=380),
        dict(type='table', var='sum_matrix', label='sum_matrix（黄 = 加，粉 = 减，绿 = 加回重复减掉的）', cell=48, h=230,
             color=_corner),
        dict(type='calls', h=130, hide=('sum_matrix',)),
    ],
    watch=[('s', 's', 'green'), ('midx', 'midx'), ('midy', 'midy')],
    captions={
        'sum_matrix = grid[:]': '先预处理==二维前缀和==：`sum_matrix[i][j]` = 左上角到 (i,j) 的矩阵和',
        'for i in range(n)': lambda S, B, r: (f'计算第 `{S.i}` 行的前缀和' if S.i != B.get('i') or 'i' not in B else '前缀和算完了'),
        'return self.build(0, 0': '从整个矩阵 `(0,0)` 到 `({x2},{y2})` 开始递归',
        's = sum_matrix[x2][y2]': _s,
        'if s == 0 or s ==': _test,
        'return Node(val, True': lambda S, B, r: f'建叶子：`val = {S.val}`，`isLeaf = True`',
        'midx = (x1 + x2) // 2': '行切一半：`midx = ({x1} + {x2}) // 2 = {midx}`',
        'midy = (y1 + y2) // 2': '列切一半：`midy = ({y1} + {y2}) // 2 = {midy}`',
        'topLeft = self.build': _call('topLeft'),
        'topRight = self.build': _call('topRight'),
        'bottomLeft = self.build': _call('bottomLeft'),
        'bottomRight = self.build': _call('bottomRight'),
        'return Node(0, False': lambda S, B, r: ('四个孩子都建好了 → 返回根节点，==整棵四叉树建成=='
                                                 if (S.x1, S.y1, S.x2, S.y2) == (0, 0, len(GRID) - 1, len(GRID) - 1)
                                                 else f'四个孩子都建好了 → 返回内部节点 `({S.x1},{S.y1})~({S.x2},{S.y2})`（`isLeaf = False`）'),
    },
    cards=dict(
        result='返回根节点：`[[0,0],[1,1],[1,0],[1,1],[0,0],…]` ✓',
        one_liner='区域和为 0 或等于面积就是叶子，否则切成四块递归',
        complexity='时间 `O(n²)`，空间 `O(n²)`（前缀和）',
        problem=['给一个 `n × n` 的 0/1 矩阵 `grid`（n 是 2 的幂），用四叉树表示它',
                 '区域内值==全部相同== → 叶子节点（`isLeaf = True`，`val` 为该值）',
                 '否则 → 内部节点，切成左上 / 右上 / 左下 / 右下四块分别递归',
                 '示例：`[[0,1],[1,0]]` → `[[0,1],[1,0],[1,1],[1,1],[1,0]]`',
                 '本视频：4×4 矩阵，只有右下角需要继续切分'],
        quote='对于判断每个位置的值是否都为0或者都为1，可以使用判断和的办法。==若都为0，那么和自然是0。若都为1，那么和就是当前矩阵的面积。==',
        quote_src='—— yiduobo 题解原文',
        idea=['先预处理前缀和，任意子矩阵的和都能 `O(1)` 算出',
              '`s == 0` 或 `s == 面积` → 叶子；否则从 `midx`、`midy` 切成四块',
              '四个孩子都建好，再返回内部节点'],
        summary=['时间 `O(n²)`：前缀和 `O(n²)`，每个四叉树节点 `O(1)` 判断',
                 '子矩阵和 = 四个前缀和加加减减，`x1 = 0` 或 `y1 = 0` 要特判',
                 '`sum_matrix = grid[:]` 是浅拷贝，会原地改掉 grid（不影响本题结果）',
                 '原文 Python 2：`midx/midy` 的 `/` 已改为 `//`，删去文档字符串',
                 '原文的 Node 定义在注释里，这里作为环境预先定义'],
    ),
)
