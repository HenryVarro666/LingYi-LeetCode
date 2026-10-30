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


def cap_even(S, B, ret):
    if B.even:
        return f'这一层是==偶数层==（从 0 数）→ 翻转：`vals[::-1] = {S.vals[::-1]}` 加入 `ans`'
    return f'奇数位的层（第一层）保持从左到右：`{S.vals}` 加入 `ans`'


CONFIG = dict(
    num='LCR 151', title='彩灯装饰记录 III', difficulty='Medium', category='二叉树',
    author='灵茶山艾府', technique='BFS · 隔层翻转',
    code='''
class Solution:
    def decorateRecord(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []
        ans = []
        q = deque([root])
        even = False
        while q:
            vals = []
            for _ in range(len(q)):
                node = q.popleft()
                vals.append(node.val)
                if node.left:  q.append(node.left)
                if node.right: q.append(node.right)
            ans.append(vals[::-1] if even else vals)
            even = not even
        return ans
''',
    call='Solution().decorateRecord(Tr([8,17,21,18,None,None,6,4,5]))',
    expect=[[8], [21, 17], [18, 6], [5, 4]],
    max_steps=80,
    views=[
        dict(type='tree', label='圣诞树（紫 = 在队列中，绿 = 已出队）', pointers={'node': 'blue'}, h=260, color=tree_color, path=False),
        dict(type='custom', draw=draw_q, h=135),
        dict(type='text', h=52, fn=lambda S: (f"当前层 `vals = {S['vals']}`，`even = {S['even']}`" if 'vals' in S else '')),
        dict(type='table', var='ans', label='ans（每行一层，偶数行是翻转后的）', h=225, cell=58,
             rows=lambda S: [str(i) for i in range(len(S.get('ans', [])))]),
    ],
    watch=[('node', 'node', 'blue'), ('even', 'even', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'if root is None': '树不为空 → 开始逐层记录',
        'ans = []': '`ans` 每一行放一层彩灯编号',
        'q = deque([root])': '队列先放根：==第 0 层只有它==',
        'even = False': '`even` 标记这一层要不要翻转：第 0 层不翻',
        'while q': cap_while,
        'vals = []': '新的一层开始：`vals` 先按从左到右收集',
        'for _ in range': cap_for,
        'node = q.popleft()': lambda S, B, ret: f'队首出队：`node = {S.node.val}`',
        'vals.append': lambda S, B, ret: f'记下编号 → `vals = {S.vals}`',
        'if node.left': cap_left,
        'if node.right': cap_right,
        'ans.append(vals': lambda S, B, ret: (f'`even` 为真 → 这层要从右到左，加入 `{S.vals[::-1]}`' if B.even
                                              else f'`even` 为假 → 保持从左到右，加入 `{S.vals}`'),
        'even = not even': '翻转标记 → `even = {even}`：下一层的顺序和这层相反',
        'return ans': lambda S, B, ret: f'返回 `{ret}`',
    },
    cards=dict(
        one_liner='入队顺序永远从左到右，只在存答案时把偶数层翻转',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['圣诞树是二叉树，节点值是彩灯颜色编号',
                 '第一层从左到右，==之后每层与上一层方向相反==',
                 '示例：`[8,17,21,18,null,null,6]` → `[[8],[21,17],[18,6]]`'],
        quote='满二叉树（每一层都填满）最后一层有大约 n/2 个节点，因此队列中最多有 O(n) 个元素，所以空间复杂度是 O(n) 的。',
        quote_src='—— 灵茶山艾府题解「方法二：一个队列」',
        idea=['遍历本身不变：照旧按层、从左到右出队、入队',
              '用布尔变量 `even` 记录当前层要不要翻转',
              '每层记完先 `vals[::-1]` 再放进 `ans`，然后 `even = not even`'],
        result='运行结束，返回 `[[8],[21,17],[18,6],[5,4]]`：第 1、3 层被翻转',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：不要去改变入队顺序，只翻转存进 `ans` 的那份 `vals`',
                 '`even` 要在每层结束后取反，别忘了更新',
                 '方法一（两个数组 `cur`/`nxt`）只是把队列换成两个列表，翻转部分完全一样'],
    ),
)
