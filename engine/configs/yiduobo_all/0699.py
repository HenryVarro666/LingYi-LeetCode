def _tree(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '线段树（f 当堆存：p 的孩子是 2p+1、2p+2）绿框 = 全覆盖', 22, T['muted'], bold=True)
    f, fl, mr = S.get('f'), S.get('same_flag'), S.get('max_r')
    if f is None or fl is None or mr is None:
        return
    inner = S.get('_inner') or {}
    cur = S.get('pos') if 'pos' in inner else None
    qi = S.get('i') if 'i' in inner else None
    qj = S.get('j') if 'j' in inner else None
    nodes = []  # (p, l, r, depth, xc)

    def build(p, l, r, d):
        if p >= len(f):
            return
        nodes.append((p, l, r, d))
        if l < r:
            m = (l + r) >> 1
            build(2 * p + 1, l, m, d + 1)
            build(2 * p + 2, m + 1, r, d + 1)
    build(0, 0, mr - 1, 0)
    depth = max(n[3] for n in nodes) + 1
    W = x1 - x0 - 60
    slot = W / mr
    top, gapy = y0 + 140, min(150, (y1 - y0 - 240) / max(1, depth - 1))
    nw, nh = min(96, slot * 0.8), 62
    pos = {}
    for p, l, r, d in nodes:
        pos[p] = (x0 + 30 + (l + r + 1) / 2 * slot, top + d * gapy)
    for p, l, r, d in nodes:
        for c in (2 * p + 1, 2 * p + 2):
            if c in pos:
                cv.line([(pos[p][0], pos[p][1] + nh / 2), (pos[c][0], pos[c][1] - nh / 2)], T['border'], 3)
    for p, l, r, d in nodes:
        X, Y = pos[p]
        inq = qi is not None and not (r < qi or l > qj)
        flag = fl[p]
        fill = T['yellow'] if p == cur else T['panel2']
        out = T['green'] if flag else (T['blue'] if inq else T['border'])
        cv.rect((X - nw / 2, Y - nh / 2, X + nw / 2, Y + nh / 2), fill=fill, r=12, outline=out, width=5 if (flag or inq) else 2)
        cv.text((X, Y), f[p], 30, T['bg'] if p == cur else T['text'], anchor='mm', bold=True)
        cv.text((X, Y + nh / 2 + 4), f'[{l},{r}]', 19, T['muted'], anchor='mt', mono=True)
        cv.text((X - nw / 2 + 4, Y - nh / 2 - 2), p, 16, T['dim'], anchor='lb', mono=True)
    if qi is not None:
        cv.text((x0 + 18, y0 + 62), f'本次操作区间 [i, j] = [{qi}, {qj}]（蓝框 = 与其相交）', 22, T['blue'], anchor='lm', bold=True)


CONFIG = dict(
    num=699, title='掉落的方块', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='离散化 + 线段树（区间最大值 + 区间覆盖）',
    tags=['线段树'],
    code='''
class Solution(object):
    def fallingSquares(self, positions):

        pos_set = set()
        for start, height in positions:
            end = start + height - 1
            pos_set.add(start)
            pos_set.add(end)

        pos_dict = {}
        for index, pos in enumerate(sorted(list(pos_set))):
            pos_dict[pos] = index

        pos_list = []
        for start, height in positions:
            end = start + height - 1
            pos_list.append([pos_dict[start], pos_dict[end], height])

        max_r = 1
        level = 0
        while max_r < len(pos_set):
            level += 1
            max_r += max_r

        f = [0] * (max_r + max_r - 1)
        same_flag = [True] * (max_r + max_r - 1)
        res = []
        for start, end, height in pos_list:
            now_height = self.get(0, 0, max_r - 1, start, end, f, same_flag)
            self.put(0, 0, max_r - 1, start, end, f, same_flag, now_height + height)
            res.append(self.get(0, 0, max_r - 1, 0, max_r - 1, f, same_flag))

        return res

    def get(self, pos, l, r, i, j, f, same_flag):
        if l == i and j == r:
            return f[pos]

        if same_flag[pos]:
            return f[pos]
        
        mid = (l + r) >> 1
        if j <= mid:
            return self.get(pos + pos + 1, l, mid, i, j, f, same_flag)
        elif i > mid:
            return self.get(pos + pos + 2, mid + 1, r, i, j, f, same_flag)
        else:
            return max(self.get(pos + pos + 1, l, mid, i, mid, f, same_flag), self.get(pos + pos + 2, mid + 1, r, mid + 1, j, f, same_flag))
    
    def put(self, pos, l, r, i, j, f, same_flag, val):
        if l == i and j == r:
            f[pos] = val
            same_flag[pos] = True
            return
        
        mid = (l + r) >> 1
        if same_flag[pos]:
            self.put(pos + pos + 1, l, mid, l, mid, f, same_flag, f[pos])
            self.put(pos + pos + 2, mid + 1, r, mid + 1, r, f,same_flag, f[pos])
            same_flag[pos] = False

        f[pos] = max(val, f[pos])

        if j <= mid:
            self.put(pos + pos + 1, l, mid, i, j, f, same_flag, val)
        elif i > mid:
            self.put(pos + pos + 2, mid + 1, r, i, j, f, same_flag, val)
        else:
            self.put(pos + pos + 1, l, mid, i, mid, f, same_flag, val)
            self.put(pos + pos + 2, mid + 1, r, mid + 1, j, f, same_flag, val)
        
        if f[pos + pos + 1] == f[pos + pos + 2] and same_flag[pos + pos + 1] and same_flag[pos + pos + 2]:
            same_flag[pos] = True
''',
    call='Solution().fallingSquares([[1, 2], [2, 3]])',
    expect=[2, 5],
    views=[
        dict(type='text', h=64, fn=lambda S: ('离散化：坐标 → 序号 `' + str(S['pos_dict']) + '`' if 'pos_dict' in S and 'pos_list' not in S else ('每个方块 [起点序号, 终点序号, 高度] = `' + str(S['pos_list']) + '`' if 'pos_list' in S else '')) if 'pos_dict' in S else ''),
        dict(type='custom', draw=_tree, h=400),
        dict(type='calls', h=130, hide=('fallingSquares',)),
    ],
    watch=['start', 'end', 'height', ('now_height', 'now_height', 'yellow'), ('res', 'res', 'green')],
    max_steps=68,
    skip=[53, 54, 'pos_set.add', 'level += 1', 'level = 0', 'max_r = 1', 'pos_dict[pos] = index', 'end = start + height - 1'],
    captions={
        'pos_set = set()': '坐标范围太大（到 10^8），先==离散化==：只关心相对大小，把用到的坐标收集起来',
        'for index, pos in enumerate': '排序后第 `{index}` 小的坐标 `{pos}` → 序号 `{index}`',
        'pos_list.append': '这个方块覆盖序号 `[{pos_dict[start]}, {pos_dict[end]}]`，高度 `{height}`',
        'while max_r < len(pos_set)': '线段树叶子数补成 2 的幂：`max_r` = {max_r}',
        'f = [0] * (max_r + max_r - 1)': '`f` 存各节点区间的最大高度，共 `{len(f)}` 个节点；`same_flag` = 整段高度一致',
        'res = []': '`res` 记录每个方块落下后的整体最大高度',
        'for start, end, height in pos_list': '落下方块：覆盖序号 `[{start}, {end}]`，高度 `{height}`',
        'now_height = self.get': '查询 `[{start}, {end}]` 里现有的最高高度 = =={now_height}==，方块会落在它上面',
        'self.put(0, 0, max_r - 1, start, end': '把 `[{start}, {end}]` 全部置为 `{now_height} + {height} = {now_height + height}`',
        'res.append': '整棵树的最大值 `f[0]` = =={f[0]}==，加入答案 `res`',
        'return res': '每个方块落下后的最高高度：`{res}`',
        'if l == i and j == r': lambda S, B, ret: ('节点区间 `[{},{}]` 与查询/更新区间完全重合 → 不用再往下'.format(S.l, S.r) if S.l == S.i and S.j == S.r else '节点区间 `[{},{}]` 比 `[{},{}]` 大，要继续往下分'.format(S.l, S.r, S.i, S.j)),
        'return f[pos]': '直接返回 `f[{pos}]` = =={f[pos]}==',
        39: lambda S, B, ret: ('`same_flag[{}]` 为真：这段高度全一样，直接用 `f[{}]` = {}'.format(S.pos, S.pos, S.f[S.pos]) if S.same_flag[S.pos] else '这段高度不一致，要往下查孩子'),
        'mid = (l + r) >> 1': '中点 `mid` = {mid}，左孩子管 `[{l},{mid}]`，右孩子管 `[{mid+1},{r}]`',
        'if j <= mid': lambda S, B, ret: ('`j={}` ≤ `mid={}`：区间全在左半边'.format(S.j, S.mid) if S.j <= S.mid else '`j={}` > `mid={}`：不只在左半边'.format(S.j, S.mid)),
        'elif i > mid': lambda S, B, ret: ('`i={}` > `mid={}`：区间全在右半边'.format(S.i, S.mid) if S.i > S.mid else '`i={}` ≤ `mid={}`：横跨中点，拆成两段'.format(S.i, S.mid)),
        'return self.get(pos + pos + 1': '去左孩子 `{pos+pos+1}` 查',
        'return self.get(pos + pos + 2': '去右孩子 `{pos+pos+2}` 查',
        'return max(self.get': '横跨中点：左右各查一段，取较大值',
        'f[pos] = val': '整段置为 `{val}`，`same_flag[{pos}] = True`：打上==全覆盖标记==，不再往下传',
        57: lambda S, B, ret: ('`same_flag[{}]` 为真：这段整段都是 {}，先要拆开'.format(S.pos, S.f[S.pos]) if S.same_flag[S.pos] else '这段已经拆开，直接往下'),
        'self.put(pos + pos + 1, l, mid, l, mid': '这段原本是全覆盖的 → 先把旧高度 `{f[pos]}` ==下放==给左孩子',
        'self.put(pos + pos + 2, mid + 1, r, mid + 1, r': '再下放给右孩子',
        'same_flag[pos] = False': '下放完，`same_flag[{pos}]` 变假：这段不再保证一致',
        'f[pos] = max(val, f[pos])': '`f[{pos}] = max({val}, {B.f[pos]}) = {f[pos]}`：新值可能没有盖住旧最大值所在位置',
        'self.put(pos + pos + 1, l, mid, i, j': '更新区间全在左半边 → 递归左孩子',
        'self.put(pos + pos + 2, mid + 1, r, i, j': '更新区间全在右半边 → 递归右孩子',
        'self.put(pos + pos + 1, l, mid, i, mid': '横跨中点：左半边更新 `[{i},{mid}]`',
        'self.put(pos + pos + 2, mid + 1, r, mid + 1, j': '右半边更新 `[{mid+1},{j}]`',
        'if f[pos + pos + 1] == f[pos + pos + 2]': lambda S, B, ret: ('两个孩子值相同且都全覆盖 → `same_flag[{}]` 置真（合并标记）'.format(S.pos) if S.f[2*S.pos+1] == S.f[2*S.pos+2] and S.same_flag[2*S.pos+1] and S.same_flag[2*S.pos+2] else '孩子不是「值相同且都全覆盖」→ 保持 `same_flag[{}]` = 假'.format(S.pos)),
    },
    cards=dict(
        one_liner='方块落在区间最高处：先查区间最大值，再整段覆盖成新高度',
        complexity='离散化排序 `O(n log n)`；每个方块 `O(log n)`；空间 `O(n)`',
        problem=['`positions[i] = [left, side]`：边长 `side` 的方块，左边缘在 `left`，依次落下',
                 '每个方块停在==下方最高的方块上==；求每个方块落下后的最高高度',
                 '示例：`[[1,2],[2,3]]` → `[2,5]`'],
        quote='对于一个下落的方块，其必然是落在left到right这一段中最高的方块上面，因此我们可以将这个问题转化一下，将其视为给出高度height以及区间[left, right]，找到区间中最大的数max，然后将区间[left, right]中的所有数置为max + height。',
        quote_src='—— yiduobo 题解原文',
        idea=['问题 = 区间求最大值 + 区间整段赋值，经典线段树',
              '坐标到 10^8 太大：只关心相对位置，==离散化==成 0,1,2,…',
              '整段赋值不逐点改：节点打上 `same_flag` 全覆盖标记，用到时再==下放=='],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：更新时 `f[pos] = max(val, f[pos])`，旧最大值所在位置可能没被盖住',
                 '易错：改孩子之前，若父节点有全覆盖标记，必须先下放',
                 '作者说明：自顶向下线段树，也可用自底向上的 zkw 线段树',
                 '原文是 Python 2 写法，但这段代码在 Python 3 下无需改动，已逐字使用'],
    ),
)
