def _fit(cv, s, size, maxw, bold=True):
    while size > 13 and cv.tlen(s, size, bold) > maxw:
        size -= 1
    return size


def _seg(cv, T, box, n, lab, kids, cur=(), chg=(), nums=None, num_hl=(), title='', root=1, bound=None):
    """线段树示意图：上排 = 数组（可选），下面每个节点 = 一段区间；黄色 = 当前节点，黄边 = 这一步刚改过，虚框 = 还没算出"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0), title, 22, T['muted'], bold=True)
    cell = min(120, (x1 - x0 - 60) / max(n, 1))
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
    top = y0 + 36
    if nums is not None:
        for i in range(n):
            X = sx + i * cell
            hl = i in num_hl
            cv.rect((X + 2, top, X + cell - 2, top + 40), fill=T['yellow'] if hl else T['panel2'], r=6)
            cv.text((X + cell / 2, top + 20), nums[i] if i < len(nums) else '', 24, T['bg'] if hl else T['text'], anchor='mm', bold=True)
            cv.text((X + cell / 2, top + 44), i, 16, T['dim'], anchor='mt', mono=True)
        top += 72
    nodes = {}
    def walk(nd, l, r, d):
        nodes[nd] = (l, r, d)
        if l < r:
            m = (l + r) // 2
            a, b = kids(nd)
            walk(a, l, m, d + 1)
            walk(b, m + 1, r, d + 1)
    walk(root, 0, n - 1, 0)
    depth = max(d for _, _, d in nodes.values()) + 1
    rowh = min(112, (y1 - top - 6) / depth)
    bh = min(54, rowh - 30)
    pos = {}
    for nd, (l, r, d) in nodes.items():
        cx = sx + (l + r + 1) / 2 * cell
        pos[nd] = (cx, top + d * rowh)
    for nd, (l, r, d) in nodes.items():
        if l < r:
            for c in kids(nd):
                cv.line([(pos[nd][0], pos[nd][1] + bh + 20), (pos[c][0], pos[c][1])], T['border'], 2)
    for nd, (l, r, d) in nodes.items():
        cx, cy = pos[nd]
        w = min(max(cell * (r - l + 1) - 8, 40), 190 if r > l else 130)
        s = lab(nd)
        is_cur = nd in cur
        changed = nd in chg
        if s is None:
            cv.rect((cx - w / 2, cy, cx + w / 2, cy + bh), outline=T['dim'], width=1, r=8)
            s = ''
        else:
            cv.rect((cx - w / 2, cy, cx + w / 2, cy + bh), fill=T['yellow'] if is_cur else T['panel2'],
                    outline=T['yellow'] if changed else T['border'], width=4 if changed else 1, r=8)
        if is_cur and s == '':
            cv.rect((cx - w / 2, cy, cx + w / 2, cy + bh), outline=T['yellow'], width=4, r=8)
        sz = _fit(cv, s, 24, w - 10)
        cv.text((cx, cy + bh / 2), s, sz, T['bg'] if is_cur and s else T['text'], anchor='mm', bold=True)
        cv.text((cx, cy + bh + 3), f'#{nd} [{l},{r}]', 15, T['dim'], anchor='mt', mono=True)



def _leafs(S, n):
    out = []
    mul = S['mul']
    def go(nd, l, r):
        if l == r:
            out.append(mul[nd])
            return
        m = (l + r) // 2
        go(nd * 2 + 1, l, m)
        go(nd * 2 + 2, m + 1, r)
    go(0, 0, n - 1)
    return out


def _draw(cv, S, B, box, T):
    f, mul, k, n = S.get('f'), S.get('mul'), S.get('k'), S.get('n')
    if f is None or mul is None or k is None or n is None:
        cv.text((box[0] + 18, box[1]), '（还没建树）', 24, T['dim'])
        return
    fb, mb = B.get('f'), B.get('mul')
    chg = set()
    if fb is not None and mb is not None and len(mb) == len(mul):
        chg = {i for i in range(len(mul)) if mb[i] != mul[i] or [fb[x][i] for x in range(k)] != [f[x][i] for x in range(k)]}
    inn = S['_inner']
    cur = inn.get('now')
    hl = ()
    if 'start' in inn and 'end' in inn:
        hl = range(inn['start'], inn['end'] + 1)
    elif 'start' in S and S.get('_line', 0) >= 100:
        hl = range(S['start'], n)
    _seg(cv, T, box, n, lambda nd: f"×{mul[nd]} {[f[x][nd] for x in range(k)]}" if nd < len(mul) else None,
         lambda nd: (nd * 2 + 1, nd * 2 + 2), cur=(cur,) if cur is not None else (), chg=chg,
         nums=_leafs(S, n), num_hl=hl, root=0,
         title=f'线段树：节点 = ×mul  f[0..{k-1}]（上排 = nums % {k}，黄 = 查询区间）')


def _info(S):
    f, mul, k = S.get('f'), S.get('mul'), S.get('k')
    if f is None or mul is None:
        return ''
    return f"根：整段乘积 mod {k} = ×{mul[0]}，`f[x][节点]` = 区间内「前缀乘积 mod {k} = x」的前缀数 = {[f[x][0] for x in range(k)]}"


CONFIG = dict(
    num=3525, title='求出数组的 X 值 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='线段树（f[x][now] + mul[now]）',
    tags=['灵神题单·常用数据结构', '难度分 2645'],
    code='''
class Solution(object):
    def resultArray(self, nums, k, queries):
        
        res = []
        n = len(nums)
        f = [[0] * (n * 4) for _ in range(k)]
        mul = [0] * (n * 4)

        def build(now, left, right, f, mul):
            if left == right:
                mul[now] = nums[left] % k
                for x in range(k):
                    f[x][now] = 0
                f[nums[left] % k][now] = 1
                return
            
            mid = (left + right) >> 1
            build(now + now + 1, left, mid, f, mul)
            build(now + now + 2, mid + 1, right, f, mul)

            mul[now] = mul[now + now + 1] * mul[now + now + 2] % k
            for x in range(k):
                f[x][now] += f[x][now + now + 1]
                f[x * mul[now + now + 1] % k][now] += f[x][now + now + 2]

        def update(now, left, right, p, v, f, mul):
            if left == right:
                mul[now] = v % k
                for x in range(k):
                    f[x][now] = 0
                f[v][now] = 1
                return 
            
            mid = (left + right) >> 1
            if p <= mid:
                update(now + now + 1, left, mid, p, v, f, mul)
            else:
                update(now + now + 2, mid + 1, right, p, v, f, mul)
            
            for x in range(k):
                f[x][now] = f[x][now + now + 1]

            left_r = mul[now + now + 1]
            for x in range(k):
                f[x * left_r % k][now] += f[x][now + now + 2]

            mul[now] = mul[now + now + 1] * mul[now + now + 2] % k

        def find_mul(now, left, right, start, end, mul):
            if left == start and right == end:
                return mul[now]
            
            mid = (left + right) >> 1
            if end <= mid:
                return find_mul(now + now + 1, left, mid, start, end, mul)
            elif start > mid:
                return find_mul(now + now + 2, mid + 1, right, start, end, mul)
            else:
                left_r = find_mul(now + now + 1, left, mid, start, mid, mul)
                if left_r == 0:
                    return 0
                return left_r * find_mul(now + now + 2, mid + 1, right, mid + 1, end, mul) % k

        def find_x(now, left, right, start, end, x, f, mul):
            if left == start and right == end:
                return f[x][now]
            
            mid = (left + right) >> 1
            if end <= mid:
                return find_x(now + now + 1, left, mid, start, end, x, f, mul)
            elif start > mid:
                return find_x(now + now + 2, mid + 1, right, start, end, x, f, mul)
            else:
                res = find_x(now + now + 1, left, mid, start, mid, x, f, mul)
                left_r = find_mul(now + now + 1, left, mid, start, mid, mul)
                if left_r == 0:
                    if x == 0:
                        return res + end - mid
                    else:
                        return res

                for v in range(k):
                    if v * left_r % k == x:
                        res += find_x(now + now + 2, mid + 1, right, mid + 1, end, v, f, mul)
                return res
        

        build(0, 0, n - 1, f, mul)
        for index, value, start, x in queries:
            update(0, 0, n - 1, index, value % k, f, mul)
            res.append(find_x(0, 0, n - 1, start, n - 1, x, f, mul))
        
        return res
''',
    call='Solution().resultArray([1, 2, 3, 4], 3, [[2, 2, 0, 2], [3, 3, 1, 0]])',
    expect=[1, 1],
    max_steps=80,
    views=[
        dict(type='text', fn=_info, h=50),
        dict(type='custom', draw=_draw, h=360),
        dict(type='calls', h=100),
    ],
    watch=[('res', 'res', 'green')],
    skip=[4, 5, 6, 7, 88, 10, 11, 12, 13, 15, 17, 18, 19, 22, 23, 24, 27, 28, 29, 30, 32, 34, 36, 38, 40, 41, 43, 44, 45,
          50, 53, 54, 55, 56, 57, 59, 60, 61, 62, 66, 68, 69, 70, 71, 72, 77, 78, 79, 80, 82, 84, 85, 76, 93],
    captions={
        14: lambda S, B, r: f"叶子 `[{S.left}]`：`nums[{S.left}] % k` = `{S.nums[S.left]} % {S.k}` = ==`{S.nums[S.left] % S.k}`==，只有一个前缀 → `mul = {S.nums[S.left] % S.k}`，`f[{S.nums[S.left] % S.k}] = 1`",
        21: lambda S, B, r: (lambda L, R, lm: f"合并节点 `{S.now}`：`mul` = 左 `{S.mul[L]}` × 右 `{S.mul[R]}` % k = =={S.mul[S.now]}==；`f` = 左 `f` 直接并入，右 `f[x]` 乘上左 `mul = {lm}` 后落到 `f[x·{lm} % k]` → `{[S.f[x][L] for x in range(S.k)]}` + 右 `{[S.f[x][R] for x in range(S.k)]}`")(S.now * 2 + 1, S.now * 2 + 2, S.mul[S.now * 2 + 1]),
        31: '到达叶子：新值 `{v}` → `mul = {v % k}`，`f[{v}] = 1`，其余 `f[x] = 0`',
        35: lambda S, B, r: f'`p = {S.p}` ' + ('≤' if S.p <= S.mid else '>') + f' `mid = {S.mid}`：在' + ('左' if S.p <= S.mid else '右') + '半，往那边走，回溯时重新合并',
        47: lambda S, B, r: f"重算节点 `{S.now}`：`f` 先拷左半，再把右半 `f[x]` 乘上左 `mul` = `{S.left_r}` 后累加 → `{[S.f[x][S.now] for x in range(S.k)]}`；`mul` = =={S.mul[S.now]}=="
,
        51: '查询区间正好等于节点 `[{left},{right}]`：乘积 = `mul[{now}]` = {mul[now]}',
        65: lambda S, B, r: (f"节点 `[{S.left},{S.right}]` 正好等于查询 `[{S.start},{S.end}]` → 直接取 `f[{S.x}][{S.now}]` = ==`{S.f[S.x][S.now]}`==" if S.left == S.start and S.right == S.end
                             else f"节点 `[{S.left},{S.right}]` 比查询 `[{S.start},{S.end}]` 大：还要继续拆"),
        74: '查询跨过中点：先递归查左半 `[start, mid]`，其中前缀乘积 mod k = `x` 的个数记进 `res`',
        75: '再算左半 `[start, mid]` 的整体乘积 `left_r`：右半的每个前缀都要先乘上它',
        83: lambda S, B, r: f"右半的前缀乘积 `v` 乘上 `left_r = {S.left_r}`：`{S.v}·{S.left_r} % {S.k} = {S.v * S.left_r % S.k}` " + (f"==等于 x = {S.x}==，加上右半 `f[{S.v}]`" if S.v * S.left_r % S.k == S.x else f"≠ `x = {S.x}`，不要"),
        89: lambda S, B, r: ('所有查询处理完了' if B.get('index') == S.index and 'start' in B else f"查询 {S.index}：把 `nums[{S.index}]` 改成 `{S.value}`；问 `start = {S.start}` 起，前缀乘积 mod k = `{S.x}` 的前缀数"),
        90: '先单点修改：把叶子换成 `value % k`，自底向上重新合并',
        91: '再查询 `[start, n-1]`：左端点固定，合并几个节点（`f` 已经统计好区间内前缀的个数）',
    },
    cards=dict(
        one_liner='右半的前缀先拼上整个左半，才是当前区间的前缀',
        complexity='时间 `O((n + q log n)k)`，空间 `O(nk)`',
        problem=['正整数数组 `nums`、`k ≤ 5`，每条查询先改 `nums[index] = value`',
                 '再对子数组 `nums[start:]` 数「保留的前缀乘积 mod k 等于 x」的方案数（后缀可以移掉）',
                 '示例：`nums=[1,2,4,8,16,32], k=4, queries=[[0,2,0,2],[0,2,0,1]]` → `[1,0]`',
                 '本视频：`[1,2,3,4]`，`k=3`，两条查询 → `[1,1]`'],
        quote='右半边区间的前缀必须拼接上整个左半边区间，才能形成当前区间的前缀，因此在这里还需要先计算左半边区间的乘积。',
        quote_src='—— yiduobo 题解',
        idea=['「移除后缀」= 数子数组里有多少个前缀的乘积 mod k 等于 x；单点修改 + 区间查询 → 线段树',
              '`f[x][now]`：节点区间里乘积 mod k = x 的前缀数；`mul[now]`：区间整体乘积 mod k',
              '合并：左半的 `f` 直接并入，右半的 `f[x]` 加到 `f[x * 左.mul % k]`',
              '查询跨中点时：左半 `mul` 为 0 要单独处理；否则枚举右半的 `v`，满足 `v * left_r % k == x` 才取右半 `f[v]`'],
        summary=['时间 `O((n + q log n)k)`，空间 `O(nk)`',
                 '易错：`f[x]` 是「前缀」个数，不是子数组个数；右半的前缀要乘上左半整体乘积',
                 '查询里 `left_r == 0` 要特判：右半所有前缀乘积都是 0，直接 `x == 0` 时加上右半长度',
                 '原文可直接在 Python 3 运行，未做修改；与灵神的区别：yiduobo 用 `k` 个数组 `f` + 一个 `mul` 数组，查询时枚举 `v` 分流'],
    ),
)
