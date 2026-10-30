def _v(n):
    return '空' if n is None else str(n.val)


CONFIG = dict(
    num=513, title='找树左下角的值', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='DFS 比较左右子树深度',
    tags=[],
    code='''
class Solution(object):
    def findBottomLeftValue(self, root):

        return self.dfs(root, 1)[0]

    def dfs(self, now, depth):
        if not now.left:
            if not now.right:
                return now.val, depth
            else:
                return self.dfs(now.right, depth + 1)
        else:
            if not now.right:
                return self.dfs(now.left, depth + 1)
            else:
                left_val, left_depth = self.dfs(now.left, depth + 1)
                right_val, right_depth = self.dfs(now.right, depth + 1)
                if left_depth >= right_depth:
                    return left_val, left_depth
                else:
                    return right_val, right_depth
''',
    call='Solution().findBottomLeftValue(Tr([1,2,3,4,None,5,6,None,None,7]))',
    expect=7,
    views=[
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=320),
        dict(type='calls', h=240),
    ],
    watch=[('now', lambda S: S['_inner']['now'].val if S['_inner'].get('now') else None, 'blue'),
           ('depth', lambda S: S['_inner'].get('depth'), 'yellow'),
           ('left', lambda S: (S['_inner'].get('left_val'), S['_inner'].get('left_depth')) if 'left_depth' in S['_inner'] else None),
           ('right', lambda S: (S['_inner'].get('right_val'), S['_inner'].get('right_depth')) if 'right_depth' in S['_inner'] else None)],
    captions={
        'return left_val, left_depth': '左子树不浅于右子树，答案在左→ 返回 `({left_val}, {left_depth})`',
        'return right_val, right_depth': '右子树严格更深，答案在右子树 → 返回 `({right_val}, {right_depth})`',
        'return self.dfs(root, 1)[0]': '从根出发，深度记为 `1`；`dfs` 返回 `(左下角的值, 它的深度)`，只取值',
        'if not now.left:': lambda S, B, r: (f'`{S.now.val}` 没有左儿子' if not S.now.left else f'`{S.now.val}` 有左儿子 `{S.now.left.val}`'),
        'if not now.right:': lambda S, B, r: (f'`{S.now.val}` 没有右儿子' if not S.now.right else f'`{S.now.val}` 有右儿子 `{S.now.right.val}`'),
        'return now.val, depth': '左右都没有 → ==叶子就是自己子树的左下角==：返回 `({now.val}, {depth})`',
        'return self.dfs(now.right, depth + 1)': '只有右孩子 → 左下角必在右子树里，深度 +1 递归',
        'return self.dfs(now.left, depth + 1)': '只有左孩子 → 左下角必在左子树里，深度 +1 递归',
        'left_val, left_depth = self': lambda S, B, r: ('先递归左子树，求它的 `(左下角值, 深度)`，深度从 `depth + 1` 起算' if 'left_val' not in S['_inner'] else f'左子树返回 `(值, 深度)` = `({S.left_val}, {S.left_depth})`'),
        'right_val, right_depth = self': lambda S, B, r: ('再递归右子树，同样求 `(值, 深度)`' if 'right_val' not in S['_inner'] else f'右子树返回 `(值, 深度)` = `({S.right_val}, {S.right_depth})`'),
        'if left_depth >= right_depth': lambda S, B, r: f'比深度：`{S.left_depth} >= {S.right_depth}` → ' + ('左子树不浅于右子树，选左' if S.left_depth >= S.right_depth else '右子树更深，选右'),
    },
    cards=dict(
        one_liner='左右子树比深度：左不浅于右就取左，否则取右',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈，h 为树高）',
        problem=['给定二叉树根节点 `root`，找出==最底层最左边==节点的值',
                 '示例：`[1,2,3,4,null,5,6,null,null,7]` → `7`'],
        quote='若root同时具有左孩子和右孩子，那么对比左子树和右子树的深度。若左子树的深度大于等于右子树的深度，那么左下角节点必然位于左子树中，否则位于右子树中。',
        quote_src='—— yiduobo 题解原文',
        idea=['原文分三种情况：叶子、只有一个孩子、两个孩子都有',
              '只有一个孩子 → 答案在那一侧；叶子 → 就是自己',
              '两个孩子 → 各自求 `(值, 深度)`，==深度更大的一侧==胜出，相等取左',
              '`dfs` 一路带着深度，返回时把「值 + 深度」一起交给父节点比较'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '易错：深度相等时必须取左（`>=`），否则会选到右边的同层节点',
                 '易错：只有一个孩子时不用比较，直接递归那一侧',
                 '对比灵神：灵神用 BFS 先右后左，最后出队的就是答案；这里是 DFS 比深度'],
    ),
)
