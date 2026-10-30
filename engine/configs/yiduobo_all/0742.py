def _v(x):
    return '空' if x is None else str(x)


def _info(S):
    I = S.get('_inner', {})
    if 'now' not in I:
        return ''
    return (f"当前节点 `{I['now'].val}`：左 `({_v(I.get('l_leaf'))}, {_v(I.get('l_dis'))}, {_v(I.get('l_step'))})`  "
            f"右 `({_v(I.get('r_leaf'))}, {_v(I.get('r_dis'))}, {_v(I.get('r_step'))})`")


def _info2(S):
    I = S.get('_inner', {})
    if 'now_leaf' not in I:
        return '三元组 = (最近叶子, 到它的距离, p 到自己的距离)'
    return f"本节点结果 `now_leaf={_v(I.get('now_leaf'))}, now_dis={_v(I.get('now_dis'))}, now_step={_v(I.get('now_step'))}`"


def _set_min(S, B, ret):
    return f'`min_dis = now_dis + now_step = {S.now_dis + S.now_step}`：p → now → 叶子 的最短距离'


def _set_res(S, B, ret):
    return f'`res = {S.now_leaf}`：记下这片叶子'


def _cap_now_leaf(S, B, ret):
    return ''


def _cap_pick(S, B, ret):
    I = S['_inner']
    if I['l_leaf'] is None and I['r_leaf'] is None:
        return f'左右都没有叶子 → `{I["now"].val}` ==自己是叶子==：`now_leaf = {I["now"].val}`，`now_dis = 0`'
    return f'左 `l_leaf={_v(I["l_leaf"])}` 右 `r_leaf={_v(I["r_leaf"])}`：比较两边的距离 `{_v(I["l_dis"])}` 与 `{_v(I["r_dis"])}`'


def _cap_l(S, B, ret):
    return f'节点 `{S["now"].val}` 有左孩子 → 递归，拿回左子树的 `(l_leaf, l_dis, l_step)`'


def _cap_r(S, B, ret):
    return f'节点 `{S["now"].val}` 有右孩子 → 递归，拿回右子树的 `(r_leaf, r_dis, r_step)`'


def _after_dis(S, B, ret):
    I = S['_inner']
    return f'选定：`now_leaf = {_v(I.get("now_leaf"))}`，`now_dis = {_v(I.get("now_dis"))}`（孩子的距离 +1）'


CONFIG = dict(
    num=742, title='二叉树最近的叶节点', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='DFS 后序 · 返回三元组',
    tags=['灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def findClosestLeaf(self, root, k):

        global min_dis, res
        min_dis = None
        res = None
        
        def dfs(now):
            if now.left is not None:
                l_leaf, l_dis, l_step = dfs(now.left)
            else:
                l_leaf, l_dis, l_step = None, None, None

            if now.right is not None:
                r_leaf, r_dis, r_step = dfs(now.right)
            else:
                r_leaf, r_dis, r_step = None, None, None

            if l_leaf is None and r_leaf is None:
                now_leaf = now.val
                now_dis = 0
            elif l_leaf is None or (r_leaf is not None and r_dis < l_dis):
                now_leaf = r_leaf
                now_dis = r_dis + 1
            else:
                now_leaf = l_leaf
                now_dis = l_dis + 1
            
            if now.val == k:
                now_step = 0
            elif l_step is None:
                if r_step is None:
                    now_step = None
                else:
                    now_step = r_step + 1
            else:
                now_step = l_step + 1
            
            global min_dis, res
            if now_step is not None and (min_dis is None or min_dis > now_dis + now_step):
                min_dis = now_dis + now_step
                res = now_leaf
        
            return now_leaf, now_dis, now_step

        dfs(root)
        return res
''',
    call='Solution().findClosestLeaf(Tr([1,2,3,None,None,None,4,None,5,None,6]), 3)',
    expect=2,
    views=[
        dict(type='text', fn=_info, size=24, h=46),
        dict(type='tree', label='二叉树（蓝 = now，粉 = 值为 k 的节点）', pointers={'now': 'blue'},
             color=lambda S, n: 'pink' if n.val == S.get('k') else None, h=250),
        dict(type='text', fn=_info2, size=24, h=46),
        dict(type='calls', h=200, hide=('root',)),
    ],
    watch=[('k', 'k', 'yellow'), ('now', lambda S: S['_inner']['now'].val if 'now' in S['_inner'] else None, 'blue'),
           ('now_dis', lambda S: S['_inner'].get('now_dis'), 'green'),
           ('now_step', lambda S: S['_inner'].get('now_step'), 'pink'),
           ],
    captions={
        'min_dis = None': '`min_dis` 记录目前最短的“k 到叶子”距离，用全局变量保存',
        'res = None': '`res` 记录对应的叶子值',
        'if now.left is not None': lambda S, B, r: (
            f'节点 `{S["now"].val}` 有左孩子 → 先递归求解左子树' if S['now'].left is not None
            else f'节点 `{S["now"].val}` 没有左孩子 → `l_leaf, l_dis, l_step` 全置为空'),
        'l_leaf, l_dis, l_step = dfs': _cap_l,
        'l_leaf, l_dis, l_step = None': '没有左孩子：三个值都是 ==None==',
        'if now.right is not None': lambda S, B, r: (
            f'节点 `{S["now"].val}` 有右孩子 → 递归求解右子树' if S['now'].right is not None
            else f'节点 `{S["now"].val}` 没有右孩子 → `r_leaf, r_dis, r_step` 全置为空'),
        'r_leaf, r_dis, r_step = dfs': _cap_r,
        'r_leaf, r_dis, r_step = None': '没有右孩子：三个值都是 ==None==',
        'if l_leaf is None and r_leaf is None': lambda S, B, r: (
            f'节点 `{S.now.val}` 的左右子树已递归完（没有孩子则为空）。左右都没有叶子 → ==自己就是叶子==：`now_leaf = {S.now.val}`，`now_dis = 0`' if S.l_leaf is None and S.r_leaf is None
            else f'有叶子可选：左 `{_v(S.l_leaf)}`（距离 {_v(S.l_dis)}），右 `{_v(S.r_leaf)}`（距离 {_v(S.r_dis)}）'),
        
        'elif l_leaf is None or': lambda S, B, r: (
            '没有左叶子，或右叶子更近（`r_dis < l_dis`）→ 取右边' if (S.l_leaf is None or (S.r_leaf is not None and S.r_dis < S.l_dis))
            else f'左叶子存在且不比右边远（`l_dis={S.l_dis}` ≤ `r_dis={_v(S.r_dis)}`）→ 取左边'),
        'now_leaf = r_leaf': '取右子树的叶子 `{now_leaf}`，距离是它到右孩子的距离再 +1：`now_dis = {r_dis} + 1 = {now_dis}`',
        'now_leaf = l_leaf': '取左子树的叶子 `{now_leaf}`，距离是它到左孩子的距离再 +1：`now_dis = {l_dis} + 1 = {now_dis}`',
        'now_dis = r_dis + 1': '取右子树的叶子 `{now_leaf}`；`now_dis = {r_dis} + 1 = {now_dis}`（往上一层，距离加一）',
        'now_dis = l_dis + 1': '取左子树的叶子 `{now_leaf}`；`now_dis = {l_dis} + 1 = {now_dis}`（往上一层，距离加一）',
        'if now.val == k': lambda S, B, r: (
            f'`{S.now.val}` 就是 `k = {S.k}` → ==p 就是它自己==，`now_step = 0`' if S.now.val == S.k
            else f'`{S.now.val}` 不是 `k = {S.k}` → 看孩子那边有没有 p'),
        'now_step = 0': '`now_step = 0`：p 到自己的距离为 0',
        'elif l_step is None': lambda S, B, r: (
            '左边没找到 p（`l_step` 为空）→ 去右边看' if S.l_step is None
            else f'p 在左子树：`l_step = {S.l_step}` → `now_step = l_step + 1`'),
        'if r_step is None': lambda S, B, r: (
            'p 也不在右子树 → 以 now 为根的子树里没有 p，`now_step = None`' if S.r_step is None
            else f'p 在右子树：`r_step = {S.r_step}` → `now_step = r_step + 1`'),
        'now_step = None': '`now_step = None`：p 不在这棵子树，现在还不能更新答案',
        'now_step = r_step + 1': '`now_step = {r_step} + 1 = {now_step}`：p 到 now 的距离',
        'now_step = l_step + 1': '`now_step = {l_step} + 1 = {now_step}`：p 到 now 的距离',
        'global min_dis, res': '回到全局：准备用 `now_dis + now_step` 更新答案',
        'if now_step is not None': lambda S, B, r: (
            'now_step 为空 → now 不在 p 到根的路径上，不能更新答案' if S.now_step is None
            else (f'now 在 p 到根的路径上：总距离 = `now_dis + now_step` = `{S.now_dis} + {S.now_step}` = =={S.now_dis + S.now_step}==，'
                  + '与全局 `min_dis` 比较：还没有答案或更短就更新')),
        'min_dis = now_dis + now_step': _set_min,
        'res = now_leaf': _set_res,
        'return now_leaf': lambda S, B, r: f'把 `(now_leaf, now_dis, now_step) = {r}` 返回给父节点',
        'dfs(root)': '从根节点开始后序 DFS',
        'return res': lambda S, B, r: f'最近的叶子是 `{r}`',
    },
    skip=['l_leaf, l_dis, l_step = None', 'r_leaf, r_dis, r_step = None', 'now_leaf = r_leaf', 'now_leaf = l_leaf', 'now_dis = 0', 'now_step = None', 'now_step = 0', 'global min_dis, res', 'now_leaf = now.val', 'l_leaf, l_dis, l_step = dfs', 'r_leaf, r_dis, r_step = dfs', 'if now.left is not None', 'if now.right is not None'],
    cards=dict(
        one_liner='p 到叶子的路 = 先上到祖先 a，再下到 a 子树里的叶子',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['给你一棵二叉树，每个节点值互不相同，再给一个值 `k`（树中一定有它）',
                 '返回离值为 `k` 的节点==最近的叶子节点==的值，距离按边数计',
                 '本视频：`root = [1,2,3,null,null,null,4,null,5,null,6]`，`k = 3` → `2`'],
        quote='将情况1合并到情况2中，即目标叶子节点位于p到root的路径上的某个点a为根节点的子树中，此时的最短距离就是p到a的距离加上以目标节点到a的距离。',
        quote_src='—— yiduobo 题解原文',
        idea=['后序 DFS：每个节点返回 `(最近叶子, 到叶子的距离, p 到自己的距离)`',
              '若 `now_step` 不为空，说明 now 在 p 到根的路径上',
              '此时 `now_dis + now_step` 就是“p 上到 now 再下到叶子”的候选答案',
              '情况 1（叶子在 p 的子树里）是 a = p 的特例，不用单独处理'],
        result='运行结束，返回 `2`：`3 → 1 → 2`，距离 2，比往下走的叶子 `6`（距离 3）更近',
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '易错：`now_step` 为空表示 p 不在这棵子树，==不能==拿来更新答案',
                 '易错：叶子判定是左右都没有叶子，此时距离为 0；否则取较近一侧再 +1',
                 '原文为 Python 2 风格，本题代码无需修改；`global` 用来在递归里共享答案'],
    ),
)
