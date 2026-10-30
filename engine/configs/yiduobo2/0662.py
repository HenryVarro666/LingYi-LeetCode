TREE_H = 390


def _layout(root, box):  # 与 views.v_tree 相同的布局
    x0, y0, x1, y1 = box
    order, depth = [], {}

    def ino(n, d):
        if n is None or n._uid in depth:
            return
        depth[n._uid] = d
        ino(n.left, d + 1)
        order.append(n)
        ino(n.right, d + 1)
    ino(root, 0)
    maxd = max(depth.values()) + 1
    sp = min(78, (x1 - x0 - 60) / max(1, len(order)))
    dy = min(95, (y1 - y0 - 80) / max(1, maxd))
    rad = max(14, min(26, sp * 0.4, dy * 0.32))
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * len(order)) / 2 + sp / 2
    pos = {n._uid: (sx + i * sp, y0 + 60 + depth[n._uid] * dy + rad) for i, n in enumerate(order)}
    return pos, rad, order



def _posmap(S):
    return {nd._uid: p for nd, p in (S.get('q') or [])}


def badges(cv, S, B, box, T):
    root = S.get('root')
    if root is None:
        return
    pos, rad, order = _layout(root, (box[0], box[1] - TREE_H, box[2], box[1]))
    pm = _posmap(S)
    for n in order:
        if n._uid not in pm:
            continue
        X, Y = pos[n._uid]
        s = f'pos {pm[n._uid]}'
        w = cv.tlen(s, 18, bold=True) + 14
        cv.rect((X - w / 2, Y + rad + 4, X + w / 2, Y + rad + 28), fill=T['panel'], outline=T['cyan'], width=2, r=8)
        cv.text((X, Y + rad + 16), s, 18, T['cyan'], anchor='mm', bold=True)


def _level(S):
    q, l, r = S.get('q'), S.get('l'), S.get('r')
    if q is None or l is None or r is None:
        return set()
    return {nd._uid for nd, p in q[l:r]}


def _ncolor(S, n):
    return 'cyan' if n._uid in _level(S) else None


def _width_text(S):
    q, l, r = S.get('q'), S.get('l'), S.get('r')
    if q is None or r is None or l is None or l >= r:
        return '每层宽度 = ==最右节点编号 − 最左节点编号 + 1==（按满二叉树编号）'
    a, b = q[l][1], q[r - 1][1]
    return f'当前层 `q[{l}:{r}]`：最左 `pos = {a}`，最右 `pos = {b}`，宽度 `{b} − {a} + 1 = {b - a + 1}`'


def _cap_while(S, B, ret):
    if S.l < S.r:
        return f'`l = {S.l} < r = {S.r}`：`q[{S.l}:{S.r}]` 是新的一层，共 `{S.r - S.l}` 个节点'
    return f'`l == r = {S.r}`：下一层没有节点了，遍历结束'


def _cap_res(S, B, ret):
    a, b = S.q[S.l][1], S.q[S.r - 1][1]
    w = b - a + 1
    tail = '，==更新答案==' if S.res > B.res else ''
    return f'这一层宽度 = 最右编号 `{b}` − 最左编号 `{a}` + 1 = `{w}`，`res = max({B.res}, {w}) = {S.res}`{tail}'


CONFIG = dict(
    num=662, title='二叉树最大宽度', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='层序遍历 + 堆式编号（2x+1, 2x+2）',
    tags=['字节30天', '热题173'],
    code='''
class Solution(object):
    def widthOfBinaryTree(self, root):
        if not root:
            return 0
        q = [[root, 0]]
        l = 0
        r = 1
        res = 0
        while l < r:
            res = max(res, q[r - 1][1] - q[l][1] + 1)
            for index in range(l, r):
                node, pos = q[index]
                if node.left:
                    q.append([node.left, pos * 2 + 1])
                if node.right:
                    q.append([node.right, pos * 2 + 2])
            l = r
            r = len(q)

        return res
''',
    call='Solution().widthOfBinaryTree(Tr([1,3,2,5,None,None,9,6,None,7]))',
    expect=7,
    skip=['for index in range'],
    views=[
        dict(type='tree', var='root', label='二叉树（青 = 当前层 q[l:r]，标签 = 编号 pos）', pointers={'node': 'blue'},
             color=_ncolor, path=False, h=TREE_H),
        dict(type='custom', draw=badges, h=0),
        dict(type='array', var=lambda S: [f'{nd.val}@{p}' for nd, p in S['q']] if 'q' in S else None,
             label='q（值@编号；青框 = 当前层 [l, r)）', cell=92, h=170,
             window=('l', 'r - 1')),
        dict(type='text', h=64, size=25, fn=_width_text),
    ],
    watch=[('l', 'l', 'cyan'), ('r', 'r', 'cyan'), ('node', 'node', 'blue'), ('pos', 'pos'), ('res', 'res', 'green')],
    captions={
        'if not root': '树非空',
        'q = [[root, 0]]': '队列里存 `[节点, 编号]`：像用数组表示堆一样，根的编号是 `0`',
        'l = 0': '`q[l:r]` 是当前这一层（左闭右开）',
        'r = 1': '第一层只有根：`l = 0, r = 1`',
        'res = 0': '`res` 记录最大宽度',
        'while l < r': _cap_while,
        'res = max(': _cap_res,
        'node, pos = q[index]': '取出 `{node.val}`，编号 `pos = {pos}`',
        'if node.left': lambda S, B, ret: (f'`{S.node.val}` 有左儿子 `{S.node.left.val}` → 编号 `2 × {S.pos} + 1 = {2 * S.pos + 1}`' if S.node.left
                                           else f'`{S.node.val}` 没有左儿子'),
        'q.append([node.left': '左儿子 `{node.left.val}` 入队，编号 `{q[-1][1]}`',
        'if node.right': lambda S, B, ret: (f'`{S.node.val}` 有右儿子 `{S.node.right.val}` → 编号 `2 × {S.pos} + 2 = {2 * S.pos + 2}`' if S.node.right
                                            else f'`{S.node.val}` 没有右儿子'),
        'q.append([node.right': '右儿子 `{node.right.val}` 入队，编号 `{q[-1][1]}`',
        'l = r': '这一层处理完，下一层从 `l = {l}` 开始',
        'r = len(q)': '下一层到队尾：`r = len(q) = {r}`',
        'return res': '返回最大宽度 `{ret}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='按满二叉树给节点编号，每层宽度 = 最右编号 − 最左编号 + 1',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['求二叉树所有层中的==最大宽度==',
                 '每层宽度：最左和最右两个非空节点之间的长度，==中间的 null 也要算==（按满二叉树）',
                 '示例：`[1,3,2,5,3,null,9]` → `4`；`[1,3,2,5,null,null,9,6,null,7]` → `7`（本视频）'],
        quote='我们可以仿照用数组表示堆的做法来为节点进行编号，而节点最终的编号差就是位置之差。具体来说就是对于某个节点，若其编号为x，那么其左右孩子的编号分别为2x+1以及2x+2。',
        quote_src='—— yiduobo 题解',
        idea=['层序遍历：用数组 `q` 当队列，`[l, r)` 是当前层',
              '编号像堆一样：左儿子 `2x+1`，右儿子 `2x+2`；同层编号差就是位置差',
              '每层：`q[r-1]` 是最右、`q[l]` 是最左，宽度 = 编号差 + 1'],
        summary=['时间 `O(n)`，空间 `O(n)`（队列存所有节点，不出队）',
                 '易错：宽度包含中间的空位，所以不能数节点个数，要用编号差',
                 '易错：编号随深度指数增长；Python 整数不溢出，其他语言可每层减去最左编号',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
