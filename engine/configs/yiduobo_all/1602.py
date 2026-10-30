def _cur(S):
    q = S.get('q')
    if q is None or 'head' not in S:
        return set()
    return {id(n) for n in q[S['head']:S['tail']]}


def _u(S):
    return S['u'].val if S.get('u') is not None else '?'


def _info(S):
    if 'head' not in S:
        return '层序遍历，在某一层找到 `u`，返回它右边的下一个节点'
    idx = S.get('index')
    return f"目标 `u = {_u(S)}`；当前层是 `q[{S['head']}:{S['tail']}]`" + (f"，正在看下标 `{idx}`" if idx is not None else '')


CONFIG = dict(
    num=1602, title='找到二叉树中最近的右侧节点', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='层序遍历 · 同层下一个',
    tags=['链表树与回溯'],
    code='''
class Solution(object):
    def findNearestRightNode(self, root, u):

        q = [root]
        head, tail = 0, 1
        while head < tail:
            for index in range(head, tail):
                if q[index] == u:
                    if index + 1 == tail:
                        return None
                    return q[index + 1]
                
                now = q[index]
                if now.left:
                    q.append(now.left)
                if now.right:
                    q.append(now.right)
            
            head, tail = tail, len(q)
''',
    setup='root = Tr([1, 2, 3, None, 4, 5, 6])\nu = root.left.right',
    call='Solution().findNearestRightNode(root, u)',
    result_fn=lambda n: n.val if n is not None else None,
    expect=5,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='tree', label='二叉树（蓝 = 当前层，黄 = 下标 index 处的节点，绿 = 目标 u）', path=False, h=330,
             pointers={'now': 'yellow'},
             color=lambda S, n: ('green' if S.get('u') is not None and n is S['u'] else 'blue' if id(n) in _cur(S) else None)),
        dict(type='array', var=lambda S: [n.val for n in S['q']] if 'q' in S else [], label='队列 q（存节点值）',
             pointers={'head': 'blue', 'index': 'yellow', 'tail': 'pink'}, cell=72, h=170,
             color=lambda S, i, v: 'green' if S.get('u') is not None and S['q'][i] is S['u'] else None),
    ],
    watch=[('u', lambda S: S['u'].val if S.get('u') is not None else None, 'green'), ('head', 'head', 'blue'),
           ('index', 'index', 'yellow'), ('tail', 'tail', 'pink')],
    captions={
        'q = [root]': '队列从根开始，一层层往下找 `u`',
        'head, tail = 0, 1': '`q[head:tail]` 圈出当前层：先是只有根的第一层',
        'while head < tail': lambda S, B, r: (f'当前层还有节点（`head = {S.head} < tail = {S.tail}`）→ 逐个检查' if S.head < S.tail
                                              else '没有下一层了（题目保证 `u` 在树里，不会走到这里）'),
        'for index in range(head, tail)': lambda S, B, r: (f'检查当前层的第 `{S.index - S.head + 1}` 个节点：`q[{S.index}] = {S.q[S.index].val}`'
                                                           if B.get('index') != S.get('index') or 'index' not in B
                                                           else '这一层都检查完了，没找到 `u`'),
        'if q[index] == u': lambda S, B, r: (f'`q[{S.index}] = {S.q[S.index].val}` 就是 `u = {S.u.val}` → ==找到了=='
                                             if S.q[S.index] is S.u
                                             else f'`q[{S.index}] = {S.q[S.index].val}` 不是 `u = {S.u.val}` → 继续'),
        'if index + 1 == tail': lambda S, B, r: (f'`index + 1 = {S.index + 1} = tail` → `u` 是本层最后一个，右边没有节点' if S.index + 1 == S.tail
                                                 else f'`index + 1 = {S.index + 1} < tail = {S.tail}` → 同层右边还有节点'),
        'return None': '`u` 在这一层最右边 → 返回 `None`',
        'return q[index + 1]': lambda S, B, r: f'`u` 右边紧挨着的是 `q[{S.index + 1}]` → 返回值 ==`{S.q[S.index + 1].val}`==',
        'now = q[index]': '不是 `u`：取出 `now = {now.val}`，把它的孩子排到下一层',
        'if now.left': lambda S, B, r: (f'`{S.now.val}` 有左孩子 `{S.now.left.val}` → 入队' if S.now.left else f'`{S.now.val}` 没有左孩子 → 跳过'),
        'if now.right': lambda S, B, r: (f'`{S.now.val}` 有右孩子 `{S.now.right.val}` → 入队' if S.now.right else f'`{S.now.val}` 没有右孩子 → 跳过'),
        'q.append(now.left)': '左孩子入队，排在下一层的末尾',
        'q.append(now.right)': '右孩子入队，仍在下一层，顺序保持从左到右',
        'head, tail = tail, len(q)': '这一层没有 `u`：下一层变成 `q[{head}:{tail}]`',
    },
    cards=dict(
        one_liner='层序遍历：在同一层里，u 的下一个就是答案',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给你二叉树的根 `root` 和树中的一个节点 `u`',
                 '返回与 `u` ==同一层、且在它右侧最近==的节点',
                 '`u` 已经是该层最右边的节点，就返回 `null`',
                 '本视频：`[1,2,3,null,4,5,6]`，`u = 4` → 同层是 `4 5 6`，答案 `5`'],
        quote='从根节点向下开始进行层序遍历，对于当前处理的这一层节点，若其中出现了u，那么返回u的下一个节点。若u是这一层的最后一个节点，那么就返回空。',
        quote_src='—— yiduobo 题解原文',
        idea=['层序遍历时，同一层的节点在队列里按从左到右连续排列',
              '用 `head, tail` 划出当前层，在里面按下标找 `u`',
              '找到后看 `index + 1` 有没有越过 `tail`：没有就返回 `q[index + 1]`，有就返回 `None`'],
        result='`u = 4` 右边最近的是节点 `5` → 返回它',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '关键是 `index + 1 == tail`：不能直接取 `q[index + 1]`，那可能是下一层的节点',
                 '比较的是节点对象（`==` 判同一个节点），不是节点值',
                 '这是会员题，原文已是 Python 3 可运行写法，未修改；视频里用 `result_fn` 显示返回节点的值'],
    ),
)
