def _trie_draw(cv, S, B, box, T, root, children, nbits, cur, title):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
    top, bot = y0 + 56, y1 - 78
    gap = (bot - top) / nbits
    W = x1 - x0 - 60
    sx = x0 + 30
    R = 20
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
    cv.text((x0 + 18, y1 - 4), '圆里 = 经过的数的个数（0 变暗）；黄 = 当前节点；叶子下 = 对应的数', 20, T['muted'], anchor='lb')


def _kids(node):
    out = []
    for c in (0, 1):
        if c in node:
            out.append((c, node[c][0], node[c][1]))
    return out


def _draw_trie(cv, S, B, box, T):
    root = S.get('root')
    if root is None:
        return
    _trie_draw(cv, S, B, box, T, root, _kids, 3, S.get('now'), '01 trie：存 pre_xor[index+1 .. p]（计数记在边上）')


def _wend(S):
    if 'index' not in S or 'p' not in S:
        return None
    return max(S['index'], S['p'] - 1)


def _txt(S):
    if 'index' not in S or 'p' not in S:
        return '目标：左边界 `index` 固定，右边界 `p` 尽量大（最大值−最小值 ≤ `k`）'
    i, p, k = S['index'], S['p'], S['k']
    seg = S['nums'][i:p]
    if not seg:
        return f'左边界 `index = {i}`，窗口还是空的'
    return f'左边界 `index = {i}`，窗口 `[{i}, {p - 1}]` = {seg}，`max − min = {max(seg) - min(seg)}`，`k = {k}`'


def _qtxt(S):
    if 'ma' not in S:
        return ''
    f = lambda q: '[' + ', '.join(f'{i}:{S["nums"][i]}' for i in q) + ']'
    return f'`ma`（队首=最大）{f(S["ma"])}　`mi`（队首=最小）{f(S["mi"])}'


def _cap_if_c(S, B, r):
    return f'第 {S.d} 位：走 `{S.c}` 边' + ('，没有就新建' if S.c not in S.now else '（已有）') + f'，边上计数 {"+" if S.delta > 0 else "−"}1'


def _cap_find(S, B, r):
    c = S.c
    ok = c in S.now and S.now[c][1] > 0
    return (f'第 {S.d} 位：想异或出 1，试 `{c}` 边：' + ('计数 > 0，==能走==，这位得 1' if ok else '没有数 → 走另一边，这位得 0'))


CONFIG = dict(
    num=3845, title='最大子数组异或值', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='双指针滑窗 + 单调队列 + 前缀异或 trie',
    tags=['灵神题单·位运算', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def maxXor(self, nums, k):
        
        def update(v, delta):
            now = root
            for d in range(2, -1, -1):
                if (v & (1 << d)) == (1 << d):
                    c = 1
                else:
                    c = 0
                
                if c not in now:
                    now[c] = [{}, 0]
                now[c][1] += delta
                now = now[c][0]

        def find(other):
            now = root
            v = 0
            for d in range(2, -1, -1):
                p2 = 1 << d
                if (other & p2) == p2:
                    c = 0
                else:
                    c = 1
                
                if c in now and now[c][1] > 0:
                    v |= p2
                    now = now[c][0]
                else:
                    now = now[c ^ 1][0]
            
            return v

        pre_xor = [0]
        for v in nums:
            pre_xor.append(pre_xor[-1] ^ v)
        
        ma = deque()
        mi = deque()

        p = 0
        n = len(nums)
        root = {}
        res = 0
        for index, v in enumerate(nums):
            while p < n:
                ma_v, mi_v = nums[p], nums[p]
                if ma:
                    ma_v = max(ma_v, nums[ma[0]])
                if mi:
                    mi_v = min(mi_v, nums[mi[0]])
                if ma_v - mi_v <= k:
                    while ma and nums[ma[-1]] <= nums[p]:
                        ma.pop()
                    ma.append(p)

                    while mi and nums[mi[-1]] >= nums[p]:
                        mi.pop()
                    mi.append(p)

                    update(pre_xor[p + 1], 1)
                    p += 1
                else:
                    break
            
            res = max(res, find(pre_xor[index]))
            if ma and ma[0] == index:
                ma.popleft()
            if mi and mi[0] == index:
                mi.popleft()
            update(pre_xor[index + 1], -1)

        return res
''',
    call='Solution().maxXor([5, 4, 6], 1)',
    expect=6,
    views=[
        dict(type='text', h=50, size=24, fn=_txt),
        dict(type='array', var='nums', label='nums（框 = 当前窗口）', pointers={'index': 'blue', 'p': 'pink'},
             window=('index', _wend), h=175, cell=64),
        dict(type='array', var='pre_xor', label='pre_xor', h=120, cell=64,
             color=lambda S, i, v: ('green' if 'index' in S and 'p' in S and S['index'] < i <= S['p'] else None)),
        dict(type='text', h=55, size=24, fn=_qtxt),
        dict(type='custom', draw=_draw_trie, h=330),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink'), ('res', 'res', 'green')],
    skip=['for v in nums', 'pre_xor.append', 'if c not in now', 'ma.popleft()', 'mi.popleft()', 'for d in range(2', 'if (v & (1 << d))', 'if (other & p2)', 'c = 1', 'c = 0', 'now[c] = [{}, 0]', 'now[c][1] += delta',
          'now = now[c][0]', 'p2 = 1 << d', 'now = root', 'v = 0', 'ma_v, mi_v = nums[p]', 'if ma:', 'if mi:',
          'ma_v = max(', 'mi_v = min(', 'ma.append(p)', 'mi.append(p)', 'now = now[c ^ 1][0]', 'root = {}', 'n = len(nums)',
          'ma = deque()', 'mi = deque()', 'p = 0'],
    captions={
        'pre_xor = [0]': '前缀异或 `pre_xor`：子数组 `[i, q]` 的异或 = ==`pre_xor[i] ^ pre_xor[q+1]`==',
        'for index, v in enumerate(nums)': lambda S, B, r: ('左边界都枚举完了' if B.get('index') == S['index'] else f'枚举左边界 `index = {S.index}`'),
        'while p < n': lambda S, B, r: (f'试着把右边界 `p = {S.p}` 往右扩' if S.p < S.n else '`p` 到头了，不能再扩'),
        'if ma_v - mi_v <= k': lambda S, B, r: (f'加入 `nums[{S.p}] = {S.nums[S.p]}` 后 `max − min = {S.ma_v} − {S.mi_v} = {S.ma_v - S.mi_v}`'
                                                  + (f' ≤ `k = {S.k}` → ==能扩==' if S.ma_v - S.mi_v <= S.k else f' > `k = {S.k}` → ==不能扩==')),
        'while ma and nums[ma[-1]] <= nums[p]': lambda S, B, r: ('队尾 ≤ 新数，当不了最大值 → 弹出' if S.ma and S.nums[S.ma[-1]] <= S.nums[S.p] else '最大队列保留队尾；`p` 入队'),
        'while mi and nums[mi[-1]] >= nums[p]': lambda S, B, r: ('队尾 ≥ 新数，当不了最小值 → 弹出' if S.mi and S.nums[S.mi[-1]] >= S.nums[S.p] else '最小队列保留队尾；`p` 入队'),
        'update(pre_xor[p + 1], 1)': '`pre_xor[{p + 1}] = {pre_xor[p + 1]}` 加入 trie：沿它的二进制路径，边计数 +1',
        'p += 1': '右边界 `p` → {p}',
        'break': '再扩就不合法了，右边界停在 `p = {p}`',
        'if c in now and now[c][1] > 0': _cap_find,
        'v |= p2': '这一位异或得 1：`v = {v}`（二进制 {v:03b}）',
        'res = max(res, find(pre_xor[index]))': '用 `pre_xor[{index}] = {pre_xor[index]}` 在 trie 里找最大异或（当前 `res = {res}`）',
        'if ma and ma[0] == index': '左边界 `{index}` 离开：是队首就弹出',
        'if mi and mi[0] == index': '最小队列同理',
        'update(pre_xor[index + 1], -1)': '`pre_xor[{index + 1}]` 移出 trie：路径边计数 −1',
        'return v': '这次最大异或是 `{v}`',
        'return res': '答案 `{res}`',
    },
    max_steps=130,
    cards=dict(
        one_liner='固定左边界，右边界只增不减；trie 里取最大异或',
        complexity='时间 `O(n log U)`，空间 `O(n log U)`',
        problem=['子数组要满足 ==最大值 − 最小值 ≤ k==',
                 '子数组的值是所有元素的异或，求最大值',
                 '演示：`nums = [5,4,6], k = 1` → `6`'],
        quote='若以index为左边界的子数组的最大合法右边界为p，那么p也必然是以index + 1为左边界的子数组的一个合法右边界，从而得到以index + 1为左边界的最大合法右边界必然大于等于p。',
        quote_src='—— yiduobo 题解原文',
        idea=['左边界 `index` 右移，最大合法右边界 `p` ==不会回退==：用单调队列维护 max / min',
              '子数组异或 = `pre_xor[index] ^ pre_xor[q+1]`，`q` 在 `[index, p-1]`',
              '`pre_xor[index+1..p]` 放进 trie，贪心走相反位；左边界前进就把旧的移除'],
        summary=['时间 `O(n log U)`，空间 `O(n log U)`',
                 '外层按==左边界==枚举（灵神是按右边界枚举），`p` 全程只增不减',
                 '查询的是 `pre_xor[index]`，trie 里是 `pre_xor[index+1..p]`',
                 '为了画得下，演示把循环范围 `range(14, -1, -1)` 改成 `range(2, -1, -1)`（示例前缀异或 < 8）；原文代码在 Python 3 下无需其他改动'],
    ),
)
