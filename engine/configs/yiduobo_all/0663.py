def _inf(S):
    if 'now' not in S:
        return '删一条边 → 切出一棵子树；看是否存在子树和 ==等于整树和的一半=='
    return f"已记录的子树和 `sum_set = {sorted(S['sum_set'])}`" if 'sum_set' in S else ''


CONFIG = dict(
    num=663, title='均匀树划分', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='后序 dfs · 哈希集合记子树和',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def checkEqualTree(self, root):

        sum_set = set()

        def dfs(now):
            s = now.val
            if now.left:
                s += dfs(now.left)
            if now.right:
                s += dfs(now.right)

            if now != root:
                sum_set.add(s)
            return s

        tot_s = dfs(root)
        return tot_s % 2 == 0 and tot_s // 2 in sum_set
''',
    call='Solution().checkEqualTree(Tr([5,10,10,None,None,2,3]))',
    expect=True,
    views=[
        dict(type='text', fn=_inf, size=26, h=60),
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=300),
        dict(type='set', var='sum_set', label='sum_set（非根子树的和）', fmt=lambda x: str(x), h=110),
        dict(type='calls', h=210),
    ],
    watch=[('now', 'now.val', 'blue'), ('s', lambda S: S['_inner'].get('s'), 'cyan'), ('tot_s', lambda S: S.get('tot_s'), 'yellow')],
    captions={
        'sum_set = set()': '`sum_set` 记下所有出现过的子树和（根的和不记）',
        's = now.val': '`s` 从自己的值 `{now.val}` 开始，等着加上左右子树和',
        's += dfs(now.left)': '递归左孩子 `{B.now.left.val}`，它返回的左子树之和累加进 `s`',
        's += dfs(now.right)': '递归右孩子 `{B.now.right.val}`，它返回的右子树之和累加进 `s`',
        'if now != root': lambda S, B, r: (f'`{S.now.val}` 不是根 → 删掉它和父亲的边就切出这棵子树，值得记录' if S.now != S.root
                                           else '这是根：它的和是整树和，==不能记==（删边要切出另一端的孩子）'),
        'sum_set.add': '子树和 `{s}` 记入集合 → `{sorted(sum_set)}`',
        'return s': '整棵子树和 `{s}` 交给父节点',
        'tot_s = dfs': '整棵树的和 `tot_s = {tot_s}`',
        'return tot_s % 2': lambda S, B, r: (f'`{S.tot_s}` 是偶数，一半 `{S.tot_s // 2}` ' + ('在集合里' if S.tot_s // 2 in S.sum_set else '不在集合里')
                                             + f' → ==返回 {r}==') if S.tot_s % 2 == 0 else f'`{S.tot_s}` 是奇数，不可能平分 → ==返回 False==',
    },
    cards=dict(
        one_liner='删边 = 切下一棵子树，找和为整树一半的子树',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给一棵二叉树，问能否==删掉一条边==，使得分成的两棵树节点值之和相等',
                 '本视频：`root = [5,10,10,null,null,2,3]`',
                 '整树和 `30`，删去根与右孩子的边，右边 `10+2+3 = 15` → `true`'],
        quote='问题就可以转化为给出一棵树，问是否存在某个子树的节点之和恰好等于整棵树节点之和的一半。需要特别注意的是，这颗子树的根节点不能是原树的根节点',
        quote_src='—— yiduobo 题解原文',
        idea=['删掉的边连着父子，孩子那一端剩下一棵完整子树',
              '后序 dfs 求每棵子树的和，==非根==的和都记进哈希集合',
              '最后：总和为偶数且「总和的一半」在集合里就成立'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：把根的和也记进去，总和为 0 的树会误判（如只有 `[0]`）',
                 '总和是奇数必定不行，要先判偶数',
                 '原文为 Python 2 写法，`tot_s / 2` 已改为整数除法 `tot_s // 2`'],
    ),
)
