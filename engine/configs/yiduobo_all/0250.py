def _inf(S):
    if 'now' not in S:
        return '同值子树：子树里==所有节点值相同==；叶子本身算一棵'
    return '后序：先处理完孩子，再判断自己；`res` 在满足时 +1'


def _lf(S, B, ret):
    return f'`now = {S.now.val}`：先把 `left_flag`、`right_flag` 都当作 ==True==（没有孩子的一侧视为同值）'


def _cl(S, B, ret):
    n = S.now
    why = []
    if n.left and n.val != n.left.val:
        why.append(f'`{n.val} != {n.left.val}`（值不同）')
    if n.left and not S.left_flag:
        why.append('左子树本身不是同值子树')
    return f'左孩子 `{n.left.val}` 破坏同值：' + '，'.join(why) + ' → ==返回 False=='


def _cr(S, B, ret):
    n = S.now
    why = []
    if n.right and n.val != n.right.val:
        why.append(f'`{n.val} != {n.right.val}`（值不同）')
    if n.right and not S.right_flag:
        why.append('右子树本身不是同值子树')
    return f'右孩子 `{n.right.val}` 破坏同值：' + '，'.join(why) + ' → ==返回 False=='


CONFIG = dict(
    num=250, title='统计同值子树', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='后序 dfs · 返回子树是否同值',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def countUnivalSubtrees(self, root):

        if not root:
            return 0

        global res
        res = 0

        def dfs(now):
            left_flag = right_flag = True
            if now.left:
                left_flag = dfs(now.left)
            if now.right:
                right_flag = dfs(now.right)

            if now.left and (now.val != now.left.val or not left_flag):
                return False
            if now.right and (now.val != now.right.val or not right_flag):
                return False

            global res
            res += 1
            return True

        dfs(root)
        return res
''',
    call='Solution().countUnivalSubtrees(Tr([5,1,5,5,5,None,5]))',
    expect=4,
    views=[
        dict(type='text', fn=_inf, size=26, h=60),
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=340),
        dict(type='text', fn=lambda S: (f"本层 `left_flag = {S['_inner'].get('left_flag')}`，`right_flag = {S['_inner'].get('right_flag')}`" if 'left_flag' in S['_inner'] else ''), size=26, h=60),
        dict(type='calls', h=240),
    ],
    watch=[('now', 'now.val', 'blue'), ('left_flag', lambda S: S['_inner'].get('left_flag'), 'cyan'),
           ('right_flag', lambda S: S['_inner'].get('right_flag'), 'pink')],
    captions={
        'if not root': '空树没有子树 → 直接返回 0；本例非空，继续',
        'res = 0': '`res` 计数，用 `global` 让内层 dfs 也能改它',
        'left_flag = right_flag = True': _lf,
        'left_flag = dfs': '先递归左孩子 `{B.now.left.val}`，它返回「左子树是否同值」存进 `left_flag`',
        'right_flag = dfs': '再递归右孩子 `{B.now.right.val}`，返回值存进 `right_flag`',
        'if now.left and': lambda S, B, r: (_cl(S, B, r) if S.now.left and (S.now.val != S.now.left.val or not S.left_flag)
                                            else '左边没问题：没有左孩子，或值相等且左子树同值'),
        'if now.right and': lambda S, B, r: (_cr(S, B, r) if S.now.right and (S.now.val != S.now.right.val or not S.right_flag)
                                             else '右边没问题：没有右孩子，或值相等且右子树同值'),
        'res += 1': '左右都满足：以 `{now.val}` 为根的子树==同值== → `res` 加 1',
        'return True': '把 ==True== 交给父节点：它可以据此判断自己',
        'return False': '把 ==False== 交给父节点：父亲也不可能同值了',
        'dfs(root)': '从根开始后序 dfs',
        'return res': '同值子树一共 `{ret}` 棵',
    },
    skip=['global res'],
    cards=dict(
        one_liner='后序 dfs：孩子同值且值等于自己，这棵子树才同值',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['给你一棵二叉树的根 `root`，统计其中==同值子树==的个数',
                 '同值子树：子树里所有节点的值都相同（叶子也算）',
                 '本视频：`root = [5,1,5,5,5,null,5]` → `4`'],
        quote='对于以节点now为根节点的子树来说，如果其所有节点是同值的，那么其左右子树必然也是同值的，且这棵树根节点的值now.val必然等于now.left.val以及now.right.val',
        quote_src='—— yiduobo 题解原文',
        idea=['先递归左右孩子，用 `left_flag`、`right_flag` 记录它们是否同值',
              '有孩子时：值要和自己相等，并且孩子那棵子树也要同值，否则返回 `False`',
              '都通过就 `res += 1` 并返回 `True`；叶子没有孩子，直接计数'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '易错：只比较值不看 `flag`，会把「孩子值相同但孩子子树不同值」的情况算进去',
                 '没有孩子的一侧 flag 默认 `True`，叶子自然算一棵',
                 '用 `global res` 累计答案，函数内要在赋值前声明',
                 '原文已是 Python 3 可运行写法，仅去掉了空白行末尾空格'],
    ),
)
