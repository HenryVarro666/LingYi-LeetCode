def _v(n):
    return 'None' if n is None else str(n.val)


CONFIG = dict(
    num=971, title='翻转二叉树以匹配先序遍历', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='先序 dfs · 对不上就翻转',
    tags=['灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def flipMatchVoyage(self, root, voyage):

        self.p = 0
        return self.dfs(root, voyage)

    def dfs(self, now, voyage):
        if now.val != voyage[self.p]:
            return [-1]
        
        self.p += 1

        if not now.left:
            if not now.right:
                return []
            else:
                return self.dfs(now.right, voyage)
        elif not now.right:
            return self.dfs(now.left, voyage)
        elif now.left.val != voyage[self.p]:
            left_ret = self.dfs(now.right, voyage)
            if left_ret == [-1]:
                return [-1]
            right_ret = self.dfs(now.left, voyage)
            if right_ret == [-1]:
                return [-1]
            return [now.val] + left_ret + right_ret
        else:
            left_ret = self.dfs(now.left, voyage)
            if left_ret == [-1]:
                return [-1]
            right_ret = self.dfs(now.right, voyage)
            if right_ret == [-1]:
                return [-1]
            return left_ret + right_ret
''',
    call='Solution().flipMatchVoyage(Tr([1,2,3,4,5]), [1,3,2,5,4])',
    expect=[1, 2],
    views=[
        dict(type='tree', label='二叉树（蓝 = now，绿 = 已匹配）', pointers={'now': 'blue'}, h=300,
             color=lambda S, node: 'green' if 'self.p' in S and node.val in S['voyage'][:S['self.p']] else None),
        dict(type='array', var='voyage', label='voyage（绿 = 已匹配，黄 = 下一个要匹配的 voyage[p]）', cell=84, h=150,
             color=lambda S, i, v: ('green' if i < S['self.p'] else 'yellow' if i == S['self.p'] else None) if 'self.p' in S else None),
        dict(type='calls', h=200, hide=('voyage',)),
    ],
    watch=[('now', lambda S: S['now'].val if 'now' in S and S['now'] else None, 'blue'),
           ('p', lambda S: S['self.p'] if 'self.p' in S else None, 'yellow'),
           ('left_ret', lambda S: S['_inner'].get('left_ret'), 'cyan'),
           ('right_ret', lambda S: S['_inner'].get('right_ret'), 'pink')],
    captions={
        'self.p = 0': '`p` 是先序序列里==当前要匹配的位置==，从 0 开始（存在 self 上，所有递归共享）',
        'return self.dfs(root, voyage)': '从根开始先序 dfs',
        'if now.val != voyage[self.p]': lambda S, B, r: (f'`now.val = {S.now.val}`，`voyage[{S.self.p}] = {S.voyage[S.self.p]}` → ' + ('==相等==，根匹配' if S.now.val == S.voyage[S.self.p] else '不等，根都对不上 → 无解')),
        'return [-1]': '无法匹配，返回 `[-1]` 向上传递失败',
        'self.p += 1': '根匹配上了，`p` 后移到 `{self.p}`',
        'if not now.left': lambda S, B, r: (f'`{S.now.val}` 没有左孩子' + ('，也没有右孩子 → 叶子' if not S.now.right else '，只有右孩子（不存在翻转）') if not S.now.left else f'`{S.now.val}` 有左孩子，再看右孩子'),
        14: lambda S, B, r: ('也没有右孩子 → 叶子，不用翻转' if not S.now.right else '只有右孩子 → 直接递归右孩子'),
        'return []': '叶子：没有任何翻转 → 返回 `[]`',
        'return self.dfs(now.right': '只有一侧孩子，无所谓翻转，直接递归并返回其结果',
        18: lambda S, B, r: ('没有右孩子，只有左孩子 → 直接递归左孩子' if not S.now.right else '左右都有，继续判断是否需要翻转'),
        'return self.dfs(now.left': '只有一侧孩子，无所谓翻转，直接递归并返回其结果',
        'elif now.left.val != voyage[self.p]': lambda S, B, r: (f'`now.left.val = {S.now.left.val}`，`voyage[{S.self.p}] = {S.voyage[S.self.p]}` → ' + ('==不等==：左子树不能先走，必须==翻转==（先右后左）' if S.now.left.val != S.voyage[S.self.p] else '相等：按原样先左后右，不能翻转（节点值互不相同）')),
        'left_ret = self.dfs(now.right': '翻转了：先递归==右子树==（它排在 voyage 前面）',
        'right_ret = self.dfs(now.left': '再递归左子树',
        'left_ret = self.dfs(now.left': '不翻转：先递归左子树',
        'right_ret = self.dfs(now.right': '再递归右子树',
        'if left_ret == [-1]': lambda S, B, r: ('第一棵子树匹配失败 → 整体失败，返回 `[-1]`' if S.left_ret == [-1] else f'第一棵子树成功，翻转的节点为 `{S.left_ret}`'),
        'if right_ret == [-1]': lambda S, B, r: ('第二棵子树匹配失败 → 整体失败，返回 `[-1]`' if S.right_ret == [-1] else f'第二棵子树成功，翻转的节点为 `{S.right_ret}`'),
        'return [now.val] + left_ret': '翻转了 `{now.val}`：结果 = `[{now.val}]` + 右子树结果 + 左子树结果 = `{ret}`',
        'return left_ret + right_ret': '没翻转：结果 = 左子树结果 + 右子树结果 = `{ret}`',
    },
    skip=[],
    cards=dict(
        one_liner='先序 dfs，左孩子对不上 voyage 就翻转它的两个孩子',
        complexity='时间 `O(n)`，空间 `O(h)`',
        problem=['二叉树节点值互不相同，给一个目标先序序列 `voyage`',
                 '可以翻转任意节点的左右孩子，使先序遍历恰好等于 `voyage`',
                 '返回被翻转的节点值列表；做不到返回 `[-1]`',
                 '本视频：`root = [1,2,3,4,5]`，`voyage = [1,3,2,5,4]` → `[1,2]`'],
        quote='若now有两侧的孩子，且此时now左孩子的值不等于voyage[p]，说明如果不进行翻转，左子树是无法匹配先序遍历的，因此必须进行翻转。',
        quote_src='—— yiduobo 题解原文',
        idea=['`self.p` 指向 voyage 里下一个要匹配的位置，访问一个节点就 `p += 1`',
              '节点值互不相同：左孩子 ≠ `voyage[p]` 时，==只有翻转这一条路==',
              '翻转时先递归右子树再左子树，并把当前节点记入答案'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '易错点：==只有一侧孩子时没有翻转这一说==，直接递归',
                 '失败用 `[-1]` 向上传递，每层都要检查，不能漏',
                 '原文本来就是 Python 3 可跑的写法，未做修改'],
    ),
)
