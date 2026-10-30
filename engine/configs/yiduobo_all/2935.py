def _trie_draw(cv, S, B, box, T, root, children, nbits, cur, title):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
    top, bot = y0 + 80, y1 - 100
    gap = (bot - top) / nbits
    W = x1 - x0 - 60
    sx = x0 + 30
    R = 22
    pos = {}

    def walk(node, d, p, cnt):
        X = sx + (p + 0.5) / (1 << d) * W
        Y = top + d * gap
        pos[id(node)] = (X, Y)
        for bit, ch, c in children(node):
            walk(ch, d + 1, p * 2 + bit, c)
    walk(root, 0, 0, None)

    def paint(node, d, p, cnt):
        X, Y = pos[id(node)]
        for bit, ch, c in children(node):
            X2, Y2 = pos[id(ch)]
            col = T['dim'] if c == 0 else T['muted']
            cv.line([(X, Y + R), (X2, Y2 - R)], col, 3)
            cv.text(((X + X2) / 2 + (-14 if bit == 0 else 14), (Y + Y2) / 2), str(bit), 22, T['cyan'] if bit == 0 else T['orange'], anchor='mm', bold=True, mono=True)
        for bit, ch, c in children(node):
            paint(ch, d + 1, p * 2 + bit, c)
        dead = cnt == 0
        is_cur = cur is not None and node is cur
        fill = T['yellow'] if is_cur else (T['bg'] if dead else T['panel2'])
        cv.rect((X - R, Y - R, X + R, Y + R), fill=fill, outline=T['dim'] if dead else T['blue'], width=3, r=R)
        label = 'R' if cnt is None else str(cnt)
        cv.text((X, Y), label, 26, T['bg'] if is_cur else (T['dim'] if dead else T['text']), anchor='mm', bold=True, mono=True)
        if d == nbits:
            cv.text((X, Y + R + 8), str(p), 22, T['dim'] if dead else T['green'], anchor='mt', bold=True, mono=True)
    paint(root, 0, 0, None)
    cv.text((x0 + 18, y1 - 6), '圆里的数字 = 经过该节点的数个数（0 = 已删除，变暗）；黄色 = 当前走到的节点；叶子下方 = 对应的数', 20, T['muted'], anchor='lb')


def _kids(node):
    out = []
    for b in (0, 1):
        ch = node[0][b]
        if ch is not None:
            out.append((b, ch, node[1][b]))
    return out


def _draw_trie(cv, S, B, box, T):
    root = S.get('root')
    if root is None:
        return
    _trie_draw(cv, S, B, box, T, root, _kids, 3, S.get('now'), '01 trie（窗口内的数，高位在上；计数记在边上）')


def _win_end(S):
    return S['nums'].index(S['v']) if 'v' in S and 'nums' in S else None


def _txt(S):
    if 'v' not in S or 'p' not in S:
        return '强数对：设 `x ≤ y`，`y − x ≤ x` 即 ==`y ≤ 2x`=='
    xs = S['nums'][S['p']:S['nums'].index(S['v']) + 1]
    return f'枚举右端 `y = {S["v"]}`：窗口 ==[{", ".join(map(str, xs))}]== 里每个 x 都满足 `y ≤ 2x`'


def _bitcap(S, B, r):
    v, i = S.v, S.i
    b = v >> i & 1
    if 'delta' in S:
        return f'第 {i} 位：`v = {v}` 的这一位是 {b}，沿 {b} 这条边走'
    return f'第 {i} 位：`v = {v}` 的这一位是 {b}，想异或出 1 → 先试==相反的边 {1 - b}=='


def _cap_cnt(S, B, r):
    t = S.t
    return f'第 {S.i} 位：`v = {S.v}` 这位是 {1 - t}，想异或出 1 → 试相反的边 `{t}`，计数是 `{S.now[1][t]}`：' + ('大于 0，==有数可走==，这一位异或能得 1' if S.now[1][t] > 0 else '为 0（没有数或已删除）→ 只能走同方向，这一位异或是 0')


CONFIG = dict(
    num=2935, title='找出强数对的最大异或值 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='排序 + 滑动窗口 + trie 树（计数在边上）',
    tags=['灵神题单·位运算', '灵神题单·常用数据结构', '难度分 2349'],
    code='''
class Solution(object):
    def maximumStrongPairXor(self, nums):

        root = [[None, None], [0, 0]]

        def add(v, delta):
            now = root
            for i in range(2, -1, -1):
                if v & (1 << i) == (1 << i):
                    t = 1
                else:
                    t = 0
                
                if now[0][t] is None:
                    now[0][t] = [[None, None], [0, 0]]
                now[1][t] += delta
                now = now[0][t]

        def get(v):
            ma = 0
            now = root
            for i in range(2, -1, -1):
                if v & (1 << i) == (1 << i):
                    t = 0
                else:
                    t = 1
                
                if now[1][t] > 0:
                    now = now[0][t]
                    ma |= (1 << i)
                else:
                    now = now[0][1 - t]
                    
            return ma

        nums.sort()
        p = 0
        res = 0
        for v in nums:
            while p < len(nums) and nums[p] + nums[p] < v:
                add(nums[p], -1)
                p += 1
            add(v, 1)
            res = max(res, get(v))
        
        return res
''',
    call='Solution().maximumStrongPairXor([5, 2, 3])',
    expect=6,
    views=[
        dict(type='text', h=60, size=30, fn=_txt),
        dict(type='array', var='nums', label='nums（已排序）', pointers={'p': 'blue'}, h=230,
             color=lambda S, i, v: ('pink' if v == S.get('v') and 'p' in S else None),
             dim=lambda S, i, v: ('p' in S and 'v' in S and (i < S['p'] or v > S['v']))),
        dict(type='custom', draw=_draw_trie, h=500),
    ],
    watch=[('v', 'v', 'pink'), ('p', 'p', 'blue'), ('res', 'res', 'green')],
    skip=['now[1][t] += delta', 'now = now[0][1 - t]', 'if v & (1 << i)', 'for i in range(2', 't = 1', 't = 0', 'now[0][t] = [[None', 'now = now[0][t]', 'now = root', 'ma = 0', 'root = [[None'],
    captions={
        'nums.sort()': '先排序：设 `x ≤ y`，绝对值拆开是 `y − x ≤ x`，即 ==`y ≤ 2x`==',
        'for v in nums': lambda S, B, r: ('`v` 都枚举完了' if B.get('v') == S['v'] else f'枚举右边界 `v = {S.v}`：用 trie 找窗口内与它异或最大的数'),
        'while p < len(nums)': lambda S, B, r: (f'`{S.nums[S.p]} + {S.nums[S.p]} = {2 * S.nums[S.p]} < {S.v}`：==x 太小，配不成强数对== → 滑出窗口'
                                                if S.p < len(S.nums) and 2 * S.nums[S.p] < S.v else f'`{2 * S.nums[S.p]} ≥ {S.v}`：窗口左端合格，不再滑出'),
        'add(nums[p], -1)': '把 `{nums[p]}` 从 trie 中删除：路径上的计数都 −1（`delta = -1`）',
        'p += 1': '窗口左端右移到 `p = {p}`',
        'add(v, 1)': '把 `v = {v}`（二进制 {v:03b}）加入 trie：路径上的计数都 +1',
        'if now[0][t] is None': lambda S, B, r: f'第 {S.i} 位：`v = {S.v}` 的这一位是 {S.t}，沿 {S.t} 边走：' + ('还没有这个子节点 → 新建' if S.now[0][S.t] is None else '已有，直接走') + f'；这条边计数 {"+" if S.delta > 0 else "−"}1',
        'if now[1][t] > 0': _cap_cnt,
        'ma |= (1 << i)': '反方向走得通 → 这一位异或能得 1：`ma = {ma}`（二进制 {ma:03b}）',
        'res = max(res, get(v))': '窗口里与 `v = {v}` 的最大异或来自 trie 从高位往下的贪心；`res` 取最大',
        'return ma': '`v` 与窗口内的数最大异或 = `{ma}`',
        'return res': '所有右边界都处理完，答案 `{res}`',
    },
    max_steps=130,
    cards=dict(
        one_liner='排序后 y ≤ 2x，窗口里用 trie 贪心找最大异或',
        complexity='时间 `O(n log n + n log U)`，空间 `O(n log U)`',
        problem=['`abs(x−y) ≤ min(x,y)` 的数对叫强数对，可选同一个数两次',
                 '求所有强数对 `x XOR y` 的最大值，`n` 到 `5×10^4`',
                 '演示：`[5,2,3]` → `6`（`3 XOR 5`）'],
        quote='不妨设x<=y，这里的绝对值拆开得到的是y - x <= x，那么强数对就是所有满足y <= x * 2的数对。……问题就变成了给出一个变长的滑动窗口在数组中从左向右滑动，问当前窗口内的数与窗口右边界的数异或值的最大值。',
        quote_src='—— yiduobo 题解原文',
        idea=['先拆绝对值，强数对就是 `y ≤ 2x`；排序后每个 `y` 的合格 `x` 是一段区间',
              '`p` 只增不减，窗口一路右滑；滑出的数在 trie 里计数 −1',
              '查询时高位到低位==尽量走相反的位==，让异或高位先出现 1（沿用 1707 题的做法）'],
        summary=['时间 `O(n log n + n log U)`，空间 `O(n log U)`',
                 'trie 的计数记在==边==上（`now[1][t]`），计数为 0 就当作没有这条边',
                 '先 `add(v, 1)` 再 `get(v)`：窗口包含 `v` 自己（可选同一个数）',
                 '为了画得下，演示把循环范围 `range(19, -1, -1)` 改成 `range(2, -1, -1)`（示例数都 ≤ 5）；原文为 Python 2 风格写法，但这段代码在 Python 3 下无需其他改动',
                 '对比灵神：灵神用 Node 类、计数在节点上；yiduobo 用嵌套列表、计数在边上'],
    ),
)
