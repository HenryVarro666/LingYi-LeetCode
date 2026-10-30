def _set(mask, n):
    return '{' + ','.join(str(i) for i in range(n) if mask >> i & 1) + '}'


def _med(a):
    return a[(len(a) - 1) // 2] if a else None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    lists = S['lists']
    n = len(lists)
    u = 1 << n
    srt = S.get('sorted_')
    f = S.get('f')
    line = S.get('_line')
    cv.text((x0 + 18, y0 + 4), 'lists 下标集合 S → 合并后的有序数组 sorted_[S] · 中位数 · 最小成本 f[S]', 22, T['muted'], bold=True)
    rowh = min(52, (y1 - y0 - 100) / (u - 1))
    y = y0 + 56
    cols = [x0 + 20, x0 + 180, x0 + 640, x0 + 780]
    for h_, cx in zip(('集合', 'sorted_[S]', 'med', 'f[S]'), cols):
        cv.text((cx, y - 4), h_, 20, T['dim'], bold=True)
    y += 28
    hi, jj = S.get('i'), S.get('j')
    kk = S.get('k')
    pre_phase = f is None or line is not None and line <= 13
    for m in range(1, u):
        row = y + (m - 1) * rowh
        tag = None
        if pre_phase:
            if 'high_bit' in S and 's' in S and m == (S['high_bit'] | S['s']) and line in (13,):
                tag = T['orange']
        else:
            if m == hi:
                tag = T['yellow']
            elif jj is not None and m == jj and line in (22, 23, 24, 25, 26):
                tag = T['cyan']
            elif kk is not None and m == kk and line in (23, 24, 25, 26):
                tag = T['pink']
        if tag:
            cv.rect((x0 + 8, row - 3, x1 - 8, row + rowh - 6), fill=tag, alpha=45, r=8, outline=tag, width=2)
        cv.text((cols[0], row + rowh / 2 - 4), _set(m, n), 22, T['text'], anchor='lm', mono=True)
        a = srt[m] if srt else []
        if a:
            s = ','.join(str(v) for v in a)
            if len(s) > 26:
                s = s[:25] + '…'
            cv.text((cols[1], row + rowh / 2 - 4), s, 22, T['text'], anchor='lm', mono=True)
            cv.text((cols[2], row + rowh / 2 - 4), _med(a), 22, T['purple'], anchor='lm', mono=True, bold=True)
        elif srt:
            cv.text((cols[1], row + rowh / 2 - 4), '—', 22, T['dim'], anchor='lm', mono=True)
        if f is not None:
            v = f[m]
            cv.text((cols[3], row + rowh / 2 - 4), '∞' if v == float('inf') else v, 22,
                    T['green'] if v != float('inf') else T['dim'], anchor='lm', mono=True, bold=True)


CONFIG = dict(
    num=3801, title='合并有序列表的最小成本', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='子集状压 DP · 预处理合并后的数组',
    tags=['灵神题单·动态规划', '灵神题单·链表树与回溯', '难度分 2399'],
    code='''
# 手写 min 更快
min = lambda a, b: b if b < a else a

class Solution:
    def minMergeCost(self, lists: List[List[int]]) -> int:
        u = 1 << len(lists)
        sorted_ = [[] for _ in range(u)]
        for i, a in enumerate(lists):  # 枚举不在 s 中的下标 i
            high_bit = 1 << i
            for s in range(high_bit):
                b = sorted_[s] + a
                b.sort()  # 线性合并的写法见另一份代码【Python3 写法二】
                sorted_[high_bit | s] = b

        f = [inf] * u
        for i in range(1, u):
            if i & (i - 1) == 0:  # i 只包含一个元素，无法分解成两个非空子集
                f[i] = 0
                continue
            # 枚举 i 的非空真子集 j
            j = i & (i - 1)
            while j > (i ^ j):
                k = i ^ j  # j 关于 i 的补集是 k
                med_j = sorted_[j][(len(sorted_[j]) - 1) // 2]
                med_k = sorted_[k][(len(sorted_[k]) - 1) // 2]
                f[i] = min(f[i], f[j] + f[k] + abs(med_j - med_k))
                j = (j - 1) & i
            f[i] += len(sorted_[i])

        return f[-1]
''',
    call='Solution().minMergeCost([[1,3,5],[2,4],[6,7,8]])',
    expect=18,
    views=[
        dict(type='text', size=28, h=60, fn=lambda S: '`lists` ' + '  '.join(f'#{i}`{a}`' for i, a in enumerate(S['lists']))),
        dict(type='custom', draw=_draw, h=480),
        dict(type='text', size=27, h=70, fn=lambda S: (
            f"`i = {_set(S['i'], len(S['lists']))}`：拆成 `j = {_set(S['j'], len(S['lists']))}` 和 `k = {_set(S['k'], len(S['lists']))}`，"
            f"`|med_j − med_k|` = `|{S['med_j']} − {S['med_k']}|` = =={abs(S['med_j'] - S['med_k'])}=="
            if all(x in S for x in ('i', 'j', 'k', 'med_j', 'med_k')) and S.get('_line') in (25, 26) and 'f' in S else '')),
    ],
    watch=[('i', "bin(i)[2:]", 'yellow'), ('j', "bin(j)[2:]", 'cyan'), ('k', "bin(k)[2:]", 'pink'), ('f[i]', 'f[i]', 'green')],
    skip=[2, 8, 9, 10, 11, 12, 16, 19, 21, 22, 23, 24, 25, 27],
    captions={
        'u = 1 << len(lists)': '`{len(lists)}` 个数组，用二进制表示它们的子集，共 `{u}` 个集合',
        'sorted_ = [[]': '`sorted_[S]`：把集合 `S` 里的数组合并成一个有序数组（预处理，因为 DP 会反复用到它的长度和中位数）',
        'sorted_[high_bit | s] = b': lambda S, B, r: f'`sorted_[{_set(S.high_bit | S.s, len(S.lists))}] = sorted_[{_set(S.s, len(S.lists))}] + lists[{S.i}]` 合并并排序 = `{S.b}`',
        'f = [inf]': '`f[S]`：把集合 `S` 合并成一个列表的最小总成本，先全设为 ∞',
        'if i & (i - 1) == 0': lambda S, B, r: (f'`i = {_set(S.i, len(S.lists))}` 只有一个数组，不需要合并' if S.i & (S.i - 1) == 0 else f'`i = {_set(S.i, len(S.lists))}` 有多个数组：最后一步把它拆成两个非空子集合并'),
        'f[i] = 0': '单个数组本身 `f = 0`',
        'f[i] = min': lambda S, B, r: (f'拆成 `j = {_set(S.j, len(S.lists))}`（中位数 {S.med_j}）和 `k = {_set(S.k, len(S.lists))}`（中位数 {S.med_k}）：'
                                      f'`f[j] + f[k] + |{S.med_j} − {S.med_k}|` = `{S.f[S.j]} + {S.f[S.k]} + {abs(S.med_j - S.med_k)}` = {S.f[S.j] + S.f[S.k] + abs(S.med_j - S.med_k)}，'
                                      f'`f[i]` {"∞" if B.f[S.i] == inf else B.f[S.i]} → =={S.f[S.i]}=='),
        'f[i] += len': lambda S, B, r: f'再加上合并后的总长度 `len(sorted_[i]) = {len(S.sorted_[S.i])}`（所有拆法的 `len(a)+len(b)` 都相同）→ f[{_set(S.i, len(S.lists))}] 变成 =={S.f[S.i]}==',
        'return f[-1]': '`f[-1]` 是全集：最小总成本 =={ret}==',
    },
    max_steps=110,
    cards=dict(
        one_liner='想想最后一步：合并的两个列表，各来自 lists 的一个子集',
        complexity='时间 `O(2^n·L + 3^n)`，空间 `O(2^n·L)`',
        problem=['`lists` 是若干非递减数组，每次选两个合并成一个有序数组',
                 '成本 = `len(a) + len(b) + |median(a) − median(b)|`，偶数长度取左中位数',
                 '本视频：`[[1,3,5],[2,4],[6,7,8]]` → `18`'],
        quote='想一想，最后一步发生了什么？我们合并了两个有序数组，分别来自 lists 中的一部分数组，以及 lists 中的另一部分数组。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[S]`：把集合 `S` 的数组合并成一个的最小成本；枚举 `S` 的非空真子集 `T` 作最后一步的一半',
              '`f[S] = len(S) + min( f[T] + f[S\\T] + |med(T) − med(S\\T)| )`，`len(T)+len(S\\T)=len(S)` 提到循环外',
              '每个集合的长度和中位数反复要用 → 预处理 `sorted_[S]`；枚举子集只取 `j > k`，省掉一半'],
        summary=['子集枚举总共 `3^n`，预处理合并数组 `O(2^n · L)`，`n ≤ 12`',
                 '中位数取左中间：下标 `(len − 1) // 2`',
                 '`j > (i ^ j)` 只枚举一半，因为 `(j, k)` 和 `(k, j)` 成本一样',
                 '另有写法二（二分中位数，省空间）和写法三（meet in the middle），本视频演示写法一']
    ),
)
