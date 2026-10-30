A0 = [9, 4, 7, 2, 10, 13]


def _fx(S):
    f = S.get('f')
    if f is None:
        return ''
    rows = []
    for k, m in enumerate(f):
        body = ', '.join(f'{d}: {v}' for d, v in m.items()) or '空'
        rows.append(f'`f[{k}]`（以 {S["a"][k]} 结尾）= {{{body}}}')
    return '\n'.join(rows)


def _col(S, k, v):
    i, j = S.get('i'), S.get('j')
    if i is None:
        return None
    if k == i:
        return 'blue'
    if j is not None and k == j and S.get('_line', 0) >= 7:
        return 'pink'
    return None


def _formula(S):
    if S.get('d') is None or S.get('_line', 0) < 6 or S.get('j') is None:
        return '`f[i][d]`：以 `a[i]` 结尾、公差为 `d` 的最长等差子序列长度（至少两个数）'
    i, j, d = S['i'], S['j'], S['d']
    prev = S['f'][j].get(d, 1)
    return f'`a[{i}] − a[{j}]` = `{S["a"][i]} − {S["a"][j]}` = 公差 =={d}==；`f[{j}]` 里这个公差的长度是 {prev}'


CONFIG = dict(
    num=1027, title='最长等差数列', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='合法子序列 DP · 哈希表 f[i][d] 1:1 翻译成递推',
    tags=['灵神题单', '动态规划', '难度分 1759'],
    code='''
class Solution:
    def longestArithSeqLength(self, a: List[int]) -> int:
        f = [{} for _ in range(len(a))]
        for i, x in enumerate(a):
            for j in range(i - 1, -1, -1):
                d = x - a[j]  # 公差
                if d not in f[i]:
                    f[i][d] = f[j].get(d, 1) + 1
        return max(max(d.values()) for d in f[1:])
''',
    call=f'Solution().longestArithSeqLength({A0!r})',
    expect=4,
    skip=['for j in range', 'for i, x in enumerate'],
    views=[
        dict(type='array', var='a', label='a（蓝 = i，粉 = j）', h=230, cell=96, color=_col,
             pointers={'i': 'blue', 'j': 'pink'}),
        dict(type='text', fn=_fx, size=22, h=250, lines=7),
        dict(type='text', fn=_formula, size=26, h=100),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('d', 'd', 'orange')],
    captions={
        'f = [{} for': '`f[i]` 是哈希表：键 = 公差 `d`，值 = 以 `a[i]` 结尾、公差为 `d` 的最长等差子序列长度',
        'd = x - a[j]': lambda S, B, r: f'`a[{S.i}]` 接在 `a[{S.j}]` 后面：公差 `d = {S.x} − {S.a[S.j]} = {S.d}`',
        'if d not in f[i]': lambda S, B, r: (f'`j` 从右往左：`f[{S.i}]` 里还没有公差 {S.d} → ==这是最靠右的 `{S.a[S.j]}`=='
                                             if S.d not in S.f[S.i] else
                                             f'`f[{S.i}]` 里已有公差 {S.d}：更靠右的 `j` 已经算过，更靠左的不会更长 → 跳过'),
        'f[i][d] = f[j].get': lambda S, B, r: (f'`f[{S.i}][{S.d}] = f[{S.j}].get({S.d}, 1) + 1` = `{S.f[S.j].get(S.d, 1)} + 1` = =={S.f[S.i][S.d]}==；'
                                               + ('`a[j]` 之前没有公差 d 的链，它自己是首项（默认 1）' if S.d not in S.f[S.j] else '接在 `a[j]` 的链后面')),
        'return max': '所有结尾、所有公差里最长的长度 = =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='结尾 + 公差决定整条链：每个位置存一张「公差 → 长度」的表',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['给你整数数组 `nums`，返回其中==最长等差子序列==的长度',
                 '子序列不要求连续，相邻两项差都相同',
                 '示例：`[9,4,7,2,10]` → `3`；本视频：`[9,4,7,2,10,13]` → `4`（4,7,10,13）'],
        quote='把所有以 a[i] 结尾的（至少有两个元素的）LAS 的公差及其长度都算出来，存到一个哈希表中，a[i] 右边的数 x 就可以直接去哈希表中查找公差 d=x-a[i] 对应的 LAS 长度了。',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['“枚举选哪个”：确定末项和公差，其余项就都确定了',
              '`f[i][d]`：以 `a[i]` 结尾、公差为 `d`；上一项 `a[j]` 的链长查 `f[j][d]`',
              '`j` 倒序遍历：同一公差==只取最靠右的 `j`==，所以每个 `d` 只算一次'],
        summary=['时间 `O(n^2)`：状态 `O(n)` 张表 × 每张表 `O(n)` 转移',
                 '易错：`f[j].get(d, 1)` 的默认值是 1（`a[j]` 自己是首项），再 +1',
                 '答案要从 `f[1:]` 里取，因为 `f[0]` 是空表',
                 '方法二：枚举公差 d，再遍历一遍 nums，`f[x] = f[x-d] + 1`，空间 `O(m)`；本视频演示方法一的递推版'],
    ),
)
