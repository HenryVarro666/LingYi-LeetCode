CONFIG = dict(
    num=1026, title='节点与其祖先之间的最大差值', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='后序 DFS · 子树最大最小值',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1446'],
    code='''
class Solution(object):
    def maxAncestorDiff(self, root):
        return self.dfs(root)[0]

    def dfs(self, now):
        res = 0
        ma = mi = now.val

        if now.left:
            l_res, l_max, l_min = self.dfs(now.left)
            res = max(res, l_res, abs(now.val - l_max), abs(now.val - l_min))
            ma = max(ma, l_max)
            mi = min(mi, l_min)

        if now.right:
            r_res, r_max, r_min = self.dfs(now.right)
            res = max(res, r_res, abs(now.val - r_max), abs(now.val - r_min))
            ma = max(ma, r_max)
            mi = min(mi, r_min)

        return res, ma, mi
''',
    call='Solution().maxAncestorDiff(Tr([8,3,10,1,6,None,14]))',
    expect=7,
    views=[
        dict(type='text', fn=lambda S: (f"子树 `{S['_inner']['now'].val}`：最大 `ma = {S['_inner'].get('ma')}`，最小 `mi = {S['_inner'].get('mi')}`，最优 `res = {S['_inner'].get('res')}`" if 'now' in S['_inner'] else ''), size=26, h=56),
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=300),
        dict(type='calls', h=250),
    ],
    watch=[('now', lambda S: S['_inner'].get('now') and S['_inner']['now'].val, 'blue'),
           ('res', lambda S: S['_inner'].get('res'), 'green'),
           ('ma', lambda S: S['_inner'].get('ma'), 'pink'), ('mi', lambda S: S['_inner'].get('mi'), 'cyan')],
    captions={
        'return self.dfs(root)[0]': '`dfs` 返回三元组 `(res, ma, mi)`，答案取第 0 项 `res`',
        'res = 0': '先假设子树里最优差值为 0',
        'ma = mi = now.val': '先只有自己：`ma = mi = {now.val}`',
        'if now.left': '`{now.val}` {"有左孩子 → 先求左子树的 (res, max, min)" if now.left else "没有左孩子，跳过"}',
        'if now.right': '`{now.val}` {"有右孩子 → 再求右子树的 (res, max, min)" if now.right else "没有右孩子，跳过"}',
        'l_res, l_max, l_min': '进入左孩子 `{B.now.left.val}`，等它返回 `(最优, 最大, 最小)`',
        'r_res, r_max, r_min': '进入右孩子 `{B.now.right.val}`，等它返回 `(最优, 最大, 最小)`',
        'res = max(res, l_res': '最优可能来自左子树内部 `{l_res}`，或 `{now.val}` 与左子树最大/最小之差（`{abs(now.val - l_max)}`、`{abs(now.val - l_min)}`）→ `res` 变为 =={res}==',
        'res = max(res, r_res': '最优可能来自右子树内部 `{r_res}`，或 `{now.val}` 与右子树最大/最小之差（`{abs(now.val - r_max)}`、`{abs(now.val - r_min)}`）→ `res` 变为 =={res}==',
        'ma = max(ma, l_max)': '子树最大值合并左边：`ma = {ma}`',
        'mi = min(mi, l_min)': '子树最小值合并左边：`mi = {mi}`',
        'ma = max(ma, r_max)': '子树最大值合并右边：`ma = {ma}`',
        'mi = min(mi, r_min)': '子树最小值合并右边：`mi = {mi}`',
        'return res, ma, mi': '把本子树的 `(res, ma, mi) = ({res}, {ma}, {mi})` 交给父节点',
    },
    max_steps=110,
    cards=dict(
        one_liner='站在祖先 now 看子树：只需要子树的最大值和最小值',
        complexity='时间 `O(n)`，空间 `O(h)`',
        problem=['找不同节点 `A`、`B`，`A` 是 `B` 的祖先，使 `|A.val - B.val|` 最大',
                 '返回这个最大差值',
                 '示例：`[8,3,10,1,6,null,14]` → `|8 - 1| = 7`'],
        quote='now.val固定的情况下，我们只需要找出子树中其他节点的最大值ma以及最小值mi，那么以now为祖先的节点对的最大差值就是max(|now.val - ma|, |now.val - mi|)。',
        quote_src='—— yiduobo 题解',
        idea=['`dfs(now)` 返回三个量：子树最优解 `res`、最大值 `ma`、最小值 `mi`',
              '先递归左右子树，用它们的 `max/min` 与 `now.val` 作差，更新 `res`',
              '最优解也可能完全在某个子树内，所以还要和 `l_res`、`r_res` 取最大',
              '再把左右的最大/最小值合并进自己，返回给父节点'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '易错：返回值有三个，漏掉 `l_res/r_res` 会丢掉深处的最优解',
                 '只对存在的孩子递归，不用给空节点准备 `inf`',
                 '对比灵神：灵神向下传路径最值（递），这里向上返回子树最值（归）',
                 '原文为 Python 2 风格，仅删去了空行，无需其他改动'],
    ),
)
