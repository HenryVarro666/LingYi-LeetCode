import sys as _sys

# 两棵输入树（按“位置”记录：'' = 根，'L' = 左儿子，'LR' = 左儿子的右儿子 ……）
T1 = {'': 1, 'L': 3, 'R': 2, 'LL': 5}
T2 = {'': 2, 'L': 1, 'R': 3, 'LR': 4, 'RR': 7}
MERGED = {p: T1.get(p, 0) + T2.get(p, 0) for p in set(T1) | set(T2)}
FN, LLINE, RLINE = 'mergeTrees', 6, 7      # 递归函数名、递归左子树 / 右子树所在行


def _up(name, test, depth=16):
    # 取调用栈上层的局部变量（custom 视图只拿到合并后的 S；这里取完整帧列表与全部关键帧）
    f = _sys._getframe(2)
    for _ in range(depth):
        if f is None:
            return None
        v = f.f_locals.get(name)
        if v is not None and test(v):
            return v
        f = f.f_back
    return None


def _positions(frames):
    """调用栈 → 每一层递归对应的位置：上一层停在左递归行就是 'L'，停在右递归行就是 'R'"""
    rec = [f for f in frames if f['name'] == FN]
    out, p = [], ''
    for fr in rec:
        out.append(p)
        p += 'L' if fr['line'] == LLINE else 'R'
    return out, rec


_cache = {}


def _history():
    vid = _up('self', lambda x: hasattr(x, 'keys') and hasattr(x, 'draw_viz'))
    if vid is None:
        return []
    if _cache.get(id(vid), (None,))[0] is not vid:  # 存下 vid 本身，避免对象 id 被复用后拿到旧缓存
        order, seen = [], set()
        for stt, _, _ in vid.keys:
            S_ = stt.get('_S')
            if S_ is None or id(S_) in seen:
                continue
            seen.add(id(S_))
            order.append((id(S_), stt.get('_frames') or []))
        _cache[id(vid)] = (vid, order)
    return _cache[id(vid)][1]


def _status(S):
    st = _up('st', lambda x: isinstance(x, dict) and '_S' in x) or {}
    frames = st.get('_frames') or []
    stack, rec = _positions(frames)
    hist = _history()
    idx = next((i for i, (k, _) in enumerate(hist) if k == id(S)), None)
    entered = set()
    for _, fr in (hist[:idx + 1] if idx is not None else []):
        entered.update(_positions(fr)[0])
    finished = entered - set(stack)
    returning = bool(rec) and frames[-1]['name'] == FN and rec[-1]['line'] == S.get('_line')
    if returning:
        finished.add(stack[-1])
    return stack, finished, returning


def _xy(p, box, dy):
    x0, y0, x1, y1 = box
    f = 0.5
    for i, c in enumerate(p):
        f += (-1 if c == 'L' else 1) * 0.25 / (2 ** i)
    return x0 + f * (x1 - x0), y0 + 62 + len(p) * dy


def _tree(cv, T, vals, box, title, tcolor, stack, cur, shown=None, color=None, rad=24):
    x0, y0, x1, y1 = box
    cv.text((x0 + 14, y0 + 4), title, 22, tcolor, bold=True)
    dy = (y1 - y0 - 62 - rad - 6) / 2
    for p in vals:
        if p and (shown is None or (p in shown and p[:-1] in shown)):
            a, b = _xy(p[:-1], box, dy), _xy(p, box, dy)
            cv.line([a, b], T['border'], 3)
    for p, v in vals.items():
        X, Y = _xy(p, box, dy)
        if shown is not None and p not in shown:
            cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), outline=(52, 58, 66), width=2)
            continue
        fill = color(p) if color else T['panel2']
        oc, w = T['border'], 2
        if p in stack:
            oc, w = T['yellow'], 4
        if p == cur:
            fill = T['blue']
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=oc, width=w)
        cv.text((X, Y), v, 24, T['bg'] if (fill != T['panel2']) else T['text'], anchor='mm', bold=True)
    if cur is not None and shown is None and cur not in vals:
        X, Y = _xy(cur, box, dy)
        cv.dashed((X - rad, Y), (X + rad, Y), T['pink'], 2, 6, 4)
        cv.text((X, Y - rad - 2), '空', 20, T['pink'], anchor='mb', bold=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    stack, finished, returning = _status(S)
    cur = stack[-1] if stack else None
    mid = (x0 + x1) / 2
    hy = y0 + (y1 - y0) * 0.47
    _tree(cv, T, T1, (x0, y0, mid - 10, hy), 'root1', T['orange'], stack, cur)
    _tree(cv, T, T2, (mid + 10, y0, x1, hy), 'root2', T['cyan'], stack, cur)
    cv.line([(x0 + 20, hy + 4), (x1 - 20, hy + 4)], T['border'], 1)
    shown = {p for p in MERGED if any(p[:i] in finished for i in range(len(p) + 1))}

    def col(p):
        if p in T1 and p in T2:
            return T['green']
        return T['orange'] if p in T1 else T['cyan']
    _tree(cv, T, MERGED, (x0 + 100, hy + 8, x1 - 100, y1), '合并结果：「归」时自底向上建', T['green'],
          [], None, shown=shown, color=col)
    cv.text((x1 - 16, hy + 14), '绿 = 两值相加　橙 / 青 = 直接用原来的子树', 18, T['muted'], anchor='ra')


def _cap1(S, B, ret):
    if B.root1 is None:
        return f'`root1` 为空 → 无需合并，直接返回 `root2`' + (f'（子树 `{B.root2.val}`）' if B.root2 else '（也是空）')
    return f'`root1 = {B.root1.val}` 不为空'


def _cap2(S, B, ret):
    if B.root2 is None:
        return f'`root2` 为空 → 无需合并，直接返回 `root1`（子树 `{B.root1.val}`）'
    return f'`root2 = {B.root2.val}` 也不为空 → 两个节点重叠，值相加'


def _cap5(S, B, ret):
    if ret is not None:
        return f'左右子树都合并好了 → 新建节点 `TreeNode({S.root1.val} + {S.root2.val})` = =={ret.val}== 并返回'
    return f'新节点的值 `{S.root1.val} + {S.root2.val} = {S.root1.val + S.root2.val}`；先递归合并左右子树'


CONFIG = dict(
    num=617, title='合并二叉树', difficulty='Easy', category='二叉树',
    author='灵茶山艾府', technique='递归 · 分类讨论（写法一：新建节点）',
    tags=['热题173'],
    code='''
class Solution:
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if root1 is None: return root2
        if root2 is None: return root1
        return TreeNode(root1.val + root2.val,
            self.mergeTrees(root1.left, root2.left),    # 合并左子树
            self.mergeTrees(root1.right, root2.right))  # 合并右子树
''',
    call='Solution().mergeTrees(Tr([1, 3, 2, 5]), Tr([2, 1, 3, None, 4, None, 7]))',
    expect=[3, 4, 5, 5, 4, None, 7],
    result_fn=tree_list,
    views=[
        dict(type='custom', draw=_draw, h=480),
        dict(type='calls', h=150),
    ],
    watch=[('root1', 'root1', 'orange'), ('root2', 'root2', 'cyan')],
    captions={
        'if root1 is None': _cap1,
        'if root2 is None': _cap2,
        'return TreeNode(root1.val + root2.val': _cap5,
        'self.mergeTrees(root1.left': '递归合并==左子树==：`root1.left` 与 `root2.left`',
        'self.mergeTrees(root1.right': '左子树合并好了；递归合并==右子树==：`root1.right` 与 `root2.right`',
    },
    cards=dict(
        one_liner='谁空就返回另一个；都不空就值相加，再递归合并左右子树',
        complexity='时间 `O(min(n, m))`，空间 `O(min(n, m))`',
        problem=['把两棵二叉树 `root1`、`root2` 叠在一起合并成一棵新树',
                 '两个节点重叠 → 值相加；否则==不为 null 的节点直接作为新树的节点==',
                 '示例：`[1,3,2,5]` + `[2,1,3,null,4,null,7]` → `[3,4,5,5,4,null,7]`'],
        quote='如果 root1 是空的，无需合并，直接返回 root2。如果 root2 是空的，无需合并，直接返回 root1。如果都不为空，那么将这两个节点的值相加……然后递归合并左右子树。',
        quote_src='—— 灵茶山艾府题解',
        idea=['三类分类讨论，前两类是递归边界：一边为空就把另一边==整棵子树==拿来用',
              '都不为空：新节点的值 = 两值之和，左儿子 = 合并左子树，右儿子 = 合并右子树',
              '新节点要等左右子树都合并完才能建出来 → 从下往上（后序）'],
        result='合并结果 `[3,4,5,5,4,null,7]` ✓',
        summary=['时间 `O(min(n, m))`：只递归两棵树==都有节点==的位置；空间同为递归栈',
                 '一边为空时直接返回另一边的子树，不用再往下递归',
                 '写法二：把结果直接存进 `root1`（`root1.val += root2.val`），不新建节点',
                 '晕递归？把 `mergeTrees` 当成已经写好的函数：它能合并任意两棵子树'],
    ),
)
