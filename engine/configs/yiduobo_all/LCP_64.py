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


def FMT(d):
    return str(d)


def _lit(S):
    st = S['_inner']['state']
    n = S['_inner']['now']
    return n.val ^ (st // 2) ^ (st % 2)


def _info(S):
    i = S['_inner']
    if 'state' not in i or i.get('now') is None:
        return '状态 `state` = 两位二进制：高位 = 父节点按了开关 3，低位 = 祖先开关 2 的奇偶'
    st, n = i['state'], i['now']
    v = n.val ^ (st // 2) ^ (st % 2)
    return (f"节点 `{n.val}`｜`state = {st}`（父开关3 = {st // 2}，祖先开关2 = {st % 2}）→ ==" + ('亮着' if v else '已灭') + '==')


def _t1(S, B, r):
    i = S['_inner']
    if 'v' not in i:  # 刚进入子调用：S 是新栈帧，改用调用前的 B
        i = B['_inner']
    n, st = i['now'], i['state']
    v = n.val ^ (st // 2) ^ (st % 2)
    if 't1' in i:
        return f'什么都不拨（亮着只拨开关 1）：亮着要 1 次、已灭要 0 次，当前{"亮" if v else "灭"} → `t1` = ==' + str(i['t1']) + '=='
    return (f'拆 `state = {st}`：`switch_root = {st // 2}`，`switch_all = {st % 2}`，灯原值 `{n.val}` → 现在 =={"亮" if v else "灭"}==（`v = {i["v"]}`）。'
            f'先试不拨 2、3：儿子拿到 `{st % 2}`，去算儿子')


def _t(name, what, cost_lit, cost_off, child):
    def f(S, B, ret):
        i = S['_inner']
        if 'v' not in i:
            i = B['_inner']
        if name in i:
            v = i['now'].val ^ (i['state'] // 2) ^ (i['state'] % 2)
            return f'{what}：亮着要 {cost_lit} 次、已灭要 {cost_off} 次，当前{"亮" if v else "灭"} → `{name}` = ==' + str(i[name]) + '=='
        return f'试「{what}」：儿子拿到 {child}，先去算两个儿子'
    return f


CONFIG = dict(
    num='LCP 64', title='二叉树灯饰', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='树形 DP · 状态压缩成两位',
    tags=['动态规划', '链表树与回溯'],
    code='''
class Solution(object):
    def closeLampInTree(self, root):

        f = {}

        def dfs(now, state):
            if not now:
                return 0

            if now not in f or state not in f[now]:
                switch_root = state // 2
                switch_all = state % 2
                v = now.val
                if switch_root == 1:
                    v = 1 - v
                if switch_all == 1:
                    v = 1 - v

                t1 = dfs(now.left, switch_all) + dfs(now.right, switch_all) + v
                t2 = dfs(now.left, 1 - switch_all) + dfs(now.right, 1 - switch_all) + 2 - v
                t3 = dfs(now.left, 2 + switch_all) + dfs(now.right, 2 + switch_all) + 2 - v
                t4 = dfs(now.left, 3 - switch_all) + dfs(now.right, 3 - switch_all) + 2 + v

                if now not in f:
                    f[now] = {}
                f[now][state] = min(t1, t2, t3, t4)

            return f[now][state]

        return dfs(root, 0)
''',
    call='Solution().closeLampInTree(Tr([1,1]))',
    expect=1,
    views=[
        dict(type='text', fn=_info, size=24, h=56),
        dict(type='tree', var='root', label='二叉树（黄 = 灯亮，蓝 = now）', pointers={'now': 'blue'}, h=290,
             color=lambda S, n: 'yellow' if n.val == 1 else None),
        dict(type='map', var='f', label='f：记忆化表 f[now][state]', fmt=lambda k, v: str(v), h=100),
        dict(type='calls', h=200, hide=('root', 'f')),
    ],
    watch=[('now', 'now.val', 'blue'), ('state', lambda S: S['_inner'].get('state'), 'cyan'),
           ('v', lambda S: S['_inner'].get('v'), 'yellow')],
    captions={
        'if now not in f or state not in f[now]': lambda S, B, r: (
            f'查记忆化表：`f[{S.now.val}][{S.state}]` 还没算过 → 往下算'),
        'if switch_all == 1xx': lambda S, B, r: (
            f'拆 `state = {S.state}`：`switch_root = {S.state // 2}`，`switch_all = {S.state % 2}`；'
            f'灯原值 `{S.now.val}` 每遇到一个 1 翻一次'),
        't1 =': _t1,
        't2 =': _t('t2', '只拨开关 2', 1, 2, '`1 - switch_all`（子树整体翻转）'),
        't3 =': _t('t3', '只拨开关 3（亮着；已灭加开关 1）', 1, 2, '`2 + switch_all`（父开关3 = 1）'),
        't4 =': _t('t4', '开关 2、3 一起拨', 3, 2, '`3 - switch_all`'),
        'f[now][state] = min': lambda S, B, r: (
            f'四种取最小：`min({S.t1}, {S.t2}, {S.t3}, {S.t4})` = =={S.f[S.now][S.state]}==，写进 `f[{S.now.val}][{S.state}]`'),
        'return f[now][state]': lambda S, B, r: f'返回 `f[{S.now.val}][{S.state}]` = =={r}==',
        'return dfs(root, 0)': lambda S, B, r: ('从根出发，`state = 0`：祖先什么都没拨' if r is None else f'`f[root][0]` = =={r}== 就是答案'),
        'f = {}': '`f` 记下已经算过的 `(节点, 状态)`，避免重复',
    },
    skip=['if not now', 'return 0', 'switch_root = state', 'switch_all = state', 'v = now.val', 'if switch_root == 1',
          'v = 1 - v', 'if switch_all == 1', 'if now not in f:', 'f[now] = {}', 'def dfs'],
    max_steps=80,
    cards=dict(
        one_liner='把「祖先开关 2 奇偶 + 父开关 3」压成两位 state，记忆化搜索',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二叉树每个节点有一盏灯和三个开关',
                 '开关 1 翻自己；开关 2 翻整棵子树；开关 3 翻自己和左右儿子',
                 '求最少操作几次让所有灯都关闭',
                 '示例：`[1,1,0,null,null,null,1]` → `2`；下面演示 `[1,1]` → `1`'],
        quote='可以将这四种情况做成一个两位的二进制编码，其中低位为开关2的使用情况，高位为开关3的使用情况。',
        quote_src='—— yiduobo 题解',
        idea=['`state` 的低位 = 祖先开关 2 的奇偶，高位 = 父节点是否按了开关 3',
              '开关 1 只影响自己，单独剥离：用 `v`（灯现在亮不亮）决定要不要补一次',
              '只需讨论开关 2、3 的四种组合：`t1…t4`，代价里的 `v` 或 `2 - v` 就是开关 1 的花销'],
        result='运行结束，返回 `1`：在根上拨一次开关 2',
        summary=['时间 `O(n)`：状态数 `4n`；空间 `O(n)`',
                 '原文为 Python 2 写法，整数除法 `state / 2` 已改为 `state // 2`',
                 '易错：`state` 低位是开关 2，高位是开关 3，别记反',
                 '易错：同一开关拨两次等于没拨，所以只枚举每个开关拨 0/1 次'],
    ),
)
