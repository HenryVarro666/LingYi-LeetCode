VALS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]


def _levels(S):
    """uid -> (层号, 层序下标)，用来判断节点值是否已被交换"""
    root = S.get('root')
    out, q, d, pos = {}, [root] if root else [], 0, 0
    while q:
        for nd in q:
            out[nd._uid] = (d, pos)
            pos += 1
        q = [c for nd in q for c in (nd.left, nd.right) if c]
        d += 1
    return out


def _color(S, node):
    if S.get('_line') == 9 and S.get('now') is not None and node._uid == S['now']._uid:
        return 'cyan'                        # 正在把孩子入队的 now
    info = _levels(S).get(node._uid)
    if info is None:
        return None
    d, pos = info
    if node.val != VALS[pos]:
        return 'green'
    return 'purple' if d % 2 == 1 else None


def _swap_phase(S):
    return S.get('_line') in (13, 14, 15)


def P_l(S):
    return S.get('l') if _swap_phase(S) else None


def P_r(S):
    return S.get('r') if _swap_phase(S) else None


def P_now(S):
    if S.get('_line') != 9 or 'now' not in S:
        return None
    return [n._uid for n in S['q']].index(S['now']._uid)


def _qcolor(S, i, v):
    if _swap_phase(S) and i in (S.get('l'), S.get('r')):
        return 'yellow'
    if i == P_now(S):
        return 'cyan'
    return None


def _cap_while(S, B, ret):
    if B.head < B.tail:
        return f'`head = {B.head} < tail = {B.tail}`：第 `{B.level}` 层还有节点 `q[{B.head}:{B.tail}]`'
    return f'`head == tail = {B.tail}`：没有下一层了，遍历结束'


def _cap_append(S, B, ret):
    nd = S.now
    return f'`now = {nd.val}` 有孩子 → 左右孩子 `{nd.left.val}`、`{nd.right.val}` 依次入队（完美二叉树，有左必有右）'


def _cap_odd(S, B, ret):
    if S.level % 2 == 1:
        return f'第 `{S.level}` 层是==奇数层== → 把 `q[{S.head}:{S.tail}]` 这一段的值反转'
    return f'第 `{S.level}` 层是偶数层，不用反转'


def _cap_inner_while(S, B, ret):
    if B.l < B.r:
        return f'`l = {B.l} < r = {B.r}`：首尾还没碰头，继续交换'
    return f'`l = {B.l} ≥ r = {B.r}`：首尾指针相遇 → 这一层反转完毕'


def _cap_swap(S, B, ret):
    a, b = B.q[B.l].val, B.q[B.r].val
    return f'交换 `q[{B.l}]`、`q[{B.r}]` 的==值==：`{a}` ↔ `{b}`；然后 `l += 1`、`r -= 1`'


CONFIG = dict(
    num=2415, title='反转二叉树的奇数层', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='层序遍历 · 反转队列中的一段',
    tags=['字节30天'],
    code='''
class Solution(object):
    def reverseOddLevels(self, root):
        q = [root]
        level = 0
        head, tail = 0, 1
        while head < tail:
            for now in q[head : tail]:
                if now.left:
                    q.append(now.left)
                    q.append(now.right)

            if level % 2 == 1:
                l, r = head, tail - 1
                while l < r:
                    q[l].val, q[r].val = q[r].val, q[l].val
                    l += 1
                    r -= 1

            head, tail = tail, len(q)
            level += 1

        return root
''',
    call=f'Solution().reverseOddLevels(Tr({VALS}))',
    result_fn=tree_list,
    expect=[1, 3, 2, 4, 5, 6, 7, 15, 14, 13, 12, 11, 10, 9, 8],
    skip=['for now in', 'if now.left', 'q.append(now.right)', 'l += 1', 'r -= 1', 'level += 1'],
    views=[
        dict(type='array', var=lambda S: [n.val for n in S['q']] if 'q' in S else None,
             label='q（只进不出的队列；青框 = 当前层 [head, tail)）', cell=64, min_slots=15,
             window=('head', 'tail - 1'), pointers={P_now: 'cyan', P_l: 'blue', P_r: 'pink'},
             pointer_labels={P_now: 'now', P_l: 'l', P_r: 'r'}, color=_qcolor, h=230),
        dict(type='tree', label='二叉树（青 = now，紫 = 奇数层待交换，绿 = 已交换）', h=400, path=False, color=_color),
    ],
    watch=[('level', 'level', 'purple'), ('head', 'head'), ('tail', 'tail'), ('l', 'l', 'blue'), ('r', 'r', 'pink')],
    captions={
        'q = [root]': '用数组当队列：只 `append`、不弹出，用 `[head, tail)` 标出==当前这一层==',
        'level = 0': '`level`：当前是第几层（根是第 0 层）',
        'head, tail = 0, 1': '第 0 层只有根：`q[0:1]`',
        'while head < tail': _cap_while,
        'q.append(now.left)': _cap_append,
        'if level % 2 == 1': _cap_odd,
        'l, r = head, tail - 1': '本层在 `q` 里是连续的一段 `[{l}, {r}]` → 首尾双指针往中间交换',
        'while l < r': _cap_inner_while,
        'q[l].val, q[r].val': _cap_swap,
        'head, tail = tail': lambda S, B, r: (f'这一层处理完：下一层是刚入队的 `q[{S.head}:{S.tail}]`（`level` 加一）' if S.head < S.tail
                                              else f'这一层全是叶子，没有新节点入队：`head = tail = {S.tail}`'),
        'return root': '只改了节点值、没动树的结构，直接返回根',
    },
    max_steps=60,
    cards=dict(
        one_liner='层序遍历时，奇数层在队列里正好是连续一段，把这段的值反转',
        complexity='时间 `O(n)`，空间 `O(n)`（队列存下所有节点）',
        problem=['给一棵==完美==二叉树，把每个==奇数层==（根为第 0 层）的节点值反转',
                 '例如某层是 `[2,1,3,4,7,11,29,18]`，反转后是 `[18,29,11,7,4,3,1,2]`',
                 '示例：`[2,3,5,8,13,21,34]` → `[2,5,3,8,13,21,34]`'],
        quote='层序遍历的每一轮恰好就是遍历某一层的所有节点……若当前遍历到奇数层，那么就将这一层的节点值反转，也就是==将当前队列中遍历的这一段的节点值反转过来==。',
        quote_src='—— yiduobo 题解原文',
        idea=['用数组模拟队列，`[head, tail)` 就是当前层的全部节点',
              '奇数层：对 `q[head..tail-1]` 用首尾双指针交换 `val`',
              '只改节点值，==不影响树的结构==，所以后续的层序遍历照常进行'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '交换的是 `val` 而不是节点：改指针会把子树也带走，后面的层就乱了',
                 '原文先把下一层全部入队、再反转本层；因为只换值，先后顺序不影响',
                 '对比灵神：灵神方法二用 DFS 同时递归一对镜像节点，空间只要 `O(log n)`',
                 '原文为 Python 2 风格：只删去了注释掉的 TreeNode 定义和类型说明文档字符串'],
    ),
)
