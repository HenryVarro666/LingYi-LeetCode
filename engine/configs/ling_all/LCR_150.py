def nv(x):
    return '空' if x is None else str(x.val)


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


def cap_while(S, B, ret):
    if B.q:
        dep = depths(S.root)
        d = dep[B.q[0]._uid]
        return f'队列非空：此刻队列里==恰好是第 {d} 层==的全部节点（{len(B.q)} 个）'
    return '队列空了 → 所有层都处理完，退出循环'


def cap_for(S, B, ret):
    if S.vals == []:
        return f'`range(len(q))` 在循环开始时就算好了：这一层==只出队 {len(S.q)} 个==，后入队的留给下一层'
    if S['_'] != B['_']:
        return f'这一层的第 {S["_"] + 1} 个节点'
    return f'这一层 {len(S.vals)} 个节点都出队了 → 结束 for 循环'


def cap_left(S, B, ret):
    n = S.node
    if n.left:
        return f'`{n.val}` 有左儿子 `{n.left.val}` → 入队（属于下一层）'
    return f'`{n.val}` 没有左儿子'


def cap_right(S, B, ret):
    n = S.node
    if n.right:
        return f'`{n.val}` 有右儿子 `{n.right.val}` → 入队（属于下一层）'
    return f'`{n.val}` 没有右儿子'


CONFIG = dict(
    num='LCR 150', title='彩灯装饰记录 II', difficulty='Easy', category='二叉树',
    author='灵茶山艾府', technique='BFS · 一个队列',
    code='''
class Solution:
    def decorateRecord(self, root: Optional[TreeNode]) -> List[List[int]]:
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
            ans.append(vals)
        return ans
''',
    call='Solution().decorateRecord(Tr([8,17,21,18,None,None,6]))',
    expect=[[8], [17, 21], [18, 6]],
    views=[
        dict(type='tree', label='圣诞树（紫 = 在队列中，绿 = 已出队）', pointers={'node': 'blue'}, h=260, color=tree_color, path=False),
        dict(type='custom', draw=draw_q, h=135),
        dict(type='text', h=52, fn=lambda S: f"当前层 `vals = {S['vals']}`" if 'vals' in S else ''),
        dict(type='table', var='ans', label='ans（每行一层彩灯）', h=225, cell=58,
             rows=lambda S: [str(i) for i in range(len(S.get('ans', [])))]),
    ],
    watch=[('node', 'node', 'blue'), ('len(q)', 'len(q)'), ('ans', 'ans', 'green')],
    captions={
        'if root is None': '树不为空 → 开始逐层记录',
        'ans = []': '`ans` 每一行放一层彩灯编号',
        'q = deque([root])': '队列先放根：==第 0 层只有它==',
        'while q': cap_while,
        'vals = []': '新的一层开始：`vals` 收集这一层的编号',
        'for _ in range': cap_for,
        'node = q.popleft()': lambda S, B, ret: f'队首出队：`node = {S.node.val}`，左边的灯先出',
        'vals.append': lambda S, B, ret: f'记下编号 → `vals = {S.vals}`',
        'if node.left': cap_left,
        'if node.right': cap_right,
        'ans.append(vals)': lambda S, B, ret: f'这一层记完：`ans` 末尾加入 `{S.vals}`',
        'return ans': lambda S, B, ret: f'返回 `{ret}`',
    },
    cards=dict(
        one_liner='队列里每次恰好是一整层：先数个数，再出队这么多个',
        complexity='时间 `O(n)`，空间 `O(n)`（满二叉树最后一层约 `n/2` 个节点）',
        problem=['圣诞树是二叉树，节点值是彩灯颜色编号',
                 '按==从左到右==的顺序，返回每一层的编号，每层一行',
                 '示例：`[8,17,21,18,null,null,6]` → `[[8],[17,21],[18,6]]`'],
        quote='满二叉树（每一层都填满）最后一层有大约 n/2 个节点，因此队列中最多有 O(n) 个元素，所以空间复杂度是 O(n) 的。',
        quote_src='—— 灵茶山艾府题解「方法二：一个队列」',
        idea=['进入 `while` 时，队列里恰好是==同一层==的全部节点',
              '`for _ in range(len(q))` 先把这一层的个数固定下来',
              '出队一个，就把它的左右儿子依次入队——它们属于下一层'],
        result='运行结束，返回 `[[8],[17,21],[18,6]]`：三层，每层从左到右',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：层的大小要在出队前用 `len(q)` 固定，否则层会混在一起',
                 '空树要特判：直接返回 `[]`',
                 '方法一（两个数组 `cur`/`nxt`）思路相同：遍历完一层后 `cur = nxt`',
                 '主站 102 题相同'],
    ),
)
