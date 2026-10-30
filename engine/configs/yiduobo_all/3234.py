def _txt(S):
    ln = S.get('_line')
    if 'rightest' in S and 'leftest' in S and ln in (37, 38, 39, 41, 42):
        k = max(0, S['rightest'] - S['leftest'] + 1)
        return (f'zero = =={S["zero"]}==，左边界 `index = {S["index"]}`：右边界可取 `[{S["leftest"]}, {S["rightest"]}]` → {k} 个')
    if 'zero' in S and 'min_length' in S:
        return f'枚举恰好含 =={S["zero"]}== 个 0 的子串：至少要 `{S["zero"]}² + {S["zero"]} = {S["min_length"]}` 长'
    if 'next_zero' in S:
        return '先从右往左：`next_zero[i]` = i 右侧最近的 0 的下标（没有则为 n）'
    return ''


CONFIG = dict(
    num=3234, title='统计 1 显著的字符串的数量', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举 0 的个数 + 滑动窗口 + next_zero',
    tags=['灵神题单·常用数据结构', '难度分 2557'],
    code='''
class Solution(object):
    def numberOfSubstrings(self, s):

        n = len(s)
        
        next_zero = []
        p = n
        tot_zero = 0
        res = 0
        for index in range(n - 1, -1, -1):
            next_zero.append(p)
            if s[index] == '0':
                res += (p - index) * (p - index - 1) // 2
                tot_zero += 1
                p = index
        next_zero.reverse()

        res += p * (p + 1) // 2

        zero = 1
        for zero in range(1, tot_zero + 1):
            min_length = zero * zero + zero
            if min_length > n:
                break

            p = 0
            zero_cnt = 0

            if s[0] == '0':
                zero_cnt = 1

            while p < n and zero_cnt < zero:
                p = next_zero[p]
                zero_cnt += 1

            for index in range(n):
                rightest = next_zero[p] - 1
                leftest = max(p, index + min_length - 1)
                res += max(0, rightest - leftest + 1)

                if s[index] == '0':
                    p = next_zero[p]
                    if p == n:
                        break

        return res
''',
    call='Solution().numberOfSubstrings("10110")',
    expect=11,
    views=[
        dict(type='string', var='s', label='s（蓝箭头 = 左边界 index，粉格 = p，黄 = 其他 0）', pointers={'index': 'blue'}, cell=90, h=200,
             color=lambda S, i, v: ('pink' if i == S.get('p') and 'zero_cnt' in S else 'yellow' if v == '0' else None)),
        dict(type='array', var='next_zero', label='next_zero[i]：i 右侧最近的 0（n 表示没有）', cell=80, h=180, pointers={'p': 'pink'}),
        dict(type='text', h=110, size=26, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink'), 'tot_zero', 'zero', 'min_length', ('res', 'res', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'next_zero.append(p)': '`next_zero[{index}]` = 右侧最近的 0 在 `{p}`（`{n}` 表示没有）',
        "if s[index] == '0'": lambda S, B, r: ('' if False else (f'`s[{S.index}] = {S.s[S.index]}`：' + ('是 0' if S.s[S.index]=='0' else '是 1') + ('，后面 `p` 要更新' if S.s[S.index]=='0' and S.get('_line') == 12 else ''))),
        'res += (p - index)': '`index` 和上一个 0 `p={p}` 之间有 `{p - index - 1}` 个连续 1：贡献 `{p-index-1}×{p-index}/2` 个全 1 子串 → `res = {res}`',
        'p = index': '最近的 0 变成 `{p}`',
        'res += p * (p + 1)': '最左边的 0 之前还剩 `{p}` 个连续 1：贡献 `{p}×{p+1}/2`；`res = {res}`（没有 0 的子串都算完）',
        'next_zero.reverse': '倒着填的，翻转后 `next_zero[i]` 就对应下标 i',
        'zero = 1': '接下来处理含 0 的子串：枚举恰好含 `zero` 个 0',
        'for zero in range': '`zero = {zero}`',
        'min_length = ': '`zero` 个 0 至少配 `zero²` 个 1，子串至少 `{zero}² + {zero}` = =={min_length}== 长',
        'if min_length > n': lambda S, B, r: (f'`{S.min_length} > n = {S.n}`：已经放不下 → ==break==，更大的 zero 也不行' if S.min_length > S.n else f'`{S.min_length} ≤ n = {S.n}`，可能有解，继续'),
        'while p < n': lambda S, B, r: (f'`p = {S.p}`，窗口里 0 的个数 `{S.zero_cnt}`，还不到 `{S.zero}`：继续' if S.p < S.n and S.zero_cnt < S.zero else f'`p` 指在第 {S.zero} 个 0（下标 =={S.p}==）'),
        'p = next_zero[p]': lambda S, B, r: (f'`p` 跳到下一个 0：=={S.p}==' if S.get('_line') == 33 else f'`index` 刚离开了一个 0，窗口少一个 0 → `p` 跳到下一个 0：=={S.p}=='),
        'if s[0]': '`s[0]` 本身是 0 吗？是的话窗口一开始就含 1 个 0',
        'zero_cnt += 1': '窗口含 `{zero_cnt}` 个 0',
        'rightest = ': '右边界最远到下一个 0 之前：`next_zero[{p}] - 1` = =={rightest}==',
        'leftest = ': '右边界至少要 `max(p, index + min_length - 1)` = `max({p}, {index + min_length - 1})` = =={leftest}==（够长且包含第 {zero} 个 0）',
        'res += max(0': lambda S, B, r: f'合法右边界 `[{S.leftest}, {S.rightest}]` 共 `max(0, {S.rightest - S.leftest + 1})` 个 → `res = {S.res}`',
        'if p == n': lambda S, B, r: ('后面已经没有足够的 0 → ==break==' if S.p == S.n else '后面还有 0，继续'),
        'return res': '`res = {res}`',
    },
    skip=[6, 7, 8, 9, 26, 27],
    max_steps=120,
    cards=dict(
        one_liner='0 的个数是根号级：枚举个数，滑动窗口数右边界',
        complexity='时间 `O(n√n)`，空间 `O(n)`',
        problem=['由 0 和 1 组成的字符串，1 的个数 ≥ 0 的个数的平方 → 1 显著子串',
                 '统计 1 显著子串的数量',
                 '本视频：`s = "10110"`'],
        quote='由于1的数量必然要大于等于0的数量的平方，因此0的数量是根号级的，规模是很小的。也就是说，在这里可以枚举0的数量zero。',
        quote_src='—— yiduobo 题解原文',
        idea=['先处理没有 0 的情形：一段 `k` 个连续的 1 贡献 `(k+1)k/2` 个子串，同时倒着扫出 `next_zero`',
              '再枚举恰好含 `zero` 个 0：子串至少 `zero² + zero` 长',
              '以 `index` 为左边界，右边界在 `max(p, index+min_length-1)` 到 `next_zero[p]-1` 之间'],
        summary=['时间 `O(n√n)`，空间 `O(n)`',
                 '易错：`p` 要在 `s[index]` 为 0 时跳到 `next_zero[p]`，保证窗口里恰好 `zero` 个 0',
                 '`p == n` 说明后面 0 不够，直接 break',
                 '原文代码在 Python 3 下可直接运行，未改动'],
    ),
)
