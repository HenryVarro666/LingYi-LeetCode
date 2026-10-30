def _is(a, b):
    return a is not None and b is not None and a._uid == b._uid


def _color(S, n):
    if _is(n, S.get('p')):
        return 'green'
    if _is(n, S.get('q')):
        return 'pink'
    return None


def _dim_text(S, B):
    now = S.get('now')
    if now is None or 'p' not in S:
        return ''
    p, q, x = S['p'].val, S['q'].val, now.val
    if x < p and x < q:
        rel = f'`{x}` < `{p}` 且 `{x}` < `{q}` → p、q 都在==右子树=='
    elif x > p and x > q:
        rel = f'`{x}` > `{p}` 且 `{x}` > `{q}` → p、q 都在==左子树=='
    else:
        rel = f'`{min(p, q)}` ≤ `{x}` ≤ `{max(p, q)}` → p、q ==分在两侧==（或 now 就是其中之一）'
    return f'now = `{x}`：{rel}'


def _cap_while(S, B, ret):
    if B.get('now') is not None:
        return f'`now = {B["now"].val}` 不为空，继续判断'
    return '`now` 为空'


def _cap_if1(S, B, ret):
    x, p, q = S.now.val, S.p.val, S.q.val
    if x < p and x < q:
        return f'`{x}` 比 `{p}`、`{q}` 都小 → 两个节点都在 now 的==右边=='
    return f'`{x}` 并不比两个都小 → 不往右走'


def _cap_if2(S, B, ret):
    x, p, q = S.now.val, S.p.val, S.q.val
    if x > p and x > q:
        return f'`{x}` 比 `{p}`、`{q}` 都大 → 两个节点都在 now 的==左边=='
    return f'`{x}` 也不比两个都大 → `{x}` 处在 `{p}` 和 `{q}` ==中间=='


CONFIG = dict(
    num=235, title='二叉搜索树的最近公共祖先', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='利用 BST 有序性 · 从根往下迭代',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def lowestCommonAncestor(self, root, p, q):
        now = root
        while now:
            if now.val < p.val and now.val < q.val:
                now = now.right
            elif now.val > p.val and now.val > q.val:
                now = now.left
            else:
                return now
''',
    call='''root = Tr([6,2,8,0,4,7,9,None,None,3,5])
p = root.left.right.left
q = root.left.right.right
Solution().lowestCommonAncestor(root, p, q)''',
    result_fn=lambda x: x.val,
    expect=4,
    views=[
        dict(type='text', fn=lambda S: (f"p = `{S['p'].val}`（绿）　q = `{S['q'].val}`（粉）　BST：左子树 < 根 < 右子树"
                                        if 'p' in S else ''), size=26, h=60),
        dict(type='tree', var='root', h=470, path=False, label='二叉搜索树（蓝箭头 = now）',
             pointers={'now': 'blue'}, color=_color),
        dict(type='text', fn=_dim_text, h=80),
    ],
    watch=[('now', lambda S: S['now'].val if S.get('now') else None, 'blue'),
           ('p.val', lambda S: S['p'].val if 'p' in S else None, 'green'),
           ('q.val', lambda S: S['q'].val if 'q' in S else None, 'pink')],
    captions={
        'now = root': '从根节点 `{now.val}` 开始往下找',
        'while now:': _cap_while,
        'if now.val < p.val': _cap_if1,
        'now = now.right': '往右子树走：`now` → `{now.val}`',
        'elif now.val > p.val': _cap_if2,
        'now = now.left': '往左子树走：`now` → `{now.val}`',
        'return now': 'p 在 now 的一侧、q 在另一侧，再往下就会把它们分开 → now 就是 LCA：返回 =={ret.val}==',
    },
    max_steps=30,
    cards=dict(
        one_liner='从根往下走：两个都小往右，两个都大往左，夹在中间就是答案',
        complexity='时间 `O(h)`（最坏 `O(n)`），空间 `O(1)`',
        problem=['给定一棵==二叉搜索树==和其中两个节点 `p`、`q`，找它们的最近公共祖先',
                 '一个节点也可以是它自己的祖先；所有节点值唯一',
                 '示例：`root = [6,2,8,0,4,7,9,null,null,3,5]`',
                 '`p = 2, q = 8 → 6`；`p = 2, q = 4 → 2`；本视频 `p = 3, q = 5 → 4`'],
        quote='若当前节点now的值==处于节点p和节点q的值的中间==，说明p和q分别位于now的左子树和右子树上，即now就是要求的最近公共祖先。否则的话，p和q位于now的同一侧，那么将now迭代到对应的子树',
        quote_src='—— yiduobo 知乎题解',
        idea=['一般树的 LCA 要转成 RMQ 或用 Tarjan；这里只问一组、且是 BST，可以优化',
              'BST 有序：`now.val` 比两个都小 → 都在右边；比两个都大 → 都在左边',
              '否则 p、q 分在两侧（或 now 就是其中之一），now 就是最近公共祖先',
              '只往下走一条路，用 `while` 迭代，不需要递归栈'],
        summary=['时间 `O(h)`，最坏退化成链 `O(n)`；空间 `O(1)`',
                 '易错：比较用严格的 `<` / `>`，等于 p 或 q 时要停下（节点可以是自己的祖先）',
                 '对比 236（普通二叉树）：没有大小关系，只能递归或记父节点',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串和注释掉的 TreeNode 定义，代码未改'],
    ),
)
