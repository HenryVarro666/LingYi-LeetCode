DONE = {}   # 节点 _uid -> (链长, 是否含 start)，在字幕回调里记录


def _rec(fn, ret_is_pair=True):
    def cap(S, B, ret):
        n = S.get('node')
        if n is not None and ret_is_pair and isinstance(ret, tuple):
            DONE[n._uid] = ret
        for m in _walk(S.get('root')):
            m._d = DONE.get(m._uid)
        return fn(S, B, ret) if callable(fn) else fn
    return cap


def _walk(root):
    out, st, seen = [], [root], set()
    while st:
        n = st.pop()
        if n is None or n._uid in seen:
            continue
        seen.add(n._uid)
        out.append(n)
        st += [n.left, n.right]
    return out


def _color(S, n):
    d = getattr(n, '_d', None)
    if n.val == 3:
        return 'yellow'
    if d is not None and d[1]:
        return 'orange'
    if d is not None:
        return 'green'
    return None


def _cap_ret_start(S, B, ret):
    return f'`{S.node.val}` 就是 `start`：以它为根往下最深 `max({S.l_len}, {S.r_len}) = {S.ans}` 就是一个候选答案，返回 `1, True` 告诉父亲「我这棵子树含 start」'


def _cap_ret_up(S, B, ret):
    return f'左右有一边含 `start`：沿含 start 的那条链继续往上，链长 `{ret[0]}`（含 start 一侧的长度 + 1）'


def _cap_ret_plain(S, B, ret):
    return f'这棵子树不含 `start`：返回最深链 `max({S.l_len}, {S.r_len}) + 1 = {ret[0]}`，标记 `False`'


def _cap_upd(S, B, ret):
    return (f'start 在一侧：左链 `{S.l_len}` + 右链 `{S.r_len}` = `{S.l_len + S.r_len}`，'
            f'这条以 start 为端点的路径从 start 往上拐弯再往下 → `ans = {S.ans}`')


def _cap_call_l(S, B, ret):
    n = S.get('node')
    return '进入左儿子' if n is not None else '左儿子为空，回到上层'


CONFIG = dict(
    num=2385, title='感染二叉树需要的总时间', difficulty='Medium',
    category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='树的直径 · 端点固定为 start',
    tags=['动态规划', '链表树与回溯', '难度分 1711'],
    code='''
class Solution:
    def amountOfTime(self, root: Optional[TreeNode], start: int) -> int:
        ans = 0
        def dfs(node: Optional[TreeNode]) -> (int, bool):
            if node is None:
                return 0, False
            l_len, l_found = dfs(node.left)
            r_len, r_found = dfs(node.right)
            nonlocal ans
            if node.val == start:
                # 计算子树 start 的最大深度
                # 注意这里和方法一的区别，max 后面没有 +1，所以算出的也是最大深度
                ans = max(l_len, r_len)
                return 1, True  # 找到了 start
            if l_found or r_found:
                # 只有在左子树或右子树包含 start 时，才能更新答案
                ans = max(ans, l_len + r_len)  # 两条链拼成直径
                # 保证 start 是直径端点
                return (l_len if l_found else r_len) + 1, True
            return max(l_len, r_len) + 1, False
        dfs(root)
        return ans
''',
    call='Solution().amountOfTime(Tr([1,5,3,None,4,10,6,9,2]), 3)',
    expect=4,
    views=[
        dict(type='tree', label='二叉树（黄 = start，橙 = 含 start 的子树，绿 = 不含）', pointers={'node': 'blue'}, h=330, color=_color),
        dict(type='text', fn=lambda S: f"当前答案 `ans = {S.get('ans', 0)}`", size=26, h=50),
        dict(type='calls', h=210),
    ],
    watch=[('node', lambda S: S['_inner'].get('node').val if S['_inner'].get('node') else None, 'blue'),
           ('l_len', lambda S: S['_inner'].get('l_len')), ('r_len', lambda S: S['_inner'].get('r_len')),
           ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 记录答案：==从 start 出发能走到的最远距离==',
        'return 0, False': '空节点 → 返回 `0, False`：长度 0，没有 start',
        'l_len, l_found = dfs': '先递归左子树，==相信它==会返回（最大链长, 是否含 start）',
        'r_len, r_found = dfs': '左边的结果拿到了，再递归右子树，同样只关心它返回的两个值',
        'if node.val == start': lambda S, B, r: (f'`{S.node.val} == {S.start}` → ==找到 start=='  if S.node.val == S.start else f'`{S.node.val}` 不是 start（`{S.start}`）'),
        'ans = max(l_len': _cap_ret_start,
        'return 1, True': _rec('start 的链长记为 `1`（自己），标记 `True`，让祖先知道 start 在这边'),
        'if l_found or r_found': lambda S, B, r: ('start 在 `' + str(S.node.val) + '` 的' + ('左' if S.l_found else '右') + '子树里 → 这里可能是「拐弯点」') if (S.l_found or S.r_found) else f'`{S.node.val}` 的两边都没有 start → 只需要往上传递最深链',
        'ans = max(ans': _cap_upd,
        'return (l_len': _rec(_cap_ret_up),
        'return max(l_len': _rec(_cap_ret_plain),
        'dfs(root)': '从根开始递归，整棵树只走一遍',
        'return ans': '`ans` 就是 start 到最远节点的距离，也就是感染需要的分钟数',
    },
    skip=['nonlocal ans', 'if node is None', 'dfs(root)'],
    max_steps=110,
    cards=dict(
        one_liner='把「感染时间」看成：端点固定为 start 的最长路径',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二叉树节点值互不相同，第 `0` 分钟从 `start` 开始感染',
                 '每分钟感染所有与已感染节点相邻的节点',
                 '示例：`root = [1,5,3,null,4,10,6,9,2]`，`start = 3` → `4`'],
        quote='设 $v$ 是离 start 最远的节点，返回 start 到 v 的距离。',
        quote_src='—— 灵茶山艾府题解「题意」',
        idea=['答案 = start 到最远点的距离，分两种：往下走（start 子树深度）、往上走再拐弯往下',
              '递归多返回一个布尔值：这棵子树是否含 `start`',
              '含 start 时，用 `l_len + r_len` 更新答案：两条链拼成端点为 start 的「直径」'],
        result='运行结束，返回 `4`：`3 → 1 → 5 → 4 → 9`（或 `2`）',
        summary=['时间 `O(n)`，空间 `O(n)`（最坏退化成链的递归栈）',
                 '易错：start 自身返回 `1, True`，而它的答案是 `max(l_len, r_len)`，不加 1',
                 '只在含 start 的节点上更新 `ans`，这样 `l_len + r_len` 一定是 start 为端点',
                 '方法一：先记录父节点，再从 start 往左、右、父三个方向 DFS；另一种写法用负数代替布尔值'],
    ),
)
