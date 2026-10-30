def _seg_view(title, getobj, n_of, root, kids, lines, cur_of, dim_of=None, nw=96):
    """线段树示意图：getobj(S)->树对象；kids(o)->(左,右)；lines(obj,o,l,r)->[文字行]；cur_of(S)->当前节点；
    黄 = 当前节点，淡黄 = 递归路径上的祖先，灰 = 已用完的节点。"""
    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
        obj = getobj(S)
        n = n_of(S, obj)
        if obj is None or not n:
            return
        nodes, parent, order = {}, {}, []

        def walk(o, l, r, d):
            nodes[o] = [l, r, d, None, None]
            if l < r:
                m = (l + r) // 2
                a, b = kids(o)
                nodes[o][3], nodes[o][4] = a, b
                parent[a] = o
                parent[b] = o
                walk(a, l, m, d + 1)
                walk(b, m + 1, r, d + 1)
        walk(root, 0, n - 1, 0)
        depth = max(v[2] for v in nodes.values()) + 1
        pos = {}
        cnt = [0]

        def place(o):
            l, r, d, a, b = nodes[o]
            if a is None:
                pos[o] = cnt[0]
                cnt[0] += 1
            else:
                place(a)
                place(b)
                pos[o] = (pos[a] + pos[b]) / 2
        place(root)
        W = x1 - x0 - 40
        gx = min(W / max(1, cnt[0]), nw + 14)
        sx = x0 + 20 + (W - gx * cnt[0]) / 2 + gx / 2
        top = y0 + 62
        gy = (y1 - top - 40) / max(1, depth)
        bw = min(nw, gx - 8)
        bh = min(gy - 18, 30 + 24 * (len(lines(obj, root, 0, 0)) - 1))
        cur = cur_of(S)
        anc = set()
        c = cur
        while c in parent:
            c = parent[c]
            anc.add(c)
        P = {o: (sx + pos[o] * gx, top + nodes[o][2] * gy + bh / 2) for o in nodes}
        for o, (l, r, d, a, b) in nodes.items():
            if a is not None:
                for ch in (a, b):
                    col = T['yellow'] if (ch == cur or ch in anc) and (o in anc or o == cur) else T['border']
                    cv.line([(P[o][0], P[o][1] + bh / 2), (P[ch][0], P[ch][1] - bh / 2)], col, 2)
        for o, (l, r, d, a, b) in nodes.items():
            x, y = P[o]
            dim = dim_of(obj, o) if dim_of else False
            if o == cur:
                cv.rect((x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2), fill=T['yellow'], r=8, alpha=70)
                oc = T['yellow']
            elif o in anc:
                oc = T['orange']
            else:
                oc = T['border'] if dim else T['blue']
            cv.rect((x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2), outline=oc, width=3, r=8)
            ls = lines(obj, o, l, r)
            for k, s in enumerate(ls):
                big = k < len(ls) - 1
                cv.text((x, y - bh / 2 + 8 + k * 24), s, 22 if big else 16,
                        (T['dim'] if dim else T['text']) if big else T['muted'], anchor='mt', bold=big, mono=True)
    return draw

_draw = _seg_view(
    '线段树：每个节点 = 区间内篮子容量的最大值（用掉的篮子变成 -1）',
    lambda S: (S.get('self') if hasattr(S.get('self'), 'max') else S.get('t')),
    lambda S, t: len(S.get('baskets') or S.get('a') or []),
    1, lambda o: (o * 2, o * 2 + 1),
    lambda t, o, l, r: [str(t.max[o]), f'[{l},{r}]'],
    lambda S: S['_inner'].get('o'),
    dim_of=lambda t, o: t.max[o] < 0)

CONFIG = dict(
    num=3479, title='水果成篮 III', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='线段树二分 + 单点修改',
    tags=['常用数据结构', '难度分 2178'],
    code='''
class SegmentTree:
    def __init__(self, a: List[int]):
        n = len(a)
        self.max = [0] * (2 << (n - 1).bit_length())
        self.build(a, 1, 0, n - 1)

    def maintain(self, o: int):
        self.max[o] = max(self.max[o * 2], self.max[o * 2 + 1])

    # 初始化线段树
    def build(self, a: List[int], o: int, l: int, r: int):
        if l == r:
            self.max[o] = a[l]
            return
        m = (l + r) // 2
        self.build(a, o * 2, l, m)
        self.build(a, o * 2 + 1, m + 1, r)
        self.maintain(o)

    # 找区间内的第一个 >= x 的数，并更新为 -1，返回这个数的下标（没有则返回 -1）
    def find_first_and_update(self, o: int, l: int, r: int, x: int) -> int:
        if self.max[o] < x:  # 区间没有 >= x 的数
            return -1
        if l == r:
            self.max[o] = -1  # 更新为 -1，表示不能放水果
            return l
        m = (l + r) // 2
        i = self.find_first_and_update(o * 2, l, m, x)  # 先递归左子树
        if i < 0:  # 左子树没找到
            i = self.find_first_and_update(o * 2 + 1, m + 1, r, x)  # 再递归右子树
        self.maintain(o)
        return i

class Solution:
    def numOfUnplacedFruits(self, fruits: List[int], baskets: List[int]) -> int:
        t = SegmentTree(baskets)
        n = len(baskets)
        ans = 0
        for x in fruits:
            if t.find_first_and_update(1, 0, n - 1, x) < 0:
                ans += 1
        return ans
''',
    call='Solution().numOfUnplacedFruits([4, 2, 5, 6], [3, 5, 4, 2, 6])',
    expect=1,
    skip=['self.max = [0]', 'n = len(a)', 'm = (l + r) // 2', 'self.max[o] = max(', 'if l == r', 'n = len(baskets)', 'ans = 0', 'return -1', 'return l', 'return i'],
    max_steps=130,
    views=[
        dict(type='text', fn=lambda S: (f"这批水果 `x = {S['x']}`：找最左边容量 >= {S['x']} 的篮子" if 'x' in S else ''), h=50),
        dict(type='custom', draw=_draw, h=400),
        dict(type='calls', label='递归调用栈', hide=('build',), h=130),
    ],
    watch=[('x', 'x', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'self.build(a, 1, 0, n - 1)': '建树：根节点 `1` 管篮子 `[0, {n - 1}]`，每个节点存区间==最大容量==',
        'self.build(a, o * 2, l, m)': '先建左半 `[{l}, {m}]`',
        'self.build(a, o * 2 + 1, m + 1, r)': '再建右半 `[{m + 1}, {r}]`',
        'self.maintain(o)': lambda S, B, r: f'回溯：`max[{S.o}]` = `max({S.self.max[S.o*2]}, {S.self.max[S.o*2+1]})` = =={max(S.self.max[S.o*2], S.self.max[S.o*2+1])}==',
        'self.max[o] = a[l]': '叶子 `{l}`：存篮子容量 `{a[l]}`',
        'for x in fruits': '下一种水果 `x = {x}`',
        'if t.find_first_and_update': '从根节点开始线段树二分：找最左边容量 >= `{x}` 的篮子',
        'ans += 1': '没有篮子容得下 `{x}` → `ans = {ans}`',
        'if self.max[o] < x': lambda S, B, r: (f'`max[{S.o}] = {S.self.max[S.o]} < {S.x}`：这棵子树里没有够大的篮子 → ==整棵剪掉==，返回 -1' if S.self.max[S.o] < S.x else f'`max[{S.o}] = {S.self.max[S.o]} >= {S.x}`：子树里至少有一个够大的篮子，继续往下找'),
        'self.max[o] = -1': '到叶子了，就是它。篮子 `{l}` 装了水果，容量改成 `-1`，以后谁也选不中它',
        'i = self.find_first_and_update(o * 2, l, m, x)': '==先递归左子树==：要最左边的，左边有就不用看右边',
        'if i < 0': lambda S, B, r: ('左子树没找到 → 去右子树' if S.i < 0 else f'左子树找到了篮子 `{S.i}`，右边不用看'),
        'i = self.find_first_and_update(o * 2 + 1, m + 1, r, x)': '左边没有够大的 → ==再递归右子树==',
    },
    cards=dict(
        one_liner='线段树维护区间最大容量，在树上二分找最左的篮子',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`fruits[i]` 是水果数量，`baskets[j]` 是篮子容量',
                 '水果从左到右依次放进==最左边容量 >= 它==的空篮子，每个篮子只装一种',
                 '求最后有几种水果没篮子放。示例：`[4,2,5,6]`、`[3,5,4,2,6]` → `1`'],
        quote='如果整棵子树的最大容量都小于 x，说明没有这样的篮子，返回 -1。所以线段树要维护 baskets 的区间最大值。否则，先递归左子树。如果左子树没找到，再递归右子树。',
        quote_src='—— 灵茶山艾府题解',
        idea=['暴力每次扫一遍篮子是 `O(n^2)`，`n = 10^5` 会超时',
              '树上每个节点存区间最大值：==最大值 < x 整棵剪掉==，否则优先走左边',
              '用掉的篮子改成 `-1`，再回溯重算最大值，线段树本身就保证“可用”'],
        summary=['时间 `O(n log n)`：每次查找+修改都是一条根到叶的路径',
                 '易错点：用掉的篮子要置 `-1`（不是 0），否则会被当成容量 0 的篮子；别忘了回溯时 `maintain`',
                 '数组开 `2 << (n-1).bit_length()`，比 `4n` 更省',
                 '同类题：本题单 §8.3 线段树（无区间更新）'],
    ),
)
