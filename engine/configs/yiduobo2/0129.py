# ---- 树上标注：caption 回调里记录每个节点的 level_dict / 贡献，custom 叠加层（h=0）画在 tree 视图里节点的下方
TREE_H = 390
LV = {}       # uid -> level_dict（该节点到叶子的所有路径长度：长度 -> 条数）
CONTRIB = {}  # uid -> 该节点贡献的价值


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


def _d(d):
    return '{' + ', '.join(f'{k}:{v}' for k, v in d.items()) + '}'


def track(fn):
    def cap(S, B, ret):
        if S.get('_line') == 30 and S.get('now') is not None:
            LV[S.now._uid] = dict(S.level_dict)
            CONTRIB[S.now._uid] = S.res - S.left_res - S.right_res
        for n in _walk(S.get('root')):
            n._lv = LV.get(n._uid)
            n._c = CONTRIB.get(n._uid)
        if callable(fn):
            return fn(S, B, ret)
        env = dict(S)
        env.update(B=B, ret=ret, _d=_d)
        return eval('f' + repr(fn), {}, env)
    return cap


def _layout(root, box):  # 与 views.v_tree 相同的布局
    x0, y0, x1, y1 = box
    order, depth = [], {}

    def ino(n, d):
        if n is None or n._uid in depth:
            return
        depth[n._uid] = d
        ino(n.left, d + 1)
        order.append(n)
        ino(n.right, d + 1)
    ino(root, 0)
    maxd = max(depth.values()) + 1
    sp = min(78, (x1 - x0 - 60) / max(1, len(order)))
    dy = min(95, (y1 - y0 - 80) / max(1, maxd))
    rad = max(14, min(26, sp * 0.4, dy * 0.32))
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * len(order)) / 2 + sp / 2
    pos = {n._uid: (sx + i * sp, y0 + 60 + depth[n._uid] * dy + rad) for i, n in enumerate(order)}
    return pos, rad, order


def badges(cv, S, B, box, T):
    root = S.get('root')
    if root is None:
        return
    pos, rad, order = _layout(root, (box[0], box[1] - TREE_H, box[2], box[1]))
    for n in order:
        lv = getattr(n, '_lv', None)
        if lv is None:
            continue
        X, Y = pos[n._uid]
        s = _d(lv)
        w = cv.tlen(s, 18, bold=True) + 14
        cv.rect((X - w / 2, Y + rad + 4, X + w / 2, Y + rad + 28), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 16), s, 18, T['green'], anchor='mm', bold=True)


def _contrib_map(S):
    out = {}
    for n in _walk(S.get('root')):
        if getattr(n, '_c', None) is not None:
            out[n.val] = n._c
    return out


def _formula(S, B):
    ln = S.get('_line')
    if ln == 28:
        k, v = S['key'], S['val']
        return f'`10^({k}−1) × {v} × {S["now"].val}` = {10 ** (k - 1) * v * S["now"].val}，`res` = =={S["res"]}=='
    if ln in (19, 21):
        return f'子树里长度 `{S["key"]}` 的路径加上 `{S["now"].val}` → 长度 `{S["key"] + 1}`：`level_dict` = {_d(S["level_dict"])}'
    if S.get('now') is not None and 'level_dict' in S['_inner']:
        return f'节点 `{S["now"].val}` 的 `level_dict` = =={_d(S["_inner"]["level_dict"])}==（路径长度 : 条数）'
    return '节点的价值 = `Σ 10^(长度−1) × 条数 × now.val`'


def nv(x):
    return 'None' if x is None else str(x.val)


def cap_if_left(S, B, ret):
    if S.now.left:
        return f'`{S.now.val}` 有左子树 `{S.now.left.val}` → 先递归求出它的路径长度'
    return f'`{S.now.val}` 没有左子树'


def cap_if_right(S, B, ret):
    pre = f'左子树返回 `({S.left_res}, {_d(S.left_level)})`；' if S.now.left else ''
    if S.now.right:
        return pre + f'有右子树 `{S.now.right.val}` → 递归'
    return pre + '没有右子树'


def cap_ld(S, B, ret):
    if not S.now.left and not S.now.right:
        return f'`{S.now.val}` 没有子树 → 没有可以合并的路径'
    if S.now.right:
        return f'右子树返回 `({S.right_res}, {_d(S.right_level)})`；合并左右的路径长度'
    return '合并左右子树的路径长度'


def cap_not(S, B, ret):
    if not S.level_dict:
        return f'`level_dict` 为空 → `{S.now.val}` 是==叶子=='
    return f'`level_dict = {_d(S.level_dict)}` 非空 → 不是叶子'


CONFIG = dict(
    num=129, title='求根节点到叶节点数字之和', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='按位贡献 · 统计到叶子的路径长度',
    tags=['热题173', '面试经典150'],
    code='''
class Solution(object):
    def sumNumbers(self, root):
        if not root:
            return 0

        res, level_dict = self.dfs(root)
        return res

    def dfs(self, now):
        left_res = right_res = 0
        left_level = right_level = {}
        if now.left:
            left_res, left_level = self.dfs(now.left)
        if now.right:
            right_res, right_level = self.dfs(now.right)

        level_dict = {}
        for key, val in left_level.items():
            level_dict[key + 1] = level_dict.get(key + 1, 0) + val
        for key, val in right_level.items():
            level_dict[key + 1] = level_dict.get(key + 1, 0) + val

        if not level_dict:
            level_dict = {1:1}

        res = left_res + right_res
        for key, val in level_dict.items():
            res += 10 ** (key - 1) * val * now.val

        return res, level_dict
''',
    call='Solution().sumNumbers(Tr([4,9,0,5,1]))',
    expect=1026,
    # for 头部单独成步很碎（叶子上还是空循环），交给循环体字幕讲
    skip=['left_res = right_res = 0', 'left_level = right_level = {}',
          'for key, val in left_level', 'for key, val in right_level', 'for key, val in level_dict'],
    views=[
        dict(type='text', fn=_formula),
        dict(type='tree', label='二叉树（绿框 = 该节点到叶子的路径长度 : 条数）', pointers={'now': 'blue'}, h=TREE_H,
             color=lambda S, n: 'green' if getattr(n, '_lv', None) is not None else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='map', var=_contrib_map, label='每个节点贡献的价值（节点值 → 价值）', h=120, fmt=lambda k, v: f'{k} → {v}'),
    ],
    watch=[('now', 'now', 'blue'), ('left_res', lambda S: S['_inner'].get('left_res')),
           ('right_res', lambda S: S['_inner'].get('right_res')), ('res', lambda S: S['_inner'].get('res'), 'green')],
    captions={
        'if not root': track('树非空，从根开始 dfs'),
        'res, level_dict = self.dfs(root)': track('`dfs(now)` 返回==以 now 为根的子树之和==，以及 now 到叶子的所有路径长度'),
        7: track('所有节点的价值加起来：返回 `res = {res}`'),
        'if now.left': track(cap_if_left),
        'left_res, left_level = self.dfs': track(lambda S, B, ret: f'进入左子树 `dfs({S.now.val})`'),
        'if now.right': track(cap_if_right),
        'right_res, right_level = self.dfs': track(lambda S, B, ret: f'进入右子树 `dfs({S.now.val})`'),
        'level_dict = {}': track(cap_ld),
        19: track('左边长度 `{key}` 的路径接上 `{now.val}` 变成长度 `{key + 1}`：`level_dict[{key + 1}] = {level_dict[key + 1]}`'),
        21: track('右边长度 `{key}` 的路径接上 `{now.val}` 变成长度 `{key + 1}`：`level_dict[{key + 1}] = {level_dict[key + 1]}`'),
        'if not level_dict': track(cap_not),
        'level_dict = {1:1}': track('叶子只能形成==一条长度为 1== 的路径：`{{1:1}}`'),
        'res = left_res + right_res': track('先把左右子树的和加上：`res = {left_res} + {right_res} = {res}`'),
        'res += 10 **': track('长度 `{key}` 的路径有 `{val}` 条，`{now.val}` 在==从右数第 {key} 位==：`+{10 ** (key - 1) * val * now.val}` → `res = {res}`'),
        'return res, level_dict': track(lambda S, B, ret: f'`{S.now.val}` 子树处理完：返回 `({S.res}, {_d(S.level_dict)})`'),
    },
    cards=dict(
        one_liner='每个节点的价值 = Σ 10^(到叶子路径长度−1) × 条数 × val',
        complexity='时间 `O(n·h)`，空间 `O(n)`（`h` 为树高）',
        problem=['二叉树每个节点是 `0~9`，每条==根到叶子==的路径代表一个数字',
                 '例如 `1 → 2 → 3` 表示 `123`，求所有这些数字之和',
                 '示例：`[4,9,0,5,1]` → `495 + 491 + 40 = 1026`'],
        quote='节点4能形成三条路径，分别为4-9-5，4-9-1，4-0……那么节点4能提供的价值为 (10^(3 - 1) * 2 + 10^(2 - 1) * 1) * 4 = 840',
        quote_src='—— yiduobo 知乎题解',
        idea=['换个角度：不拼数字，而是算==每个节点贡献了多少==',
              '节点在长度为 `L` 的路径里处在第 `L` 位 → 贡献 `10^(L−1) × val`',
              '`dfs` 自底向上返回 `level_dict`（路径长度 → 条数）：子树的长度 ==+1== 就是自己的'],
        result='`840 + 180 + 5 + 1 + 0 = 1026` ✓',
        summary=['时间 `O(n·h)`：每个节点要合并子树的路径长度表（最多 `h` 种长度）',
                 '易错：叶子要手动设成 `{1:1}`，否则价值算不进去',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串和 TreeNode 注释',
                 '`left_level = right_level = {}` 共用一个空字典，但只读不写，所以安全',
                 '对比灵神：灵神自顶向下传 `x`，到叶子再累加，更直接'],
    ),
)
