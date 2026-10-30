N, K0 = 25, 15
ORDER = sorted(range(1, N + 1), key=str)          # 字典序 = 十叉树的先序遍历
RANK = {v: i + 1 for i, v in enumerate(ORDER)}


def _in_sub(u, v):
    return str(u).startswith(str(v))


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), f'n = {N} 的十叉树：按先序遍历（= 字典序）从左到右摆放', 24, T['muted'], bold=True)
    sp = (x1 - x0 - 60) / N
    rad = min(17, sp * 0.45)

    def X(v):
        return x0 + 30 + (RANK[v] - 0.5) * sp

    def Y(v):
        return y0 + 150 if v < 10 else y0 + 250

    rx, ry = (x0 + x1) / 2, y0 + 62
    line = S.get('_line', 0)
    node = S.get('node')
    k = S.get('k')
    visited = K0 - k if isinstance(k, int) else 0
    measuring = node is not None and line in (11, 12, 13, 14, 15, 20, 21)
    last_layer = None
    if line in (13, 14, 15) and 'left' in S:
        last_layer = (S['left'], min(S['right'], N + 1) - 1)
    # 边
    for v in range(1, N + 1):
        px, py = (rx, ry) if v < 10 else (X(v // 10), Y(v // 10))
        cv.line([(px, py + (12 if v < 10 else rad)), (X(v), Y(v) - rad)], T['border'], 2)
    cv.d.ellipse((rx - 22, ry - 22, rx + 22, ry + 22), fill=T['panel2'], outline=T['border'], width=2)
    cv.text((rx, ry), '根', 20, T['muted'], anchor='mm', bold=True)
    # 正在统计大小的子树：画一个底色框
    if measuring:
        sub = [u for u in range(1, N + 1) if _in_sub(u, node)]
        a, b = min(RANK[u] for u in sub), max(RANK[u] for u in sub)
        top = Y(node) - rad - 10
        cv.rect((x0 + 30 + (a - 1) * sp + 2, top, x0 + 30 + b * sp - 2, y0 + 282), fill=T['yellow'], alpha=30, r=12)
        cv.rect((x0 + 30 + (a - 1) * sp + 2, top, x0 + 30 + b * sp - 2, y0 + 282), outline=T['yellow'], width=2, r=12)
        cv.text((x0 + 30 + (a - 1) * sp + 6, top - 14), f'子树 {node}：{len(sub)} 个节点', 20, T['yellow'], anchor='lm', bold=True)
    for v in range(1, N + 1):
        r = RANK[v]
        fill, tc, oc, ow = T['panel2'], T['text'], T['border'], 2
        if r <= visited:
            fill, tc = (30, 70, 45), T['text']
        if v == node:
            fill, tc = T['blue'], T['bg']
        if last_layer and last_layer[0] <= v <= last_layer[1]:
            oc, ow = T['orange'], 4
        cv.d.ellipse((X(v) - rad, Y(v) - rad, X(v) + rad, Y(v) + rad), fill=fill, outline=oc, width=ow)
        cv.text((X(v), Y(v)), v, 17 if v >= 10 else 20, tc, anchor='mm', bold=True)
    # 字典序排名
    yr = y0 + 300
    cv.text((x0 + 18, yr + 28), '↑ 字典序第几个', 18, T['dim'])
    for v in ORDER:
        r = RANK[v]
        c = T['pink'] if r == K0 else (T['green'] if r <= visited else T['dim'])
        cv.text((X(v), yr + 2), r, 16, c, anchor='mt', mono=True, bold=r == K0)
    cv.text((X(ORDER[K0 - 1]), yr + 26), f'第 {K0} 个 = 答案', 18, T['pink'], anchor='mt', bold=True)
    cv.text((x1 - 20, yr + 28), '绿 = 已访问　蓝 = node', 19, T['muted'], anchor='ra')


def _text(S):
    if 'node' not in S:
        return f'先算 `pow10`：`n = {N}` 有 2 位，子树 1 的最后一层在 `pow10 = 10` 倍处'
    if S['_line'] in (11, 12, 13, 14, 15):
        full = (S['pow10'] - 1) // 9
        if 'left' in S and S['left'] <= N:
            return f"`size({S['node']})` = 满层 `{full}` + 最后一层 `[{S['left']}, {min(S['right'], N + 1) - 1}]` 共 `{min(S['right'], N + 1) - S['left']}` 个"
        return f"`size({S['node']})` = 满层 `(pow10 - 1) // 9 = {full}`"
    return f"已访问 `{K0 - S['k']}` 个节点（最后一个是 `node = {S['node']}`），还要再往后访问 `k = {S['k']}` 个"


def _go(S, B, ret):
    if S.size <= S.k:
        return f'`size = {S.size} ≤ k = {S.k}`：第 k 个不在子树 `{S.node}` 里 → ==向右=='
    return f'`size = {S.size} > k = {S.k}`：答案在子树 `{S.node}` 里 → ==向下=='


CONFIG = dict(
    num=440, title='字典序的第K小数字', difficulty='Hard', category='数学',
    author='灵茶山艾府', technique='十叉树先序遍历 · O(1) 算子树大小',
    tags=['热题173'],
    code='''
class Solution:
    def findKthNumber(self, n: int, k: int) -> int:
        pow10 = 1  # 直接跳到子树 1 最后一层，left 和 right 需要乘以 pow10
        x = n // 10
        while x > 0:
            pow10 = pow10 * 10
            x //= 10

        # 统计 node 子树大小，O(1)
        def count_subtree_size(node: int) -> int:
            size = (pow10 - 1) // 9  # 1+10+100+...
            left, right = node * pow10, (node + 1) * pow10
            if left <= n:
                size += min(right, n + 1) - left  # 余项
            return size

        node = 1
        k -= 1  # 访问节点 node
        while k > 0:
            size = count_subtree_size(node)
            if size <= k:  # 向右，跳过 node 子树
                node += 1  # 访问 node 右侧兄弟节点
                k -= size  # 访问子树中的每个节点，以及新的 node 节点
            else:  # 向下，深入 node 子树
                pow10 //= 10  # 子树层数减一
                node *= 10  # 访问 node 的第一个儿子
                k -= 1  # 访问新的 node 节点
        return node
''',
    call=f'Solution().findKthNumber({N}, {K0})',
    expect=22,
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='text', fn=_text, size=25, h=56),
        dict(type='calls', h=130),
    ],
    watch=[('node', 'node', 'blue'), ('k', 'k', 'pink'), ('pow10', 'pow10'), ('size', 'size', 'yellow')],
    captions={
        'x = n // 10': '`x = n // 10 = {x}`：n 有几位，子树 1 就有几层',
        'while x > 0': lambda S, B, r: ('`x > 0` → 还有一层，`pow10` 再乘 10' if B.x > 0 else
                                        f'`pow10 = {S.pow10}`：子树 1 的最后一层是 `[{S.pow10}, {2 * S.pow10 - 1}]`'),
        'pow10 = pow10 * 10': '`pow10` → `{pow10}`',
        'x //= 10': '`x` → `{x}`',
        'pow10 = 1  #': '`pow10`：子树 1 的==最后一层==从 `1 × pow10` 开始；先看 n 有几位',
        'size = (pow10 - 1) // 9': lambda S, B, r: (f'满的那些层：`1 + 10 + … = (pow10 - 1) // 9 = {S.size}`（等比数列之和 `11…1`）'
                                                    if S.size else '`pow10 = 1`：子树只剩一层，没有满层，`size` 先为 `0`'),
        'left, right = node': '最后一层：`[node·pow10, (node+1)·pow10)` = `[{left}, {right})`',
        'if left <= n': lambda S, B, r: (f'`left = {S.left} ≤ n`：最后一层有节点' if S.left <= S.n else
                                         f'`left = {S.left} > n`：最后一层一个节点都没有'),
        'size += min(right, n + 1) - left': '余项：`min({right}, n + 1) - {left}` → `size = {size}`',
        'return size': '子树 `{node}` 共 =={ret}== 个节点',
        'k -= 1  # 访问节点 node': '从根的第一个儿子 `1` 开始：访问它，`k` → `{k}`',
        'while k > 0': lambda S, B, r: (f'`k = {S.k} > 0`：还要再访问 `{S.k}` 个节点' if S.k > 0 else
                                        f'`k = 0`：当前节点就是第 {K0} 个 → 结束'),
        'size = count_subtree_size(node)': '算子树 `{node}` 的大小',
        'if size <= k': _go,
        'node += 1': '向右，跳过 node 子树：访问右侧兄弟 `node = {node}`',
        'k -= size': '子树里的 `{size}` 个节点（含原来的 node）+ 新 node：`k` 减 `{size}` → `{k}`',
        'pow10 //= 10': '向下：子树层数减一，`pow10` → `{pow10}`',
        'node *= 10': '访问 node 的第一个儿子 `{node}`',
        'k -= 1  # 访问新的 node 节点': '访问了新节点 `{node}`：`k` → `{k}`',
        'return node': '返回 =={ret}==：字典序第 15 小',
    },
    skip=['node = 1'],
    cards=dict(
        one_liner='在十叉树上先序遍历：子树不够 k 个就整棵跳过，否则钻进去',
        complexity='时间 `O(D log n)`（D = 10），空间 `O(1)`',
        problem=['给定整数 `n` 和 `k`，返回 `[1, n]` 中==字典序==第 `k` 小的数字',
                 '示例：`n = 13, k = 2` → `10`（`[1,10,11,12,13,2,3,…,9]`）',
                 '`1 <= k <= n <= 10⁹`：不能把所有数排序'],
        quote='先序遍历这棵树，等价于从左到右遍历字典序列表。所以==先序遍历访问到的第 k 个节点就是答案==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每访问一个节点 `k -= 1`；子树大小 `size ≤ k` → 整棵跳过，`k -= size`',
              '否则向下到第一个儿子，`k -= 1`（为什么是 ≤：子树根已经访问过了）',
              '子树大小 = 满层 `11…1 = (10^m − 1) / 9` + 最后一层余项，`O(1)` 算出'],
        result='第 15 小是 `22` ✓（`1,10..19,2,20,21,22`）',
        summary=['时间 `O(D log n)`：每层至多看 D 个兄弟，每个 `O(1)` 算子树大小',
                 '易错：`size ≤ k` 就向右；算子树最后一层用 `min(right, n + 1)` 截断',
                 '向下时 `pow10 //= 10`：子树少一层',
                 '优化前写法：逐层统计子树大小，`O(D log² n)`；还可以每层二分或解不等式'],
    ),
)
