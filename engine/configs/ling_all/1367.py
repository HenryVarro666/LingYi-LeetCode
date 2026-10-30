def _nv(x):
    return '空' if x is None else str(x.val)


def _info(S):
    I = S.get('_inner', {})
    if 's' not in I:
        return ''
    s, t = I['s'], I['t']
    mode = '==重新开始匹配==（s 是链表头）' if s is S.get('head') else f'匹配中（已匹配到链表第 {_depth(S, s)} 个）'
    return f"链表节点 `s = {_nv(s)}`，树节点 `t = {_nv(t)}`：{mode}"


def _depth(S, s):
    d, x = 0, S.get('head')
    while x is not None and x is not s:
        x, d = x.next, d + 1
    return d + 1 if x is s else '?'


def _u(x):
    return None if x is None else x._uid


def _cap_ret(S, B, ret):
    calling = _u(S.s) != _u(B.s) or _u(S.t) != _u(B.t)
    if calling:
        s, t = B.s, B.t
        nxt = f'进入 `dfs({_nv(S.s)}, {_nv(S.t)})`'
        if s.val == t.val:
            return f'`s.val = {s.val}` == `t.val = {t.val}` → 这一位匹配，==s 走下一个==：{nxt}'
        return nxt
    s, t = S.s, S.t
    if ret is not None:
        return f'这一层 `dfs({_nv(s)}, {_nv(t)})` 返回 =={ret}=='
    if s.val == t.val:
        return f'`s.val = {s.val}` == `t.val = {t.val}` → 匹配，==s 走下一个==，去 `t` 的左右儿子找下一位'
    return f'`s.val = {s.val}` ≠ `t.val = {t.val}` → 这一位不匹配，看看 `s is head` 能否重启'


def _cap_restart(S, B, ret):
    calling = _u(S.s) != _u(B.s) or _u(S.t) != _u(B.t)
    if calling:
        return f'`s is head` 成立 → 从 `head` 重新匹配：进入 `dfs(head, {_nv(S.t)})`'
    if ret is not None:
        return f'这一层返回 =={ret}=='
    return f'`s = {_nv(S.s)}` 不是链表头 → ==不重启==（否则会指数级重复），这一层失败'


CONFIG = dict(
    num=1367, title='二叉树中的链表', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='合并两个递归 · s is head 重启',
    tags=['二叉树', '链表', '难度分 1650'],
    code='''
class Solution:
    def isSubPath(self, head: ListNode, root: TreeNode) -> bool:
        def dfs(s: Optional[ListNode], t: Optional[TreeNode]) -> bool:
            if s is None:  # 整个链表匹配完毕
                return True
            # 否则需要继续匹配
            if t is None:  # 无法继续匹配
                return False
            # 节点值相同则继续匹配，否则从 head 开始重新匹配
            return s.val == t.val and (dfs(s.next, t.left) or dfs(s.next, t.right)) or \\
                   s is head and (dfs(head, t.left) or dfs(head, t.right))
        return dfs(head, root)
''',
    call='Solution().isSubPath(L([4,2,8]), Tr([1,4,4,2,None,None,2,None,None,None,8]))',
    expect=True,
    views=[
        dict(type='text', fn=_info, size=24, h=46),
        dict(type='tree', label='二叉树（蓝 = t）', pointers={'t': 'blue'}, path=False, h=230),
        dict(type='linked', label='链表（蓝 = s，粉 = head）', pointers={'s': 'blue', 'head': 'pink'}, h=150),
        dict(type='calls', h=210, hide=('head', 'root')),
    ],
    watch=[('s', lambda S: S['_inner']['s'].val if S['_inner'].get('s') is not None else '空', 'blue'),
           ('t', lambda S: S['_inner']['t'].val if S['_inner'].get('t') is not None else '空', 'pink')],
    skip=['if s is None', 'if t is None'],
    max_steps=80,
    captions={
        'return True': '`s` 是空：整个链表匹配完毕 → 找到了一条向下的路径，返回 `True`',
        'return False': '`t` 是空：树上没有节点了，链表还没匹配完 → 返回 `False`，回溯',
        'return s.val == t.val': _cap_ret,
        's is head and': _cap_restart,
        'return dfs(head, root)': '从链表头 `head` 和树根 `root` 开始：每个树节点都可能是路径的起点',
    },
    cards=dict(
        one_liner='官解两个递归合成一个：`s is head` 时才允许重启匹配',
        complexity='时间 `O(m^2)`，空间 `O(m)`（m 为树的节点数）',
        problem=['给你二叉树根 `root` 和链表头 `head`',
                 '树里是否存在一条==一直向下==的路径，节点值与链表逐个对应？',
                 '本视频：`head = [4,2,8]`，`root = [1,4,4,2,null,null,2,null,null,null,8]` → `True`'],
        quote='如果 `s == head`，则对应着官解的 `isSubPath` 递归函数；如果 `s != head`，则对应着官解的 `dfs` 递归函数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(s, t)`：链表节点 `s` 与树节点 `t` 配对。`s` 空 → 成功；`t` 空 → 失败',
              '值相同：`s.next` 去匹配 `t` 的左右儿子',
              '值不同：只有 `s is head` 才从 `head` 重新匹配 `t` 的左右儿子',
              '不加 `s is head`，匹配到一半失败的节点都会重启，递归会指数级重复'],
        summary=['时间 `O(m^2)`，空间 `O(m)`：每个树节点作为起点最多访问其子树各一次',
                 '易错：重启只能在 `s is head` 时发生，否则指数爆炸',
                 '另一写法（方法二）：滚动哈希，复杂度 `O(n+m)`；KMP 在树上无法均摊成线性',
                 '本视频用方法一（暴力匹配）演示'],
    ),
)
