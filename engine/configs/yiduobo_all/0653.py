CONFIG = dict(
    num=653, title='两数之和 IV - 输入二叉搜索树', difficulty='Easy', category='二叉树与回溯',
    author='yiduobo', technique='中序遍历 + 双指针', tags=[],
    code='''
class Solution(object):
    def findTarget(self, root, k):

        num_list = self.dfs(root)

        l = 0
        r = len(num_list) - 1
        while l < r:
            if num_list[l] + num_list[r] == k:
                return True
            elif num_list[l] + num_list[r] > k:
                r -= 1
            else:
                l += 1

        return False

    def dfs(self, now):
        if now is None:
            return []

        return self.dfs(now.left) + [now.val] + self.dfs(now.right)
''',
    call='Solution().findTarget(Tr([5,3,6,2,4,None,7]), 9)',
    expect=True,
    views=[
        dict(type='tree', var='root', label='BST（蓝 = now）', pointers={'now': 'blue'}, h=230),
        dict(type='array', var='num_list', label='num_list（中序 = 升序）', pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r'), cell=72, h=150),
        dict(type='text', fn=lambda S: (f"`{S['num_list'][S['l']]} + {S['num_list'][S['r']]}` = =={S['num_list'][S['l']] + S['num_list'][S['r']]}== ，目标 `k = {S['k']}`" if 'r' in S and 0 <= S['l'] < S['r'] else ''), size=28, h=56),
        dict(type='calls', h=160, hide=()),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('k', 'k', 'yellow')],
    captions={
        'num_list = self.dfs': '先中序遍历整棵 BST，得到升序数组',
        'return []': '空节点返回空列表',
        'return self.dfs(now.left)': '`{now.val}` 的左子树列表 + `[{now.val}]` + 右子树列表：拼出升序列表',
        'l = 0': '左指针指向最小值',
        'r = len': '右指针指向最大值：`r = {r}`',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}` → 两个数还没碰头，继续' if S.l < S.r else '指针相遇，没有找到 → 结束'),
        'if num_list[l] + num_list[r] == k': '`{num_list[l]} + {num_list[r]} = {num_list[l] + num_list[r]}`，和 `k = {k}` ' + '{"相等" if num_list[l] + num_list[r] == k else "不相等"}',
        'elif num_list[l] + num_list[r] > k': '和 `{num_list[l] + num_list[r]}` {">" if num_list[l] + num_list[r] > k else "<"} `{k}`',
        'return True': '找到两个数之和为 `{k}` → ==True==',
        'r -= 1': '和太大 → 右指针左移，换更小的数：`r = {r}`',
        'l += 1': '和太小 → 左指针右移，换更大的数：`l = {l}`',
        'return False': '没有找到 → False',
    },
    skip=['if now is None:'],
    cards=dict(
        one_liner='BST 的中序遍历是有序数组，在上面双指针找两数之和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给 BST 的根 `root` 和整数 `k`', '判断树中是否存在==两个不同节点==，值之和等于 `k`',
                 '本视频：`root = [5,3,6,2,4,null,7]`，`k = 9`', '`2 + 7 = 9` → `true`'],
        quote='对于输入的bst，其中序遍历是天然有序的，因此我们可以通过求其中序遍历得到有序的序列，然后在有序序列上使用双指针就能很快得到答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dfs` 返回 左子树列表 + 当前值 + 右子树列表 = 升序数组', '和太大就让右指针左移，太小就让左指针右移', '`l < r` 保证取到的是两个不同的节点'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`dfs` 用列表拼接，每层都会复制，最坏是 `O(n^2)`，本题数据范围内可接受',
                 '循环条件是 `l < r`，不能取同一个节点两次',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
