def _ser(t):
    if t is None:
        return '∅'
    vals = tree_list(t)
    return '[' + ','.join('null' if v is None else str(v) for v in vals) + ']'


def _inner(S, name):
    return S.get('_inner', {}).get(name)


def _range(S):
    i = S.get('_inner', {})
    if 'left' not in i:
        return '分治：区间 `[left, right]` 能组成的所有 BST'
    return f"当前区间 `[{i['left']}, {i['right']}]`" + (f"，枚举根 `root = {i['root']}`" if 'root' in i else '')


def _lists(S):
    i = S.get('_inner', {})
    if 'left_res' not in i:
        return ''
    l = ' '.join(_ser(t) for t in i['left_res'])
    r = ' '.join(_ser(t) for t in i['right_res']) if 'right_res' in i else '…'
    return f"左子树候选 `{l}`　右子树候选 `{r}`"


def _flist(S):
    f = _inner(S, 'f')
    if f is None:
        return ''
    return '本层 `f` = ' + ('`' + '  '.join(_ser(t) for t in f) + '`' if f else '`[]`')


def _ret(S, B, r):
    if r is None:
        return None
    if r == [None]:
        return f'`left = {B.left} > right = {B.right}`：空区间只有一种——==空树==，返回 `[None]`'
    if isinstance(r, list) and r and all(t is None or hasattr(t, 'val') for t in r):
        return f'区间 `[{B.left}, {B.right}]` 共 =={len(r)}== 棵 BST，返回上一层'
    return None


def _draw_f(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    i = S.get('_inner', {})
    f = i.get('f')
    if 'left' not in i:
        return
    if f is None:
        cv.text((x0 + 18, y0 + 4), f"区间 [{i['left']}, {i['right']}] 为空：不建树，直接返回 [None]", 22, T['muted'], bold=True)
        return
    cv.text((x0 + 18, y0 + 4), f"f：区间 [{i['left']}, {i['right']}] 已拼好的树（绿 = 根，黄框 = 这一步新加的）", 22, T['muted'], bold=True)
    if not f:
        return
    n = S.get('n', 3)
    new = S.get('_line') == 21
    k = len(f)
    w = min(240, (x1 - x0 - 40) / max(k, 1))
    top = y0 + 64
    R = 19
    for idx, t in enumerate(f):
        sx = x0 + 20 + idx * w
        if new and idx == k - 1:
            cv.rect((sx + 4, top - 30, sx + w - 4, y1 - 6), outline=T['yellow'], width=3, r=10)
        pos = {}

        def walk(node, d):
            if node is None:
                return
            pos[id(node)] = (sx + (node.val - 0.5) / n * w, top + d * 62, node)
            walk(node.left, d + 1)
            walk(node.right, d + 1)
        walk(t, 0)
        for X, Y, node in pos.values():
            for ch in (node.left, node.right):
                if ch is not None:
                    cx, cy, _ = pos[id(ch)]
                    cv.line([(X, Y), (cx, cy)], T['border'], 3)
        for X, Y, node in pos.values():
            cv.rect((X - R, Y - R, X + R, Y + R), fill=T['green'] if node is t else T['blue'], r=R)
            cv.text((X, Y), node.val, 22, T['bg'], anchor='mm', bold=True)


CONFIG = dict(
    num=95, title='不同的二叉搜索树II', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='分治：枚举根，组合左右子树',
    tags=['labuladong'],
    code='''
class Solution(object):
    def generateTrees(self, n):
        if n == 0:
            return []

        return self.dfs(1, n)

    def dfs(self, left, right):
        if left > right:
            return [None]

        f = []
        for root in range(left, right + 1):
            left_res = self.dfs(left, root - 1)
            right_res = self.dfs(root + 1, right)
            for left_tree in left_res:
                for right_tree in right_res:
                    tmp = TreeNode(root)
                    tmp.left = left_tree
                    tmp.right = right_tree
                    f.append(tmp)

        return f
''',
    call='[tree_list(t) for t in Solution().generateTrees(3)]',
    expect=[[1, None, 2, None, 3], [1, None, 3, 2], [2, 1, 3], [3, 1, None, None, 2], [3, 2, None, 1]],
    views=[
        dict(type='text', fn=_range, size=26, h=56),
        dict(type='text', fn=_lists, size=24, h=56),
        dict(type='custom', draw=_draw_f, h=280),
        dict(type='calls', h=200),
    ],
    watch=[('left', lambda S: _inner(S, 'left'), 'blue'), ('right', lambda S: _inner(S, 'right'), 'pink'),
           ('root', lambda S: _inner(S, 'root'), 'orange'),
           ('len(f)', lambda S: len(_inner(S, 'f')) if _inner(S, 'f') is not None else None, 'green')],
    captions={
        'if n == 0': '`n = {n}` ≠ 0',
        'return self.dfs(1, n)': '`dfs(1, {n})` 返回全部 =={len(ret)}== 棵树',
        'return [None]': lambda S, B, r: f'`[{S.left}, {S.right}]` 是空区间：只有一种——==空树==，返回 `[None]`',
        'left_res = self.dfs': '枚举根 =={root}==：先递归左子树区间 `[{left}, {right}]`',
        'right_res = self.dfs': '左子树有 =={len(left_res)}== 种；再递归右子树 `[{root + 1}, {right}]`',
        'f.append(tmp)': lambda S, B, r: f'根 `{S.root}` + 左 `{_ser(S.left_tree)}` + 右 `{_ser(S.right_tree)}` → `{_ser(S.tmp)}` 放进 `f`',
        'return f': '区间 `[{left}, {right}]` 共 =={len(f)}== 棵 BST，返回上一层',
    },
    skip=['if left > right', 'f = []', 'for root in range', 'for left_tree in', 'for right_tree in', 'tmp = TreeNode', 'tmp.left =', 'tmp.right ='],
    max_steps=62,
    cards=dict(
        one_liner='枚举根，左右区间分别递归，再把左右子树两两组合',
        complexity='时间、空间均与卡特兰数 `C(n)` 同阶（约 `O(4^n / n^1.5)` 棵树）',
        problem=['给你整数 `n`，生成所有由 `1…n` 为节点值、==互不相同==的二叉搜索树',
                 '可以按任意顺序返回',
                 '示例：`n = 3` → 共 `5` 棵树'],
        quote='对于一颗节点编号为left到right的树，枚举root节点，然后分别用left到root - 1和root + 1到right构造左右子树，最后将所有可能的左右子树与root组合起来即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['BST 的根是 `root`，左子树只能用 `[left, root-1]`，右子树只能用 `[root+1, right]`',
              '`dfs(left, right)` 返回这个区间的所有树；左右两份结果做==笛卡尔积==',
              '空区间返回 `[None]`：空树也是一种选择，才能和另一边组合'],
        result='运行结束：`n = 3` 共 ==5== 棵不同的 BST ✓',
        summary=['树的个数是卡特兰数：`n = 3` 有 5 棵，`n = 8` 有 1430 棵',
                 '==空区间必须返回 `[None]`==，返回 `[]` 会让内层双重循环一次都不跑',
                 '不同的树==共享==子树节点（同一个 `left_tree` 被多次挂上），题目允许',
                 '可以用记忆化缓存 `dfs(left, right)` 的结果',
                 '原文为 Python 2 风格（`class Solution(object)`），代码未改动'],
    ),
)
