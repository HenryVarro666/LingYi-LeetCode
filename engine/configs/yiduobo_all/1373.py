def _t(x):
    return '空' if x is None else str(x)


def _info(S):
    I = S['_inner']
    now = I.get('now')
    if now is None:
        return '每个节点求五个值：是否 BST、和、BST 子树最大和、最小值、最大值'
    s = f'节点 `{now.val}`：'
    if 'l_flag' in I:
        s += f"左 `(BST={I['l_flag']}, 和={I['l_sum']}, 最小={_t(I['l_min'])}, 最大={_t(I['l_max'])})`"
    if 'r_flag' in I:
        s += f"　右 `(BST={I['r_flag']}, 和={I['r_sum']}, 最小={_t(I['r_min'])}, 最大={_t(I['r_max'])})`"
    return s


def _lcheck(S, B, ret):
    n = S.now.val
    if S.l_max >= n:
        return f'`l_max = {S.l_max} >= {n}` → `l_flag = False`'
    return f'`l_max = {S.l_max} < {n}`：左边够小，`l_flag` 不变'


def _rcheck(S, B, ret):
    n = S.now.val
    if S.r_min <= n:
        return f'`r_min = {S.r_min} <= {n}` → `r_flag = False`'
    return f'`r_min = {S.r_min} > {n}`：右边够大，`r_flag` 不变'


def _both(S, B, ret):
    if S.l_flag and S.r_flag:
        return '左右都是 BST 且夹得住 `now` → 当前子树是 ==BST=='
    return f'`l_flag = {S.l_flag}`，`r_flag = {S.r_flag}` → 当前子树 ==不是 BST=='


CONFIG = dict(
    num=1373, title='二叉搜索子树的最大键值和', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='dfs 返回五元组 · 自底向上',
    tags=['灵神题单', '链表树与回溯', '难度分 1914'],
    code='''
class Solution(object):
    def maxSumBST(self, root):

        return self.dfs(root)[2]

    def dfs(self, now):
        mi = ma = now.val

        if now.left is None:
            l_flag = True
            l_sum = 0
            l_res = 0
            l_min = None
            l_max = None
        else:
            l_flag, l_sum, l_res, l_min, l_max = self.dfs(now.left)
            if l_max >= now.val:
                l_flag = False
            mi = min(mi, l_min)
            ma = max(ma, l_max)

        if now.right is None:
            r_flag = True
            r_sum = 0
            r_res = 0
            r_min = None
            r_max = None
        else:
            r_flag, r_sum, r_res, r_min, r_max = self.dfs(now.right)
            if r_min <= now.val:
                r_flag = False
            mi = min(mi, r_min)
            ma = max(ma, r_max)

        if l_flag and r_flag:
            flag = True
        else:
            flag = False

        s = now.val + l_sum + r_sum

        res = max(l_res, r_res)
        if flag:
            res = max(res, now.val + l_sum + r_sum)

        return flag, s, res, mi, ma
''',
    call='Solution().maxSumBST(Tr([5,4,8,3,None,6,3]))',
    expect=7,
    views=[
        dict(type='text', fn=_info, size=22, h=70),
        dict(type='tree', label='二叉树（蓝 = now，黄圈 = 递归路径）', pointers={'now': 'blue'}, h=330),
        dict(type='calls', h=200, hide=()),
    ],
    watch=[('now', lambda S: getattr(S['_inner'].get('now'), 'val', None), 'blue'),
           ('l_flag', lambda S: S['_inner'].get('l_flag'), 'cyan'), ('r_flag', lambda S: S['_inner'].get('r_flag'), 'orange'),
           ('s', lambda S: S['_inner'].get('s'), 'yellow'), ('res', lambda S: S['_inner'].get('res'), 'green')],
    captions={
        'return self.dfs(root)[2]': '从根开始 dfs，返回值下标 2 的 `res` 就是答案',
        'mi = ma = now.val': '先假设子树只有 `now`：`mi = ma = {now.val}`',
        'l_flag = True': '==左子树为空==：当作 BST，和 0，最小/最大记 `None`',
        'r_flag = True': '==右子树为空==：同样当作 BST，和 0',
        'self.dfs(now.left)': '递归左子树，拿回 `l_flag, l_sum, l_res, l_min, l_max`',
        'self.dfs(now.right)': '递归右子树，拿回 `r_flag, r_sum, ...`',
        'if l_max >= now.val': _lcheck,
        'l_flag = False': '`l_flag = False`：左子树即使自己是 BST，放在 `now` 下面也 ==破坏了 BST 定义==',
        'if r_min <= now.val': _rcheck,
        'r_flag = False': '`r_flag = False`：右子树里有不大于 `now` 的值，==破坏了 BST 定义==',
        'mi = min(mi, l_min)': '合并左子树的最小值：`mi = {mi}`',
        'ma = max(ma, l_max)': '合并左子树的最大值：`ma = {ma}`',
        'mi = min(mi, r_min)': '合并右子树的最小值：`mi = {mi}`',
        'ma = max(ma, r_max)': '合并右子树的最大值：`ma = {ma}`',
        'if l_flag and r_flag': _both,
        's = now.val': '子树所有节点之和：`s = {now.val} + {l_sum} + {r_sum} =` =={s}==',
        'res = max(l_res, r_res)': '`res` 先取左右较大者：`max({l_res}, {r_res}) = {res}`',
        'res = max(res, now.val': '整棵也是 BST，和 `{s}` 来竞争 → `res =` =={res}==',
        'return flag, s, res, mi, ma': '返回 `({flag}, {s}, {res}, {mi}, {ma})` 给父节点',
    },
    skip=['l_sum = 0', 'l_res = 0', 'l_min = None', 'l_max = None', 'r_sum = 0', 'r_res = 0', 'r_min = None', 'r_max = None',
          36, 38, 'mi = min(mi', 'ma = max(ma', 'if flag:', 'if now.left is None', 'if now.right is None'],
    max_steps=110,
    cards=dict(
        one_liner='dfs 自底向上返回五个值，BST 才用子树和去竞争答案',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['给你一棵二叉树，求其中==任意二叉搜索子树==的最大键值和',
                 'BST：左子树的值都小于当前值，右子树的值都大于当前值',
                 '示例：`[1,4,3,2,4,2,5,...]` → `20`',
                 '本视频：`[5,4,8,3,null,6,3]` → `7`（子树 `4-3`）'],
        quote='对于某个节点now，其左子树必须是二叉搜索树，且其中最大的节点值必须小于now.val；其右子树必须也是二叉搜索树，且其中最小的节点值必须大于now.val。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个节点要知道四件事：==是不是 BST、最大值、最小值、节点和==',
              '原文再顺手带上第五个：子树里 BST 的最大键值和 `res`，所以返回五元组',
              '`flag = l_flag and r_flag` 且 `l_max < now < r_min`；`res` 先取左右较大者，若 `flag` 再与 `s` 比较'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '空子树 `flag = True`、和为 0，最小/最大值记 `None`，只在子树非空的分支里才比较',
                 '`res` 不会因为当前不是 BST 而丢失：它始终带着子树里更小 BST 的答案',
                 '原文写 `mi` 是三者中的“最大”，应为最小；代码本身是对的',
                 '对比灵神：灵神用 `(-∞, ∞, 0)` 标记非 BST 并用 `ans` 全局变量；yiduobo 显式返回 flag 和 res，不用全局变量'],
    ),
)
