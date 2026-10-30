def depths(root):
    d, st = {}, [(root, 0)]
    while st:
        n, k = st.pop()
        if n is None or n._uid in d:
            continue
        d[n._uid] = k
        st += [(n.left, k + 1), (n.right, k + 1)]
    return d


def draw_q(cv, S, B, box, T):
    """队列：按层分组，新入队的绿色，队首紫色"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'q（队首 → 队尾，绿 = 刚入队）', 24, T['muted'], bold=True)
    q = S.get('q')
    if q is None:
        cv.text((x0 + 18, y0 + 50), '（尚未创建）', 24, T['dim'])
        return
    items = list(q)
    if not items:
        cv.text((x0 + 22, y0 + 66), '空', 26, T['dim'], anchor='lm')
        return
    dep = depths(S.get('root'))
    before = {n._uid for n in (B.get('q') or [])}
    x, y, w = x0 + 22, y0 + 44, 64
    last = None
    for k, n in enumerate(items):
        d = dep.get(n._uid)
        if last is not None and d != last:
            x += 16
            cv.line([(x - 8, y - 4), (x - 8, y + 56)], T['border'], 2)
            x += 8
        if last != d:
            cv.text((x, y + 70), f'第 {d} 层', 18, T['muted'], anchor='lm')
        last = d
        new = n._uid not in before
        fill = T['green'] if new else (T['purple'] if k == 0 else T['panel2'])
        cv.rect((x, y, x + w, y + 48), fill=fill, outline=T['border'], width=1, r=10)
        cv.text((x + w / 2, y + 24), str(n.val), 24, T['bg'] if fill != T['panel2'] else T['text'],
                anchor='mm', bold=True, mono=True)
        x += w + 8


def tree_color(S, n):
    done = {v for row in S.get('ans', []) for v in row} | set(S.get('vals', []))
    if n.val in done:
        return 'green'
    if any(m._uid == n._uid for m in (S.get('q') or [])):
        return 'purple'
    return None


def dir_text(S):
    if 'vals' not in S or 'ans' not in S:
        return ''
    k = len(S['ans'])
    if S.get('_line') == 14:  # 刚 append 完，看上一层
        k -= 1
        row = S['ans'][k]
        how = '反转后' if k % 2 else '原样'
        return f"第 {k} 层：`len(ans) % 2 = {k % 2}` → {how}加入 ==`{row}`=="
    way = '==从右到左==（收集完再反转）' if k % 2 else '==从左到右=='
    return f"正在收集第 {k} 层 `vals = {S['vals']}`，这一层要 {way}"


def cap_while(S, B, ret):
    if B.q:
        d = depths(S.root)[B.q[0]._uid]
        return f'队列非空：此刻队列里==恰好是第 {d} 层==的全部节点（{len(B.q)} 个）'
    return '队列空了 → 所有层都处理完，退出循环'


def cap_for(S, B, ret):
    if S.vals == []:
        return f'`range(len(q))` 先固定这一层的个数：==只出队 {len(S.q)} 个==，后入队的留给下一层'
    if S['_'] != B['_']:
        return f'这一层的第 {S["_"] + 1} 个节点'
    return f'这一层 {len(S.vals)} 个节点都出队了 → 结束 for 循环'


def cap_child(side, word):
    def f(S, B, ret):
        n = S.node
        ch = getattr(n, side)
        if ch:
            return f'`{n.val}` 有{word}儿子 `{ch.val}` → 入队（属于下一层）'
        return f'`{n.val}` 没有{word}儿子'
    return f


def cap_append(S, B, ret):
    k = len(B.ans)
    v = S.vals
    if k % 2:
        return f'`len(ans) = {k}` 是==奇数== → 第 {k} 层要从右往左：`vals[::-1]` = =={v[::-1]}=='
    return f'`len(ans) = {k}` 是==偶数== → 第 {k} 层从左往右，原样加入 =={v}=='


CONFIG = dict(
    num=103, title='二叉树的锯齿形层序遍历', difficulty='Medium', category='二叉树',
    author='灵茶山艾府', technique='BFS · 一个队列 + 奇数层反转',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []
        ans = []
        q = deque([root])
        while q:
            vals = []
            for _ in range(len(q)):
                node = q.popleft()
                vals.append(node.val)
                if node.left:  q.append(node.left)
                if node.right: q.append(node.right)
            ans.append(vals[::-1] if len(ans) % 2 else vals)
        return ans
''',
    call='Solution().zigzagLevelOrder(Tr([3,9,20,None,None,15,7]))',
    expect=[[3], [20, 9], [15, 7]],
    views=[
        dict(type='tree', label='二叉树（紫 = 在队列中，绿 = 已出队）', pointers={'node': 'blue'}, h=250, color=tree_color, path=False),
        dict(type='custom', draw=draw_q, h=135),
        dict(type='text', h=56, fn=dir_text, size=26),
        dict(type='table', var='ans', label='ans（第 k 行 = 第 k 层，奇数层已反转）', h=200, cell=58,
             rows=lambda S: [str(i) for i in range(len(S.get('ans', [])))],
             color=lambda S, i, j, v: 'orange' if i % 2 else None),
    ],
    watch=[('node', 'node', 'blue'), ('len(q)', 'len(q)'), ('len(ans)', 'len(ans)', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'if root is None': '根不为空 → 开始 BFS（空树直接返回 `[]`）',
        'ans = []': '`ans` 存每一层的节点值',
        'q = deque([root])': '队列里先放根节点：==第 0 层只有它==',
        'while q': cap_while,
        'vals = []': '新的一层开始：`vals` 先==从左到右==收集这一层的值',
        'for _ in range': cap_for,
        'node = q.popleft()': lambda S, B, ret: f'队首出队：`node = {S.node.val}`',
        'vals.append': lambda S, B, ret: f'记下它的值 → `vals = {S.vals}`',
        'if node.left': cap_child('left', '左'),
        'if node.right': cap_child('right', '右'),
        'ans.append': cap_append,
        'return ans': lambda S, B, ret: f'返回 `{ret}`',
    },
    cards=dict(
        one_liner='照常层序遍历，奇数层收集完后反转一下',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给你二叉树的根 `root`，返回节点值的==锯齿形层序遍历==',
                 '第 0 层从左往右，第 1 层从右往左，第 2 层再从左往右……交替进行',
                 '示例：`[3,9,20,null,null,15,7]` → `[[3],[20,9],[15,7]]`'],
        before=[dict(heading='BFS 为什么要用队列？', lines=[
            '方法一用==两个数组==：`cur` 是当前层，把儿子放进 `nxt`，然后 `cur = nxt`',
            '先放进来的先处理——这正是==队列==：方法二合并成一个 `deque`',
            '锯齿形只是==输出顺序==不同，遍历顺序完全不变'])],
        quote='`ans.append(vals[::-1] if len(ans) % 2 else vals)`',
        quote_src='—— 灵茶山艾府题解代码（方法二：一个队列），和 102 题只差这一行',
        idea=['进入 `while` 时，队列里恰好是==同一层==的全部节点',
              '`len(ans)` 就是当前层号：偶数层原样，==奇数层 `vals[::-1]`==',
              '不要去改入队顺序，否则下一层的顺序也跟着乱了'],
        result='运行结束，返回 `[[3],[20,9],[15,7]]`：第 1 层被反转成 `[20,9]`',
        summary=['时间 `O(n)`：每个节点入队、出队各一次；空间 `O(n)`',
                 '层号用 `len(ans)` 现成拿到，==不用额外计数器==',
                 '易错：只反转输出的 `vals`，不要反转队列或交换左右儿子的入队顺序',
                 '空树特判返回 `[]`；方法一（两个数组 `cur`/`nxt`）同样 `O(n)`'],
    ),
)
