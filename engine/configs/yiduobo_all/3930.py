def _root(S):
    for k in ('bst', 'self'):
        b = S.get(k)
        r = getattr(b, 'root', None)
        if r is not None:
            return r
    return None


def _draw_tree(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'BST（每个节点：值 + 下方 size = 子树里已插入的个数）', 24, T['muted'], bold=True)
    r = _root(S)
    if r is None:
        return
    order, depth = [], {}

    def ino(n, d):
        if n is None:
            return
        depth[id(n)] = d
        ino(n.left, d + 1)
        order.append(n)
        ino(n.right, d + 1)
    ino(r, 0)
    maxd = max(depth.values()) + 1
    sp = min(130, (x1 - x0 - 60) / len(order))
    dy = min(110, (y1 - y0 - 110) / max(1, maxd))
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * len(order)) / 2 + sp / 2
    pos = {id(n): (sx + i * sp, y0 + 80 + depth[id(n)] * dy) for i, n in enumerate(order)}
    cur = S.get('curr')
    for n in order:
        for c in (n.left, n.right):
            if c is not None:
                cv.line([pos[id(n)], pos[id(c)]], T['border'], 3)
    for n in order:
        X, Y = pos[id(n)]
        hit = cur is n
        fill = T['green'] if n.size > 0 else (60, 66, 76)
        cv.rect((X - 30, Y - 28, X + 30, Y + 28), fill=fill, outline=T['yellow'] if hit else None, width=5 if hit else 1, r=28)
        cv.text((X, Y), n.val, 28, T['bg'] if n.size > 0 else T['text'], anchor='mm', bold=True)
        cv.text((X, Y + 40), f'size={n.size}', 20, T['yellow'] if hit else T['muted'], anchor='mm', mono=True)


def _sizes(S):
    r = _root(S)
    if r is None:
        return ''
    out = []

    def go(n):
        if n is None:
            return
        go(n.left)
        out.append(f'{n.val}:{n.size}')
        go(n.right)
    go(r)
    return '各节点 `值:size`（size = 子树里已插入的个数）　' + '　'.join(out)


CONFIG = dict(
    num=3930, title='插入后第K大更新的幂II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='离线 · 完美平衡树 + 子树计数',
    tags=[],
    code='''
class Node():
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.size = 0
        self.left = None
        self.right = None

class BST():
    def build(self, nums, start, end):
        mid = (start + end) // 2
        node = Node(nums[mid], None, None)
        if start < mid:
            node.left = self.build(nums, start, mid - 1)
        if mid < end:
            node.right = self.build(nums, mid + 1, end)
        return node

    def __init__(self, nums):
        self.root = self.build(nums, 0, len(nums) - 1)

    def update(self, v):
        curr = self.root
        curr.size += 1
        while curr.val != v:
            if v < curr.val:
                curr = curr.left
            else:
                curr = curr.right
            curr.size += 1
    
    def kth(self, k):
        curr = self.root
        while True:
            if curr.left and curr.left.size >= k:
                curr = curr.left
            elif curr.right and curr.size - curr.right.size < k:
                k -= curr.size - curr.right.size
                curr = curr.right
            else:
                return curr.val

class Solution(object):
    def powerUpdate(self, nums, p, queries):
        
        all_nums = sorted(list(set(nums + [v for v, _ in queries])))
        bst = BST(all_nums)
        for v in nums:
            bst.update(v)
        
        mod = 10 ** 9 + 7
        def quick_pow(base, p):
            if p == 0:
                return 1
            if p == 1:
                return base
            
            res = quick_pow(base, p // 2)
            res = res * res % mod
            if p & 1:
                res = res * base % mod
            return res

        res = []
        tot = len(nums)
        for v, k in queries:
            bst.update(v)
            tot += 1
            x = bst.kth(tot - k + 1)
            p = quick_pow(p, x)
            res.append(p)
        
        return res
''',
    call='Solution().powerUpdate([3], 2, [[5, 1], [1, 2]])',
    expect=[32, 32768],
    views=[
        dict(type='custom', draw=_draw_tree, h=330),
        dict(type='text', size=26, fn=lambda S: (f"`tot = {S['tot']}`　第 `k` 大 = 第 `tot - k + 1` 小" if 'tot' in S and 'k' in S else '')),
        dict(type='calls', h=130),
    ],
    watch=['tot', 'v', 'k', 'x', 'p', ('res', 'res', 'green')],
    skip=['if v < curr.val', 'curr = self.root', 'if p == 0', 'if p == 1', 'if p & 1', 'while True', 'mod = 10', 'res = []', 'mid = (start', 'node = Node', 'self.right = None', 'self.left = None', 'self.size = 0', 'self.val = val'],
    max_steps=140,
    captions={
        'all_nums = sorted': '离线：先把初始 `nums` 和所有查询的值收集、去重、排序 → `all_nums = {all_nums}`（最终会出现的全部值）',
        'bst = BST': '用 `all_nums` 建一棵==高度完美平衡的 BST==，每个节点带 `size` 计数，一开始全是 0',
        'node.left = self.build': '递归建左子树：区间 `[{start}, {mid - 1}]`',
        'node.right = self.build': '递归建右子树：区间 `[{mid + 1}, {end}]`',
        'return node': '这个区间建好了，返回 `{node.val}` 这个节点',
        'self.root = self.build': '整棵树建好：根是 `{self.root.val}`，所有 `size` 都是 0',
        'for v in nums': lambda S, B, r: ('初始值都“插入”完了，开始处理查询' if 'v' in B and S.v == B.v
                                          else '把初始 `nums` 里的值逐个“插入”：不改树形，只给路径上的 `size` 加 1'),
        'bst.update(v)': '沿路径把 `{v}` 插入：根到 `{v}` 这条路径上每个节点 `size + 1`',
        'curr.size += 1': '`curr = {curr.val}` 的 `size` → {curr.size}',
        'while curr.val != v': lambda S, B, r: (f'`curr.val = {S.curr.val}` 已经是 `{S.v}` → 到达，停' if S.curr.val == S.v
                                                else f'`curr.val = {S.curr.val} ≠ {S.v}`，继续往下走'),
        'if v < curr.val': lambda S, B, r: (f'`{S.v} < {S.curr.val}` → 往左' if S.v < S.curr.val else f'`{S.v} > {S.curr.val}` → 往右'),
        'curr = curr.left': '走到左孩子 `{curr.val}`',
        'curr = curr.right': '走到右孩子 `{curr.val}`',
        'mod = 10': '结果要对 `10^9 + 7` 取模',
        'tot = len(nums)': '`tot` 记录当前一共插入了几个数：`{tot}`',
        'for v, k in queries': lambda S, B, r: (f'第 `{len(S.res) + 1}` 个查询：插入 `v = {S.v}`，要第 `k = {S.k}` 大' if (S.get('v'), S.get('k')) != (B.get('v'), B.get('k')) or 'v' not in B
                                                else '所有查询都处理完了'),
        'tot += 1': '插入后共 `tot = {tot}` 个数',
        'x = bst.kth': '第 K 大 = 第 `tot - K + 1 = {k}` 小：调用 `kth` 去树里找第 `{k}` 小',
        'def kth': '找第 `k` 小：用 `size` 判断往哪边走',
        'if curr.left and curr.left.size': lambda S, B, r: (f'左子树有 `{S.curr.left.size}` 个 ≥ `k = {S.k}` → 答案在左边' if S.curr.left and S.curr.left.size >= S.k
                                                          else f'左子树只有 `{S.curr.left.size if S.curr.left else 0}` 个，不够 `k = {S.k}`，答案不在左边'),
        'elif curr.right': lambda S, B, r: (f'`size - 右子树 size = {S.curr.size - S.curr.right.size}`（左子树 + 自己）`< k = {S.k}` → 答案在右边'
                                            if S.curr.right and S.curr.size - S.curr.right.size < S.k
                                            else '右边没有或者“左子树 + 自己”已经够 k 个'),
        'k -= curr.size': '跳过“左子树 + 自己”：`k` → {k}，去右子树里找',
        'return curr.val': '就是当前节点：第 `k` 小 = =={ret}==',
        'def quick_pow': '快速幂：`base^p % mod`',
        'if p == 0': '`p == 0` → 返回 1',
        'if p == 1': '`p == 1` → 返回 `base`',
        'res = quick_pow': '先算 `base^(p//2)`：进入递归，`p = {p}`',
        'res = res * res': '平方：`res = res² % mod` = {res}',
        'if p & 1': lambda S, B, r: ('`p` 是奇数，还要再乘一个 `base`' if S.p & 1 else '`p` 是偶数，不用再乘'),
        'res = res * base': '`res = res * base % mod` = {res}',
        'return res': '返回 `{ret}`',
        'return base': '`p == 1` → 返回 `{ret}`',
        'return 1': '`p == 0` → 返回 1',
        'p = quick_pow': '`p = p^x % mod`：用快速幂计算（`x` 可能很大）',
        'res.append(p)': '`p` 更新为 =={p}==，记下这次答案：`res = {res}`',
        'return res\n': '全部查询处理完：`{ret}`',
    },
    cards=dict(
        one_liner='离线建好平衡树，每个节点记子树已插入个数，插入加一、找第 k 小按 size 走',
        complexity='时间 `O((n+q) log(n+q))`，空间 `O(n+q)`',
        problem=['数组 `nums`、整数 `p`、查询 `[val, k]`',
                 '每次查询：把 `val` 加入 `nums`，取第 `k` 大的 `x`，令 `p = p^x % (10^9+7)`',
                 '返回每次查询后的 `p`；本视频：`nums=[3]`，`p=2`，`[[5,1],[1,2]]` → `[32, 32768]`',
                 '（题面为按 yiduobo 文章整理）'],
        quote='本题实际上可以理解成动态区间第k大值的问题，不过本题中只有插入没有删除，因此在这里可以使用离线技巧。',
        quote_src='—— yiduobo 题解原文',
        idea=['先过一遍所有查询，得到最终会出现的全部数值，排序去重',
              '用它们建一棵==完美平衡树==，节点带 `size`，一开始都是 0',
              '“插入”只是沿路径给 `size` 加 1；第 `k` 大 = 第 `tot-k+1` 小，按 `size` 往左/往右走',
              '用快速幂算 `p^x % mod`，`x` 可能很大'],
        result='每次查询后的 p：`[32, 32768]` ✓',
        summary=['时间 `O((n+q) log(n+q))`：建树、每次插入/查询都是树高 `O(log)`',
                 '第 `k` 大要换成第 `tot - k + 1` 小再找',
                 '`kth` 里 `curr.size - curr.right.size` = 左子树 + 自己 的个数',
                 '原文已是 Python 3 可运行写法（`//` 整除），代码未改',
                 '3935 题（I，弱化版）同一思路也能做'],
    ),
)
