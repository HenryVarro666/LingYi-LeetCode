def _nodes_of(S):
    """从变量里找出所有线段树节点：{(start, end): node}"""
    found = {}
    seen = set()

    def walk(x, d=0):
        if d > 40 or x is None or id(x) in seen:
            return
        if isinstance(x, (list, tuple)):
            seen.add(id(x))
            for y in x:
                walk(y, d + 1)
        elif hasattr(x, 'start') and hasattr(x, 'end') and hasattr(x, 'both'):
            seen.add(id(x))
            found[(x.start, x.end)] = x
            walk(getattr(x, 'left', None), d + 1)
            walk(getattr(x, 'right', None), d + 1)
        elif hasattr(x, 'root'):
            seen.add(id(x))
            walk(x.root, d + 1)
    for k, v in S.items():
        if not k.startswith('_') or k in ('self._done',):
            walk(v)
    return found


def _skeleton(n):
    out = []

    def go(s, e, d):
        out.append((s, e, d))
        if s < e:
            m = (s + e) // 2
            go(s, m, d + 1)
            go(m + 1, e, d + 1)
    go(0, n - 1, 0)
    return out


def _vals(nd):
    return (nd.head, nd.tail, nd.both, nd.neither)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(S['nums'])
    cur, old = _nodes_of(S), _nodes_of(B)
    sk = _skeleton(n)
    maxd = max(d for _, _, d in sk) + 1
    cv.text((x0 + 18, y0 + 4), '线段树节点：head tail / both neither（黄 = 刚改动，虚线 = 还没建）', 22, T['muted'], bold=True)
    slot = (x1 - x0 - 40) / n
    bw, bh = min(slot * 0.92, 160), 92
    dy = min(150, (y1 - y0 - 110 - bh) / max(1, maxd - 1))
    node = S.get('node')
    nkey = (node.start, node.end) if node is not None and hasattr(node, 'start') else None
    path = set()
    for p in (S.get('node_list') or []):
        path.add((p.start, p.end))
    pos = {}
    for s, e, d in sk:
        pos[(s, e)] = (x0 + 20 + (s + e + 1) / 2 * slot, y0 + 78 + d * dy + bh / 2)
    for s, e, d in sk:
        if s < e:
            m = (s + e) // 2
            for c in ((s, m), (m + 1, e)):
                cv.line([(pos[(s, e)][0], pos[(s, e)][1] + bh / 2), (pos[c][0], pos[c][1] - bh / 2)], T['border'], 3)
    for s, e, d in sk:
        X, Y = pos[(s, e)]
        nd = cur.get((s, e))
        rect = (X - bw / 2, Y - bh / 2, X + bw / 2, Y + bh / 2)
        if nd is None:
            cv.rect(rect, outline=T['dim'], width=2, r=10)
            cv.text((X, Y - bh / 2 + 4), f'[{s},{e}]' if s < e else f'[{s}]', 17, T['dim'], anchor='mt', mono=True)
            continue
        v = _vals(nd)
        ov = _vals(old[(s, e)]) if (s, e) in old else None
        outline, width = T['border'], 2
        if (s, e) in path:
            outline, width = T['cyan'], 3
        if ov is not None and ov != v:
            outline, width = T['yellow'], 4
        if (s, e) == nkey:
            outline, width = T['blue'], 4
        cv.rect(rect, fill=T['panel2'], outline=outline, width=width, r=10)
        cv.text((X, Y - bh / 2 + 4), f'[{s},{e}]' if s < e else f'[{s}]', 17, T['muted'], anchor='mt', mono=True)
        for k, (dx, dyy) in enumerate(((-1, 0), (1, 0), (-1, 1), (1, 1))):
            col = T['text']
            cv.text((X + dx * bw * 0.24, Y - 1 + dyy * 28), v[k], 22, col, anchor='mm', bold=(k == 2))
    if nkey in pos:
        X, Y = pos[nkey]
        cv.text((X + bw / 2 + 6, Y - bh / 2 - 2), 'node', 18, T['blue'], anchor='lb', bold=True)
    cv.text((x0 + 18, y1 - 34), '左上 head：含首不含尾　　右上 tail：含尾不含首', 19, T['dim'], anchor='lb')
    cv.text((x0 + 18, y1 - 8), '左下 both：首尾都含　　右下 neither：首尾都不含', 19, T['dim'], anchor='lb')


def _root_best(S):
    ns = _nodes_of(S)
    r = ns.get((0, len(S['nums']) - 1))
    return max(_vals(r)) if r else 0


CONFIG = dict(
    num=3165, title='不包含相邻元素的子序列的最大和', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='线段树 · head/tail/both/neither',
    tags=['灵神题单·常用数据结构', '难度分 2697'],
    code='''
class Node(object):
    def __init__(self, start, end):
        self.left = self.right = None
        self.start, self.end = start, end
        self.head = 0
        self.tail = 0
        self.both = 0
        self.neither = 0

    def update(self, v=0):
        if self.start == self.end:
            self.both = max(v, 0)
        else:
            self.head = max(0, self.left.head + max(0, self.right.head, self.right.neither), self.left.both + self.right.neither)
            self.tail = max(0, self.right.tail + max(0, self.left.tail, self.left.neither), self.left.neither + self.right.both)
            self.both = max(0, self.left.head + self.right.tail, self.left.both + self.right.tail, self.left.head + self.right.both)
            self.neither = max(0, self.left.tail + self.right.neither, self.left.neither + self.right.head, self.left.neither + self.right.neither)

class Tree(object):
    def __init__(self, nums):
        n = len(nums)
        self.root = self.build(0, n - 1, nums)

    def build(self, start, end, nums):
        if start == end:
            node = Node(start, end)
            node.update(nums[start])
        else:
            node = Node(start, end)
            mid = (start + end) // 2
            node.left = self.build(start, mid, nums)
            node.right = self.build(mid + 1, end, nums)
            node.update()

        return node

    def update(self, index, v):
        node_list = [self.root]
        while node_list[-1].start != node_list[-1].end:
            if index <= node_list[-1].left.end:
                node_list.append(node_list[-1].left)
            else:
                node_list.append(node_list[-1].right)
        
        for node in node_list[::-1]:
            node.update(v)

        return max(self.root.head, self.root.tail, self.root.both, self.root.neither)

class Solution(object):
    def maximumSumSubsequence(self, nums, queries):

        tree = Tree(nums)
        res = 0
        mod = 10 ** 9 + 7
        for index, v in queries:
            res += tree.update(index, v)
            if res >= mod:
                res -= mod
        
        return res
''',
    setup='''
_orig_build = Tree.build
def _build_logged(self, start, end, nums):
    r = _orig_build(self, start, end, nums)
    self.__dict__.setdefault('_done', []).append(r)   # 仅供动画画图：记下已建好的子树
    return r
Tree.build = _build_logged
''',
    call='Solution().maximumSumSubsequence([3, 5, 9], [[1, -2], [0, -3]])',
    expect=21,
    views=[
        dict(type='text', fn=lambda S: f"当前查询：`nums[{S['index']}] = {S['v']}`" if 'index' in S and 'res' in S else '先建树：左右各自建好，再合并', h=50),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('res', 'res', 'green'), ('index', 'index', 'blue'), ('v', 'v', 'pink')],
    skip=['self.left = self.right = None', 'self.start, self.end = start, end', 'self.head = 0', 'self.tail = 0',
          'self.both = 0', 'self.neither = 0', 'mod = 10', 'return node', 'if self.start == self.end', 'if start == end',
          'while node_list[-1].start', 'for node in node_list[::-1]'],
    max_steps=58,
    captions={
        'node = Node(start, end)': '为区间 `[{start}, {end}]` 创建节点，四个值先都是 0',
        'node.update(nums[start])': '叶子 `[{start}]`：只有 both，其余三个不存在，按 0 处理',
        'self.both = max(v, 0)': '叶子的 `both = max({v}, 0)` = =={max(v, 0)}==（空子序列和为 0，负数不选）',
        'mid = (start + end) // 2': '`mid = {mid}`：左半 `[{start}, {mid}]`，右半 `[{mid + 1}, {end}]`',
        'node.left = self.build': '先建左半，挂到 `node.left`',
        'node.right = self.build': '再建右半，挂到 `node.right`',
        'node.update()': '左右都建好了，用它们合并出 `[{start}, {end}]` 的四个值',
        'self.head = max': '`head` = =={self.head}==（含首不含尾）：左 head 配右 head/neither，或左 both 配右 neither',
        'self.tail = max': '`tail` = =={self.tail}==（含尾不含首，与 head 对称）',
        'self.both = max(0': '`both` = =={self.both}==：首尾都含，==left.both 与 right.both 不能同取==',
        'self.neither = max': '`neither` = =={self.neither}==：首尾都不含，==left.tail 与 right.head 不能同取==',
        'node_list = [self.root]': '从根出发，记下根到目标叶子的路径 `node_list`',
        'if index <= node_list[-1].left.end': lambda S, B, r: f'`index = {S.index}` 在左儿子区间内？ → ==' + ('是，走左边' if S.index <= B.node_list[-1].left.end else '否，走右边') + '==',
        'node_list.append(node_list[-1].left)': '路径加入左儿子 `[{node_list[-1].start}, {node_list[-1].end}]`',
        'node_list.append(node_list[-1].right)': '路径加入右儿子 `[{node_list[-1].start}, {node_list[-1].end}]`',
        'for node in node_list[::-1]': '从叶子往根倒着走：先改叶子，再逐层重新合并',
        'node.update(v)': '倒着更新节点 `[{node.start}, {node.end}]`：先叶子，再往上逐层合并',
        'return max(self.root': '整棵树的答案 = 根节点四个值的最大值',
        'res += tree.update': '查询：`nums[{index}] = {v}`，调用 `tree.update`，改完返回当前最大和',
        'if res >= mod': '本次最大和已加进 `res` = =={res}==；`res >= mod` 才需要减一次模',
        'res -= mod': '超过 mod 就减一次 mod',
    },
    cards=dict(
        one_liner='带单点修改的区间最优：线段树每个节点存四个值',
        complexity='时间 `O(n + q log n)`，空间 `O(n)`',
        problem=['`nums` 每次先改一个位置，再求不含相邻元素的子序列最大和（可为空）',
                 '把所有查询的答案加起来，对 `10^9+7` 取模',
                 '示例：`[3,5,9]`，查询 `[[1,-2],[0,-3]]` → `12 + 9 = 21`'],
        quote='对于区间[start, end]而言，从[start, end]这个层面需要关注的事情就是mid和mid + 1这两个元素只能选择其中一个，而[start, mid]以及[mid + 1, end]中保证子序列的元素不相邻则由子区间自行负责。',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素 DP 每次 `O(n)`，查询 5 万次会超时；改成「单点修改 + 全局查询」',
              '每个节点存 `head / tail / both / neither`：首尾元素各自 ==是否被选中==',
              '合并时只需保证 `mid` 和 `mid+1` 不同时选，其余交给子区间'],
        summary=['时间 `O(n + q log n)`，空间 `O(n)`',
                 '叶子里只有 `both = max(0, nums[i])`，不存在的情况按 0 处理（空子序列）',
                 '`both` 和 `neither` 各有三种合法组合，要排除 mid 与 mid+1 同时选',
                 '更新要沿路径==自底向上==，所以先记录 `node_list` 再倒着更新',
                 '原文本身可直接在 Python 3 运行，代码未改动；动画里另挂了一个记录已建子树的辅助，仅用于画图'],
    ),
)
