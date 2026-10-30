CONFIG = dict(
    num=865, title='具有所有最深节点的最小子树', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='层次遍历记父亲 · 从最深层向上爬',
    tags=['灵神题单', '链表树与回溯', '难度分 1534'],
    code='''
class Solution(object):
    def subtreeWithAllDeepest(self, root):

        if not root:
            return root

        fa = {}
        q = [root]
        l = 0
        r = 1
        last_l = last_r = None
        while l < r:
            for now in q[l:r]:
                if now.left:
                    fa[now.left] = now
                    q.append(now.left)
                if now.right:
                    fa[now.right] = now
                    q.append(now.right)
        
            last_l, last_r, l, r = l, r, r, len(q)

        q = q[last_l:last_r]
        l = 0
        r = len(q)
        used = set()
        while l < r - 1:
            for now in q[l:r]:
                if now in fa and fa[now].val not in used:
                    q.append(fa[now])
                    used.add(fa[now].val)

            l, r = r, len(q)

        return q[l]
''',
    call='Solution().subtreeWithAllDeepest(Tr([3,5,1,6,2,0,None,None,None,7,4]))',
    expect=[2, 7, 4],
    result_fn=tree_list,
    views=[
        dict(type='tree', label='二叉树（蓝 = now；绿 = 最深层 / 爬升队列）', pointers={'now': 'blue'}, path=False, h=300,
             color=lambda S, nd: 'green' if S['_line'] >= 23 and 'q' in S and 'l' in S and nd in S['q'][S['l']:S['r']] else None),
        dict(type='queue', var='q', fmt=lambda x: str(x.val), label='q（节点值）', h=130),
        dict(type='text', fn=lambda S: f"`fa`：{ {k.val: v.val for k, v in S['fa'].items()} }（子 → 父）" if 'fa' in S else '', size=24, h=56),
        dict(type='set', var='used', label='used（已入队的父亲值）', h=100),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('last_l', 'last_l', 'cyan'), ('last_r', 'last_r', 'orange')],
    captions={
        'if not root': '空树直接返回',
        'fa = {}': '`fa` 记录每个节点的父亲：之后要从最深层往上爬',
        'q = [root]': '`q` 是层次遍历的队列，`[l, r)` 是当前这一层',
        'if now.left:': lambda S, B, r: (f'`{S.now.val}` 有左孩子 `{S.now.left.val}`' if S.now.left else f'`{S.now.val}` 没有左孩子'),
        'if now.right:': lambda S, B, r: (f'`{S.now.val}` 有右孩子 `{S.now.right.val}`' if S.now.right else f'`{S.now.val}` 没有右孩子'),
        13: '处理当前层 `q[{l}:{r}]` 的节点 `{now.val}`',
        'fa[now.left] = now': '`{now.left.val}` 的父亲是 `{now.val}`，入队',
        'fa[now.right] = now': '`{now.right.val}` 的父亲是 `{now.val}`，入队',
        'last_l, last_r, l, r': '这一层处理完：记下它的范围 `last_l={last_l}, last_r={last_r}`，下一层是 `[{l}, {r})`；==最后一次记录的就是最深层==',
        'q = q[last_l:last_r]': '最深层节点：`{[x.val for x in q]}`，用它们重新当队列',
        'used = set()': '`used` 记录已经入队的父亲，避免重复',
        'while l < r - 1': lambda S, B, r_: (f'当前层有 `{S.r - S.l}` 个节点（>1）→ 还没汇合，继续向上爬' if S.l < S.r - 1 else f'当前层只剩 `{S.r - S.l}` 个节点 → ==汇合了=='),
        28: '检查 `{now.val}` 的父亲',
        'if now in fa': lambda S, B, r_: (f'`{S.now.val}` 的父亲 `{S.fa[S.now].val}`' + ('已在 used 里 → 不重复加入' if S.fa[S.now].val in S.used else ' 还没加入 → 入队') if S.now in S.fa else f'`{S.now.val}` 是根，没有父亲'),
        'q.append(fa[now])': '父亲 `{fa[now].val}` 加入队尾',
        'l, r = r, len(q)': '这一轮爬完：新的一层是 `q[{l}:{r}]` = `{[x.val for x in q[l:r]]}`',
        'return q[l]': '只剩一个节点 `{q[l].val}`：所有最深节点都汇集到它 → ==答案=='
    },
    max_steps=110,
    cards=dict(
        one_liner='先记下每个节点的父亲，再让最深层的节点一起往上爬，汇成一个就是答案',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找包含树中==所有最深节点==的最小子树，返回它的根',
                 '本视频：`[3,5,1,6,2,0,null,null,null,7,4]`',
                 '最深层是 `7, 4`，向上汇合于节点 `2`',
                 '答案子树：`[2,7,4]`'],
        quote='从根节点开始进行层次遍历，同时在遍历过程中储存每个节点的父亲节点是什么；从层次遍历最底层的节点开始进行爬升，直到当前轮次的bfs队列中只有一个节点为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一遍 BFS：按层遍历，用 `fa` 存父亲，最后一层的范围存进 `last_l, last_r`',
              '第二遍：把最深层当队列，每轮把还没入队的父亲加进来，这就是一次「同时上一层」',
              '队列里只剩一个节点，就是它们汇合的地方'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：`used` 防止同一个父亲被多个孩子重复加入，这样「只剩一个」才成立',
                 '`while l < r - 1`：当前层多于一个节点才继续爬',
                 '本题节点值唯一，所以 `used` 用值去重；`fa` 用节点对象作键',
                 '对比灵神：灵神一次递归返回（高度，lca）；yiduobo 层次遍历 + 向上爬',
                 '原文可直接在 Python 3 运行，代码未改'],
    ),
)
