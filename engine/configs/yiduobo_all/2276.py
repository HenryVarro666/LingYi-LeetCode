def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'node_list 里的线段树：每个节点 = [l, r] + cnt（绿 = 整段已覆盖，黄 = 当前节点）', 22, T['muted'], bold=True)
    nl = S.get('self.node_list')
    if not nl:
        return
    root = nl[0]
    lo, hi = root[0], root[1]
    n = hi - lo + 1
    slot = (x1 - x0 - 60) / n
    inner = S.get('_inner') or {}
    cur = S.get('now') if 'now' in inner else None
    nodes = []

    def walk(i, d):
        nodes.append((i, d))
        for ch in (nl[i][2], nl[i][3]):
            if ch != -1:
                walk(ch, d + 1)
    walk(0, 0)
    depth = max(d for _, d in nodes) + 1
    top = y0 + 80
    gapy = min(120, (y1 - 80 - top - 90) / max(1, depth - 1))
    nw, nh = min(80, slot * 0.92), 52
    pos = {i: (x0 + 30 + ((nl[i][0] + nl[i][1]) / 2 - lo + 0.5) * slot, top + d * gapy) for i, d in nodes}
    for i, d in nodes:
        for ch in (nl[i][2], nl[i][3]):
            if ch != -1:
                cv.line([(pos[i][0], pos[i][1] + nh / 2), (pos[ch][0], pos[ch][1] - nh / 2)], T['border'], 2)
    for i, d in nodes:
        l, r, _, _, cnt = nl[i]
        X, Y = pos[i]
        full = cnt == r - l + 1
        fill = T['yellow'] if i == cur else (T['green'] if full else T['panel2'])
        tc = T['bg'] if (i == cur or full) else T['text']
        cv.rect((X - nw / 2, Y - nh / 2, X + nw / 2, Y + nh / 2), fill=fill, r=10, outline=T['border'], width=2)
        cv.text((X, Y - 8), f'cnt={cnt}', 19, tc, anchor='mm', bold=True)
        cv.text((X, Y + 13), f'[{l},{r}]', 17, tc, anchor='mm', mono=True)
        cv.text((X - nw / 2 + 2, Y - nh / 2 - 2), i, 15, T['dim'], anchor='lb', mono=True)

    def covered(v):
        i = 0
        while i != -1:
            l, r, lc, rc, cnt = nl[i]
            if cnt == r - l + 1:
                return True
            i = lc if (lc != -1 and v <= nl[lc][1]) else (rc if (rc != -1 and v >= nl[rc][0]) else -1)
        return False
    yy = y1 - 64
    cv.text((x0 + 18, yy - 28), '整数是否已被 add 覆盖：', 20, T['muted'])
    for v in range(lo, hi + 1):
        X = x0 + 30 + (v - lo) * slot
        c = covered(v)
        cv.rect((X + 3, yy, X + slot - 3, yy + 34), fill=T['green'] if c else T['panel2'], r=6, outline=T['border'], width=1)
        cv.text((X + slot / 2, yy + 17), v, 20, T['bg'] if c else T['dim'], anchor='mm', bold=True)


def _node(S, i):
    return S['self.node_list'][i]


CONFIG = dict(
    num=2276, title='统计区间中的整数数目', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='动态新建节点的线段树（数组存节点）',
    tags=['八、树状数组和线段树', '难度分 2222'],
    code='''
class CountIntervals(object):

    def __init__(self):
        self.node_list = [[1, 10 ** 9, -1, -1, 0]]

    def update(self, now, left, right):
        l, r, left_child, right_child, cnt = self.node_list[now]

        if r - l + 1 == cnt:
            return
        
        if l == left and r == right:
            self.node_list[now][-1] = right - left + 1
            return
        
        mid = (l + r) >> 1
        if right <= mid:
            if left_child == -1:
                self.node_list.append([l, mid, -1, -1, 0])
                left_child = self.node_list[now][2] = len(self.node_list) - 1
            self.update(left_child, left, right)
        
        elif left > mid:
            if right_child == -1:
                self.node_list.append([mid + 1, r, -1, -1, 0])
                right_child = self.node_list[now][3] = len(self.node_list) - 1
            self.update(right_child, left, right)
        
        else:
            if left_child == -1:
                self.node_list.append([l, mid, -1, -1, 0])
                left_child = self.node_list[now][2] = len(self.node_list) - 1
            self.update(left_child, left, mid)

            if right_child == -1:
                self.node_list.append([mid + 1, r, -1, -1, 0])
                right_child = self.node_list[now][3] = len(self.node_list) - 1
            self.update(right_child, mid + 1, right)

        self.node_list[now][-1] = 0

        if left_child > 0:
            self.node_list[now][-1] += self.node_list[left_child][-1]
        
        if right_child > 0:
            self.node_list[now][-1] += self.node_list[right_child][-1]
            
    def add(self, left, right):
        self.update(0, left, right)

    def count(self):

        return self.node_list[0][-1]
''',
    call='''c = CountIntervals()
c.node_list[0][1] = 8
c.add(2, 3)
c.add(3, 6)
c.count()''',
    expect=5,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='calls', h=100, hide=('add',)),
    ],
    watch=['now', 'left', 'right', ('mid', 'mid', 'blue'), ('cnt', 'cnt', 'green')],
    skip=['self.node_list = [[1', 'self.update(0, left, right)', 'self.node_list.append', 'if left_child > 0', 'if right_child > 0'],
    max_steps=68,
    captions={
        'l, r, left_child, right_child, cnt = self.node_list[now]': '取出节点 `{now}`：管 `[{l},{r}]`，已覆盖 `cnt = {cnt}`',
        'if r - l + 1 == cnt': lambda S, B, ret: ('节点 `[{},{}]` 已被整个覆盖（cnt = 长度）→ 本次 add 无需任何操作'.format(S.l, S.r) if S.r - S.l + 1 == S.cnt else '节点 `[{},{}]` 还没被盖满，继续'.format(S.l, S.r)),
        'if l == left and r == right': lambda S, B, ret: ('节点范围与 `[{},{}]` 恰好重合 → ==不再向下==，直接覆盖'.format(S.left, S.right) if S.l == S.left and S.r == S.right else '范围 `[{},{}]` 与要加的 `[{},{}]` 不重合，需要往下拆'.format(S.l, S.r, S.left, S.right)),
        'self.node_list[now][-1] = right - left + 1': '`cnt` 记为 `{right-left+1}`：整段都算已覆盖',
        'mid = (l + r) >> 1': '中点 `mid = {mid}`：左孩子管 `[{l},{mid}]`，右孩子管 `[{mid+1},{r}]`',
        'if right <= mid': lambda S, B, ret: ('`right={}` ≤ `mid={}`：要加的区间整个在左半边'.format(S.right, S.mid) if S.right <= S.mid else '`right={}` > `mid={}`：不全在左半边'.format(S.right, S.mid)),
        'elif left > mid': lambda S, B, ret: ('`left={}` > `mid={}`：要加的区间整个在右半边'.format(S.left, S.mid) if S.left > S.mid else '`left={}` ≤ `mid={}`：横跨中点，要拆成两段'.format(S.left, S.mid)),
        'if left_child == -1': lambda S, B, ret: ('左孩子还不存在（-1）→ ==新建节点== `[{},{}]` 追加到 node_list'.format(S.l, S.mid) if S.left_child == -1 else '左孩子已存在（下标 {}）'.format(S.left_child)),
        'if right_child == -1': lambda S, B, ret: ('右孩子还不存在（-1）→ ==新建节点== `[{},{}]` 追加到 node_list'.format(S.mid + 1, S.r) if S.right_child == -1 else '右孩子已存在（下标 {}）'.format(S.right_child)),
        'left_child = self.node_list[now][2]': '记下左孩子的下标 `{left_child}`',
        'right_child = self.node_list[now][3]': '记下右孩子的下标 `{right_child}`',
        'self.update(left_child, left, right)': '递归进入左孩子 `{left_child}`',
        'self.update(right_child, left, right)': '递归进入右孩子 `{right_child}`',
        'self.update(left_child, left, mid)': '横跨中点：左段 `[{left},{mid}]` 交给左孩子',
        'self.update(right_child, mid + 1, right)': '右段 `[{mid+1},{right}]` 交给右孩子',
        'self.node_list[now][-1] = 0': '回溯：先把 `cnt` 清零，再加上孩子的',
        '+= self.node_list[left_child][-1]': '`cnt` 加上左孩子的 `cnt`，节点 `{now}`：`{self.node_list[now][-1]}`',
        '+= self.node_list[right_child][-1]': '再加右孩子的 `cnt`：节点 `{now}` 的 `cnt = {self.node_list[now][-1]}`',
        'return self.node_list[0][-1]': '根节点的 `cnt` = =={ret}==：直接读，不用遍历',
    },
    cards=dict(
        one_liner='只建出走过的节点：树随着 add 一点点长出来',
        complexity='`add` 时间 `O(log U)`，空间 `O(q log U)`；`count` 为 `O(1)`',
        problem=['`add(left, right)` 把闭区间里的整数加入集合，`count()` 返回集合里的整数个数',
                 '值域 `1..10^9`、操作 `10^5` 次，且是在线操作',
                 '示例（视频里把根范围缩成 `[1,8]`）：`add(2,3)`，再 `add(3,6)`（和前一个重叠在 3）→ `count()` = `5`'],
        quote='与常规的线段树不同，一开始建树时并不会将树中所有节点建好，而是只构造一个根节点，管辖范围为1到10^9。接下来对于插入的区间，……若要求解的区间对应的节点不存在，那么就新建这个节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['区间边界太大又是在线问题，==离散化行不通==，只剩平衡树或动态开点线段树',
              '节点用 `[l, r, 左孩子下标, 右孩子下标, cnt]` 存在数组里，孩子是 `-1` 就是还没建',
              '两个优化：已被盖满就直接返回；恰好重合就直接记满，不再往下'],
        summary=['`add` 每次只走 `O(log U)` 层，节点总数不超过约 `4·10^5`',
                 '易错：回溯时 `cnt` 必须先清零再加孩子的，否则会重复累加',
                 '孩子下标判断用 `> 0`，因为 0 号是根，不可能是孩子',
                 '为看清过程，演示时把根范围改成 `[1,8]`（调用里写的 `c.node_list[0][1] = 8`），代码本身未改',
                 '这份代码在 Python 3 下无需修改；灵神同题用的是对象版动态开点，思路相同'],
    ),
)
