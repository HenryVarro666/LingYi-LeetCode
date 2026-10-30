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
        ch = node.children[b]
        if ch is not None:
            out.append((b, ch, ch.cnt))
    return out


def _draw_trie(cv, S, B, box, T):
    t = S.get('t')
    if t is None:
        cv.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), '（trie 还没创建）', 28, T['muted'], anchor='mm')
        return
    _trie_draw(cv, S, B, box, T, t.root, _kids, 3, S.get('cur'), '0-1 字典树（窗口内的数，高位在上）')


def _pair(S):
    if 'y' not in S or 'nums' not in S:
        return '强数对：排序后 `x ≤ y`，`|x−y| ≤ min(x,y)` 化简为 ==`2x ≥ y`=='
    y, left = S['y'], S.get('left', 0)
    xs = [x for x in S['nums'] if x * 2 >= y and x <= y]
    return f'`y = {y}`：窗口里 `2x ≥ {y}` 的 x 有 ==[{", ".join(map(str, xs))}]=='


CONFIG = dict(
    num=2935, title='找出强数对的最大异或值 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='排序 + 滑动窗口 + 0-1 字典树',
    tags=['灵神题单·位运算', '灵神题单·常用数据结构', '难度分 2349'],
    code='''
class Node:
    __slots__ = 'children', 'cnt'

    def __init__(self):
        self.children = [None, None]
        self.cnt = 0  # 子树大小

class Trie:
    HIGH_BIT = 2

    def __init__(self):
        self.root = Node()

    # 添加 val
    def insert(self, val: int) -> None:
        cur = self.root
        for i in range(Trie.HIGH_BIT, -1, -1):
            bit = (val >> i) & 1
            if cur.children[bit] is None:
                cur.children[bit] = Node()
            cur = cur.children[bit]
            cur.cnt += 1  # 维护子树大小
        return cur

    # 删除 val，但不删除节点
    # 要求 val 必须在 trie 中
    def remove(self, val: int) -> None:
        cur = self.root
        for i in range(Trie.HIGH_BIT, -1, -1):
            cur = cur.children[(val >> i) & 1]
            cur.cnt -= 1  # 维护子树大小
        return cur

    # 返回 val 与 trie 中一个元素的最大异或和
    # 要求 trie 中至少有一个元素
    def max_xor(self, val: int) -> int:
        cur = self.root
        ans = 0
        for i in range(Trie.HIGH_BIT, -1, -1):
            bit = (val >> i) & 1
            # 如果 cur.children[bit^1].cnt == 0，视作空节点
            if cur.children[bit ^ 1] and cur.children[bit ^ 1].cnt:
                ans |= 1 << i
                bit ^= 1
            cur = cur.children[bit]
        return ans

class Solution:
    def maximumStrongPairXor(self, nums: List[int]) -> int:
        nums.sort()
        t = Trie()
        ans = left = 0
        for y in nums:
            t.insert(y)
            while nums[left] * 2 < y:
                t.remove(nums[left])
                left += 1
            ans = max(ans, t.max_xor(y))
        return ans
''',
    call='Solution().maximumStrongPairXor([5, 2, 3])',
    expect=6,
    views=[
        dict(type='text', h=60, size=30, fn=_pair),
        dict(type='array', var='nums', label='nums（已排序）', pointers={'left': 'blue'}, h=230,
             color=lambda S, i, v: ('pink' if v == S.get('y') else None),
             dim=lambda S, i, v: ('y' in S and ('left' in S and i < S['left'] or v > S['y']))),
        dict(type='custom', draw=_draw_trie, h=500),
    ],
    watch=['y', ('left', 'left', 'blue'), ('val', 'val if "val" in S else None', 'cyan'), ('ans', 'ans', 'green')],
    skip=['bit = (val >> i) & 1', 'return cur', 'cur = self.root', 'ans = 0', 'for i in range(Trie.HIGH_BIT', 'self.children = [None', 'self.cnt = 0', 'self.root = Node()', 'cur.children[bit] = Node()', 'cur = cur.children[bit]', 'cur = cur.children[(val', 'bit ^= 1', 'class Trie'],
    captions={
        'nums.sort()': '答案和元素顺序无关，先排序：设 `x ≤ y`，条件化简成 ==`2x ≥ y`==',
        'for y in nums': lambda S, B, r: ('`y` 都枚举完了，窗口扫过整个数组' if B.get('y') == S['y'] else f'枚举 `y = {S.y}` 作右端点：窗口内是所有满足 `2x ≥ y` 的 x'),
        't.insert(y)': '`y = {y}`（二进制 {y:03b}）先入窗口：沿高位到低位插进字典树',
        'while nums[left] * 2 < y': lambda S, B, r: (f'`{S.nums[S.left]} × 2 = {S.nums[S.left]*2} < {S.y}`：==太小，配不成强数对== → 滑出窗口'
                                                    if S.nums[S.left] * 2 < S.y else f'`{S.nums[S.left]} × 2 = {S.nums[S.left]*2} ≥ {S.y}`：窗口左端合格，停止滑出'),
        't.remove(nums[left])': '`y` 变大后最小的 x 也要变大：把 `{nums[left]}` 从 trie 里删掉（只让 cnt 减 1）',
        'left += 1': '窗口左端右移到 `left = {left}`',
        'if cur.children[bit] is None': '往下走第 `{i}` 位 `{bit}`：没有这个子节点就新建',
        'cur.cnt += 1': '经过该节点的数多了一个：`cnt = {cur.cnt}`',
        'cur.cnt -= 1': '经过该节点的数少了一个：`cnt = {cur.cnt}`（减到 0 就当作空节点）',
                'if cur.children[bit ^ 1]': lambda S, B, r: (f'第 {S.i} 位 `val` 是 {S.bit}，想要异或出 1 → 看反方向 `{S.bit ^ 1}` 有没有数（cnt 非 0）：'
                                                     + ('==有==' if (S.cur.children[S.bit ^ 1] and S.cur.children[S.bit ^ 1].cnt) else '==没有==，只能走同方向')),
        'ans |= 1 << i': '反方向有数 → 这一位异或能得 1：`ans = {ans}`（二进制 {ans:03b}）',
        'ans = max(ans, t.max_xor(y))': '窗口准备好了：求 `y = {y}` 与窗口内数的最大异或（当前 `ans = {ans}`），下面沿 trie 从高位往下走',
        46: '`y = {y}` 的最大异或是 `{ans}`（局部 ans）：每位能走反方向就拿到一个 1',
        59: '所有 y 都处理完，全局最大异或值 `{ans}`',
    },
    max_steps=130,
    cards=dict(
        one_liner='排序后强数对变成 2x ≥ y，窗口里找最大异或',
        complexity='时间 `O(n log n + n log U)`，空间 `O(n log U)`',
        problem=['`|x−y| ≤ min(x,y)` 的数对叫强数对，可以选同一个数两次',
                 '在所有强数对里求 `x XOR y` 的最大值',
                 '演示：`[5,2,3]` → `6`（`3 XOR 5`）'],
        quote='排序后设 x≤y，那么 |x-y|≤min(x,y) 可以化简为 2x≥y。……由于 y 越大，能选到的最小 x 也越大，所以需要用滑动窗口。每次滑出元素时，把它从 0-1 trie 中删掉。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后，每个 `y` 能配的 `x` 是一段连续区间 `[left, y]`',
              '`y` 增大时 `left` 只会右移 → ==滑动窗口==',
              '窗口里的数放进 0-1 trie，从高位往下==尽量走相反的位==，异或就最大'],
        summary=['时间 `O(n log n + n log U)`，空间 `O(n log U)`',
                 '删除只把路径上 `cnt` 减 1，不删节点；`cnt == 0` 当作空节点',
                 '为了画得下，演示把 `HIGH_BIT` 从 19 改成 2（示例数都 ≤ 5），其余代码照搬',
                 '灵神还给了方法二：按位试填 + 哈希表，空间只要 `O(n)`'],
    ),
)
