def _inf(S):
    if 'now' not in S:
        return '平均值 = 子树节点值之和 ÷ 节点数；找最大的那棵'
    return '后序：先拿到左右子树的（和，个数），再算自己的平均'


CONFIG = dict(
    num=1120, title='子树的最大平均值', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='后序 dfs · 返回(和, 个数)',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def maximumAverageSubtree(self, root):

        global res
        res = 0

        def dfs(now):
            s = now.val
            cnt = 1

            if now.left:
                left_s, left_cnt = dfs(now.left)
                s += left_s
                cnt += left_cnt

            if now.right:
                right_s, right_cnt = dfs(now.right)
                s += right_s
                cnt += right_cnt

            global res
            res = max(res, s * 1.0 / cnt)
            return s, cnt

        dfs(root)
        return res
''',
    call='Solution().maximumAverageSubtree(Tr([5,6,1,None,None,3,2]))',
    expect=6.0,
    views=[
        dict(type='text', fn=_inf, size=26, h=60),
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=320),
        dict(type='text', fn=lambda S: (f"本层 `s = {S['_inner']['s']}`，`cnt = {S['_inner'].get('cnt')}`" if 's' in S['_inner'] and 'cnt' in S['_inner'] and 'now' in S else ''), size=26, h=60),
        dict(type='calls', h=230),
    ],
    watch=[('now', 'now.val', 'blue'), ('s', lambda S: S['_inner'].get('s'), 'cyan'),
           ('cnt', lambda S: S['_inner'].get('cnt'), 'pink')],
    captions={
        'res = 0': '`res` 记录最大平均值，用 `global` 共享',
        's = now.val': '以 `{now.val}` 为根的子树：和 `s` 先是自己的值 `{s}`',
        'cnt = 1': '节点数 `cnt` 先算自己 = 1',
        'left_s, left_cnt = dfs': '递归左孩子 `{B.now.left.val}`，返回左子树的（和，个数）',
        's += left_s': '加上左子树：`s = {s}`',
        'cnt += left_cnt': '`cnt = {cnt}`',
        'right_s, right_cnt = dfs': '递归右孩子 `{B.now.right.val}`，返回右子树的（和，个数）',
        's += right_s': '加上右子树：`s = {s}`',
        'cnt += right_cnt': '`cnt = {cnt}`',
        'res = max': '本子树平均 `{s} / {cnt}` = =={s * 1.0 / cnt:.2f}==，用它去更新最大值 `res`',
        'return s, cnt': '把（和，个数）`({s}, {cnt})` 交给父节点，让它求自己的平均',
        'dfs(root)': '从根开始后序 dfs',
        'return res': '最大平均值 `{ret}`',
    },
    skip=['global res'],
    cards=dict(
        one_liner='每棵子树返回（和，个数），当场算平均更新答案',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['给一棵二叉树，子树指某节点及其==全部后代==',
                 '子树的平均值 = 节点值之和 ÷ 节点个数，求最大平均值',
                 '本视频：`root = [5,6,1,null,null,3,2]` → `6.0`（叶子 6 自己）'],
        quote='子树中所有节点值之和等于根节点的值加上左右子树中所有节点值之和，而子树中的节点数量则等于左右子树的节点数量之和再加上一。',
        quote_src='—— yiduobo 题解原文',
        idea=['`s` 从 `now.val` 起，`cnt` 从 1 起',
              '有孩子就递归，把孩子的（和，个数）累加进来',
              '算出 `s / cnt` 更新 `res`，再把（和，个数）返回给父亲'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '易错：不能只比较平均值再往上传，上层要的是（和，个数）而不是平均值',
                 '`s * 1.0 / cnt` 保证是浮点除法',
                 '原文已是 Python 3 可运行写法（`s * 1.0 / cnt` 本就是浮点除），无需修改'],
    ),
)
