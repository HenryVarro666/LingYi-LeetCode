import sys as _sys

# 两棵输入树（按“位置”记录：'' = 根，'L' = 左儿子，'LR' = 左儿子的右儿子 ……）
T1 = {'': 1, 'L': 3, 'R': 2, 'LL': 5}
T2 = {'': 2, 'L': 1, 'R': 3, 'LR': 4, 'RR': 7}
MERGED = {p: T1.get(p, 0) + T2.get(p, 0) for p in set(T1) | set(T2)}
FN, LLINE, RLINE = 'dfs', 13, 14            # 递归函数名、递归左子树 / 右子树所在行


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


def _tree(cv, T, vals, box, title, tcolor, stack, cur, shown=None, color=None, rad=24, edges=None):
    x0, y0, x1, y1 = box
    cv.text((x0 + 14, y0 + 4), title, 22, tcolor, bold=True)
    dy = (y1 - y0 - 62 - rad - 6) / 2
    for p in vals:
        if p and (shown is None or (p in shown and p[:-1] in shown)) and (edges is None or p in edges):
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


def _created(S):
    """当前调用栈里已经执行过 tmp = TreeNode(...) 的那些层：结果节点已新建，但子树还没接完"""
    st = _up('st', lambda x: isinstance(x, dict) and '_S' in x) or {}
    stack, rec = _positions(st.get('_frames') or [])
    return {p for p, fr in zip(stack, rec) if 'tmp' in fr['locals']}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    stack, finished, returning = _status(S)
    created = _created(S)
    cur = stack[-1] if stack else None
    mid = (x0 + x1) / 2
    hy = y0 + (y1 - y0) * 0.47
    _tree(cv, T, T1, (x0, y0, mid - 10, hy), 't1', T['orange'], stack, cur)
    _tree(cv, T, T2, (mid + 10, y0, x1, hy), 't2', T['cyan'], stack, cur)
    cv.line([(x0 + 20, hy + 4), (x1 - 20, hy + 4)], T['border'], 1)
    done = {p for p in MERGED if any(p[:i] in finished for i in range(len(p) + 1))}
    shown = done | (created & set(MERGED))

    def col(p):
        if p in T1 and p in T2:
            return T['green']
        return T['orange'] if p in T1 else T['cyan']
    box2 = (x0 + 100, hy + 8, x1 - 100, y1)
    _tree(cv, T, MERGED, box2, '合并结果：「递」时先建 tmp，「归」时接上子树', T['green'],
          [p for p in shown if p not in done], None, shown=shown, color=col, edges=done)  # 子树返回后才接到父节点上
    cv.text((x1 - 16, hy + 14), '黄圈 = 已新建、子树未接完', 18, T['yellow'], anchor='ra')


def _cap_t1(S, B, ret):
    if B.t1 is None:
        return '`t1` 为空 → 合并结果就是 `t2`'
    return f'`t1 = {B.t1.val}` 不为空'


def _cap_t2(S, B, ret):
    if B.t2 is None:
        return '`t2` 为空 → 合并结果就是 `t1`'
    return f'`t2 = {B.t2.val}` 也不为空'


def _sub(x):
    return f'子树 `{x.val}`' if x is not None else '空'


CONFIG = dict(
    num=617, title='合并二叉树', difficulty='Easy', category='二叉树',
    author='yiduobo', technique='递归 · 先建结果节点，再递归求解左右子树',
    tags=['热题173'],
    code='''
class Solution(object):
    def mergeTrees(self, t1, t2):
        return self.dfs(t1, t2)

    def dfs(self, t1, t2):
        if t1 is None:
            return t2

        if t2 is None:
            return t1

        tmp = TreeNode(t1.val + t2.val)
        tmp.left = self.dfs(t1.left, t2.left)
        tmp.right = self.dfs(t1.right, t2.right)
        return tmp
''',
    call='Solution().mergeTrees(Tr([1, 3, 2, 5]), Tr([2, 1, 3, None, 4, None, 7]))',
    expect=[3, 4, 5, 5, 4, None, 7],
    result_fn=tree_list,
    views=[
        dict(type='custom', draw=_draw, h=480),
        dict(type='calls', h=150),
    ],
    watch=[('t1', 't1', 'orange'), ('t2', 't2', 'cyan'), ('tmp', 'tmp', 'green')],
    captions={
        'return self.dfs(t1, t2)': '从根节点开始合并两棵二叉树',
        'if t1 is None': _cap_t1,
        'return t2': lambda S, B, r: f'返回 `t2`（{_sub(r)}）',
        'if t2 is None': _cap_t2,
        'return t1': lambda S, B, r: f'返回 `t1`（{_sub(r)}）',
        'tmp = TreeNode': '都不为空：新建结果节点 `tmp`，值 = `{t1.val} + {t2.val}` = =={tmp.val}==',
        'tmp.left = self.dfs': '递归求解==左子树==，结果挂到 `tmp.left`',
        'tmp.right = self.dfs': '左子树已挂到 `tmp.left`；再递归求解==右子树==',
        'return tmp': lambda S, B, r: f'`tmp.left`、`tmp.right` 都接好了 → 返回 `tmp`（{r.val}）',
    },
    cards=dict(
        one_liner='谁为空就返回另一个；否则值相加，递归求解左右子树',
        complexity='时间 `O(min(n, m))`，空间 `O(min(n, m))`',
        problem=['把两棵二叉树 `t1`、`t2` 叠在一起合并成一棵新树',
                 '两个节点重叠 → 值相加；否则==不为 null 的节点直接作为新树的节点==',
                 '示例：`[1,3,2,5]` + `[2,1,3,null,4,null,7]` → `[3,4,5,5,4,null,7]`'],
        quote='1、若当前t1为空，那么合并结果就是t2；2、若当前t2位空，那么合并结果就是t1；3、否则设置合并结果节点的值为t1.val + t2.val，然后==递归求解左右子树==',
        quote_src='—— yiduobo 题解',
        idea=['前两条是递归边界：一边为空，另一边的==整棵子树==就是合并结果',
              '第 3 条：先 `tmp = TreeNode(t1.val + t2.val)`，再递归求 `tmp.left`、`tmp.right`',
              '结果节点在「递」时就建好，子树在「归」时接上'],
        result='合并结果 `[3,4,5,5,4,null,7]` ✓',
        summary=['时间 `O(min(n, m))`：只在两棵树都有节点的位置递归',
                 '为空时直接复用另一棵树的子树：结果树和输入树==共享节点==',
                 '对比灵神：灵神一行 `TreeNode(值, 左, 右)` 先递归再建节点；yiduobo 先建节点再挂子树',
                 '原文为 Python 2 风格：删去 docstring 和节点定义注释，代码未改'],
    ),
)
