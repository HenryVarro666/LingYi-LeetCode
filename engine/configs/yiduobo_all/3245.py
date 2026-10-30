def _marks(S):
    left, right, n = S.get('left'), S.get('right'), S.get('n')
    if left is None or n is None:
        return None
    out = []

    def go(now, l, r):
        if l == r:
            if left[now] is not None:
                out.append(l)
            return
        m = (l + r) // 2
        go(now + now + 1, l, m)
        go(now + now + 2, m + 1, r)
    go(0, 0, n - 1)
    return out


def _bit(S):
    f, g = S.get('f'), S.get('g')
    if f is None:
        return None
    return ['—'] + [f'{g[i]}个,{f[i]}' for i in range(1, len(f))]


CONFIG = dict(
    num=3245, title='交替组 III', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='标记法 + 线段树找邻居 + 树状数组',
    tags=['难度分 2740'],
    code='''
class Solution(object):
    def numberOfAlternatingGroups(self, colors, queries):

        n = len(colors)
        f = [0] * (n + 1)
        g = [0] * (n + 1)

        left = [None] * (n * 4)
        right = [None] * (n * 4)

        def add(v, sign):
            delta = v * sign
            v = n - v + 1
            while v <= n:
                f[v] += delta
                g[v] += sign
                v += v & -v
        
        def get(v):
            s = 0
            cnt = 0
            delta = v - 1
            v = n - v + 1
            while v > 0:
                s += f[v]
                cnt += g[v]
                v -= v & -v

            return s - delta * cnt

        def update(now, start, end, index):
            if start == end:
                if left[now] is None:
                    left[now] = index
                    right[now] = index
                else:
                    left[now] = None
                    right[now] = None
            else:
                mid = (start + end) // 2
                if index <= mid:
                    update(now + now + 1, start, mid, index)
                else:
                    update(now + now + 2, mid + 1, end, index)
                
                if left[now + now + 1] is None:
                    left[now] = left[now + now + 2]
                else:
                    left[now] = left[now + now + 1]
                
                if right[now + now + 2] is None:
                    right[now] = right[now + now + 1]
                else:
                    right[now] = right[now + now + 2]

        def find(now, start, end, ts, te, arr, left_flag):
            if start == ts and end == te:
                return arr[now]
            
            mid = (start + end) // 2
            if te <= mid:
                return find(now + now + 1, start, mid, ts, te, arr, left_flag)
            elif ts > mid:
                return find(now + now + 2, mid + 1, end, ts, te, arr, left_flag)
            else:
                if left_flag:
                    v = find(now + now + 1, start, mid, ts, mid, arr, left_flag)
                else:
                    v = find(now + now + 2, mid + 1, end, mid + 1, te, arr, left_flag)
                
                if v is not None:
                    return v

                if left_flag:
                    return find(now + now + 2, mid + 1, end, mid + 1, te, arr, left_flag)
                else:
                    return find(now + now + 1, start, mid, ts, mid, arr, left_flag)

        pre = None
        for index in range(n):
            if colors[index] == colors[(index - 1 + n) % n]:
                if pre is not None:
                    length = index - pre
                    add(length, 1)

                pre = index
                update(0, 0, n - 1, index)
        
        if left[0] is not None:
            add(left[0] + n - right[0], 1)
        
        res = []
        for q in queries:
            if q[0] == 1:
                if left[0] is None:
                    res.append(n)
                else:
                    res.append(get(q[1]))
            else:
                if colors[q[1]] == q[2]:
                    continue
                
                x = (q[1] - 1 + n) % n
                y = q[1]
                z = (q[1] + 1) % n

                pre = None
                if y > 0:
                    pre = find(0, 0, n - 1, 0, y - 1, right, False)
                if pre is None:
                    pre = right[0]

                nxt = None
                if z + 1 < n:
                    nxt = find(0, 0, n - 1, z + 1, n - 1, left, True)
                if nxt is None:
                    nxt = left[0]

                if colors[x] == colors[y] and colors[y] == colors[z]:
                    if nxt == y:
                        add(n - 1, -1)
                        add(1, -1)
                    else:
                        add((y + n - pre) % n, -1)
                        add(1, -1)
                        add((nxt + n - z) % n, -1)
                        add((nxt + n - 1 - pre) % n + 1 , 1)
                elif colors[x] == colors[y]:
                    if nxt == y:
                        pass
                    else:
                        add((y + n - pre) % n, -1)
                        add((nxt + n - y) % n, -1)
                        add((z + n - pre) % n, 1)
                        add((nxt + n - z) % n, 1)
                elif colors[y] == colors[z]:
                    if nxt == z:
                        pass
                    else:
                        add((z + n - pre) % n, -1)
                        add((nxt + n - z) % n, -1)
                        add((y + n - pre) % n, 1)
                        add((nxt + n - y) % n, 1)
                else:
                    if left[0] is None:
                        add(n - 1, 1)
                        add(1, 1)
                    else:
                        add((nxt + n - 1 - pre) % n + 1, -1)
                        add((y + n - pre) % n, 1)
                        add(1, 1)
                        add((nxt + n - z) % n, 1)

                update(0, 0, n - 1, y)
                update(0, 0, n - 1, z)
                colors[q[1]] = q[2]

        return res
''',
    call='Solution().numberOfAlternatingGroups([0,0,1,0,1,1], [[1,3],[2,2,0],[1,3]])',
    expect=[2, 0],
    views=[
        dict(type='array', var='colors', label='colors（环）', pointers={'y': 'pink', 'index': 'blue'}, h=160, color=lambda S, i, v: 'blue' if v == 1 else None),
        dict(type='array', var=_marks, label='被标记的瓷砖（与上一块同色）', h=120, cell=70),
        dict(type='array', var=_bit, label='树状数组：个数,长度之和（下标越小长度越大）', h=130, cell=88),
    ],
    watch=['pre', 'nxt', ('res', 'res', 'green')],
    skip=[58, 103, 104, 15, 33, 42, 44, 4, 5, 6, 8, 9, 12, 13, 14, 17, 20, 21, 22, 23, 24, 25, 27, 31, 32, 40, 41, 46, 47, 49, 51, 52, 54, 57, 60, 61, 62, 63, 64, 66, 67, 68, 69, 71, 72, 74, 75, 76, 77, 35, 37, 38, 79, 80, 92, 93, 94, 106, 107, 108, 113, 114],
    max_steps=100,
    captions={
        16: '树状数组下标 `{v}` 处：长度和 `f = {f[v]}`，个数 `g = {g[v]}`（加入长度 `{delta}`，`sign = {sign}`），再沿 `v += v & -v` 往上更新',
        26: '累加长度 `>= {delta + 1}` 的子段：`s = {s}`，`cnt = {cnt}`',
        29: '答案 = 长度之和 − (size − 1) × 个数 = `{s} − {delta}×{cnt}` = =={s - delta * cnt}==',
        34: '叶子：`index` 原来没标记 → 标记它（`left = right = index`）；已标记则取消',
        81: lambda S, B, ret: ('`colors[{}]` 与上一块 `colors[{}]` 同色 → ==标记 {}=='.format(S.index, (S.index - 1 + S.n) % S.n, S.index) if S.colors[S.index] == S.colors[(S.index - 1 + S.n) % S.n]
                              else '`colors[{}]` 与上一块不同色，不标记'.format(S.index)),
        82: '已有上一个标记 `pre = {pre}`：两个标记之间就是一个最长交替子段',
        83: '子段长度 = `index − pre` = `{length}`',
        84: '把长度 `{length}` 加入树状数组',
        86: '`pre` 更新为 `{pre}`',
        87: '线段树里标记 `{index}`：沿路径更新各区间最左 / 最右标记',
        89: '有标记：还要把「最右标记 → 回绕 → 最左标记」这一段也加进去',
        90: '回绕子段长度 = `left[0] + n − right[0]` = `{left[0] + n - right[0]}`',
        95: lambda S, B, ret: ('没有任何标记 → 环上任意 size 块都交替 → 答案 `n`' if S.left[0] is None else '有标记：用树状数组算，查询 size = {}'.format(S.q[1])),
        98: '树状数组里统计「长度 >= size」的子段个数 `cnt` 与长度之和 `s`',
        100: lambda S, B, ret: ('修改前后颜色相同，直接跳过' if S.colors[S.q[1]] == S.q[2] else '颜色会变：要看 y 左右的标记怎么变'),
        105: '`x = {x}`，`y = {y}`，`z = {z}`：被改的瓷砖和它的左右邻居',
        109: '线段树查 `[0, y-1]` 里最右的标记，就是 y 左边最近的标记 `pre`',
        110: lambda S, B, ret: ('`y` 左边找到标记：`pre = {}`'.format(S.pre) if S.pre is not None else '`y` 左边没有标记 → 要回绕到环的尾部'),
        115: '线段树查 `[z+1, n-1]` 里最左的标记，就是 z 右边最近的标记 `nxt`',
        116: lambda S, B, ret: ('`z` 右边找到标记：`nxt = {}`'.format(S.nxt) if S.nxt is not None else '`z` 右边没有标记 → 要回绕到环的头部'),
        111: '回绕：取全环最右的标记 `pre = right[0]`',
        117: '回绕：取全环最左的标记 `nxt = left[0]`',
        58: '这段区间正好落在查询区间内 → 直接取它记录的标记下标',
        119: lambda S, B, ret: '看 x、y、z 三块颜色：`{}` `{}` `{}` → {}'.format(S.colors[S.x], S.colors[S.y], S.colors[S.z],
                              '三块同色' if S.colors[S.x] == S.colors[S.y] == S.colors[S.z] else '`x == y`' if S.colors[S.x] == S.colors[S.y] else '`y == z`' if S.colors[S.y] == S.colors[S.z] else '互不相同：y、z 当前都没标记，改后都要标记'),
        145: lambda S, B, ret: ('没有任何标记（整环）' if S.left[0] is None else '已有标记：这是从 `pre` 到 `nxt` 前一块的一整段，现在要从中断开'),
        149: '旧的整段 `pre→nxt` 长度 `{(nxt + n - 1 - pre) % n + 1}`：先移除',
        150: '断出左段 `pre → y 前一块`，长度 `{(y + n - pre) % n}`',
        151: '`y` 自己孤立一段，长度 1',
        152: '断出右段 `z → nxt 前一块`，长度 `{(nxt + n - z) % n}`',
        154: '线段树切换 `y` 的标记（改后 `y` 与邻居同色 → 被标记）',
        155: '线段树切换 `z` 的标记',
        156: '最后才真正改颜色：`colors[{q[1]}] = {q[2]}`',
        158: '返回 `{res}`',
    },
    cards=dict(
        one_liner='把环切成「最长交替子段」：标记同色相邻处，树状数组数段长',
        complexity='时间 `O((n+q) log n)`，空间 `O(n)`',
        problem=['环形数组 `colors`（0/1）。查询 `[1, size]`：长度为 `size` 的交替组有几个',
                 '查询 `[2, i, c]`：把 `colors[i]` 改成 `c`',
                 '本视频：`[0,0,1,0,1,1]`，查询 `[1,3]` `[2,2,0]` `[1,3]` → `[2, 0]`'],
        quote='标记每一块与其上一块瓷砖同色的瓷砖……从某一块被标记的瓷砖开始，到下一块被标记的瓷砖的前一块瓷砖结束，这就是一个尽量长的分割的子段。',
        quote_src='—— yiduobo 题解原文',
        idea=['长度 `>= k` 的子段长度和 `S`、个数 `t`：答案 `S − (k−1)·t`，树状数组维护',
              '修改 `y` 只会改变 `y`、`z` 的标记，按 x、y、z 颜色分 4 类讨论，每类改几个子段长度',
              '找 `pre` / `nxt` 用线段树：每个区间记最左、最右标记；没有就回绕到环的另一端'],
        summary=['时间 `O((n+q) log n)`，空间 `O(n)`',
                 '没有标记时（整环交替）答案恒为 `n`；只有一个标记时子段长为 `n`',
                 '长度取模用 `(nxt + n - 1 - pre) % n + 1`，避免 `pre == nxt` 时得到 0',
                 '`x==y!=z` 与 `x!=y==z` 且 `nxt` 是自己时，只是标记转了一格，直接跳过',
                 '原文是 Python 2 风格，本题代码无需改动'],
    ),
)
