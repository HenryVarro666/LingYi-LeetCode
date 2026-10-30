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
    for b in (0, 1):
        ch = node.son[b]
        if ch is not None:
            out.append((b, ch, ch.leaf))
    return out


def _draw_trie(cv, S, B, box, T):
    t = S.get('t')
    if t is None:
        return
    _trie_draw(cv, S, B, box, T, t.root, _kids, 3, S.get('cur'), '0-1 字典树：窗口内的前缀异或和 pre[left..right]')


def _qtxt(S):
    if 'min_q' not in S:
        return ''
    f = lambda q: '[' + ', '.join(f'{i}:{S["nums"][i]}' for i in q) + ']'
    return f'`min_q`（队首=最小）{f(S["min_q"])}　`max_q`（队首=最大）{f(S["max_q"])}'


def _txt(S):
    if 'right' not in S or 'min_q' not in S:
        return '约束：窗口内 `max − min ≤ k`（单调队列）；目标：窗口内某个 `pre[i]` 与 `pre[right+1]` 异或最大'
    nums, l, r = S['nums'], S['left'], S['right']
    seg = nums[l:r + 1]
    if not S['min_q'] or not S['max_q']:
        return f'窗口 `[{l}, {r}]`'
    mx, mn = nums[S['max_q'][0]], nums[S['min_q'][0]]
    ok = mx - mn <= S['k']
    return f'窗口 `[{l}, {r}]`：`max − min = {mx} − {mn} = {mx - mn}`' + (' ≤ ' if ok else ' > ') + f'`k = {S["k"]}`'


CONFIG = dict(
    num=3845, title='最大子数组异或值', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='单调队列滑窗 + 前缀异或 + 0-1 字典树',
    tags=['灵神题单·位运算', '灵神题单·常用数据结构'],
    code='''
WIDTH = 3  # nums[i] 二进制长度的最大值

class Node:
    __slots__ = 'son', 'leaf'

    def __init__(self):
        self.son = [None] * 2
        self.leaf = 0  # 子树叶子个数

class Trie:
    def __init__(self):
        self.root = Node()

    def put(self, val: int) -> Node:
        cur = self.root
        for i in range(WIDTH - 1, -1, -1):
            bit = val >> i & 1
            if cur.son[bit] is None:
                cur.son[bit] = Node()
            cur = cur.son[bit]
            cur.leaf += 1

    def delete(self, val: int) -> Node:
        cur = self.root
        for i in range(WIDTH - 1, -1, -1):
            cur = cur.son[val >> i & 1]
            cur.leaf -= 1  # 如果减成 0 了，说明子树是空的，可以理解成 cur is None

    def max_xor(self, val: int) -> int:
        cur = self.root
        ans = 0
        for i in range(WIDTH - 1, -1, -1):
            bit = val >> i & 1
            if cur.son[bit ^ 1] and cur.son[bit ^ 1].leaf:
                ans |= 1 << i
                bit ^= 1
            cur = cur.son[bit]
        return ans

class Solution:
    def maxXor(self, nums: list[int], k: int) -> int:
        pre = list(accumulate(nums, xor, initial=0))

        t = Trie()
        min_q = deque()
        max_q = deque()
        ans = left = 0
        for right, x in enumerate(nums):
            # 1. 入
            t.put(pre[right])

            while min_q and x <= nums[min_q[-1]]:
                min_q.pop()
            min_q.append(right)

            while max_q and x >= nums[max_q[-1]]:
                max_q.pop()
            max_q.append(right)

            # 2. 出
            while nums[max_q[0]] - nums[min_q[0]] > k:
                t.delete(pre[left])
                left += 1
                if min_q[0] < left:
                    min_q.popleft()
                if max_q[0] < left:
                    max_q.popleft()

            # 3. 更新答案
            ans = max(ans, t.max_xor(pre[right + 1]))
        return ans
''',
    call='Solution().maxXor([5, 4, 6], 1)',
    expect=6,
    views=[
        dict(type='text', h=50, size=26, fn=_txt),
        dict(type='array', var='nums', label='nums（框 = 窗口）', pointers={'left': 'blue', 'right': 'pink'},
             window=('left', 'right'), h=175, cell=64),
        dict(type='array', var='pre', label='pre（绿 = 窗口内）', h=120, cell=64,
             color=lambda S, i, v: ('green' if 'left' in S and 'right' in S and S['left'] <= i <= S['right'] else None)),
        dict(type='text', h=55, size=24, fn=_qtxt),
        dict(type='custom', draw=_draw_trie, h=330),
    ],
    watch=[('right', 'right', 'pink'), ('left', 'left', 'blue'), ('ans', 'ans', 'green')],
    skip=['for right, x in enumerate', 'ans |= 1 << i', 'cur.leaf += 1', 'cur.leaf -= 1', 'min_q.append(right)', 'max_q.append(right)', 'bit = val >> i & 1', 'cur = self.root', 'ans = 0', 'for i in range(WIDTH', 'cur = cur.son[bit]',
          'cur = cur.son[val', 'cur.son[bit] = Node()', 'self.root = Node()', 'self.son =', 'self.leaf = 0',
          'bit ^= 1', 't = Trie()', 'min_q = deque()', 'max_q = deque()', 'ans = left = 0', 'class Trie', 'WIDTH = 3'],
    captions={
        'pre = list(accumulate': '前缀异或 `pre`：子数组 `[i, r]` 的异或 = ==`pre[r+1] ^ pre[i]`==',
        't.put(pre[right])': '入：`pre[{right}] = {pre[right]}` 进字典树',
        'while min_q and x <= nums[min_q[-1]]': lambda S, B, r: ('队尾 ≥ `x`，当不了最小值 → ==弹出==' if S.min_q and S.x <= S.nums[S.min_q[-1]] else '队尾 < `x`，保留；`right` 入队'),
        'while max_q and x >= nums[max_q[-1]]': lambda S, B, r: ('队尾 ≤ `x`，当不了最大值 → ==弹出==' if S.max_q and S.x >= S.nums[S.max_q[-1]] else '队尾 > `x`，保留；`right` 入队'),
        'while nums[max_q[0]] - nums[min_q[0]] > k': lambda S, B, r: (f'出：`{S.nums[S.max_q[0]]} − {S.nums[S.min_q[0]]} = {S.nums[S.max_q[0]] - S.nums[S.min_q[0]]}`'
                                                                    + (f' > `k = {S.k}`' + ' → ==缩窗口==' if S.nums[S.max_q[0]] - S.nums[S.min_q[0]] > S.k else f' ≤ `k = {S.k}`，窗口合法')),
        't.delete(pre[left])': '`pre[{left}] = {pre[left]}` 出字典树',
        'left += 1': '`left` → {left}',
        'if min_q[0] < left': '最小队首 `{min_q[0]}` < `left = {left}`？过期就弹',
        'if max_q[0] < left': '最大队首 `{max_q[0]}` < `left = {left}`？过期就弹',
        'cur.son[bit] is None': lambda S, B, r: f'第 {S.i} 位是 {S.bit}，走 {S.bit} 边' + ('（新建）' if S.cur.son[S.bit] is None else '（已有）'),
        'cur.son[bit ^ 1] and': lambda S, B, r: (f'第 {S.i} 位 `val` 是 {S.bit}，看反方向 {S.bit ^ 1}：'
                                                 + (f'==有数==，这位得 1' if (S.cur.son[S.bit ^ 1] and S.cur.son[S.bit ^ 1].leaf) else '==没有==，走同方向')),
        'ans = max(ans, t.max_xor': '3. 查 `pre[{right + 1}] = {pre[right + 1]}` 与窗口内前缀的最大异或',
        'return ans': lambda S, B, r: (f'这次最大异或是 `{S.ans}`' if 'val' in S else f'答案 `{S.ans}`'),
    },
    max_steps=130,
    cards=dict(
        one_liner='滑窗保证 max−min≤k，字典树在窗口里找最大异或',
        complexity='时间 `O(n log U)`，空间 `O(n log U)`',
        problem=['选一个子数组，要求 ==最大值 − 最小值 ≤ k==',
                 '子数组的值 = 所有元素的 XOR，求最大值',
                 '演示：`nums = [5,4,6], k = 1` → `6`（子数组 `[6]`）'],
        quote='「最大值与最小值之间的差值不超过 k」这个约束和 1438 题是一样的，用滑动窗口和单调队列解决。子数组异或和可以用前缀和快速计算。……这等价于：计算 s[r+1] 与 i 在 [l,r] 中的一个 s[i] 的最大异或和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['约束交给==单调队列==：两个队列的队首就是窗口的最大、最小值',
              '子数组异或 = `pre[r+1] ^ pre[i]`，左端点 `i` 在窗口 `[left, right]` 里',
              '窗口里的前缀异或和放进 0-1 字典树，出窗口就删，每次查最大异或'],
        summary=['时间 `O(n log U)`，空间 `O(n log U)`（`U` = 最大值）',
                 '`right` 入的是 `pre[right]`，查的是 `pre[right+1]`：左端点 `i ∈ [left, right]`',
                 '字典树删除只减计数，`leaf == 0` 当作空节点',
                 '演示把 `WIDTH` 从 15 改成 3（示例前缀异或都 < 8），其余代码照搬',
                 '灵神还给了方法二：按位试填 + 记录前缀最近出现位置，空间更省'],
    ),
)
