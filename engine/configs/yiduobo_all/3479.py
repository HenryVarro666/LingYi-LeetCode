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
    '线段树 ma：每个节点 = 区间内篮子容量的最大值（用掉的篮子变成 0）',
    lambda S: S.get('ma'),
    lambda S, ma: len(S.get('baskets') or []),
    0, lambda p: (p * 2 + 1, p * 2 + 2),
    lambda ma, p, l, r: [str(ma[p]), f'[{l},{r}]'],
    lambda S: S['_inner'].get('p'),
    dim_of=lambda ma, p: ma[p] <= 0)

CONFIG = dict(
    num=3479, title='水果成篮 III', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='线段树维护区间最大值',
    tags=['常用数据结构', '难度分 2178'],
    code='''
class Solution(object):
    def numOfUnplacedFruits(self, fruits, baskets):
        
        n = len(baskets)
        ma = [0] * (n * 4)

        def update(p, left, right, index, v):
            if left == right:
                ma[p] = v
                return

            mid = (left + right) // 2
            if index <= mid:
                update(p * 2 + 1, left, mid, index, v)
            else:
                update(p * 2 + 2, mid + 1, right, index, v)
            ma[p] = max(ma[p * 2 + 1], ma[p * 2 + 2])

        def find(p, left, right, v):
            if left == right:
                return left
            mid = (left + right) // 2
            if ma[p * 2 + 1] >= v:
                return find(p * 2 + 1, left, mid, v)
            else:
                return find(p * 2 + 2, mid + 1, right, v)

        for index, b in enumerate(baskets):
            update(0, 0, n - 1, index, b)
        
        res = 0
        for index, f in enumerate(fruits):
            if ma[0] < f:
                res += 1
            else:
                p = find(0, 0, n - 1, f)
                update(0, 0, n - 1, p, 0)
        
        return res
''',
    call='Solution().numOfUnplacedFruits([4, 2, 5, 6], [3, 5, 4, 2, 6])',
    expect=1,
    skip=['ma = [0]', 'n = len(baskets)', 'res = 0', 'mid = (left + right) // 2', 'return left', 'ma[p] = v', 'if left == right', 'ma[p] = max(', 'update(p * 2 + 1', 'update(p * 2 + 2', 'return find(p * 2 + 1', 'return find(p * 2 + 2'],
    max_steps=130,
    views=[
        dict(type='text', fn=lambda S: (f"水果 `f = {S['f']}`（第 {S['index']} 种）" if 'f' in S else '先把每个篮子容量写进线段树'), h=50),
        dict(type='custom', draw=_draw, h=400),
        dict(type='calls', label='递归调用栈', h=130),
    ],
    watch=[('f', 'f', 'yellow'), ('ma[0]', 'ma[0]', 'cyan'), ('res', 'res', 'green')],
    captions={
        'for index, b in enumerate(baskets)': lambda S, B, r: ('篮子都写进线段树了，开始放水果' if B.get('index') == S.index and B.get('b') == S.b else f'第 `{S.index}` 个篮子容量 `{S.b}`，用单点修改写进线段树'),
        'update(0, 0, n - 1, index, b)': '建树 = 一个个单点赋值：`update` 把叶子 `{index}` 设为 `{b}`，沿路径向上重算最大值',
        'if index <= mid': lambda S, B, r: f'`index = {S.index} <= mid = {S.mid}`？' + ('在左半区间 → 往左儿子走' if S.index <= S.mid else '在右半区间 → 往右儿子走'),
        'for index, f in enumerate(fruits)': lambda S, B, r: ('所有水果都处理完了' if B.get('index') == S.index and B.get('f') == S.f else f'第 `{S.index}` 种水果，数量 `{S.f}`'),
        'if ma[0] < f': lambda S, B, r: (f'根节点最大容量 `ma[0] = {S.ma[0]} < {S.f}`：没有篮子装得下 → ==未放置==' if S.ma[0] < S.f else f'根节点最大容量 `ma[0] = {S.ma[0]} >= {S.f}`：至少有一个篮子装得下，下去找最左的'),
        'res += 1': '未放置的水果 +1 → `res = {res}`',
        'p = find(0, 0, n - 1, f)': '从根开始二分：找最左边容量 >= `{f}` 的篮子',
        'update(0, 0, n - 1, p, 0)': '这个篮子放了水果，容量改成 `0`（以后装不下任何水果，也不影响最大值逻辑），再向上重算最大值',
        'if ma[p * 2 + 1] >= v': lambda S, B, r: (f'左儿子最大容量 `{S.ma[S.p*2+1]} >= {S.v}`：左半区间里有够大的篮子 → ==优先往左走==' if S.ma[S.p*2+1] >= S.v else f'左儿子最大容量 `{S.ma[S.p*2+1]} < {S.v}`：左边没有 → 去右半区间'),
        'return res': '一共 `{res}` 种水果没有篮子放',
    },
    cards=dict(
        one_liner='区间最大值 + 优先走左边：线段树上的二分查找',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`fruits[i]` 是第 `i` 种水果的数量，`baskets[j]` 是第 `j` 个篮子的容量',
                 '按顺序把水果放进==最左边、容量不小于它==的篮子，一个篮子只放一种',
                 '求未放置的水果种类数。示例：`[4,2,5,6]`、`[3,5,4,2,6]` → `1`'],
        quote='对于区间[left, right]，若区间最大值ma大于等于指定值v，说明区间中至少存在一处可用的下标。现在要求找出最左侧的可用下标，那么在这里可以先递归求解左半区间，若不存在，再递归求解右半区间。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n` 到 `10^5`，每种水果都扫一遍篮子会超时',
              '线段树每个节点存==区间最大容量==：左儿子够大就走左边，否则走右边',
              '用掉的篮子把容量改成 `0`：不会再被选中，也不破坏最大值的逻辑',
              '所以只需要“单点修改 + 区间最大值”'],
        summary=['时间 `O(n log n)`，数组开 `4n`，下标用 `p*2+1`、`p*2+2`（根为 0）',
                 '易错点：先判 `ma[0] < f` 再 `find`，保证一定找得到，`find` 里不用判无解',
                 '用掉的篮子改 `0`，不是删除；水果数量至少为 1，所以 0 永远装不下',
                 '代码逐字照搬原文（原文已用 `//` 整除，Python 3 可直接运行）',
                 '线段树细节可参考作者的 699 题题解'],
    ),
)
