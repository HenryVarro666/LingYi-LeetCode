CONFIG = dict(
    num=938, title='二叉搜索树的范围和', difficulty='Easy', category='二叉树与回溯',
    author='yiduobo', technique='递归 · 逐步收窄范围',
    tags=['灵神题单', '链表树与回溯', '难度分 1335'],
    code='''
class Solution(object):
    def rangeSumBST(self, root, low, high):

        return self.sum(root, low, high)

    def sum(self, now, low, high):
        ret = 0
        if now.val < low:
            if now.right:
                ret = self.sum(now.right, low, high)
        elif now.val > high:
            if now.left:
                ret = self.sum(now.left, low, high)
        else:
            ret = now.val
            if now.left:
                ret += self.sum(now.left, low, now.val)
            if now.right:
                ret += self.sum(now.right, now.val, high)
        
        return ret
''',
    call='''s = Solution()
s.tree = Tr([10,5,15,3,7,None,18])
s.rangeSumBST(s.tree, 7, 15)''',
    expect=32,
    views=[
        dict(type='text', h=50, fn=lambda S: (f"当前要求的范围 `[low, high] = [{S['_inner']['low']}, {S['_inner']['high']}]`" if 'low' in S['_inner'] else '')),
        dict(type='tree', label='BST（黄圈 = 当前递归路径）', pointers={'now': 'blue'}, h=340,
             color=lambda S, n: 'green' if 7 <= n.val <= 15 else None),
        dict(type='calls', h=210, hide=('rangeSumBST',)),
    ],
    watch=[('now', lambda S: S['_inner'].get('now').val if S['_inner'].get('now') is not None else None, 'blue'),
           ('low', lambda S: S['_inner'].get('low'), 'cyan'), ('high', lambda S: S['_inner'].get('high'), 'orange'),
           ('ret', lambda S: S['_inner'].get('ret'), 'green')],
    captions={
        'return self.sum(root': '交给 `sum` 从根节点开始递归',
        'ret = 0': '`ret` 先记为 0：这棵子树目前没有累加到任何值',
        'if now.val < low': lambda S, B, r: (f"`{S.now.val} < {S.low}`：它和==左子树==都小于 low → 只需递归右子树" if S.now.val < S.low
                                             else f"`{S.now.val} < {S.low}` 不成立"),
        'elif now.val > high': lambda S, B, r: (f"`{S.now.val} > {S.high}`：它和==右子树==都大于 high → 只需递归左子树" if S.now.val > S.high
                                                else f"`{S.now.val} > {S.high}` 不成立 → `{S.now.val}` 落在 `[{S.low}, {S.high}]` 内"),
        'ret = now.val': lambda S, B, r: f"`{S.now.val}` 在范围内，先记下 `ret = {S['_inner']['ret']}`",
        'if now.left': lambda S, B, r: (f"有左儿子 `{S.now.left.val}` → 去求它在 `[{S.low}, {S.high if S.now.val > S.high else S.now.val}]` 内的和" if S.now.left else '没有左儿子，跳过'),
        'if now.right': lambda S, B, r: (f"有右儿子 `{S.now.right.val}` → 去求它在 `[{S.low if S.now.val < S.low else S.now.val}, {S.high}]` 内的和" if S.now.right else '没有右儿子，跳过'),
        'ret = self.sum(now.right, low, high)': lambda S, B, r: f"右子树的值都大于 `{S.now.val}`，范围不变 → `ret = {S['_inner']['ret']}`",
        'ret = self.sum(now.left, low, high)': lambda S, B, r: f"左子树的值都小于 `{S.now.val}`，范围不变 → `ret = {S['_inner']['ret']}`",
        'ret += self.sum(now.left, low, now.val)': lambda S, B, r: f"左子树的上界收窄成 `{S.now.val}`，`ret` 累加到 `{S['_inner']['ret']}`",
        'ret += self.sum(now.right, now.val, high)': lambda S, B, r: f"右子树的下界收窄成 `{S.now.val}`，`ret` 累加到 `{S['_inner']['ret']}`",
        'return ret': lambda S, B, r: f"以 `{S.now.val}` 为根的子树在范围内的和是 `{r}`，返回给上一层",
    },
    cards=dict(
        one_liner='落在范围内就以它为界，左右子树各自收窄范围',
        complexity='时间 `O(n)`，空间 `O(n)`（最坏退化成链）',
        problem=['给 BST 的根 `root` 和范围 `[low, high]`，求值在范围内的所有节点之和',
                 '示例：`root = [10,5,15,3,7,null,18], low = 7, high = 15` → `32`'],
        quote='若 low <= now.val <= high，那么此时可以以now为界划分[low, high]，对于左子树我们递归求解大小处于[low, now.val]之间的节点值之和，而对于右子树则递归求解[now.val, high]之间的节点值之和。',
        quote_src='—— yiduobo 题解原文',
        idea=['`now.val < low`：now 和左子树都太小 → 只递归右子树',
              '`now.val > high`：now 和右子树都太大 → 只递归左子树',
              '在范围内：左子树求 `[low, now.val]`，右子树求 `[now.val, high]`，再加上 `now.val`'],
        summary=['时间 `O(n)`，空间 `O(n)`：最坏是一条链',
                 '递归前先判断 `now.left`、`now.right` 是否存在，`sum` 里就不用处理空节点',
                 '范围收窄后，`low`、`high` 参数在更深的层里会变化，注意看调用栈',
                 '易错：范围内的节点先赋给 `ret = now.val`，不要漏掉自己'],
    ),
)
