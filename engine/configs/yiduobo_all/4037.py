
# p 在「找 p」阶段（线段树下标已减去 m）才画到 nums 上；在线段树里时画到 f 上
_PP = "p if _line in (83, 86, 100, 103, 105) else None"
_PT = "p if _line in (38, 39, 63, 64, 66, 70, 73, 77, 79, 82, 89, 92, 95, 97, 98, 99, 106, 107, 109) and p < len(f) else None"

CONFIG = dict(
    num=4037, title='最多有效分割位置 II', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='前后缀 gcd + 线段树上二分',
    tags=['灵神题单·数学算法', '难度分 2372'],
    code='''
class Solution(object):
    def maxValidSplits(self, nums):
        
        def gcd(x, y):
            while y > 0:
                x, y = y, x % y
            return x
        
        def generate(start, end, step, g_list, first):
            g = 0
            for index in range(start, end, step):
                v = nums[index]
                g = gcd(g, v)
                if g not in first:
                    first[g] = index
                g_list.append(g)

        n = len(nums)
        pre = []
        pre_first = {}
        suf = []
        suf_first = {}
        generate(0, n, 1, pre, pre_first)
        generate(n - 1, -1, -1, suf, suf_first)
        suf.reverse()

        m = 1
        while m < n:
            m <<= 1
        
        f = [0] * (m << 1)
        for index, v in enumerate(nums):
            f[m + index] = v
        
        length = m >> 1
        while length >= 1:
            for index in range(length):
                p = length + index
                f[p] = gcd(f[p << 1], f[p << 1 | 1])
            length >>= 1

        res = max(0, suf_first[f[1]] - pre_first[f[1]])
        for index, v in enumerate(nums):
            if index == 0:
                pre_g = 0
            else:
                pre_g = pre[index - 1]
            
            if index == n - 1:
                suf_g = 0
            else:
                suf_g = suf[index + 1]
            
            g = gcd(pre_g, suf_g)

            if g == pre_g and g == suf_g:
                res = max(res, suf_first[g] - pre_first[g] - 1)
                continue
            
            if g != pre_g and g != suf_g:
                continue
            
            p = index + m
            f[p] = 0
            while p > 1:
                f[p >> 1] = gcd(f[p], f[p ^ 1])
                p >>= 1

            if g == pre_g:
                p = 1
                other = 0
                while p < m:
                    if f[p << 1 | 1] == g:
                        p <<= 1
                        p |= 1
                    else:
                        x = gcd(other, f[p << 1 | 1])
                        p <<= 1
                        if x == g:
                            p |= 1
                        else:
                            other = x
                p -= m
                if p == index:
                    p -= 1
                score = p - pre_first[g]

            else:
                p = 1
                other = 0
                while p < m:
                    if f[p << 1] == g:
                        p <<= 1
                    else:
                        x = gcd(other, f[p << 1])
                        p <<= 1
                        if x != g:
                            p |= 1
                            other = x
                p -= m
                if index == p:
                    p += 1
                score = suf_first[g] - p

            res = max(res, score)
            p = index + m
            f[p] = v
            while p > 1:
                f[p >> 1] = gcd(f[p], f[p ^ 1])
                p >>= 1

        return res
''',
    call='Solution().maxValidSplits([10, 15, 10])',
    expect=1,
    max_steps=90,
    skip=['while y > 0', 'x, y = y, x % y', 'return x', 'p = length + index', 'length >>= 1', 'for index in range(length)',
          'length = m >> 1', 'while length >= 1',
          'if index == 0', 'pre_g = 0', 'pre_g = pre[index - 1]', 'if index == n - 1', 'suf_g = 0', 'suf_g = suf[index + 1]',
          'n = len(nums)', 'pre = []', 'pre_first = {}', 'suf = []', 'suf_first = {}', 'for index in range(start', 'v = nums[index]',
          'g_list.append(g)', 'g = 0', 'm = 1', 'while m < n', 'm <<= 1', 32, 33,
          'while p > 1', 66, 105, 73, 92, 'if g not in first', 'x = gcd(other', 'p = 1', 109, 'p >>= 1', 'while p < m', 'p <<= 1', 'other = 0', 'if p == index', 'if index == p', 'continue',
          'p = index + m'],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前删除的 index，红 = 被删的数，粉 = p）', cell=70, h=150,
             pointers={'index': 'blue', _PP: 'pink'}, pointer_labels={_PP: 'p'},
             color=lambda S, i, v: ('red' if (S.get('pre_g') is not None and S['_line'] >= 63 and i == S.get('index')) else None)),
        dict(type='array', var='pre', label='pre[i]：前缀 gcd', cell=70, h=125),
        dict(type='array', var='suf', label='suf[i]：后缀 gcd', cell=70, h=125),
        dict(type='array', var='f', label='线段树 f（f[1] = 根；叶子 f[m..] 是 nums，被删的叶子置 0）', cell=60, h=150,
             pointers={_PT: 'pink'}, pointer_labels={_PT: 'p'}),
        dict(type='text', h=64, size=26, fn=lambda S: (f"`pre_first = {S['pre_first']}`　`suf_first = {S['suf_first']}`" if 'pre_first' in S and 'suf_first' in S and S['_line'] >= 25 else '')),
    ],
    watch=['index', 'pre_g', 'suf_g', ('g', 'g', 'cyan'), ('p', 'p', 'pink'), ('score', 'score', 'yellow'), ('res', 'res', 'green')],
    captions={
        'generate(0, n, 1': '正向扫：记下前缀 gcd，以及每种 gcd ==第一次出现==的位置',
        'generate(n - 1, -1, -1': '反向扫：记下后缀 gcd，以及每种 gcd 最靠右的出现位置',
        'g = gcd(g, v)': '把 `{v}` 并入当前的 gcd：`gcd({g}, {v})`',
        'first[g] = index': '记下 gcd `{g}` 第一次出现的位置：`{index}`',
        'suf.reverse()': '`suf` 是倒着生成的，翻转后 `suf[i]` 就是后缀 `nums[i:]` 的 gcd',
        'f = [0] * (m << 1)': '建线段树：叶子放 `nums`（`m = {m}`），内部节点放区间 gcd',
        'f[p] = gcd(f[p << 1]': '`f[{p}] = gcd(f[{p << 1}], f[{(p << 1) | 1}])`',
        'res = max(0, suf_first[f[1]]': '不删：整体 gcd `g = {f[1]}`，分割点在 `pre_first[g]` 与 `suf_first[g]` 之间 → `res = {res}`',
        43: '枚举删除位置 `index = {index}`：`pre_g`/`suf_g` 是左右两侧的 gcd，空的一侧记 0',
        'g = gcd(pre_g, suf_g)': '删掉它后整个数组的 gcd：`gcd({pre_g}, {suf_g})`',
        'if g == pre_g and g == suf_g': lambda S, B, r: ('两侧都等于 `g` → ==情况 1==：`pre_first`、`suf_first` 在 `index` 两侧' if (S.g == S.pre_g and S.g == S.suf_g) else f'`g = {S.g}`，`pre_g = {S.pre_g}`，`suf_g = {S.suf_g}`：不是两侧都等于 g'),
        'res = max(res, suf_first[g] - pre_first[g] - 1)': '分割点 `pre_first..suf_first−1` 但 `index` 被删，少一个：`{suf_first[g]} − {pre_first[g]} − 1` → `res = {res}`',
        'if g != pre_g and g != suf_g': lambda S, B, r: ('两侧都不等于 `g` → ==情况 2==：没有合法分割点，跳过' if (S.g != S.pre_g and S.g != S.suf_g) else '恰好有一侧等于 `g` → 要用线段树找出删除后的分界点 `p`'),
        63: '定位 `nums[{index}]` 的叶子：`p = index + m = {p}`',
        'f[p] = 0': '叶子置 0（`gcd(0, x) = x`）→ 相当于==删掉== `nums[{index}]`，再向上重算祖先',
        'f[p >> 1] = gcd': '重算父节点：`f[{p >> 1}] = gcd(f[{p}], f[{p ^ 1}])`',
        'if g == pre_g:': lambda S, B, r: ('只有左边是 g → ==情况 3==：分割点在 index 左侧；从根往下二分找最大的 `p`，使 `arr[p:]` 的 gcd 为 g' if S.g == S.pre_g else '只有右边是 g → ==情况 4==：分割点在 index 右侧；从根往下二分找最小的 `p`，使 `arr[:p+1]` 的 gcd 为 g'),
        'if f[p << 1 | 1] == g': lambda S, B, r: (f'右孩子 `f[{(S.p << 1) | 1}] = {S.f[(S.p << 1) | 1]}` 等于 g → 后缀只取右半就够，往右走' if S.f[(S.p << 1) | 1] == S.g else f'右孩子 `f[{(S.p << 1) | 1}] = {S.f[(S.p << 1) | 1]}` ≠ g → 要把右半并入后缀，看能否凑到 g'),
        'if x == g': lambda S, B, r: (f'`x = gcd(other, 右孩子) = {S.x} == g` → 右半并入后缀后 gcd 到了 g，所以 `p` 应在右孩子里：往右走' if S.x == S.g else f'`x = gcd(other, 右孩子) = {S.x} ≠ g` → 右半还不够，并入后缀（`other = x`），`p` 在左孩子里'),
        'p |= 1': '往右孩子走：`p = {p}`',
        82: '`other = {other}`：右孩子已经并入后缀',
        'if f[p << 1] == g': lambda S, B, r: (f'左孩子 `f[{S.p << 1}] = {S.f[S.p << 1]}` 等于 g → 前缀只取左半就够，往左走' if S.f[S.p << 1] == S.g else f'左孩子 `f[{S.p << 1}] = {S.f[S.p << 1]}` ≠ g → 要把左半并入前缀，看能否凑到 g'),
        'if x != g': lambda S, B, r: (f'`x = gcd(other, 左孩子) = {S.x} ≠ g` → 左半并入前缀后还没到 g，`p` 在右孩子里：并入并往右走' if S.x != S.g else f'`x = gcd(other, 左孩子) = {S.x} == g` → 左半就够了，`p` 在左孩子里'),
        99: '`other = {other}`：左孩子已经并入前缀',
        'p -= m': '线段树下标还原成数组下标：`p = {p}`',
        'p -= 1': '`p` 撞上被删的位置 → 向左挪一位',
        'p += 1': '`p` 撞上被删的位置 → 向右挪一位',
        'score = p - pre_first[g]': '分割点可取 `pre_first[g]..p−1`：`{p} − {pre_first[g]}` = ==`{score}`==（≤ 0 表示没有）',
        'score = suf_first[g] - p': '分割点可取 `p..suf_first[g]−1`：`{suf_first[g]} − {p}` = ==`{score}`==（≤ 0 表示没有）',
        'res = max(res, score)': '`res = max({B.res}, {score}) = {res}`',
        'f[p] = v': '把叶子改回 `nums[{index}] = {v}`，向上重算，线段树恢复原样',
        'return res': '最多有效分割位置：`{res}`',
    },
    cards=dict(
        one_liner='整体 gcd 是 g：删一个数后，分割点落在两个「第一次出现 g」的位置之间',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['可以删除至多一个元素，得到 `arr`；分割位置 `index` 有效：前缀 gcd 等于后缀 gcd',
                 '求最多的有效分割位置个数',
                 '示例：`[10,15,10]` → `1`（删掉 15，`[10,10]` 有 1 个分割位置）'],
        quote='若pre[index]等于suf[index + 1]，而整个数组的最大公约数又可以写作gcd(pre[index], suf[index + 1])，那么就说明pre[index]与suf[index + 1]都恰好等于整个数组的最大公约数。',
        quote_src='—— yiduobo 题解原文',
        idea=['不删时：用 `pre_first[g]`、`suf_first[g]` 记下 gcd 第一次到 g 的位置，答案 `max(0, suf_first[g] − pre_first[g])`',
              '删 `index` 后分四种情况：两侧都是 g（算差再减 1）、都不是（跳过）、只有左侧是（线段树找 `p`）、只有右侧是',
              '线段树把 `nums[index]` 置 0 后，从根往下二分，找出删除后的分界点 `p`，再恢复'],
        summary=['时间 `O(n log n)`：建树 `O(n)`，每个 index 一次线段树下行 `O(log n)`（不计 gcd 本身的对数）',
                 '易错点：`p` 可能和被删的 `index` 重合，要左挪或右挪一位；`suf_first` 记录的是后缀里最靠右的位置',
                 '0 当作「空」：`gcd(0, x) = x`，所以 `index = 0`、`index = n−1` 时用 `pre_g = 0`、`suf_g = 0`',
                 '原文已是 Python 3 可运行写法（只用位运算与 `//` 无关的整数运算），没有改动',
                 '对比灵神：灵神证明至多删一个位置并只需 p、q 两个下标；yiduobo 保持逐位枚举，用线段树二分补全情况 3、4'],
    ),
)
