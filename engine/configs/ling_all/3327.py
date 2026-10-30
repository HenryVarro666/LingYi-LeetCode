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
    x = S.get('x')
    if isinstance(x, int) and 'dfsStr' in S and 'halfLen' not in S and 'l' not in S:
        return {x: 'yellow'}
    l, r = S.get('l'), S.get('r')
    if 'nodes' in S and l is not None and r is not None:
        for k, (a, b) in enumerate(S['nodes']):
            if (a, b) == (l, r):
                return {k: 'pink'}
    return {}


def _tags(S):
    nd, t = S.get('nodes'), S.get('time', 0)
    if nd is None:
        return {}
    out = {}
    for k, (a, b) in enumerate(nd):
        if b > 0 and (b <= t or 'halfLen' in S or 'l' in S):
            out[k] = f'[{a},{b})'
        elif b == 0 and a < t:
            out[k] = f'[{a},…'
    return out


def _tcol(S, i, v):
    h, ii = S.get('hl'), S.get('i')
    if ii is None or h is None or 'boxM' not in S:
        return None
    if i == ii:
        return 'blue'
    if S.get('_line') in (55, 56, 57) and 0 <= ii - h and ii + h < len(S['t']) and i in (ii - h, ii + h):
        return 'green' if S['t'][ii - h] == S['t'][ii + h] else 'red'
    return None


def _hcol(S, i, v):
    if 'boxM' not in S or S.get('i') is None:
        return None
    if S.get('l') is not None:
        return 'pink' if i == S['l'] + S['r'] + 1 else None
    if i == S['i']:
        return 'blue'
    if i == S['boxM'] and S['boxM'] > 0:
        return 'green'
    return None


def _formula(S):
    if 'halfLen' in S and S.get('l') is None:
        return '`halfLen[i]`：以 `t[i]` 为中心的回文半径；`boxM / boxR`：已知覆盖最靠右的回文串'
    if S.get('l') is not None:
        return f"子树 `[l, r) = [{S['l']}, {S['r']})` 是 `dfsStr` 的子串，回文中心在 `t[l + r + 1]` = `t[{S['l'] + S['r'] + 1}]`"
    return '后序遍历：先孩子、后自己；子树的字符串 = `dfsStr` 里的一段连续子串'


CONFIG = dict(
    num=3327, title='判断 DFS 字符串是否是回文串', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='DFS 时间戳（后序）+ Manacher 算法',
    tags=['链表树与回溯', '字符串', '难度分 2454'],
    code='''
class Solution:
    def findAnswer(self, parent: List[int], s: str) -> List[bool]:
        n = len(parent)
        g = [[] for _ in range(n)]
        for i in range(1, n):
            p = parent[i]
            # 由于 i 是递增的，所以 g[p] 必然是有序的，下面无需排序
            g[p].append(i)

        # dfsStr 是后序遍历整棵树得到的字符串
        dfsStr = [''] * n
        # nodes[i] 表示子树 i 的后序遍历的开始时间戳和结束时间戳+1（左闭右开区间）
        nodes = [[0, 0] for _ in range(n)]
        time = 0

        def dfs(x: int) -> None:
            nonlocal time
            nodes[x][0] = time
            for y in g[x]:
                dfs(y)
            dfsStr[time] = s[x]  # 后序遍历
            time += 1
            nodes[x][1] = time
        dfs(0)

        # Manacher 模板
        # 将 dfsStr 改造为 t，这样就不需要讨论 n 的奇偶性，因为新串 t 的每个回文子串都是奇回文串（都有回文中心）
        # dfsStr 和 t 的下标转换关系：
        # (dfsStr_i+1)*2 = ti
        # ti/2-1 = dfsStr_i
        # ti 为偶数，对应奇回文串（从 2 开始）
        # ti 为奇数，对应偶回文串（从 3 开始）
        t = '#'.join(['^'] + dfsStr + ['$'])

        # 定义一个奇回文串的回文半径=(长度+1)/2，即保留回文中心，去掉一侧后的剩余字符串的长度
        # halfLen[i] 表示在 t 上的以 t[i] 为回文中心的最长回文子串的回文半径
        # 即 [i-halfLen[i]+1,i+halfLen[i]-1] 是 t 上的一个回文子串
        halfLen = [0] * (len(t) - 2)
        halfLen[1] = 1
        # boxR 表示当前右边界下标最大的回文子串的右边界下标+1
        # boxM 为该回文子串的中心位置，二者的关系为 r=mid+halfLen[mid]
        boxM = boxR = 0
        for i in range(2, len(halfLen)):
            hl = 1
            if i < boxR:
                # 记 i 关于 boxM 的对称位置 i'=boxM*2-i
                # 若以 i' 为中心的最长回文子串范围超出了以 boxM 为中心的回文串的范围（即 i+halfLen[i'] >= boxR）
                # 则 halfLen[i] 应先初始化为已知的回文半径 boxR-i，然后再继续暴力匹配
                # 否则 halfLen[i] 与 halfLen[i'] 相等
                hl = min(halfLen[boxM * 2 - i], boxR - i)
            # 暴力扩展
            # 算法的复杂度取决于这部分执行的次数
            # 由于扩展之后 boxR 必然会更新（右移），且扩展的的次数就是 boxR 右移的次数
            # 因此算法的复杂度 = O(len(t)) = O(n)
            while t[i - hl] == t[i + hl]:
                hl += 1
                boxM, boxR = i, i + hl
            halfLen[i] = hl

        # t 中回文子串的长度为 hl*2-1
        # 由于其中 # 的数量总是比字母的数量多 1
        # 因此其在 dfsStr 中对应的回文子串的长度为 hl-1
        # 这一结论可用在 isPalindrome 中

        # 判断左闭右开区间 [l,r) 是否为回文串  0<=l<r<=n
        # 根据下标转换关系得到 dfsStr 的 [l,r) 子串在 t 中对应的回文中心下标为 l+r+1
        # 需要满足 halfLen[l + r + 1] - 1 >= r - l，即 halfLen[l + r + 1] > r - l
        def isPalindrome(l: int, r: int) -> bool:
            return halfLen[l + r + 1] > r - l

        return [isPalindrome(l, r) for l, r in nodes]
''',
    call='Solution().findAnswer([-1, 0, 0, 1], "abba")',
    expect=[True, False, True, True],
    views=[
        dict(type='text', fn=_formula, size=22, h=50),
        dict(_tree_view(CH, 0, _colors, '树（黄 = 正在 dfs；标注 = 子树在 dfsStr 里的 [开始, 结束)）', tags=_tags, lab=lambda u: f'{u}:' + 'abba'[u]), h=300),
        dict(type='array', var='dfsStr', label='dfsStr（后序遍历得到的字符）', h=100, cell=60, index=False),
        dict(type='array', var='t', label='t（蓝 = 中心 i，绿/红 = 正在比较的一对）', h=112, cell=60, color=_tcol),
        dict(type='array', var='halfLen', label='halfLen（蓝 = i，绿 = boxM，粉 = 判断时用到的中心）', h=112, cell=60, color=_hcol),
    ],
    watch=['time', 'i', 'hl', ('boxM', 'boxM', 'green'), ('boxR', 'boxR', 'orange'), 'l', 'r'],
    max_steps=90,
    skip=['for i in range(1, n)', 'p = parent[i]', 'g[p].append', 'for y in g[x]', 'nonlocal time', 'nodes = [[0, 0]', 'hl = 1', 'halfLen[1] = 1', 'time += 1', 'nodes[x][0] = time', 'for i in range(2, len(halfLen))', 'hl += 1', 'boxM, boxR = i, i + hl', 'return [isPalindrome', 'time = 0', 'dfsStr = ['],
    captions={
        'n = len(parent)': '`n = {n}` 个节点；孩子列表 `g` 按编号升序建好（`i` 递增，无需排序）',
        'g = [[] for': '`g[p]`：节点 `p` 的孩子（已按编号升序）',
        'dfsStr = [': '`dfsStr`：整棵树后序遍历的字符串，先留空',
        'time = 0': '`time` 是时间戳；`nodes[i] = [开始, 结束)` 记下子树 `i` 在 `dfsStr` 里的区间',
        'dfs(0)': '`dfsStr` 存后序字符，`time` 是时间戳，`nodes[i]` 记子树 `i` 的 `[开始, 结束)`；从根 `0` 后序遍历：先孩子，再自己',
        'nodes[x][0] = time': '进入 `{x}`：开始时间戳 `nodes[{x}][0]` = ==`{time}`==',
        'dfsStr[time] = s[x]': '节点 `{x}` 的开始时间戳是 `nodes[{x}][0]` = {nodes[x][0]}；孩子都处理完，轮到自己：`dfsStr[{time}] = s[{x}]` = ==`{s[x]}`==（后序）',
        'time += 1': '`time` → {time}',
        'nodes[x][1] = time': '`time` 加 1 后离开 `{x}`：子树区间 ==`[{nodes[x][0]}, {nodes[x][1]})`==（左闭右开）',
        't = ': '`t` = 在字符间插入 `#`，再加首尾哨兵：`{t}`——这样所有回文串都是奇回文串',
        'halfLen = [0]': '`halfLen[i]`：以 `t[i]` 为中心的回文半径，先全填 0',
        'boxM = boxR = 0': '`boxM`、`boxR`：目前覆盖最靠右的回文串的中心和右边界+1',
        'for i in range(2, len(halfLen))': '依次求每个中心 `i = {i}` 的回文半径',
        'if i < boxR': lambda S, B, ret: (f'求中心 `i = {S.i}`：`i = {S.i} < boxR = {S.boxR}`：`i` 在已知回文串里 → 可以借对称点 `{S.boxM * 2 - S.i}` 的结果' if S.i < S.boxR
                                          else f'求中心 `i = {S.i}`：`i = {S.i} >= boxR = {S.boxR}`：不在任何已知回文串里，只能从半径 1 起暴力扩展'),
        'hl = min(halfLen[boxM * 2 - i], boxR - i)': '对称点 `{boxM * 2 - i}` 的半径 `{halfLen[boxM * 2 - i]}` 与 `boxR - i = {boxR - i}` 取小：起始 `hl` = =={hl}==',
        'while t[i - hl] == t[i + hl]': lambda S, B, ret: (f"`t[{S.i - S.hl}] = {S.t[S.i - S.hl]}` 与 `t[{S.i + S.hl}] = {S.t[S.i + S.hl]}` " + (f'相等 → 半径扩大到 {S.hl + 1}，`boxM = {S.i}`，`boxR` 右移到 {S.i + S.hl + 1}（每次扩展都右移 `boxR`，总共 `O(n)`）' if S.t[S.i - S.hl] == S.t[S.i + S.hl] else '不等 → 扩展结束')),
        'hl += 1': '半径 `hl` → {hl}',
        'boxM, boxR = i, i + hl': '右边界更远了：`boxM = {boxM}`，`boxR` = ==`{boxR}`==（每次扩展都会右移 `boxR`，所以总共 `O(n)`）',
        'halfLen[i] = hl': '`halfLen[{i}] = {hl}`：以 `t[{i}]` 为中心的最长回文，半径 {hl}',
        'return halfLen[l + r + 1] > r - l': lambda S, B, ret: (f"子串 `dfsStr[{S.l}:{S.r}]` 的中心在 `t[{S.l + S.r + 1}]`：`halfLen = {S.halfLen[S.l + S.r + 1]}` " +
                                                              (f"> 长度 {S.r - S.l}" if ret else f"<= 长度 {S.r - S.l}") + (' → ==是回文==' if ret else ' → ==不是回文==')),
        'return [isPalindrome': '把每个子树的区间 `[l, r)` 交给 `isPalindrome`，得到答案：==`{ret}`==',
    },
    cards=dict(
        one_liner='子树字符串是整棵树后序串的子串，Manacher 一次扫描判回文',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['树的根是 `0`，`parent[i]` 是父节点，`s[i]` 是节点 `i` 的字符',
                 '`dfs(x)`：依次对孩子（编号升序）`dfs`，再把 `s[x]` 加到 `dfsStr` 末尾',
                 '对每个 `i`，`dfs(i)` 得到的字符串是回文吗？本视频：`parent=[-1,0,0,1]`，`s="abba"`'],
        quote='构造 dfsStr 的过程是后序遍历。子树的后序遍历字符串，是整棵树的后序遍历字符串的子串。……在 dfsStr 上跑 Manacher 算法，这样就可以 O(1) 判断任意子串是否回文了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['后序遍历一次，同时记下每个节点的 `[开始, 结束)` 时间戳',
              '子树 `i` 的字符串就是 `dfsStr[开始:结束]`',
              '在 `dfsStr` 上跑 Manacher，得到每个中心的回文半径',
              '区间 `[l, r)` 的回文中心在 `t[l + r + 1]`，只要 `halfLen > r - l` 就是回文'],
        summary=['时间 `O(n)`：每次暴力扩展都会右移 `boxR`',
                 '易错：区间是左闭右开；`t` 里的中心下标是 `l + r + 1`',
                 '后序遍历 + 时间戳是「子树 = 连续区间」的通用技巧（先序同理）',
                 '递归深度可能到 `n`，真正提交时要注意递归栈（视频里 `n = 4`）',
                 '孩子列表按 `i` 递增建立，天然是升序，不用排序'],
    ),
)
