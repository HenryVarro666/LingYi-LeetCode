VALS = [6, 2, 13, 1, 4, 9, 15]
QS = [16, 2, 5]


def _merge(S):
    return S.get('_line', 0) >= 17 and 'p' in S


def _tree_color(S, nd):
    if _merge(S):
        return 'yellow' if nd.val == S.get('num') and S.get('_line') in (20, 21, 22, 24, 25) else None
    return 'green' if nd.val in (S.get('num_list') or []) else None


COLS = sorted(set(VALS) | set(QS))


def _draw_merge(cv, S, B, box, T):
    """按数值把节点值（上）和询问（下）放在同一条数轴上：两个有序序列一起往右扫"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '同一条数轴：上 = num_list（节点值），下 = sorted_queries（询问值#原下标）', 22,
            T['muted'], bold=True)
    nl = S.get('num_list') or []
    sq = S.get('sorted_queries') or []
    merge = _merge(S)
    p = S.get('p', 0) if merge else 0
    num = S.get('num') if merge and S.get('_line') in (20, 21, 22, 24, 25) else None
    pre = S.get('pre') if merge else None
    cw = min(110, (x1 - x0 - 120) / len(COLS))
    sx = x0 + 100 + ((x1 - x0 - 120) - cw * len(COLS)) / 2

    def X(v):
        return sx + COLS.index(v) * cw + cw / 2
    ya, yb = y0 + 96, y0 + 182
    cv.text((sx - 20, ya), '节点', 20, T['muted'], anchor='rm', bold=True)
    cv.text((sx - 20, yb), '询问', 20, T['muted'], anchor='rm', bold=True)
    cv.line([(sx, (ya + yb) / 2), (sx + cw * len(COLS), (ya + yb) / 2)], T['border'], 2)
    for v in VALS:
        have = v in nl
        fill = T['panel2']
        if v == num:
            fill = T['yellow']
        elif merge and v == pre and pre != -1:
            fill = T['blue']
        elif have and not merge:
            fill = T['green']
        r = 24
        cv.d.ellipse((X(v) - r, ya - r, X(v) + r, ya + r), fill=fill if have else T['bg'],
                     outline=T['border'] if have else T['dim'], width=2)
        cv.text((X(v), ya), v, 20, T['bg'] if fill in (T['yellow'], T['blue'], T['green']) else
                (T['text'] if have else T['dim']), anchor='mm', bold=True)
    if num is not None:
        cv.text((X(num), ya - 30), 'num', 18, T['yellow'], anchor='mb', bold=True)
    if merge and pre is not None and pre != -1:
        cv.text((X(pre), ya - 30), 'pre', 18, T['blue'], anchor='mb', bold=True)
    for k, (q, idx) in enumerate(sq):
        done = merge and k < p
        cur = merge and k == p
        w, h = 74, 40
        cv.rect((X(q) - w / 2, yb - h / 2, X(q) + w / 2, yb + h / 2), fill=T['green'] if done else T['panel2'],
                outline=T['cyan'] if cur else T['border'], width=3 if cur else 1, r=8)
        cv.text((X(q), yb), f'{q}#{idx}', 18, T['bg'] if done else T['text'], anchor='mm', bold=True, mono=True)
        if cur:
            cv.tri_up(X(q), yb + h / 2 + 6, 9, T['cyan'])
            cv.text((X(q), yb + h / 2 + 20), 'p', 18, T['cyan'], anchor='mt', bold=True)


def _text(S):
    if not _merge(S):
        return '中序遍历：二叉搜索树 → ==按节点值排好序==的 `num_list`'
    ln = S['_line']
    if ln in (29, 30, 31, 33):
        return f"所有节点都比剩下的询问小：答案 `[pre = {S['pre']}, -1]`"
    if 'num' not in S:
        return '`pre`：上一个节点值（初始 -1）'
    return f"`pre = {S['pre']}` < 询问 < `num = {S['num']}` → 答案 `[pre, num]`；询问 == num → `[num, num]`"


def _cap_w1(S, B, ret):
    p, n, sq, num = B.p, B.n, B.sorted_queries, B.num
    if p < n and sq[p][0] < num:
        return f'询问 `{sq[p][0]}` < `num = {num}`：它夹在 `pre = {B.pre}` 和 `{num}` 之间'
    if p >= n:
        return '询问都处理完了'
    if sq[p][0] == num:
        return f'询问 `{sq[p][0]}` 不小于 `{num}`（相等，交给下一个 while）'
    return f'询问 `{sq[p][0]}` > `{num}` → 等更大的节点值'


def _cap_w2(S, B, ret):
    p, n, sq, num = B.p, B.n, B.sorted_queries, B.num
    if p < n and sq[p][0] == num:
        return f'询问 `{sq[p][0]}` == `num`：树里正好有这个值'
    return '没有等于 `num` 的询问'


CONFIG = dict(
    num=2476, title='二叉搜索树最近节点查询', difficulty='Medium', category='二分查找',
    author='yiduobo', technique='中序遍历 + 询问排序后双指针',
    tags=['字节30天'],
    code='''
class Solution(object):
    def closestNodes(self, root, queries):
        n = len(queries)
        res = [[-1, -1] for _ in range(n)]
        sorted_queries = sorted([q, index] for index, q in enumerate(queries))
        num_list = []

        def dfs(now):
            if now.left:
                dfs(now.left)
            num_list.append(now.val)
            if now.right:
                dfs(now.right)

        dfs(root)

        pre = -1
        p = 0

        for num in num_list:
            while p < n and sorted_queries[p][0] < num:
                res[sorted_queries[p][1]] = [pre, num]
                p += 1
            while p < n and sorted_queries[p][0] == num:
                res[sorted_queries[p][1]] = [num, num]
                p += 1
            pre = num

        while p < n:
            res[sorted_queries[p][1]] = [pre, -1]
            p += 1

        return res
''',
    call=f'Solution().closestNodes(Tr({VALS}), {QS})',
    expect=[[15, -1], [2, 2], [4, 6]],
    skip=['n = len(queries)', 'if now.left', 'if now.right', 'p += 1', 'pre = num', 'p = 0',
          'while p < n and sorted_queries[p][0] == num'],
    views=[
        dict(type='tree', label='二叉搜索树（绿 = 已加入 num_list）', h=240, pointers={'now': 'yellow'},
             color=_tree_color),
        dict(type='custom', draw=_draw_merge, h=240),
        dict(type='text', fn=_text, h=50, size=23),
        dict(type='map', var=lambda S: {i: v for i, v in enumerate(S['res'])} if 'res' in S else None,
             label='res（按原下标存）', fmt=lambda k, v: f'res[{k}] = [{v[0]},{v[1]}]', h=96),
    ],
    watch=[('pre', 'pre', 'blue'), ('num', 'num', 'yellow'), ('p', 'p', 'cyan')],
    captions={
        'res = [[-1, -1]': '`res` 先全填 `[-1, -1]`，按询问的==原下标==回填',
        'sorted_queries = sorted(': '把询问==连同原下标==一起排序：`{sorted_queries}`',
        'num_list = []': '`num_list` 收集中序遍历结果',
        'dfs(now.left)': lambda S, B, r: f'`{B.now.val}` 有左孩子 → 先遍历左子树',
        'num_list.append(now.val)': '记录 `{now.val}` → `num_list = {num_list}`',
        'dfs(now.right)': lambda S, B, r: f'`{B.now.val}` 有右孩子 → 再遍历右子树',
        'dfs(root)': '中序遍历整棵树（递归前先判断孩子是否存在）',
        'pre = -1': '`num_list` 已有序，询问也有序 → ==利用单调性==一起往右扫；`pre` 是上一个节点值',
        'for num in num_list': lambda S, B, r: (f'下一个节点值 `num = {S.num}`（`pre = {S.pre}`）'
                                                if 'num' not in B or S.num != B.num else '节点值扫完了'),
        'while p < n and sorted_queries[p][0] < num': _cap_w1,
        'res[sorted_queries[p][1]] = [pre, num]': lambda S, B, r: (
            f'第 {B.sorted_queries[B.p][1]} 个询问：`res[{B.sorted_queries[B.p][1]}] = [{B.pre}, {B.num}]`'),
        'while p < n and sorted_queries[p][0] == num': _cap_w2,
        'res[sorted_queries[p][1]] = [num, num]': lambda S, B, r: (
            f'询问 `{B.sorted_queries[B.p][0]}` ==等于== `num`：树里正好有这个值 → '
            f'`res[{B.sorted_queries[B.p][1]}] = [{B.num}, {B.num}]`'),
        'while p < n:': lambda S, B, r: (f'还剩询问 `{B.sorted_queries[B.p][0]}`：比所有节点都大' if B.p < B.n
                                         else '所有询问都回答完了'),
        'res[sorted_queries[p][1]] = [pre, -1]': lambda S, B, r: (
            f'没有 ≥ 它的节点：`res[{B.sorted_queries[B.p][1]}] = [{B.pre}, -1]`'),
        'return res': '返回 `{ret}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='中序遍历得到有序数组，把询问也排好序，两个有序序列一起往右扫',
        complexity='时间 `O(n + q log q)`，空间 `O(n + q)`',
        problem=['给二叉搜索树 `root` 和询问数组 `queries`，对每个 `q` 求 `[min, max]`',
                 '`min`：树中 ==≤ q 的最大值==；`max`：树中 ==≥ q 的最小值==；不存在用 `-1`',
                 '示例：`[6,2,13,1,4,9,15,null,…,14]`，`[2,5,16]` → `[[2,2],[4,6],[15,-1]]`',
                 '本视频：`[6,2,13,1,4,9,15]`，询问 `[16,2,5]` → `[[15,-1],[2,2],[4,6]]`'],
        quote='对这棵树进行一趟中序遍历就可以得到一个按照节点值排好序的数组。接下来只需要在这个数组中二分每个查询，或者==将查询排序后利用单调性==求出每个询问对应的结果就行了。',
        quote_src='—— yiduobo 题解',
        idea=['询问排序时带上原下标：`[q, index]`，答案按原下标写回 `res`',
              '扫到节点值 `num`：所有 `< num` 的询问答案都是 `[pre, num]`，`== num` 的是 `[num, num]`',
              '节点扫完还剩的询问：比所有节点都大 → `[pre, -1]`'],
        result='`[[15,-1],[2,2],[4,6]]` ✓（按原询问顺序）',
        summary=['时间 `O(n + q log q)`：中序 `O(n)` + 询问排序；合并扫描 `O(n + q)`',
                 '离线做法：先把询问排序，再和有序数组==双指针合并==（原文也提到可以直接二分）',
                 '易错：排序会打乱顺序，必须记住原下标再写回',
                 '原文为 Python 2 风格，仅删去 docstring 和 TreeNode 定义注释，代码未改'],
    ),
)
