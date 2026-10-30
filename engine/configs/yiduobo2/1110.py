VALS = [1, 2, 3, 4, 5, 6, 7]
TO_DEL = [3, 5]


def _res(S):
    return S.get('self.res') or []


def _color(S, n):
    if n.val in TO_DEL:
        return 'red'
    if n._uid in {t._uid for t in _res(S)}:
        return 'green'
    return None


def _forest(res):
    return '，'.join(str(tree_list(t)) for t in res) if res else '（空）'


def _in_del(S, B, ret):
    v = S.now.val
    if v in S.del_set:
        return f'`{v}` 出现在 `to_delete` 中 → 需要被删除'
    return f'`{v}` 不用删除'


def _child(side, word):
    def cap(S, B, ret):
        ch = getattr(B.now, side)
        if ch is None:
            return f'`{B.now.val}` 没有{word}孩子'
        return (f'递归{word}孩子 `{ch.val}`，配套的 `new_root_flag = del_flag = {B.del_flag}`'
                + ('：==父亲被删，它可能成为新根==' if B.del_flag else '：父亲还在，它不会是新根'))
    return cap


def _root_if(S, B, ret):
    v, d, f = S.now.val, S.del_flag, S.new_root_flag
    if not d and f:
        return f'`{v}` 没被删，且' + ('它是整棵树的根' if v == VALS[0] else '父亲被删了') + ' → ==是森林中一棵树的根=='
    if d:
        return f'`{v}` 自己要被删，不是树根'
    return f'`{v}` 的父亲还在 → 只是普通节点'


CONFIG = dict(
    num=1110, title='删点成林', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='先序 DFS · 携带 new_root_flag',
    tags=['字节30天'],
    code='''
class Solution(object):
    def delNodes(self, root, to_delete):
        del_set = set(to_delete)
        self.res = []
        self.dfs(root, del_set, True)
        return self.res

    def dfs(self, now, del_set, new_root_flag):
        if now.val in del_set:
            del_flag = True
        else:
            del_flag = False

        if now.left and self.dfs(now.left, del_set, del_flag):
            now.left = None
        if now.right and self.dfs(now.right, del_set, del_flag):
            now.right = None

        if not del_flag and new_root_flag:
            self.res.append(now)

        return del_flag
''',
    call=f'Solution().delNodes(Tr({VALS}), {TO_DEL})',
    result_fn=lambda a: [tree_list(t) for t in a],
    expect=[[6], [7], [1, 2, None, 4]],
    views=[
        dict(type='text', fn=lambda S: f"`res` = {_forest(_res(S))}" if 'self.res' in S else '', h=56),
        dict(type='tree', h=400, pointers={'now': 'blue'}, color=_color,
             label='树 / 森林（红 = 要删除，绿 = 已加入 res 的树根）'),
        dict(type='calls', h=200, hide=('del_set',), label='调用栈（del_set 参数省略）'),
    ],
    watch=[('now', 'now', 'blue'), ('new_root_flag', 'new_root_flag', 'yellow'), ('del_flag', 'del_flag', 'red'),
           ('res', lambda S: [t.val for t in _res(S)] if 'self.res' in S else None, 'green')],
    captions={
        'del_set = set(to_delete)': '`del_set`：要删除的点，`O(1)` 查询',
        'self.res = []': '`self.res` 收集森林中每棵树的根',
        'self.dfs(root, del_set, True)': '从根开始 dfs：根节点的 `new_root_flag = True`（它没被删就一定是树根）',
        'if now.val in del_set': _in_del,
        'del_flag = True': '用 `del_flag = True` 记录下来',
        'del_flag = False': '`del_flag = False`',
        'if now.left and self.dfs': _child('left', '左'),
        'now.left = None': lambda S, B, r: f'左孩子 `{B.now.left.val}` 被删除了 → `now.left = None`',
        'if now.right and self.dfs': _child('right', '右'),
        'now.right = None': lambda S, B, r: f'右孩子 `{B.now.right.val}` 被删除了 → `now.right = None`',
        'if not del_flag and new_root_flag': _root_if,
        'self.res.append(now)': lambda S, B, r: f'把 `{S.now.val}` 加入答案',
        'return del_flag': lambda S, B, r: ('整棵树的根处理完毕' if S.now.val == VALS[0] else
                                            f'返回 `del_flag = {r}`：' + ('==让父亲把这一侧的孩子置空==' if r else '父亲不用动这一侧')),
        'return self.res': lambda S, B, r: f'返回森林 {_forest(r)}',
    },
    cards=dict(
        one_liner='树根要么是整棵树的根，要么父亲被删了：往下传一个标记',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['二叉树每个节点值都不同；删去值在 `to_delete` 里的节点，得到一个森林',
                 '返回森林中每棵树的根（顺序任意）',
                 '示例：`root = [1,2,3,4,5,6,7], to_delete = [3,5]`',
                 '→ `[[1,2,null,4],[6],[7]]`'],
        quote='树的根节点必然不能是to_delete当中的点。接下来，==树的根节点要么是整棵树的根节点，要么其父亲节点被删除了==。',
        quote_src='—— yiduobo 题解',
        idea=['dfs 时携带 `new_root_flag`：当前节点是否需要作为树根（= 父亲的 `del_flag`）',
              '没被删且 `new_root_flag` 为真 → 加入答案',
              '返回 `del_flag`，让父亲判断要不要把这一侧的孩子置空'],
        result='返回 `[[6],[7],[1,2,null,4]]` ✓（顺序任意）',
        summary=['时间 `O(n + m)`：每个节点访问一次；空间：递归栈 + 集合',
                 '父→子传 `new_root_flag`，子→父传 `del_flag`，两个方向的信息各走一次',
                 '易错：孩子被删后要把 `now.left / now.right` 置空，否则森林里还连着被删的点',
                 '对比灵神：灵神用后序遍历的返回值直接替换儿子，不需要额外标记',
                 '原文为 Python 2 风格，只删去了文档字符串和节点定义注释'],
    ),
)
