TREE_H = 380
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


def track(fn, record=False):
    def cap(S, B, ret):
        if record and S.get('now') is not None:
            DONE[S['now']._uid] = ret
        for n in _walk(S.get('root')):
            n._d = DONE.get(n._uid)
        if callable(fn):
            return fn(S, B, ret)
        return eval('f' + repr(fn), {'B': B, 'ret': ret}, dict(S))
    return cap


def _layout(root, box):
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
        d = getattr(n, '_d', None)
        if d is None:
            continue
        X, Y = pos[n._uid]
        s = FMT(d)
        w = cv.tlen(s, 19, bold=True) + 16
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 18), s, 19, T['green'], anchor='mm', bold=True)


OPS = {2: 'OR', 3: 'AND', 4: 'XOR', 5: 'NOT'}


def _nm(n):
    return {0: '叶子 0', 1: '叶子 1'}.get(n.val) or OPS[n.val]


def FMT(d):
    return d


def badges(cv, S, B, box, T):
    root = S.get('root')
    f = S.get('f')
    if root is None or not f:
        return
    pos, rad, order = _layout(root, (box[0], box[1] - TREE_H, box[2], box[1]))
    for n in order:
        a, b = f.get((n, True)), f.get((n, False))
        if a is None and b is None:
            continue
        X, Y = pos[n._uid]
        s = f"T:{'?' if a is None else a} F:{'?' if b is None else b}"
        w = cv.tlen(s, 19, bold=True) + 16
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 18), s, 19, T['green'], anchor='mm', bold=True)


def _info(S):
    i = S['_inner']
    n = i.get('now')
    if n is None or 'target' not in i:
        return '节点值：`0/1` = 叶子，`2` = OR，`3` = AND，`4` = XOR，`5` = NOT'
    return f"节点 `{n.val}`（{_nm(n)}）｜目标 `{i['target']}`｜`f[节点][目标]` = 让该子树变成目标的最少翻转"


def _cap_if(S, B, r):
    i = B['_inner']
    n, t = i['now'], i['target']
    return f'求 `f[{n.val}:{_nm(n)}][{t}]`：查表，没算过 → 往下算' if (n, t) not in S['f'] else f'`f[{n.val}:{_nm(n)}][{t}]` 已经在表里 → 直接用'


def _cap_set(S, B, r):
    i = B['_inner']
    n, t = i['now'], i['target']
    key = i['key']
    done = len(S['f']) > len(B['f'])
    val = list(S['f'].values())[-1] if S['f'] else None
    v = n.val
    tt = '真' if t else '假'
    if v in (0, 1):
        return f'叶子 `{v}` 想变成{tt}：值{"" if v != t else "已经"}{"相等，不用翻转" if v == t else "不同，翻转 1 次"} → `f` = =={val}=='
    if v == 2:
        how = ('OR 要真：==一边真就行==，取两边较小的' if t else 'OR 要假：==两边都得假==，翻转次数相加')
    elif v == 3:
        how = ('AND 要真：==两边都得真==，翻转次数相加' if t else 'AND 要假：==一边假就行==，取两边较小的')
    elif v == 4:
        how = ('XOR 要真：==左右不同==，两种搭配取小' if t else 'XOR 要假：==左右相同==，两种搭配取小')
    else:
        how = 'NOT：目标取反交给儿子 `not target`'
    if done:
        return f'{how} → `f[..][{t}]` = ==' + str(val) + '=='
    return f'{how}：先去递归求儿子'


CONFIG = dict(
    num=2313, title='二叉树中得到结果所需的最少翻转次数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='树形 DP · f[节点][目标值]',
    tags=['链表树与回溯'],
    code='''
class Solution(object):
    def minimumFlips(self, root, result):

        f = {}

        def dfs(now, target):
            key = (now, target)
            if key not in f:

                if now.val == 0 or now.val == 1:
                    if target:
                        f[key] = 1 - now.val
                    else:
                        f[key] = now.val
                elif now.val == 2:
                    if target:
                        f[key] = min(dfs(now.left, True), dfs(now.right, True))
                    else:
                        f[key] = dfs(now.left, False) + dfs(now.right, False)
                elif now.val == 3:
                    if target:
                        f[key] = dfs(now.left, True) + dfs(now.right, True)
                    else:
                        f[key] = min(dfs(now.left, False), dfs(now.right, False))
                elif now.val == 4:
                    if target:
                        f[key] = min(dfs(now.left, True) + dfs(now.right, False), \\
                               dfs(now.right, True) + dfs(now.left, False))
                    else:
                        f[key] = min(dfs(now.left, True) + dfs(now.right, True), \\
                               dfs(now.left, False) + dfs(now.right, False))
                else:
                    if now.left:
                        f[key] = dfs(now.left, not target)
                    else:
                        f[key] = dfs(now.right, not target)

            return f[key]

        return dfs(root, result)
''',
    call='Solution().minimumFlips(Tr([4,1,3,None,None,1,0]), False)',
    expect=1,
    views=[
        dict(type='text', fn=_info, size=22, h=50),
        dict(type='tree', var='root', label='布尔表达式树（蓝 = now，绿 = 已算的 f）', pointers={'now': 'blue'}, h=TREE_H),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=170, hide=('root', 'f')),
    ],
    watch=[('now', 'now.val', 'blue'), ('target', lambda S: S['_inner'].get('target'), 'cyan')],
    captions={
        'if key not in f': _cap_if,
        'f[key] =': _cap_set,
        'dfs(now.left, False) + dfs(now.right, False))': '另一种搭配：左右都变成假，再相加；两种搭配取小',
        'return f[key]': lambda S, B, r: f'返回 `f[key]` = =={r}==：让这棵子树变成 `{B["_inner"]["target"]}` 最少翻转 {r} 次',
        'return dfs(root, result)': lambda S, B, r: ('从根出发，目标是 `result`' if r is None else f'答案 = `f[root][result]` = =={r}=='),
    },
    skip=['key = (now, target)', 'if now.val == 0 or now.val == 1', 'elif now.val', 'if target:', 'if now.left:', 'else:', 'f = {}', 'def dfs'],
    max_steps=80,
    cards=dict(
        one_liner='f[节点][目标]：每种运算符各讲一次「要变成目标，儿子该是什么」',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二叉树表示布尔表达式：叶子 `0/1`，内部节点是运算符',
                 '`2` = OR，`3` = AND，`4` = XOR，`5` = NOT（只有一个儿子）',
                 '每次可以翻转一个叶子，求让整棵树的值等于 `result` 的最少翻转次数',
                 '示例：`[4,1,3,null,null,1,0]`，`result = false` → `1`'],
        quote='令f[node][target]表示将以node为根节点的子树值变为target所需的最少翻转次数',
        quote_src='—— yiduobo 题解',
        idea=['叶子：目标和自己相同要 0 次，不同要 1 次',
              'OR / AND：看目标是否「一边就够」还是「两边都要」，取 `min` 或相加',
              'XOR：真 = 左右不同，假 = 左右相同，各两种搭配取小',
              'NOT：目标取反，原样交给唯一的儿子'],
        result='运行结束，返回 `1`：把 `AND(1,0)` 里的 0 或叶子 1 翻转一次',
        summary=['时间 `O(n)`：每个 `(节点, 目标)` 只算一次；空间 `O(n)`',
                 '易错：NOT 节点只有一个儿子，可能在左也可能在右',
                 '易错：XOR 要真 / 要假时，两种搭配都要取 `min`，别只算一种',
                 '原文续行符 `\\` 与代码一致；这个演示的树里没有 NOT 节点'],
    ),
)
