def _layout(g, n):
    """简单树布局：叶子按 dfs 序等距排开，父节点在子节点中间；返回 {i: (列坐标, 深度)}"""
    pos, cnt = {}, [0]

    def go(x, d):
        ch = g[x]
        if not ch:
            pos[x] = (cnt[0], d)
            cnt[0] += 1
        else:
            for y in ch:
                go(y, d + 1)
            pos[x] = ((pos[ch[0]][0] + pos[ch[-1]][0]) / 2, d)
    go(0, 0)
    return pos, cnt[0]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g, vals, n = S.get('g'), S.get('vals'), S.get('n')
    cv.text((x0 + 18, y0 + 4), '树（黄 = 正在 dfs 的节点；dfs 时记下每个节点的进出时间）', 22, T['muted'], bold=True)
    if g is None or vals is None:
        return
    pos, w = _layout(g, n)
    dmax = max(d for _, d in pos.values())
    gx = (x1 - x0 - 120) / max(1, w - 1) if w > 1 else 0
    gy = min(110, (y1 - y0 - 160) / max(1, dmax))
    P = {i: (x0 + 60 + c * gx, y0 + 100 + d * gy) for i, (c, d) in pos.items()}
    for i in range(n):
        for y in g[i]:
            cv.line([P[i], P[y]], T['border'], 3)
    cur = S.get('now')
    qs = None
    for i in range(n):
        X, Y = P[i]
        hot = (i == cur)
        cv.rect((X - 28, Y - 24, X + 28, Y + 24), fill=T['yellow'] if hot else T['panel2'], outline=T['border'], r=24)
        cv.text((X, Y), i, 28, T['bg'] if hot else T['text'], anchor='mm', bold=True)
        cv.text((X, Y + 30), f'v={vals[i]}', 18, T['muted'], anchor='mt', mono=True)
        if qs and qs[i]:
            cv.text((X + 32, Y - 30), ','.join(f'k={k}' for k, _ in qs[i]), 18, T['cyan'], anchor='lm', bold=True)



def _xor(S):
    x = S.get('xor')
    return None if x is None else list(x)


def _freq(S):
    return None


CONFIG = dict(
    num=3590, title='第 K 小的路径异或和', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='dfs 序 + 莫队 + 树状数组二分',
    tags=['难度分 2646'],
    code='''
class Solution(object):
    def kthSmallest(self, par, vals, queries):
        
        n = len(par)
        g = [[] for _ in range(n)]
        for index, fa in enumerate(par[1:], 1):
            g[fa].append(index)

        start = [None] * n
        end = [None] * n
        xor = []

        def dfs(now, x):
            x ^= vals[now]
            start[now] = len(xor)
            xor.append(x)

            for nxt in g[now]:
                dfs(nxt, x)
            
            end[now] = len(xor) - 1
        

        dfs(0, 0)

        q = [[start[v], end[v], k, index] for index, (v, k) in enumerate(queries)]
        res = [-1] * len(q)

        b = int(n ** 0.5)
        if b == 0:
            b += 1

        q.sort(key=lambda d:(d[0] // b, d[1]))
        f = [0] * 131073

        def add(x, delta):
            while x <= 131072:
                f[x] += delta
                x += x & -x
        
        def get(k):
            left = 1
            right = 131073
            while left < right:
                mid = (left + right) // 2
                x = mid
                cnt = 0
                while x > 0:
                    cnt += f[x]
                    x -= x & -x

                if cnt >= k:
                    right = mid
                else:
                    left = mid + 1
            
            if left == 131073:
                return -1
            return left - 1

        freq = {}

        for v in range(q[0][0], q[0][1] + 1):
            freq[xor[v] + 1] = freq.get(xor[v] + 1, 0) + 1
            if freq[xor[v] + 1] == 1:
                add(xor[v] + 1, 1)
        res[q[0][3]] = get(q[0][2])
        nowx, nowy = q[0][0], q[0][1]

        for x, y, k, index in q[1:]:
            while nowx > x:
                nowx -= 1
                freq[xor[nowx] + 1] = freq.get(xor[nowx] + 1, 0) + 1
                if freq[xor[nowx] + 1] == 1:
                    add(xor[nowx] + 1, 1)

            while nowx < x:
                freq[xor[nowx] + 1] = freq.get(xor[nowx] + 1, 0) - 1
                if freq[xor[nowx] + 1] == 0:
                    add(xor[nowx] + 1, -1)
                nowx += 1
            
            while nowy > y:
                freq[xor[nowy] + 1] = freq.get(xor[nowy] + 1, 0) - 1
                if freq[xor[nowy] + 1] == 0:
                    add(xor[nowy] + 1, -1)
                nowy -= 1

            while nowy < y:
                nowy += 1
                freq[xor[nowy] + 1] = freq.get(xor[nowy] + 1, 0) + 1
                if freq[xor[nowy] + 1] == 1:
                    add(xor[nowy] + 1, 1)

            res[index] = get(k)
        
        return res
''',
    call='Solution().kthSmallest([-1,0,0,1,1], [1,2,3,1,2], [[0,2],[1,3],[1,4]])',
    expect=[2, 3, -1],
    views=[
        dict(type='custom', draw=_draw, h=230),
        dict(type='array', var='xor', label='xor：按 dfs 序记下的路径异或和', pointers={'nowx': 'blue', 'nowy': 'pink'}, window=('nowx', 'nowy'), h=185, cell=70),
        dict(type='map', var='freq', label='freq：当前区间里每个值（+1 后）出现次数', h=110),
        dict(type='calls', label='调用栈', h=80),
    ],
    watch=['x', 'k', 'nowx', 'nowy', ('res', 'res', 'green')],
    skip=[4, 6, 7, 9, 10, 11, 18, 19, 30, 31, 34, 37, 38, 39, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 61, 70, 71, 77, 83, 89, 63],
    max_steps=110,
    captions={
        5: '先建好儿子列表 `g`',
        14: '路径异或和：根到 `{now}` = 父节点的 `x` ^ `vals[{now}]` = =={x}==',
        15: '==dfs 序==：首次到达 `{now}`，记下此刻 `xor` 的长度 `start[{now}] = {start[now]}`',
        16: '把 `{x}` 追加到 `xor` 末尾：`xor = {xor}`',
        21: '`{now}` 的所有孩子都走完：`end[{now}] = {end[now]}`。区间 `[{start[now]}, {end[now]}]` 就是以 `{now}` 为根的子树',
        24: '从根开始 dfs，把子树变成 `xor` 上的一段连续区间',
        26: '每个询问 `(u, k)` 变成区间问题：`xor[start[u]..end[u]]` 里不重复的第 `k` 小',
        27: '`res` 先全填 -1',
        29: '莫队分块：块大小 `b = {b}`',
        33: '按「左端点所在块、右端点」排序，让两个指针移动总量最小：`{q}`',
        'f = [0]': '`f` 是值域树状数组（值 +1 后下标 1..131072），记录区间里「出现过」的值',
        'for v in range(q[0][0]': '先暴力算第一个区间 `[{q[0][0]}, {q[0][1]}]`',
        64: '`xor[{v}] + 1 = {xor[v] + 1}` 的出现次数 → `freq`',
        65: lambda S, B, ret: ('次数刚变成 1：这个值第一次出现，要在树状数组里记一笔' if S.freq[S.xor[S.v] + 1] == 1 else '之前已经出现过，不用动树状数组（求的是不重复第 k 小）'),
        66: '树状数组里加上值 `{xor[v] + 1}`',
        67: '树状数组二分求区间里第 `{q[0][2]}` 小的值',
        68: '`nowx = {nowx}`，`nowy = {nowy}`：当前窗口 `[nowx, nowy]`',
        72: '`nowx` 左移：左边界向前扩展，把 `xor[{nowx}]` 纳入区间',
        73: '`xor[{nowx}] + 1` 的次数 +1 → `freq`',
        78: '`nowx` 右移前，把 `xor[{nowx}]` 移出：次数 −1',
        79: lambda S, B, ret: ('次数减到 0：这个值不在区间里了，树状数组里要抹掉' if S.freq[S.xor[S.nowx] + 1] == 0 else '还有别的位置出现它，树状数组不动'),
        84: '`nowy` 左移：把 `xor[{nowy}]` 移出，次数 −1',
        85: lambda S, B, ret: ('次数减到 0：树状数组里抹掉' if S.freq[S.xor[S.nowy] + 1] == 0 else '还有别的位置出现它，树状数组不动'),
        90: '`nowy` 右移：把 `xor[{nowy}]` 纳入区间，次数 +1',
        92: lambda S, B, ret: ('次数刚变成 1：树状数组里加上它' if S.freq[S.xor[S.nowy] + 1] == 1 else '重复值，树状数组不动'),
        'res[index] = get(k)': '区间对齐到 `[{x}, {y}]`：树状数组二分求不重复的第 `{k}` 小（不够 `k` 个得 -1）',
        58: '区间里不重复的值不到 `k` 个 → 返回 -1',
        59: '二分结果还原（之前 +1 了）：第 `k` 小的值 = `{left - 1}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='子树变成 dfs 序上的区间，莫队移动窗口，树状数组二分求第 k 小',
        complexity='时间 `O((n+q)·√n·log V)`，空间 `O(n + V)`',
        problem=['有根树（根 `0`），节点值 `vals`；`s(x)` = 根到 `x` 路径异或和',
                 '询问 `[u, k]`：`u` 子树里不同的 `s` 的第 `k` 小，不够返回 -1',
                 '示例：`par=[-1,0,0,1,1]`，`vals=[1,2,3,1,2]`，询问 `[0,2] [1,3] [1,4]` → `[2,3,-1]`'],
        quote='对于这类询问子树中所有节点相关的问题，通常可以通过 dfs 序将其转化为区间问题。……这样一来，问题就转化为了如何求解静态的区间中不重复的第 k 小值。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟 dfs：`xor` 按 dfs 序存路径异或和，每个节点记 `[start, end]`，子树 = 一段区间',
              '不重复第 k 小：莫队离线移动窗口，`freq` 记次数，次数 0↔1 时才改值域树状数组',
              '值域 ≤ 131071，所以树状数组开 131072；查询时在树状数组上二分，值要 +1 平移'],
        summary=['时间 `O((n+q)√n·log V)`，空间 `O(n + V)`（`V = 131072`）',
                 '树状数组下标从 1 开始，所以异或值 +1 存进去，答案再 −1 还原',
                 '只有 `freq` 在 0 ↔ 1 之间变化才改树状数组，这样才是「不重复」',
                 '二分上界取 131073，结果等于 131073 说明不足 `k` 个，返回 -1',
                 '原文是 Python 2 风格，本题代码无需改动'],
    ),
)
