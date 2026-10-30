DONE = {}


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


def _rec(fn, record=False):
    def cap(S, B, ret):
        n = S.get('node')
        if record and n is not None:
            DONE[n._uid] = ret
        for m in _walk(S.get('self.tree')):
            m._d = DONE.get(m._uid)
        return fn(S, B, ret) if callable(fn) else fn
    return cap


import re as _re


def _fmt(t):
    def f(S, B, r):
        env = {'B': B, 'ret': r, 'sorted': sorted, 'len': len, 'max': max, 'min': min}
        return _re.sub(r'\{([^{}]+)\}', lambda m: str(eval(m.group(1), env, S)), t)
    return f


def _wrap(d):
    return {k: _rec(v if callable(v) else _fmt(v)) for k, v in d.items()}


def _st(n):
    d = getattr(n, '_d', None)
    return None if d is None else ('green' if d >= 0 else 'red')


def _cap_l(S, B, ret):
    if S.node is None:
        return '空节点直接返回 `-1`：比叶子（高度 0）还小一级'
    return f'先递归左子树 `dfs({S.node.val})`：==相信它返回左子树高度==，不合法则返回 `-2`'


def _cap_r(S, B, ret):
    return f'左边拿到 `left_h = {B.left_h}`，再递归右子树'


def _cap_if(S, B, ret):
    n = S.node
    if S.left_h == -2 or S.left_h != S.right_h:
        return f'节点 `{n.val}`：左 `{S.left_h}`，右 `{S.right_h}` → ==不合法==（有子树不完美或高度不等）'
    return f'节点 `{n.val}`：左右高度都是 `{S.left_h}` → 以它为根的子树是==完美二叉树=='


def _info(S):
    c = S.get('cnt')
    if c is None:
        return ''
    s = '  '.join(f'{i+1}层×{x}' for i, x in enumerate(c) if x)
    return f'已发现的完美子树：{s or "暂无"}'


CONFIG = dict(
    num=3319, title='第 K 大的完美二叉子树的大小', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='后序 DFS + 计数排序',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1603'],
    code='''
class Solution:
    def kthLargestPerfectSubtree(self, root: Optional[TreeNode], k: int) -> int:
        cnt = [0] * 10
        def dfs(node: Optional[TreeNode]) -> int:
            if node is None:
                return -1
            left_h = dfs(node.left)
            right_h = dfs(node.right)
            if left_h == -2 or left_h != right_h:
                return -2  # 不合法
            cnt[left_h + 1] += 1
            return left_h + 1
        dfs(root)

        for i in range(len(cnt) - 1, -1, -1):
            c = cnt[i]
            if c >= k:
                return (1 << (i + 1)) - 1
            k -= c
        return -1
''',
    call='''s = Solution()
s.tree = Tr([1,2,3,4,5,6,7,8,9])
s.kthLargestPerfectSubtree(s.tree, 2)''',
    expect=3,
    views=[
        dict(type='tree', label='二叉树（绿 = 完美子树，红 = 不合法）', pointers={'node': 'blue'}, h=330, color=lambda S, n: _st(n)),
        dict(type='array', var='cnt', label='cnt[i]：层数为 i+1 的完美子树个数（大小 2^(i+1)-1）', cell=60, h=135,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='text', fn=_info, size=24, h=50),
        dict(type='calls', h=210, hide=('cnt',)),
    ],
    watch=[('node', lambda S: S['_inner'].get('node').val if S['_inner'].get('node') else None, 'blue'),
           ('left_h', lambda S: S['_inner'].get('left_h')), ('right_h', lambda S: S['_inner'].get('right_h')),
           ('k', 'k', 'yellow')],
    captions=_wrap({
        'cnt = [0]': lambda S, B, r: DONE.clear() or '`cnt[i]` 统计「有 `i+1` 层」的完美子树个数；==叶子的高度记为 0==，充分利用数组',
        'dfs(root)': '从根开始后序 DFS：==先左右、后自己==，高度从下往上传',
        'left_h = dfs': _cap_l,
        'right_h = dfs': _cap_r,
        'if left_h == -2': _cap_if,
        'return -2': _rec('返回 `-2` 表示不合法：==所有祖先也都不可能完美==', True),
        'cnt[left_h + 1] += 1': '发现一棵 `{left_h + 2}` 层的完美子树（大小 `{2**(left_h+2)-1}`）：`cnt[{left_h + 1}] += 1` → `{cnt}`',
        'return left_h + 1': _rec(lambda S, B, r: f'返回高度 `{r}` 给父节点：完美子树只能由==高度相同==的完美子树拼成', True),
        'if c >= k': lambda S, B, r: (f'{S.i+1} 层的有 `{S.c}` 棵：`{S.c} >= {S.k}` → 第 `k` 大就落在这一档，大小 `2^{S.i+1}-1`'
                                      if S.c >= S.k else f'`{S.c} < {S.k}` → 这一档不够，==`k -= c`==，往更小的层数里找'),
        'return (1 << (i + 1)) - 1': '`(1 << {i + 1}) - 1` = =={ret}==：{i+1} 层的完美二叉树有 `2^{i+1}-1` 个节点',
    }),
    skip=['dfs(root)', 'if node is None', 'return -1', 'for i in range', 'c = cnt[i]', 'k -= c'],
    max_steps=90,
    cards=dict(
        one_liner='完美二叉树的大小只看高度：高 h 就是 `2^h - 1`',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['给你二叉树 `root` 和整数 `k`，求第 `k` 大的==完美二叉子树==的节点数',
                 '完美二叉树：所有叶子在同一层，且每个非叶节点恰有两个儿子',
                 '不存在则返回 `-1`',
                 '本视频：`root = [1,2,3,4,5,6,7,8,9]`，`k = 2` → `3`'],
        quote='由于知道高度就知道了子树大小，DFS 只需返回子树高度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['高为 `h` 的完美二叉树每层 `1,2,4,...,2^(h-1)` 个节点，共 `2^h - 1`',
              '后序 DFS：左右高度都合法且相等 → 当前子树完美，高度 +1；否则返回 ==不合法==',
              '写法二用「计数排序」：统计每个高度出现几次，再从大到小数到第 `k` 个'],
        result='返回 `3`：2 层的完美子树有 2 棵，第 2 大的大小就是 `2^2 - 1 = 3`',
        summary=['时间 `O(n)`，空间 `O(n)`；节点数 ≤ 2000，高度不超过 10，所以 `cnt` 开 10 就够',
                 '易错：不合法要用 `-2` 这种==独立的标记==，不能和空节点的 `-1` 混在一起',
                 '写法一把高度放进列表 `hs` 再排序取 `hs[-k]`；写法二用计数代替排序',
                 '同类题：「§2.3 自底向上 DFS」，如 110、543、1339'],
    ),
)
