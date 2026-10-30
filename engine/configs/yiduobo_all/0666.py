def _sub(f, i):
    l = _sub(f, 2 * i + 1) if 2 * i + 1 < len(f) and f[2 * i + 1] != -1 else (0, 0)
    r = _sub(f, 2 * i + 2) if 2 * i + 2 < len(f) and f[2 * i + 2] != -1 else (0, 0)
    c = l[1] + r[1]
    return (f[i], 1) if c == 0 else (f[i] * c + l[0] + r[0], c)


def _done(S):
    """已经返回的节点 -> (路径和, 叶子数)：按 dfs 前序，排在 now 之前且不是 now 祖先的节点已返回"""
    f, now = S.get('f'), S['_inner'].get('now')
    if f is None or now is None or f[0] == -1 or len(f) < 31 or f[1] == -1 and f[2] == -1 and f[0] == -1:
        return {}
    pre, st = [], [0]
    while st:
        i = st.pop()
        pre.append(i)
        for c in (2 * i + 2, 2 * i + 1):
            if c < len(f) and f[c] != -1:
                st.append(c)
    anc, a = set(), now
    while a:
        a = (a - 1) // 2
        anc.add(a)
    out = [i for i in pre[:pre.index(now)] if i not in anc]
    if S['_line'] in (24, 26):
        out.append(now)
    return {i: _sub(f, i) for i in out}


def _pos(box, i):
    x0, y0, x1, y1 = box
    d = (i + 1).bit_length() - 1
    k = i + 1 - (1 << d)
    W = x1 - x0 - 60
    return x0 + 30 + W * (k + 0.5) / (1 << d), y0 + 90 + d * 95


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    f = S.get('f')
    if f is None:
        return
    cv.text((x0 + 18, y0 + 4), '数组模拟的满二叉树（下标 i：左孩子 2i+1，右孩子 2i+2；绿标 = 子树 (路径和, 叶子数)）', 22, T['muted'], bold=True)
    now = S['_inner'].get('now')
    DONE = _done(S)
    n = 15
    for i in range(n):
        if f[i] == -1:
            continue
        for c in (2 * i + 1, 2 * i + 2):
            if c < n and f[c] != -1:
                cv.line([_pos(box, i), _pos(box, c)], T['border'], 3)
    for i in range(n):
        if f[i] == -1:
            continue
        X, Y = _pos(box, i)
        done = i in DONE
        fill = T['blue'] if i == now else (T['green'] if done else T['panel2'])
        cv.circle((X, Y), 25, fill=fill, outline=T['border'], width=2) if hasattr(cv, 'circle') else cv.rect((X - 25, Y - 25, X + 25, Y + 25), fill=fill, r=25, outline=T['border'], width=2)
        cv.text((X, Y), f[i], 26, T['bg'] if (i == now or done) else T['text'], anchor='mm', bold=True)
        cv.text((X - 30, Y - 28), i, 17, T['dim'], anchor='rb', mono=True)
        if done:
            s, c = DONE[i]
            t = f'({s}, {c})'
            w = cv.tlen(t, 19, bold=True) + 14
            cv.rect((X - w / 2, Y + 29, X + w / 2, Y + 55), fill=T['panel'], outline=T['green'], width=2, r=8)
            cv.text((X, Y + 42), t, 19, T['green'], anchor='mm', bold=True)


def track(fn, record=False, reset=False):
    def cap(S, B, ret):
        return fn(S, B, ret) if callable(fn) else fn
    return cap


def _cap_ret(S, B, ret):
    if S.leaf_cnt == 0:
        return f'`leaf_cnt = 0`：下标 `{S.now}` 是叶子 → 返回 (自己的值 `{S.f[S.now]}`, 叶子数 `1`)'
    return (f'`{S.f[S.now]} × {S.leaf_cnt} + {S.left_s} + {S.right_s}` = =={ret[0]}==：'
            f'==自己这个值被它下面的 {S.leaf_cnt} 条路径共用==')


CONFIG = dict(
    num=666, title='路径总和 IV', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='数组模拟满二叉树 · DFS 返回(路径和, 叶子数)',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def pathSum(self, nums):

        f = [-1] * 31
        for num in nums:
            d = num // 100
            p = num // 10 % 10
            v = num % 10
            f[(1 << (d - 1)) - 1 + p - 1] = v
        
        def dfs(now):
            if f[now + now + 1] != -1:
                left_s, left_cnt = dfs(now + now + 1)
            else:
                left_s, left_cnt = 0, 0
            
            if f[now + now + 2] != -1:
                right_s, right_cnt = dfs(now + now + 2)
            else:
                right_s, right_cnt = 0, 0
            
            leaf_cnt = left_cnt + right_cnt
            if leaf_cnt == 0:
                return f[now], 1
            else:
                return f[now] * leaf_cnt + left_s + right_s, leaf_cnt

        return dfs(0)[0]
''',
    call='Solution().pathSum([113, 215, 221, 316, 324])',
    expect=30,
    views=[
        dict(type='custom', draw=_draw, h=380),
        dict(type='array', var='f[:15]', label='f（前 15 格，-1 = 没有节点）', h=135,
             color=lambda S, i, v: None if v == -1 else 'blue' if i == S['_inner'].get('now') else 'green' if i in _done(S) else None,
             dim=lambda S, i, v: v == -1),
        dict(type='calls', h=165),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'blue'),
           ('left_s,cnt', lambda S: (S['_inner'].get('left_s'), S['_inner'].get('left_cnt')), 'cyan'),
           ('right_s,cnt', lambda S: (S['_inner'].get('right_s'), S['_inner'].get('right_cnt')), 'pink'),
           ('leaf_cnt', lambda S: S['_inner'].get('leaf_cnt'), 'green')],
    max_steps=110,
    captions={
        'f = [-1] * 31': track(lambda S, B, r: '用数组 `f` 模拟满二叉树，`-1` 表示这个位置没有节点', reset=True),
        'for num in nums': '依次处理三位数 `{num}`',
        'd = num // 100': '百位 = 层数：`d = {d}`',
        'p = num // 10 % 10': '十位 = 该层第几个：`p = {p}`',
        'v = num % 10': '个位 = 节点值：`v = {v}`',
        'f[(1 << (d - 1))': '前 `d-1` 层共 `2^(d-1) - 1 = {(1 << (d - 1)) - 1}` 个 → 下标 = `{(1 << (d - 1)) - 1} + {p} - 1` = =={(1 << (d - 1)) - 1 + p - 1}==，存入 `{v}`',
        'if f[now + now + 1] != -1': lambda S, B, r: (f'下标 `{S.now}` 的左孩子在 `{2 * S.now + 1}`，有节点 → 递归求左子树' if S.f[2 * S.now + 1] != -1
                                                      else f'下标 `{S.now}` 的左孩子 `{2 * S.now + 1}` 是 `-1` → 没有左孩子'),
        'left_s, left_cnt = dfs': lambda S, B, r: f'左子树 `{2 * S.now + 1}` 返回：路径和 `left_s = {S.left_s}`，叶子数 `left_cnt = {S.left_cnt}`',
        'left_s, left_cnt = 0, 0': '没有左孩子：路径和、叶子数都记 `0`',
        'if f[now + now + 2] != -1': lambda S, B, r: (f'右孩子在 `{2 * S.now + 2}`，有节点 → 递归求右子树' if S.f[2 * S.now + 2] != -1
                                                      else f'右孩子 `{2 * S.now + 2}` 是 `-1` → 没有右孩子'),
        'right_s, right_cnt = dfs': lambda S, B, r: f'右子树 `{2 * S.now + 2}` 返回：路径和 `right_s = {S.right_s}`，叶子数 `right_cnt = {S.right_cnt}`',
        'right_s, right_cnt = 0, 0': '没有右孩子：路径和、叶子数都记 `0`',
        'leaf_cnt = left_cnt': '以 `{now}` 为根的子树叶子数 = `{left_cnt} + {right_cnt}` = =={leaf_cnt}==',
        'if leaf_cnt == 0': lambda S, B, r: ('`leaf_cnt == 0`：两边都没孩子，==自己就是叶子==' if S.leaf_cnt == 0
                                             else f'`leaf_cnt = {S.leaf_cnt}`：下面有 `{S.leaf_cnt}` 条到叶子的路径'),
        'return f[now], 1': track(_cap_ret, record=True),
        'return f[now] * leaf_cnt': track(_cap_ret, record=True),
        'return dfs(0)[0]': lambda S, B, r: ('从根（下标 `0`）开始 dfs' if r is None else f'返回值第一项就是所有根到叶路径之和 = =={r}=='),
    },
    cards=dict(
        one_liner='节点值乘上它下面的叶子数，就是它对答案的贡献',
        complexity='时间 `O(n)`，空间 `O(n)`（数组大小固定 31，递归深度 ≤ 4）',
        problem=['树用三位数列表表示：百位 `d` 层数，十位 `p` 位置，个位 `v` 节点值',
                 '求==所有根到叶子路径==上的数字之和',
                 '示例：`[113,215,221,316,324]` → 路径 `3-5-6`、`3-5-4`、`3-1` → `14+12+4 = 30`'],
        quote='数组中下标0的元素表示整棵树的根节点，而对于下标i而言，其左孩子的下标为i * 2 + 1，右孩子的下标则为i * 2 + 2。',
        quote_src='—— yiduobo 题解原文',
        idea=['第 `d` 层第 `p` 个的下标 = `2^(d-1) - 1 + p - 1`，先把树建在数组里',
              'dfs 返回 `(子树路径和, 叶子数)`',
              '非叶子：`值 × 叶子数 + left_s + right_s`，自己被每条路径各算一次'],
        summary=['时间 `O(n)`，不用显式建树，数组下标就是父子关系',
                 '易错：`f` 里用 `-1` 表示空，节点值是 `1..9` 所以不会混淆',
                 '易错：只有一个孩子时，另一侧叶子数为 `0`，当前节点仍不是叶子',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
