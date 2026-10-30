def _root(S):
    b = S.get('bst')
    return getattr(b, 'root', None) if b is not None else None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '完美平衡树（节点 = 值 / size：该子树已插入的个数）', 24, T['muted'], bold=True)
    root = _root(S)
    if root is None:
        cv.text((x0 + 18, y0 + 70), '建树中：把排好序的 all_nums 递归取中点', 26, T['dim'])
        return
    order, depth = [], {}

    def ino(n, d):
        if n is None:
            return
        depth[id(n)] = d
        ino(n.left, d + 1)
        order.append(n)
        ino(n.right, d + 1)
    ino(root, 0)
    n = len(order)
    xi = {id(o): i for i, o in enumerate(order)}
    maxd = max(depth.values()) + 1
    sp = min(110, (x1 - x0 - 60) / n)
    dy = min(110, (y1 - y0 - 130) / maxd)
    rad = max(22, min(34, sp * 0.42))
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * n) / 2 + sp / 2

    def P(o):
        return sx + xi[id(o)] * sp, y0 + 70 + depth[id(o)] * dy + rad
    cur = S.get('curr')
    for o in order:
        X, Y = P(o)
        for ch in (o.left, o.right):
            if ch is not None:
                X2, Y2 = P(ch)
                cv.line([(X, Y), (X2, Y2)], T['border'], 3)
    for o in order:
        X, Y = P(o)
        live = o.size > 0
        fill = T['green'] if (cur is o) else (T['panel2'] if live else (36, 40, 48))
        out = T['yellow'] if cur is o else (T['blue'] if live else T['border'])
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=out, width=4 if cur is o else 2)
        cv.text((X, Y), o.val, int(rad * 0.9), T['bg'] if cur is o else (T['text'] if live else T['dim']), anchor='mm', bold=True)
        cv.text((X, Y + rad + 4), f'size={o.size}', 20, T['yellow'] if live else T['dim'], anchor='mt', bold=True)
    if cur is not None and 'k' in S and S.get('_line') in (KTH_LINES):
        cv.text((x1 - 20, y0 + 6), f"找第 {S['k']} 小", 22, T['green'], anchor='ra', bold=True)


KTH_LINES = tuple(range(31, 42))


def _info(S):
    if 'queries' not in S or 'tot' not in S:
        return ''
    return f"树里已插入 `tot = {S['tot']}` 个数（size 为 0 的节点还没插入）"


CONFIG = dict(
    num=3935, title='插入后第K大更新的幂I', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='离线 + 完美平衡树 + size 查第 k 小',
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
    call='Solution().powerUpdate([4], 2, [[3, 1], [1, 2]])',
    expect=[16, 4096],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='all_nums', h=150, label='all_nums（离线收集的全部不同数值，绿 = 本次取出的第 k 大）',
             color=lambda S, i, v: ('green' if 'x' in S and S['x'] == v else None)),
        dict(type='text', size=28, h=60, fn=_info),
    ],
    watch=['v', 'k', 'tot', 'x'],
    max_steps=120,
    skip=['curr = self.root', 'while curr.val != v', 'if v < curr.val', 'mod = 10', 'res = []', 'while True', 'if p == 0', 'return 1', 'self.val = val', 'self.size = 0', 'self.left = None', 'self.right = None'],
    captions={
        'all_nums = sorted': '离线：先把 nums 和所有查询的 `val` 都收起来，去重排序 → `{all_nums}`',
        'bst = BST(': '用 all_nums 建一棵高度最小的平衡树，所有 size 先为 0',
        'mid = (start + end)': '取 `[{start}, {end}]` 的中点 `mid = {mid}` 当根',
        'node = Node': '新建节点，值取 `nums[{mid}] = {nums[mid]}`',
        'node.left = self.build': '`start < mid`：左半 `[{start}, {mid - 1}]` 还有数，递归建左子树',
        'node.right = self.build': '`mid < end`：右半 `[{mid + 1}, {end}]` 还有数，递归建右子树',
        'return node': '这一段建完，返回节点 `{node.val}`',
        'self.root = self.build': '平衡树建好，`root = {root.val}`',
        'curr = self.root': '从根出发',
        'curr.size += 1': '到了节点 `{curr.val}`（目标 `v = {v}`）：`size` 加 1 → =={curr.size}==',
        'while curr.val != v': lambda S, B, r: f'`curr.val = {S.curr.val}` 和 `v = {S.v}` 比：{"==找到了，停==" if S.curr.val == S.v else "还没到，继续往下"}',
        'if v < curr.val': '`{v} < {curr.val}` → {"往左" if v < curr.val else "往右"}走',
        'curr = curr.left': '`v = {v}` 比上一个节点小 → 往左走到 `{curr.val}`',
        'curr = curr.right': '`v = {v}` 更大 → 往右走到 `{curr.val}`',
        'for v in nums': '先把初始 nums 的值逐个插入树里（只更新 size）',
        'for v, k in queries': lambda S, B, r: (f'取下一个查询：`val = {S.v}`，`k = {S.k}`' if S.v != B.v else '查询全部处理完'),
        'bst.update(v)': '把 `val = {v}` 插入：沿路径所有节点的 `size` 加 1',
        'tot += 1': '树里现在有 `tot = {tot}` 个数',
        'x = bst.kth': '第 `{B.k}` 大 = 第 `tot − k + 1 = {B.tot - B.k + 1}` 小（tot = {B.tot}），用 size 在树里查',
        'curr.left and curr.left.size >= k': lambda S, B, r: (f'左子树 `size = {B.curr.left.size}` ≥ `k = {B.k}` → ==第 k 小在左边==' if B.curr.left and B.curr.left.size >= B.k else f'左子树装不下第 `{B.k}` 个（size = {B.curr.left.size if B.curr.left else 0}），不在左边'),
        'curr.right and curr.size - curr.right.size < k': lambda S, B, r: (f'`size − 右子树 size = {B.curr.size - B.curr.right.size}` < `k = {B.k}` → ==在右边==' if B.curr.right and B.curr.size - B.curr.right.size < B.k else '右边没有更多（或 k 已落在当前节点）'),
        'k -= curr.size - curr.right.size': '跳过根和左边这 `{B.curr.size - B.curr.right.size}` 个，`k` 变成 {k}，去右子树找',
        'return curr.val': '就是当前节点：第 k 小 = ==`{curr.val}`==',
        'p = quick_pow': '`p = p^x % mod`，用快速幂：`x = {x}`',
        'res.append(p)': '记录这次查询后的 `p = {p}`',
        'if p == 1': '指数 `{p}`：{"==是 1，直接返回 base==" if p == 1 else "还大于 1，继续折半"}（指数为 0 时返回 1，此处略过）',
        'res = quick_pow': '指数折半：先算 `base^{p // 2}`',
        'res = res * res': '平方：`res` = res² % mod = {res}',
        'if p & 1': '指数 `{p}` 是奇数吗？→ {"==是，再乘一个 base==" if p & 1 else "否"}',
        'res = res * base': '补乘一个 `base` → {res}',
        'return res': lambda S, B, ret: (f'全部查询完，返回 `{ret}`' if isinstance(ret, list) else f'快速幂结果 `{S.res}`'),
        'return base': '指数 1：返回 `base = {base}`',
        'return 1': '指数 0：返回 1',
    },
    cards=dict(
        one_liner='离线建好完美平衡树，每个节点记 size，查询只需 O(log n) 找第 k 小',
        complexity='时间 `O((n+q) log n)`，空间 `O(n+q)`',
        problem=['给整数数组 `nums`、整数 `p`、查询 `queries[i] = [val, k]`',
                 '每次查询：把 `val` 加入 `nums`，取当前第 `k` 大的数 `x`，令 `p = p^x % (10^9+7)`',
                 '本视频：`nums=[4], p=2, [[3,1],[1,2]]` → `[16, 4096]`'],
        quote='本题实际上可以理解成动态区间第k大值的问题，不过本题中只有插入没有删除，因此在这里可以使用离线技巧。',
        quote_src='—— yiduobo 题解原文',
        idea=['先扫一遍所有查询，得知最终会出现哪些数 → 排序去重',
              '用这些数建一棵高度最小的平衡树，节点多一个 `size`，一开始全 0',
              '插入 = 沿路径给 `size` +1；第 `k` 大 = 第 `tot−k+1` 小，按 size 往下走'],
        summary=['时间 `O((n+q) log n)`，空间 `O(n+q)`',
                 '易错点：第 k ==大==要换成第 `tot − k + 1` ==小==',
                 '`kth` 里 `curr.size − curr.right.size` 是根加左子树的已插入个数；树不变形，插入只是 size 加一',
                 '快速幂 `quick_pow` 递归折半，指数是 `x`（树里取出的值），不是 `p` 本身'],
    ),
)
