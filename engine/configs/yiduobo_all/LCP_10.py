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
    s, p = d
    return f'串{s:g} 并{p:g}'


def nv(x):
    return '空' if x is None else str(x.val)


def cap_leaf(S, B, ret):
    return f'叶子 `{S.now.val}`：只有它自己的任务 → 串行 `{ret[0]}`，并行 `{ret[1]}`'


def cap_single(S, B, ret):
    return (f'`{S.now.val}` 只有一个儿子：没有可并行的兄弟子树 → 子树任务全部串行，'
            f'串行 = ==子树串行 + {S.now.val} = {ret[0]}==，并行 `{ret[1]}`')


def cap_eq(S, B, ret):
    return (f'左右串行时间相等（都是 `{S.left_s_time}`）→ 两边==刚好一一配对并行==：'
            f'串行只剩 `{ret[0]}`（自己），并行 `{ret[1]}`')


def cap_big(S, B, ret):
    other = S.right_p_time if S.left_s_time > S.right_s_time else S.left_p_time
    return (f'`delta = {S.delta}` ≤ 对面并行时间的两倍 `{2 * other}`，'
            f'==全部能被拆开配对==：串行只剩自己 `{ret[0]}`，并行 `{ret[1]:g}`')


def cap_over(S, B, ret):
    return (f'`delta = {S.delta}` 太大，配对不完 → 多出的 ==串行== 只能留着：串行 `{ret[0]}`，并行 `{ret[1]:g}`')


def cap_dfs_call(side):
    def f(S, B, ret):
        return f'递归求{side}子树 `{nv(S.now)}` 的（串行，并行）时间'
    return f


CONFIG = dict(
    num='LCP 10', title='二叉树任务调度', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='树形 DP · 串行/并行配对',
    tags=['链表树与回溯'],
    code='''
class Solution(object):
    def minimalExecTime(self, root):

        def dfs(now):
            if not now.left:
                if not now.right:
                    return now.val, 0
                else:
                    s_time, p_time = dfs(now.right)
                    return s_time + now.val, p_time
            elif not now.right:
                s_time, p_time = dfs(now.left)
                return s_time + now.val, p_time
            else:
                left_s_time, left_p_time = dfs(now.left)
                right_s_time, right_p_time = dfs(now.right)
                if left_s_time == right_s_time:
                    return now.val, left_s_time + left_p_time + right_p_time
                elif left_s_time > right_s_time:
                    delta = left_s_time - right_s_time
                    if delta <= right_p_time + right_p_time:
                        return now.val, right_s_time + delta * 0.5 + left_p_time + right_p_time
                    else:
                        return now.val + delta - right_p_time - right_p_time, right_s_time + right_p_time + left_p_time + right_p_time
                else:
                    delta = right_s_time - left_s_time
                    if delta <= left_p_time + left_p_time:
                        return now.val, left_s_time + delta * 0.5 + left_p_time + right_p_time
                    else:
                        return now.val + delta - left_p_time - left_p_time, left_s_time + left_p_time + left_p_time + right_p_time

        s_time, p_time = dfs(root)
        return s_time + p_time
''',
    call='Solution().minimalExecTime(Tr([1,3,2,None,None,4,4]))',
    expect=7.5,
    views=[
        dict(type='tree', label='任务树（蓝 = now，绿 = 已算出 串行/并行 时间）', pointers={'now': 'blue'}, h=TREE_H),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=210, hide=('root',)),
    ],
    watch=[('now', 'now.val', 'blue'),
           ('左 s/p', lambda S: f"{S['_inner'].get('left_s_time')}/{S['_inner'].get('left_p_time')}", 'cyan'),
           ('右 s/p', lambda S: f"{S['_inner'].get('right_s_time')}/{S['_inner'].get('right_p_time')}", 'pink'),
           ('delta', lambda S: S['_inner'].get('delta'), 'yellow')],
    captions={
        'def dfs': track('`dfs(now)` 返回一对数：==（串行时间，并行时间）==；答案 = 两者之和'),
        'elif not now.right': track('左儿子存在，右儿子是否为空？'),
        'if not now.right': track('左边为空，再看右边是否也为空'),
        'if not now.left': track(lambda S, B, r: f'节点 `{S.now.val}` 左儿子是否为空？先处理缺儿子的情况'),
        'return now.val, 0': track(cap_leaf, record=True),
        's_time, p_time = dfs(now.right)': track('只有右儿子：递归求右子树'),
        's_time, p_time = dfs(now.left)': track('只有左儿子：递归求左子树'),
        'return s_time + now.val, p_time': track(cap_single, record=True),
        'left_s_time, left_p_time = dfs': track(cap_dfs_call('左')),
        'right_s_time, right_p_time = dfs': track(lambda S, B, r: (
            f'左子树：串行 `{S.left_s_time}`，并行 `{S.left_p_time:g}`；再递归求右子树 `{nv(S.now.right)}`')),
        'if left_s_time == right_s_time': track(lambda S, B, r: (
            f'比较左右串行时间：`{S.left_s_time}` 对 `{S.right_s_time}` → '
            + ('==相等==，可以完美配对' if S.left_s_time == S.right_s_time else '不等，需要拆分较长的一边去配对'))),
        'return now.val, left_s_time + left_p_time': track(cap_eq, record=True),
        'elif left_s_time > right_s_time': track(lambda S, B, r: (
            f'`{S.left_s_time} > {S.right_s_time}`？' + ('左边串行更长，多出的部分要和右边的并行任务配对' if S.left_s_time > S.right_s_time else '不是 → 右边串行更长'))),
        'delta = left_s_time': track('`delta = {delta}`：左边比右边多出的串行时间，需要靠右子树的并行任务来消化'),
        'delta = right_s_time': track('`delta = {delta}`：右边比左边多出的串行时间，需要靠左子树的并行任务来消化'),
        'if delta <= right_p_time': track('右子树的每个并行任务最多能「供应」==2 倍==时间的配对（拆成两个 0.5）：`{delta} ≤ {2 * right_p_time}`？'),
        'if delta <= left_p_time': track('左子树的每个并行任务最多能供应 2 倍时间的配对：`{delta} ≤ {2 * left_p_time}`？'),
        'return now.val, right_s_time + delta': track(cap_big, record=True),
        'return now.val, left_s_time + delta': track(cap_big, record=True),
        'return now.val + delta - right_p_time': track(cap_over, record=True),
        'return now.val + delta - left_p_time': track(cap_over, record=True),
        's_time, p_time = dfs(root)': track('从根出发递归，拿到整棵树的（串行，并行）'),
        'return s_time + p_time': track('答案 = 串行 `{s_time}` + 并行 `{p_time:g}` = ==`{ret:g}`=='),
    },
    skip=['def dfs'],
    cards=dict(
        one_liner='把左右子树的串行任务尽量配对并行，只剩下 root 自己必须串行',
        complexity='时间 `O(n)`，空间 `O(h)`',
        problem=['二叉树每个节点是一个任务，值 = 耗时',
                 '任务必须先做完子节点，再做父节点；==不同子树的任务可以并行==',
                 '示例：`root = [1,3,2,null,null,4,4]` → `7.5`'],
        quote='由于树中所有任务所需的时间总和为常数，且root自身的任务只能串行，那么为了使得总的执行时间最短，就应该尽量让左右两颗子树中的任务并行起来。',
        quote_src='—— yiduobo 题解',
        idea=['每棵子树只用两个数描述：==串行时间 s==、并行时间 p',
              '左右 `s` 相等：刚好配对，`s` 只剩 root，`p` 加上 `s`',
              '`s` 不等：差 `delta` 用对面的 p 去拆成 0.5 配对，配不完的留作串行'],
        result='运行结束，返回 `7.5`：串行 `1` + 并行 `6.5`',
        summary=['时间 `O(n)`：每个节点递归一次；空间 `O(h)` 递归栈',
                 '易错：并行时间会出现 `0.5`，所以返回值是小数（`delta * 0.5`）',
                 '易错：只有一个儿子时没法并行，直接把儿子的串行时间加上自己',
                 '`delta` 超过对面并行任务的 2 倍时，多出来的部分只能串行'],
    ),
)
