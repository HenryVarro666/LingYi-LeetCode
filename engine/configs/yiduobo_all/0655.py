def _q(S):
    q = S.get('q')
    if q is None or 'head' not in S:
        return ''
    return '队列 `q` = ' + '  '.join(f'[{x[0].val}: {x[1]}~{x[2]}]' for x in q) + f'；`head={S["head"]}, tail={S["tail"]}`'


def _h(S):
    if 'n' not in S:
        return '先 DFS 求出树高 `h`，每层宽度 `n = 2^h − 1`'
    return f"树高 `h = {S['h']}`，矩阵是 `{S['h']} × {S['n']}`"


CONFIG = dict(
    num=655, title='输出二叉树', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='求树高 + 层序遍历按区间填位置',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def printTree(self, root):

        h = self.dfs(root)
        n = 2 ** h - 1

        q = [[root, 0, n - 1]]
        head = 0
        tail = 1
        res = []
        while head < tail:
            res.append([''] * (n))
            for index in range(head, tail):
                node, l, r = q[index]
                pos = (l + r) >> 1
                res[-1][pos] = str(node.val)
                if node.left:
                    q.append([node.left, l, pos - 1])
                if node.right:
                    q.append([node.right, pos + 1, r])
            
            head = tail
            tail = len(q)

        return res

    def dfs(self, now):
        if not now:
            return 0

        return max(self.dfs(now.left), self.dfs(now.right)) + 1
''',
    call='''s = Solution()
s.tree = Tr([1,2,3,None,4])
s.printTree(s.tree)''',
    expect=[['', '', '', '1', '', '', ''], ['', '2', '', '', '', '3', ''], ['', '', '4', '', '', '', '']],
    max_steps=90,
    skip=['if not now:', 'return 0'],
    views=[
        dict(type='text', fn=_h, size=24, h=50),
        dict(type='tree', label='二叉树（蓝 = 当前处理的 node）', pointers={'node': 'blue', 'now': 'blue'}, h=220, path=False),
        dict(type='text', fn=_q, size=22, h=50),
        dict(type='grid', var='res', label='res（每层一行，空位是 \'\'）', cell=70, h=230,
             color=lambda S, i, j, v: 'green' if v != '' else None),
        dict(type='calls', h=120, hide=('root',)),
    ],
    watch=[('h', 'h', 'yellow'), ('n', 'n', 'cyan'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('pos', 'pos', 'green')],
    captions={
        'h = self.dfs(root)': '先用一趟 DFS 求树的高度 `h`',
        'return max(self.dfs': lambda S, B, r: ('空节点，高度 `0`，返回上一层' if S.now is None else f'递归求节点 `{S.now.val}` 的高度：左右子树的高度都拿到后取 `max`，再 `+ 1`' if r is None
                                          else f'节点 `{S.now.val}` 的子树高度：`max(左, 右) + 1 = {r}`，==取较高的一边再加自己这一层=='),
        'n = 2 ** h - 1': '每层宽度 `n = 2^{h} − 1 = =={n}==`：答案是 `{h} × {n}` 的矩阵，先用 `\'\'` 占位',
        'q = [[root': '队列里放 `[节点, l, r]`：根管辖整行 `[0, {n - 1}]`',
        'head = 0': '`head` 到 `tail` 之间是==同一层==的节点',
        'tail = 1': '第一层只有根，`tail = 1`',
        'res = []': '`res` 逐层加行',
        'while head < tail': lambda S, B, r: (f'`head = {S.head} < tail = {S.tail}`：还有一层要填' if S.head < S.tail else f'`head = {S.head} == tail`：没有下一层了 → 结束'),
        "res.append([''": '新开一层：一行 `{n}` 个空串',
        'for index in range': '处理这一层的下标 `{head}` 到 `{tail - 1}` 的节点',
        'node, l, r = q': '取出节点 `{node.val}`，它管辖区间 `[{l}, {r}]`',
        'pos = (l + r)': '放在区间正中间：`pos = ({l} + {r}) >> 1 = =={pos}==`',
        'res[-1][pos]': '`res[-1][{pos}] = "{node.val}"`：节点值写进这一层的第 `{pos}` 格',
        'if node.left': lambda S, B, r: (f'`{S.node.val}` 有左孩子 `{S.node.left.val}` → 它管辖 `[{S.l}, {S.pos - 1}]`，入队' if S.node.left else f'`{S.node.val}` 没有左孩子'),
        'if node.right': lambda S, B, r: (f'`{S.node.val}` 有右孩子 `{S.node.right.val}` → 它管辖 `[{S.pos + 1}, {S.r}]`，入队' if S.node.right else f'`{S.node.val}` 没有右孩子'),
        'q.append([node.left': '左孩子带着区间 `[l, pos − 1]` 入队',
        'q.append([node.right': '右孩子带着区间 `[pos + 1, r]` 入队',
        'tail = len(q)': '这一层处理完：`head = {head}`，`tail = len(q) = {tail}`，下一层的节点就是 `q[head:tail]`',
        'return res': '`h × n` 的矩阵完成：`{res}`',
    },
    cards=dict(
        one_liner='每个节点管辖一个区间，永远放在区间正中间',
        complexity='时间 `O(2^h)`（填满矩阵），空间 `O(2^h)`',
        problem=['把二叉树打印成 `h × (2^h − 1)` 的字符串矩阵',
                 '根在第一行正中间；左右子树各占左右两半，递归放在各自那一行的正中间；空位是空串',
                 '本视频：`root = [1,2,3,null,4]`，`h = 3`，矩阵 `3 × 7`'],
        quote='对于树中的每个节点，其都管辖着某个区间[l, r]。节点本身位于mid = (l + r) / 2这个位置上，其左右子树则分别管辖着[l, mid - 1]以及[mid + 1, r]。',
        quote_src='—— yiduobo 题解原文',
        idea=['先 DFS 求高度 `h`，宽度 `n = 2^h − 1`，答案矩阵用空串初始化',
              '层序遍历：队列里存 `[节点, l, r]`，节点写在 `(l + r) >> 1`',
              '左孩子管辖 `[l, pos−1]`，右孩子管辖 `[pos+1, r]`'],
        summary=['时间、空间都是 `O(2^h)`',
                 '`head`/`tail` 圈出队列中的一层，处理完一层再整体后移',
                 '作者说也可以一趟完成，但要边算边修正位置，会麻烦',
                 '原文无需修改（`>> 1` 本来就是整数运算）；题面按 LeetCode 655 的字符串矩阵版本补写'],
    ),
)
