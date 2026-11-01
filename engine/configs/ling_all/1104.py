L0 = 14   # 起点标号


def _par(x):
    return (1 << (x.bit_length() - 2)) * 3 - 1 - x // 2


def _path(x):  # 从 x 一路走到根
    out = [x]
    while x > 1:
        x = _par(x)
        out.append(x)
    return out


P0 = _path(L0)
ROWS = L0.bit_length()


def _zig(r):  # 第 r 行（从 1 起）自左向右的标号
    a = list(range(1 << (r - 1), 1 << r))
    return a if r % 2 == 1 else a[::-1]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cur = S['_inner'].get('label')
    visited = set()
    if cur in P0:
        visited = set(P0[:P0.index(cur) + 1])
    cv.text((x0 + 18, y0 + 4), '之字形二叉树（橙 = 当前 label，蓝 = 已走过的祖先链，灰框 = 还没走到的路径）', 22, T['muted'], bold=True)
    top = y0 + 50
    dy = min(110, (y1 - y0 - 80) / ROWS)
    W = x1 - x0 - 60
    cw = min(96, W / (1 << (ROWS - 1)))
    pos = {}
    for r in range(1, ROWS + 1):
        row = _zig(r)
        slot = W / len(row)
        for k, v in enumerate(row):
            pos[v] = (x0 + 30 + slot * (k + 0.5), top + (r - 1) * dy + 24)
        cv.text((x0 + 8, top + (r - 1) * dy + 24), f'{r}', 18, T['dim'], anchor='lm')
    for r in range(2, ROWS + 1):
        up, row = _zig(r - 1), _zig(r)
        for k, v in enumerate(row):
            cv.line([pos[v], pos[up[k // 2]]], T['border'], 2)
    for v, (X, Y) in pos.items():
        on = v in P0
        fill = T['orange'] if v == cur else (T['blue'] if v in visited else T['panel2'])
        cv.rect((X - cw * 0.42, Y - 20, X + cw * 0.42, Y + 20), fill=fill, outline=T['yellow'] if on and v not in visited and v != cur else T['border'], width=3 if on else 1, r=10)
        cv.text((X, Y), v, 22, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)


def _cap_if(S, B, ret):
    x = S.label
    if x == 1:
        return '`label == 1` 成立：到根节点了，==递归边界==，路径只有 `[1]`'
    n = x.bit_length()
    return f'`label = {x}`，二进制长 `n = {n}`，不是根 → 要先求父节点的路径'


def _cap_ret(S, B, ret):
    x = B.label
    if ret is not None:
        return f'父节点路径 `{ret[:-1]}` 已回来，末尾补上 `label = {x}` → `{ret}`'
    n = x.bit_length()
    s = (1 << (n - 2)) * 3 - 1
    return (f'上一排最小+最大 `sum = 2^{n-2} + 2^{n-1} - 1 = {s}`；'
            f'父节点 = `sum - label/2 = {s} - {x // 2} = {s - x // 2}`，递归去求它')


CONFIG = dict(
    num=1104, title='二叉树寻路', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='递归 · 之字形父节点公式（Go 原文转写）',
    tags=['灵神题单·链表树与回溯', '难度分 1545'],
    code='''
class Solution:
    def pathInZigZagTree(self, label: int) -> List[int]:
        if label == 1:
            return [1]
        return self.pathInZigZagTree((1 << (label.bit_length() - 2)) * 3 - 1 - label // 2) + [label]
''',
    call='Solution().pathInZigZagTree(14)',
    expect=[1, 3, 4, 14],
    views=[
        dict(type='text', fn=lambda S: (lambda x: '' if x is None else ('根节点：`label = 1`' if x == 1 else
             f"普通二叉树父节点是 `{x}//2 = {x // 2}`；之字形要翻转：`sum - {x // 2}` = =={(1 << (x.bit_length() - 2)) * 3 - 1 - x // 2}=="))(S['_inner'].get('label')), size=28),
        dict(type='custom', draw=_draw, h=330),
        dict(type='calls', h=190),
    ],
    watch=[('label', lambda S: S['_inner'].get('label'), 'blue'), ('n', lambda S: S['_inner'].get('label').bit_length() if S['_inner'].get('label') else None)],
    captions={
        'if label == 1': _cap_if,
        'return [1]': '到达根：返回 `[1]`，开始一层层往回补自己',
        'return self.pathInZigZagTree': _cap_ret,
    },
    cards=dict(
        one_liner='父节点 = 上一排最小加最大 − label/2',
        complexity='时间 `O(log label)`，空间 `O(log label)`（递归栈）',
        problem=['无限满二叉树，奇数行从左到右、偶数行从右到左依次标号',
                 '给一个标号 `label`，返回从根到它的路径（途经节点的标号）',
                 '示例：`label = 14` → `[1,3,4,14]`'],
        quote='在进行“之”字形标记后，其父节点为 sum - label/2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`label` 二进制长度 `n`，上一排标号最小值加最大值 `sum = 2^(n-2) + 2^(n-1) - 1`',
              '正常二叉树父节点是 `label/2`；之字形等于在上一排==镜像翻转==，所以是 `sum - label/2`',
              '递归到 `label == 1` 为止，回来时在末尾追加自己'],
        result='运行结束，返回 `[1, 3, 4, 14]`',
        summary=['原文为 Go，已按原逻辑逐行转写为 Python：`bits.Len` → `bit_length()`，`append` → `+ [label]`',
                 '`sum = 2^(n-2) + 2^(n-1) - 1 = 3 * 2^(n-2) - 1`，原文写成 `1<<(n-2)*3-1`',
                 '时间/空间 `O(log label)`；易错：`label/2` 要用整除 `//`，且是用 `sum` 去减，不是直接取 `label//2`'],
    ),
)
