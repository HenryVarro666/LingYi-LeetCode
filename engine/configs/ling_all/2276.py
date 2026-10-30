def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '动态开点线段树：每个节点 = 范围 [l,r] + 已 add 的整数个数 cnt（绿 = 整段已覆盖）', 22, T['muted'], bold=True)
    import builtins
    me = S.get('self')
    root = getattr(builtins, '_ROOTS', {}).get(id(me))
    if root is None:
        return
    inner = S.get('_inner') or {}
    cur = None
    lo, hi = root.l, root.r
    n = hi - lo + 1
    W = x1 - x0 - 60
    slot = W / n
    nodes = []

    def walk(nd, d):
        nodes.append((nd, d))
        for ch in (nd.left, nd.right):
            if ch is not None:
                walk(ch, d + 1)
    walk(root, 0)
    depth = max(d for _, d in nodes) + 1
    top = y0 + 100
    bottom_strip = y1 - 80
    gapy = min(120, (bottom_strip - top - 90) / max(1, depth - 1))
    nw, nh = min(78, slot * 0.92 * max(1, 1)), 52
    pos = {}
    for nd, d in nodes:
        pos[id(nd)] = (x0 + 30 + ((nd.l + nd.r) / 2 - lo + 0.5) * slot, top + d * gapy)
    for nd, d in nodes:
        for ch in (nd.left, nd.right):
            if ch is not None:
                cv.line([(pos[id(nd)][0], pos[id(nd)][1] + nh / 2), (pos[id(ch)][0], pos[id(ch)][1] - nh / 2)], T['border'], 2)
    for nd, d in nodes:
        if nd.l == me.l and nd.r == me.r:
            cur = nd
    for nd, d in nodes:
        X, Y = pos[id(nd)]
        full = nd.cnt == nd.r - nd.l + 1
        fill = T['yellow'] if nd is cur else (T['green'] if full else T['panel2'])
        tc = T['bg'] if (nd is cur or full) else T['text']
        cv.rect((X - nw / 2, Y - nh / 2, X + nw / 2, Y + nh / 2), fill=fill, r=10, outline=T['border'], width=2)
        cv.text((X, Y - 8), f'cnt={nd.cnt}', 19, tc, anchor='mm', bold=True)
        cv.text((X, Y + 13), f'[{nd.l},{nd.r}]', 17, tc, anchor='mm', mono=True)
    # 底部：整数 lo..hi 哪些已被覆盖
    def covered(v):
        nd = root
        while nd is not None:
            if nd.cnt == nd.r - nd.l + 1:
                return True
            nd = nd.left if (nd.left is not None and v <= nd.left.r) else (nd.right if v > nd.l and nd.right is not None and v >= nd.right.l else None)
        return False
    yy = y1 - 64
    cv.text((x0 + 18, yy - 28), '整数是否已被 add 覆盖：', 20, T['muted'])
    for v in range(lo, hi + 1):
        X = x0 + 30 + (v - lo) * slot
        c = covered(v)
        cv.rect((X + 3, yy, X + slot - 3, yy + 34), fill=T['green'] if c else T['panel2'], r=6, outline=T['border'], width=1)
        cv.text((X + slot / 2, yy + 17), v, 20, T['bg'] if c else T['dim'], anchor='mm', bold=True)


CONFIG = dict(
    num=2276, title='统计区间中的整数数目', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='动态开点线段树',
    tags=['八、树状数组和线段树', '难度分 2222'],
    code='''
class CountIntervals:
    __slots__ = 'left', 'right', 'l', 'r', 'cnt'

    def __init__(self, l=1, r=10 ** 9):
        self.left = self.right = None
        self.l, self.r, self.cnt = l, r, 0

    def add(self, l: int, r: int) -> None:
        if self.cnt == self.r - self.l + 1: return  # self 已被完整覆盖，无需执行任何操作
        if l <= self.l and self.r <= r:  # self 已被区间 [l,r] 完整覆盖，不再继续递归
            self.cnt = self.r - self.l + 1
            return
        mid = (self.l + self.r) // 2
        if self.left is None: self.left = CountIntervals(self.l, mid)  # 动态开点
        if self.right is None: self.right = CountIntervals(mid + 1, self.r)  # 动态开点
        if l <= mid: self.left.add(l, r)
        if mid < r: self.right.add(l, r)
        self.cnt = self.left.cnt + self.right.cnt

    def count(self) -> int:
        return self.cnt
''',
    call='''c = CountIntervals(1, 8)
import builtins; builtins._R = c
c.add(2, 3)
c.add(6, 7)
r1 = c.count()
c.add(3, 6)
r2 = c.count()
[r1, r2]''',
    expect=[4, 6],
    setup='''
import copy, builtins
builtins._ROOTS = {}
builtins._busy = [False]
_UNSET = object()
def _dc(self, memo):
    new = CountIntervals.__new__(CountIntervals)
    memo[id(self)] = new
    for a in ('l', 'r', 'cnt'):
        v = getattr(self, a, _UNSET)
        if v is not _UNSET:
            setattr(new, a, v)
    for a in ('left', 'right'):
        v = getattr(self, a, _UNSET)
        if v is not _UNSET:
            setattr(new, a, copy.deepcopy(v, memo))
    root = getattr(builtins, '_R', None)
    if root is not None and not builtins._busy[0]:
        builtins._busy[0] = True
        try:
            builtins._ROOTS[id(new)] = copy.deepcopy(root, {})
        finally:
            builtins._busy[0] = False
    return new
CountIntervals.__deepcopy__ = _dc
''',
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='calls', h=100),
    ],
    watch=['l', 'r', ('mid', 'mid', 'blue'), ('self.cnt', 'self.cnt', 'green')],
    skip=['self.left = self.right = None', 'self.l, self.r, self.cnt = l, r, 0'],
    max_steps=58,
    captions={
        'if self.cnt == self.r - self.l + 1': lambda S, B, ret: ('节点 `[{},{}]` 已被完整覆盖（cnt = {} = 长度）→ 什么都不用做'.format(S.self.l, S.self.r, S.self.cnt) if S.self.cnt == S.self.r - S.self.l + 1 else '节点 `[{},{}]` 还没被完整覆盖（cnt={}），继续'.format(S.self.l, S.self.r, S.self.cnt)),
        'if l <= self.l and self.r <= r': lambda S, B, ret: ('节点 `[{},{}]` 被 `[{},{}]` 完整覆盖 → ==不再递归==，直接记满'.format(S.self.l, S.self.r, S.l, S.r) if S.l <= S.self.l and S.self.r <= S.r else '节点 `[{},{}]` 只被部分覆盖 → 要往下走'.format(S.self.l, S.self.r)),
        'self.cnt = self.r - self.l + 1': '`cnt` = 长度 =={self.cnt}==：整段都算已添加，无需 lazy 标记',
        'mid = (self.l + self.r) // 2': '中点 `mid` = =={mid}==，左儿子管 `[{self.l},{mid}]`，右儿子管 `[{mid+1},{self.r}]`',
        'if self.left is None': lambda S, B, ret: ('左儿子还不存在 → ==动态开点==：新建 `[{},{}]`'.format(S.self.l, S.mid) if B['self'].left is None else '左儿子已经存在'),
        'if self.right is None': lambda S, B, ret: ('右儿子还不存在 → ==动态开点==：新建 `[{},{}]`'.format(S.mid + 1, S.self.r) if B['self'].right is None else '右儿子已经存在'),
        'if l <= mid': lambda S, B, ret: ('`l={}` ≤ `mid={}`：要添加的区间碰到左半边 → 递归左儿子'.format(S.l, S.mid) if S.l <= S.mid else '`l={}` > `mid={}`：左半边没有要添加的'.format(S.l, S.mid)),
        'if mid < r': lambda S, B, ret: ('`mid={}` < `r={}`：要添加的区间碰到右半边 → 递归右儿子'.format(S.mid, S.r) if S.mid < S.r else '`mid={}` ≥ `r={}`：右半边没有要添加的'.format(S.mid, S.r)),
        'self.cnt = self.left.cnt + self.right.cnt': '回溯更新：`cnt` = 左 `{self.left.cnt}` + 右 `{self.right.cnt}` = =={self.cnt}==',
        'return self.cnt': '返回根节点的 `cnt` = =={ret}==：不用遍历，直接 `O(1)`',
    },
    cards=dict(
        one_liner='线段树只在用到时才开点；整段被盖住就不再往下',
        complexity='`add` 时间 `O(log U)`（U 为值域），`count` 为 `O(1)`；空间 `O(q log U)`',
        problem=['`add(left, right)` 把闭区间 `[left, right]` 的整数加入集合，`count()` 返回集合里不同整数的个数',
                 '值域到 `10^9`，操作共 `10^5` 次，数组开不下',
                 '示例（本视频缩小到 `[1,8]`）：`add(2,3)` `add(6,7)` → `4`；`add(3,6)` → `6`'],
        quote='线段树的每个节点可以保存对应范围的左右端点 l 和 r，以及范围内 add 过的整数个数 cnt。代码实现时，无需记录 lazy tag，这是因为被覆盖的范围无需再次覆盖，因此若 cnt 等于范围的长度 r-l+1，则可直接返回。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['根节点管整个 `[1, 10^9]`；==需要时才新建==左右儿子（动态开点）',
              '`add`：完整覆盖就记满 `cnt = r-l+1` 并返回；否则拆成左右两半递归，回溯时 `cnt = 左 + 右`',
              '`cnt == 长度` 说明这一段早被盖满，再 add 直接 `return`，所以不需要 lazy tag'],
        summary=['`add` 每次最多新开 `O(log U)` 个点，`count` 直接读根节点 `cnt`',
                 '易错：回溯时别漏掉 `self.cnt = left.cnt + right.cnt`',
                 '为了动画能看清，示例把根范围改成了 `[1,8]`（原题是 `1..10^9`），代码一字未改',
                 '方法一：珂朵莉树，用 `SortedDict` 存不相交区间，合并后摊还 `O(log n)`（同 715 题）'],
    ),
)
