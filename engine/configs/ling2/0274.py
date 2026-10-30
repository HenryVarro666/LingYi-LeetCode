def _counting(S):
    return 'cnt' in S and 's' not in S


def _cit_color(S, i, v):
    if 's' in S and 'i' in S:
        return 'cyan' if v >= S['i'] else None
    if not _counting(S):
        return None
    done = sum(S['cnt'])
    if S.get('_line') == 6 and i == done - 1:
        return 'yellow'
    if i < done:
        return 'green'
    return None


def _cnt_color(S, i, v):
    if 'i' in S and 's' in S and S['i'] <= i:
        return 'cyan'
    if _counting(S) and S.get('_line') == 6 and i == min(S['c'], S['n']):
        return 'yellow'
    return None


def _info(S):
    if 's' in S and 'i' in S:
        i, s = S['i'], S['s']
        ok = '≥' if s >= i else '<'
        return f"引用次数 `≥ {i}` 的论文有 `s = {s}` 篇：`{s} {ok} {i}`" + (' → ==h 指数就是 ' + str(i) + '==' if s >= i else ' → h 不能是 ' + str(i))
    if 'n' in S:
        return f"`n = {S['n']}` 篇论文：h 最大是 `n`，引用次数 `> n` 的论文按 `n` 统计"
    return ''


CONFIG = dict(
    num=274, title='H 指数', difficulty='Medium', category='普通数组',
    author='灵茶山艾府', technique='计数 + 倒序后缀和 O(n)',
    tags=['字节30天', '面试经典150'],
    code='''
class Solution:
    def hIndex(self, citations: List[int]) -> int:
        n = len(citations)
        cnt = [0] * (n + 1)
        for c in citations:
            cnt[min(c, n)] += 1  # 引用次数 > n，等价于引用次数为 n
        s = 0
        for i in range(n, -1, -1):  # i=0 的时候，s>=i 一定成立
            s += cnt[i]
            if s >= i:  # 说明有至少 i 篇论文的引用次数至少为 i
                return i
''',
    call='Solution().hIndex([3, 0, 6, 1, 5])',
    expect=3,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='array', var='citations', label='citations（绿 = 已统计，黄 = 当前；倒序阶段青 = 引用 ≥ i）', cell=96, h=150,
             color=_cit_color),
        dict(type='array', var='cnt', label='cnt[x]：引用次数为 x 的论文数（x = n 表示 ≥ n）', cell=96,
             pointers={'i': 'pink'}, window=('i', 'n'), color=_cnt_color, h=230),
        dict(type='text', fn=lambda S: (f"倒序累加：`s = cnt[{S['i']}] + … + cnt[{S['n']}] = {S['s']}`（框内）"
                                        if 's' in S and 'i' in S else ''), size=26, h=60),
    ],
    watch=[('n', 'n'), ('c', 'c', 'yellow'), ('i', 'i', 'pink'), ('s', 's', 'cyan')],
    captions={
        'n = len': '`n = {n}`：一共 {n} 篇论文，==h 不可能超过 n==',
        'cnt = [0]': '`cnt` 长 `n + 1`：统计 `min(citations[i], n)` 出现的次数',
        'for c in citations': lambda S, B, ret: (f'下一篇论文：引用 `c = {S.c}` 次' if sum(S.cnt) < S.n
                                                 else '每篇论文都统计完了'),
        'cnt[min(c, n)] += 1': lambda S, B, ret: (
            f'`{S.c} > n`，==等价于引用次数为 n==：`cnt[{S.n}]` +1 → {S.cnt[S.n]}' if S.c > S.n
            else f'`cnt[{S.c}]` +1 → {S.cnt[S.c]}'),
        's = 0': '`s` = 引用次数 `≥ i` 的论文数，从大到小枚举 i 时==倒着累加 cnt==',
        'for i in range': lambda S, B, ret: f'枚举 `i = {S.i}`（从 n 开始倒序）',
        's += cnt[i]': '`s += cnt[{i}]` → `{s}`：引用次数 `≥ {i}` 的论文有 {s} 篇',
        'if s >= i': lambda S, B, ret: (f'`s = {S.s} ≥ {S.i}`：==至少 {S.i} 篇论文引用至少 {S.i} 次==；倒序枚举，第一次成立就是最大的 h'
                                        if S.s >= S.i else f'`s = {S.s} < {S.i}`：不到 {S.i} 篇 → h 不能是 {S.i}，继续'),
        'return i': '返回 h 指数 =={ret}==',
    },
    cards=dict(
        one_liner='h 不超过 n：把引用次数截到 n 计数，再倒序累加找第一个 s ≥ i',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`citations[i]` 是第 i 篇论文的被引次数，求 ==h 指数==',
                 'h 指数：==至少有 h 篇论文被引用了至少 h 次==，取最大的 h',
                 '示例：`[3,0,6,1,5]` → `3`（3、6、5 这 3 篇都 ≥ 3 次）'],
        quote='题意：给你一个数组，求一个最大的 h，使得数组中==有至少 h 个数都大于等于 h==。……对于引用次数大于 n 的论文，我们在统计的时候，可以看成是引用次数等于 n 的论文。',
        quote_src='—— 灵茶山艾府题解',
        idea=['h 最多是 n，所以 `6` 和 `5` 对 `n = 5` 来说没区别 → 计数数组只要长 `n + 1`',
              '设 `s` 为引用次数 `≥ i` 的论文数：从 `i = n` 倒序，每次 `s += cnt[i]`',
              '倒序循环中==第一次== `s ≥ i` 的 i 就是最大的 h，直接返回'],
        result='h 指数为 `3` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`；排序做法是 `O(n log n)`',
                 '`i = 0` 时 `s ≥ 0` 一定成立，所以循环里一定会 return',
                 '易错：计数时要 `min(c, n)`，否则下标越界',
                 '思考题：数组有序时可以二分 → 275. H 指数 II'],
    ),
)
