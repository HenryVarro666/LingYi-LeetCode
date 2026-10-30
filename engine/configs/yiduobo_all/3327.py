def _layout_tree(ch, root):
    pos, cnt = {}, [0]

    def go(u, d):
        kids = ch.get(u, [])
        if not kids:
            x = cnt[0]
            cnt[0] += 1
        else:
            xs = [go(v, d + 1) for v in kids]
            x = (xs[0] + xs[-1]) / 2
        pos[u] = (x, d)
        return x
    go(root, 0)
    return pos, cnt[0]


def _tree_view(ch, root, colors, title, tags=None, wt=None, lab=None):
    """ch: {父: [子...]}；colors(S) -> {节点: 颜色名}；tags(S) -> {节点: 小字}；wt: {子: 边权}"""
    pos, W = _layout_tree(ch, root)
    D = max(d for _, d in pos.values()) + 1

    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
        cell = min(120, (x1 - x0 - 60) / max(W, 1))
        rowh = min(110, (y1 - y0 - 165) / max(D - 1, 1))
        sx = x0 + 30 + ((x1 - x0 - 60) - cell * W) / 2
        r = min(28, cell * 0.36, rowh * 0.42)
        P = {u: (sx + (x + 0.5) * cell, y0 + 80 + d * rowh) for u, (x, d) in pos.items()}
        for u, kids in ch.items():
            for v in kids:
                cv.line([P[u], P[v]], T['border'], 3)
                if wt:
                    left = P[v][0] <= P[u][0] + 1
                    cv.text(((P[u][0] + P[v][0]) / 2 + (-10 if left else 10), (P[u][1] + P[v][1]) / 2 - 6), wt[v], 22, T['orange'],
                            anchor='rm' if left else 'lm', bold=True)
        cm = colors(S) or {}
        tg = (tags(S) if tags else None) or {}
        for u, (X, Y) in P.items():
            c = cm.get(u)
            cv.rect((X - r, Y - r, X + r, Y + r), fill=T[c] if c else T['panel2'], outline=T['border'], width=2, r=r)
            cv.text((X, Y), lab(u) if lab else u, 26, T['bg'] if c else T['text'], anchor='mm', bold=True)
            if u in tg:
                cv.text((X + r + 6, Y + r * 0.5), tg[u], 20, T['muted'], anchor='lm', bold=True)
    return dict(type='custom', draw=draw, h=0)
CH = {0: [1, 2], 1: [3]}


def _colors(S):
    if 'now' in S and 'expand_list' not in S:
        return {S['now']: 'yellow'}
    ix = S.get('index')
    if 'left_in_expand' in S and isinstance(ix, int) and 0 <= ix < 4 and S.get('_line', 0) >= 66:
        return {ix: 'pink'}
    return {}


def _tags(S):
    sz, lf = S.get('size'), S.get('left')
    if sz is None or lf is None:
        return {}
    out = {}
    for i in range(4):
        if sz[i] > 0 and ('expand_list' in S or 'left_in_expand' in S or i not in (S.get('now'),)):
            out[i] = f'[{lf[i]},{lf[i] + sz[i]})'
    return out


def _ecol(S, i, v):
    ix = S.get('index')
    if S.get('right') is None or ix is None or 'f' not in S or 'res' in S:
        return None
    if len(S['f']) <= ix:
        return None
    if i == ix:
        return 'blue'
    if S['mid'] and i == S['mid']:
        return 'green'
    return None


def _fcol(S, i, v):
    ix = S.get('index')
    if S.get('right') is None or ix is None or 'res' in S:
        if 'mid_in_expand' in S and i == S['mid_in_expand']:
            return 'pink'
        return None
    if i == ix:
        return 'blue'
    if S['mid'] and i == S['mid']:
        return 'green'
    return None


def _judge(S, B, ret):
    ix = S.index
    l = S.left[ix] * 2 + 1
    r = (S.left[ix] + S.size[ix] - 1) * 2 + 1
    m = (l + r) // 2
    v = m - S.f[m] + 1
    ok = v <= l
    return f'节点 `{ix}`：区间 `[{l}, {r}]`，中心 `{m}`，`{m} - f[{m}] + 1 = {v}` ' + (f'<= `{l}` → ==是回文==' if ok else f'> `{l}` → ==不是回文==')


def _formula(S):
    if 'left_in_expand' in S:
        return f"区间 `[{S['left_in_expand']}, {S['right_in_expand']}]`（在扩展串里），中心 `{(S['left_in_expand'] + S['right_in_expand']) // 2}`；半径盖住整段才是回文"
    if 'expand_list' in S and 'f' in S:
        return '`f[i]`：以 `expand_list[i]` 为中心的回文半径（含中心）；`mid / right`：已知覆盖最靠右的回文串'
    return '`dfs(x)` 的字符串，是 `dfs(0)` 字符串里「起点 left[x]、长度 size[x]」的一段'


CONFIG = dict(
    num=3327, title='判断 DFS 字符串是否是回文串', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='子树 = dfs 序子串 + 马拉车',
    tags=['链表树与回溯', '字符串', '难度分 2454'],
    code='''
class Solution(object):
    def findAnswer(self, parent, s):
        
        n = len(parent)
        childs = [[] for _ in range(n)]
        root = None
        size = [0] * n
        left = [0] * n
        dfs_list = []

        for index in range(n - 1, -1, -1):
            fa = parent[index]
            if fa == -1:
                root = index
            else:
                childs[fa].append(index)
        
        def dfs(now):
            size[now] += 1
            left[now] = len(dfs_list)
            dfs_list.append(s[now])
            for c in childs[now]:
                dfs(c)
                size[now] += size[c]
            
            print(now, size[now])
        
        dfs(root)
        
        expand_list = ['!']
        for char in dfs_list:
            expand_list.append(char)
            expand_list.append('#')
        expand_list[-1] = '@'

        f = [0]
        mid = 0
        right = 0
        for index in range(1, len(expand_list) - 1):
            if index < right:
                f.append(min(f[2 * mid - index], right - index))
            else:
                f.append(1)
            
            while expand_list[index - f[index]] == expand_list[index + f[index]]:
                f[index] += 1
            if right < index + f[index]:
                right = index + f[index]
                mid = index

        res = []
        for index in range(n):
            left_in_expand = left[index] * 2 + 1
            right_in_expand = (left[index] + size[index] - 1) * 2 + 1
            mid_in_expand = (left_in_expand + right_in_expand) // 2
            if mid_in_expand - f[mid_in_expand] + 1 <= left_in_expand:
                res.append(True)
            else:
                res.append(False)
        
        return res
''',
    call='Solution().findAnswer([-1, 0, 0, 1], "abba")',
    expect=[True, False, True, True],
    views=[
        dict(type='text', fn=_formula, size=22, h=50),
        dict(_tree_view(CH, 0, _colors, '树（标注 = 子树在 dfs 序里的 [起点, 起点+大小)；粉 = 正在判断）', tags=_tags, lab=lambda u: f'{u}:' + 'abba'[u]), h=300),
        dict(type='array', var='dfs_list', label='dfs_list（dfs(0) 的字符串）', h=100, cell=60, index=False),
        dict(type='array', var='expand_list', label='expand_list（插入 # 并加哨兵；蓝 = index，绿 = mid）', h=112, cell=60, color=_ecol),
        dict(type='array', var='f', label='f（回文半径）', h=112, cell=60, color=_fcol),
    ],
    watch=['index', 'now', ('mid', 'mid', 'green'), ('right', 'right', 'orange'), 'left_in_expand', 'right_in_expand', 'mid_in_expand'],
    max_steps=90,
    skip=['for index in range(n - 1', 'fa = parent[index]', 'if fa == -1', 'root = index', 'else:', 'childs[fa].append',
          'size[now] += 1', 'left[now] = len(dfs_list)', 'for c in childs[now]', 'size[now] += size[c]', 'dfs_list.append(s[now])',
          'for char in dfs_list', 'expand_list.append(', 'for index in range(1, len(expand_list) - 1)', 'for index in range(n):',
          'left_in_expand = ', 'right_in_expand = ', 'res.append(', 'f = [0]', 'right = 0', 'mid = 0', 'res = []',
          'f.append(1)', 'f[index] += 1', 'right = index + f[index]', 'mid = index', 'mid_in_expand = ', 'size = [0]', 'left = [0]', 'dfs_list = []', 'root = None'],
    captions={
        'n = len(parent)': '`n = {n}`；下面先把 `parent` 反过来建成孩子列表 `childs`，再找出根',
        'childs = [[] for': '`childs[x]`：`x` 的孩子（从大编号往小编号加入，所以是降序）',
        'dfs(root)': '`size[x]`：子树节点数；`left[x]`：`x` 在 `dfs_list` 里的位置。先序走一遍（本视频孩子降序），记下两者',
        'print(now, size[now])': '节点 `{now}`：子树 ==`{size[now]}`== 个节点，从位置 ==`{left[now]}`== 开始 → 子树字符串是 `dfs_list[{left[now]}:{left[now] + size[now]}]`',
        'expand_list = [': '马拉车要处理奇偶：在每个字符后插入 `#`，并加哨兵 `!`、`@`',
        "expand_list[-1] = '@'": '最后一个 `#` 换成哨兵 `@`：`expand_list` = `{expand_list}`',
        'mid = 0': '`mid`、`right`：覆盖最靠右的回文串的中心和右边界',
        'if index < right': lambda S, B, ret: (f'`index = {S.index} < right = {S.right}`：在已知回文串里 → `f[{S.index}]` 先借对称位置 `{2 * S.mid - S.index}` 的值，再与 `right - index` 取小' if S.index < S.right
                                               else f'`index = {S.index} >= right = {S.right}`：不在已知回文串里 → 半径从 1 开始'),
        'f.append(min(f[2 * mid - index], right - index))': '借来的初始半径 `f[{index}]` = =={f[index]}==',
        'f.append(1)': '初始半径 `f[{index}] = 1`（只有自己）',
        'while expand_list[index - f[index]] == expand_list[index + f[index]]': lambda S, B, ret: (f"`{S.expand_list[S.index - S.f[S.index]]}`（位置 {S.index - S.f[S.index]}）与 `{S.expand_list[S.index + S.f[S.index]]}`（位置 {S.index + S.f[S.index]}）" +
                                                                                                    (f' 相等 → `f[{S.index}]` 扩大到 {S.f[S.index] + 1}' if S.expand_list[S.index - S.f[S.index]] == S.expand_list[S.index + S.f[S.index]] else ' 不等 → 扩展结束，`f[{}]` = =={}=='.format(S.index, S.f[S.index]))),
        'f[index] += 1': '`f[{index}]` → {f[index]}',
        'if right < index + f[index]': lambda S, B, ret: (f'`right = {S.right} < index + f[index] = {S.index + S.f[S.index]}`：这个回文串伸得更远 → `mid = {S.index}`，`right = {S.index + S.f[S.index]}`' if S.right < S.index + S.f[S.index]
                                                         else f'`right = {S.right}` 已经够远，不更新'),
        'right = index + f[index]': '`right` → =={right}==',
        'mid = index': '`mid` → =={mid}==',
        'if mid_in_expand - f[mid_in_expand] + 1 <= left_in_expand': _judge,
        'return res': '每个子树是否回文：==`{ret}`==',
    },
    cards=dict(
        one_liner='子树的 dfs 串是整棵树 dfs 串的一段，马拉车 O(1) 判回文',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['树根是 `0`，`parent[i]` 是父节点，`s[i]` 是节点 `i` 的字符',
                 '`dfs(x)`：按编号升序遍历孩子，再把 `s[x]` 加到末尾；对每个 `i` 判断 `dfs(i)` 的串是否回文',
                 '本视频：`parent=[-1,0,0,1]`，`s="abba"`'],
        quote='对于任意节点x，通过dfs(x)形成的dfsStr必然是通过dfs(0)形成的dfsStr的一个子串。换言之，问题就转化成了对于dfs(0)生成的字符串dfsStr，其中某个特定子串是否为回文串的问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dfs(x)` 的字符串长度 = 子树节点数 `size[x]`，起点 `left[x]`',
              '先序 + 孩子降序建的串，正好是后序串的镜像，回文性质不变',
              '先在 `dfs_list` 里插入 `#` 变成奇长度，再用马拉车求每个中心的半径 `f`',
              '子串的中心在 `(left_in_expand + right_in_expand) // 2`；`f` 盖住左端就是回文'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：偶数长度回文要靠插入 `#` 处理；`left_in_expand = left * 2 + 1`',
                 '原文为 Python 2 写法，`print now, size[now]` 已改为 `print(now, size[now])`',
                 '对比灵神：灵神直接建后序串并记时间戳；这里先序、孩子降序建串，是后序串的镜像，回文判断等价',
                 '同样需要注意：递归深度可能达到 `n`，视频里只用 `n = 4`'],
    ),
)
