def _vals(name):
    return lambda S: [n.val for n in S[name]] if S.get(name) is not None else []


def _info(S):
    if 'self.l' not in S:
        return '初始化：用 BFS 找出「倒数第二层」和「最后一层」'
    return (f"倒数第二层 `now_q` 里下一个可挂孩子的是下标 `l = {S['self.l']}`（共 `r = {S['self.r']}` 个）；"
            f"最后一层已有 `{len(S['self.child_q'])}` 个节点")


def _par(S):
    q = S.get('self.now_q')
    if not q or S.get('self.l') is None or S['self.l'] >= len(q):
        return None
    return q[S['self.l']]


CONFIG = dict(
    num=919, title='完全二叉树插入器', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='BFS 队列 · 维护最后两层',
    tags=['链表树与回溯', '设计'],
    code='''
class CBTInserter(object):

    def __init__(self, root):
        self.now_q = [root]
        self.child_q = []
        self.root = root
        self.l = 0
        self.r = 1
        while True:
            for now in self.now_q[self.l : self.r]:
                if now.left:
                    self.child_q.append(now.left)
                    if now.right:
                        self.child_q.append(now.right)
                        self.l += 1
            if self.l == self.r:
                self.now_q = self.child_q[:]
                self.child_q = []
                self.l = 0
                self.r = len(self.now_q)
            else:
                break

    def insert(self, v):
        node = TreeNode(v)
        self.child_q.append(node)
        now = self.now_q[self.l]
        if now.left:
            now.right = node
            self.l += 1
            if self.l == self.r:
                self.now_q = self.child_q[:]
                self.child_q = []
                self.l = 0
                self.r = len(self.now_q)
        else:
            now.left = node
        
        return now.val

    def get_root(self):
        return self.root
''',
    call='c = CBTInserter(Tr([1, 2, 3, 4]))\nres = [c.insert(5), c.insert(6), c.insert(7)]\nres',
    expect=[2, 3, 3],
    views=[
        dict(type='text', fn=_info, size=24, h=70),
        dict(type='tree', label='完全二叉树（蓝 = 下一个要挂孩子的节点 now，绿 = 新插入的 node）', path=False, h=270,
             var='self.root', pointers={'now': 'blue', 'node': 'green'}),
        dict(type='array', var=_vals('self.now_q'), label='now_q（倒数第二层，l 之前的已经挂满）', cell=60, h=170,
             pointers={'self.l': 'blue', 'self.r': 'pink'}),
        dict(type='array', var=_vals('self.child_q'), label='child_q（最后一层，按从左到右）', cell=60, h=110),
    ],
    watch=[('l', 'self.l', 'blue'), ('r', 'self.r', 'pink'), ('now', lambda S: S['now'].val if S.get('now') is not None else None, 'yellow')],
    captions={
        4: '`now_q` 存「倒数第二层」：先放根',
        5: '`child_q` 存它下面的「最后一层」，先空着',
        7: '`l` 指向 `now_q` 中第一个还没挂满孩子的节点',
        8: '`r` 是 `now_q` 的长度：`l` 走到 `r` 说明这一层挂满了',
        9: '不断 BFS，一直推到最后一层（还没挂满的那层的上一层）',
        10: lambda S, B, r: ('这一层扫完了 → 看是否全部挂满' if getattr(B.get('now'), '_uid', 0) == getattr(S.get('now'), '_uid', 1) else f'扫描 `now_q` 里还没处理的节点：`now = {S.now.val}`'),
        11: lambda S, B, r: (f'`{S.now.val}` 有左孩子 `{S.now.left.val}` → 它属于最后一层' if S.now.left
                                        else f'`{S.now.val}` 没有左孩子 → 完全二叉树里，它就是下一个要挂孩子的节点'),
        12: '左孩子加入 `child_q`',
        13: lambda S, B, r: (f'`{S.now.val}` 也有右孩子 `{S.now.right.val}`' if S.now.right
                                         else f'`{S.now.val}` 没有右孩子 → 它只有左孩子，右边的空位就是下一个插入位置'),
        14: '右孩子加入 `child_q`',
        15: '`{now.val}` 左右都满了 → `l` 后移到 `{self.l}`',
        16: lambda S, B, r: (f'`l = {S["self.l"]} == r = {S["self.r"]}`：这一层全挂满了 → ==最后一层升级成新的倒数第二层==' if S['self.l'] == S['self.r']
                                                else f'`l = {S["self.l"]} < r = {S["self.r"]}`：这一层还有节点没挂满，==当前就是目标层=='),
        17: '`child_q` 复制成新的 `now_q`',
        31: lambda S, B, r: (f'`l = {S["self.l"]} == r = {S["self.r"]}`：倒数第二层挂满了 → ==最后一层升级成新的倒数第二层==' if S['self.l'] == S['self.r']
                             else f'`l = {S["self.l"]} < r = {S["self.r"]}`：倒数第二层还有空位，不用换层'),
        32: '`child_q` 复制成新的 `now_q`',
        18: '`child_q` 清空，等待更下一层的节点',
        33: '`child_q` 清空，等待更下一层的节点',
        19: '`l` 回到 0：新的一层从最左开始',
        34: '`l` 回到 0：新的一层从最左开始',
        20: '`r = {self.r}`：新一层的节点数',
        35: '`r = {self.r}`：新一层的节点数',
        22: '找到了：`now_q[l]` 就是下一个要挂孩子的节点，初始化结束',
        25: '为插入的值 `{v}` 新建节点',
        26: '新节点一定落在最后一层，先把它追加到 `child_q` 末尾',
        27: '父亲就是 `now_q[l]` = `{now.val}`：最左边还有空位的节点',
        28: lambda S, B, r: (f'`{S.now.val}` 已有左孩子 → 新节点挂到它的右边' if S.now.left
                                        else f'`{S.now.val}` 还没有左孩子 → 新节点挂到它的左边'),
        29: '`{now.val}` 的右孩子 = `{node.val}`，这个父亲满了',
        37: '`{now.val}` 的左孩子 = `{node.val}`，这个父亲还留着右边的空位',
        30: '父亲 `{now.val}` 挂满了 → `l` 后移到 `{self.l}`',
        39: '返回父亲的值 ==`{ret}`==',
        'res = [': '依次插入 5、6、7，得到每次的父亲值：`{res}`',
    },
    skip=['else:', 'c = CBTInserter'],
    max_steps=110,
    cards=dict(
        one_liner='只维护最后两层：倒数第二层找父亲，最后一层收新节点',
        complexity='初始化 `O(n)`，每次 `insert` 为 `O(1)`（均摊）',
        problem=['完全二叉树插入器：`CBTInserter(root)` 用一棵完全二叉树初始化',
                 '`insert(v)`：插入值为 `v` 的新节点，保持完全二叉树，==返回它父亲的值==',
                 '`get_root()` 返回根',
                 '本视频：`[1,2,3,4]`，依次插入 5、6、7 → 返回 `[2,3,3]`'],
        quote='最后一层的所有节点只与倒数第二层有关，同时插入的顺序是严格从左至右的，因此我们可以使用类似层次遍历的做法，使用一个队列储存bfs倒数第二轮以及最后一轮的节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['`now_q` 是倒数第二层，`child_q` 是最后一层，`l` 指向第一个还没挂满的父亲',
              '插入：父亲没有左孩子就挂左，否则挂右；新节点同时追加进 `child_q`',
              '父亲挂满则 `l += 1`；`l == r` 时最后一层升级为新的倒数第二层'],
        summary=['初始化 `O(n)`；每次 `insert` 只改常数个指针，`O(1)`（换层时的复制摊还为 `O(1)`）',
                 '易错：挂右孩子后才 `l += 1`，挂左孩子时 `l` 不动',
                 '`l == r` 时必须同时重置 `now_q / child_q / l / r` 四个量',
                 '原文已是 Python 3 可运行写法，未修改；`TreeNode` 由平台预置'],
    ),
)
