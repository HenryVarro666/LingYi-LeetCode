import math

def _fmt_first(d):
    return '  '.join(f'`{k}`→{v}' for k, v in d.items())


def _info(S):
    ln = S.get('_line', 0)
    pre, suf = S.get('pre'), S.get('suf')
    if pre is None:
        return ''
    parts = [f'前缀 gcd `pre` = {pre}']
    if S.get('suf'):
        parts.append(f'后缀 gcd `suf` = {suf}')
    return '；'.join(parts)


def _node(S, k, v):
    return None


CONFIG = dict(
    num=4035, title='最多有效分割位置 I', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='前后缀 gcd + 线段树二分',
    tags=[],
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
    call='Solution().maxValidSplits([2, 2, 3])',
    expect=1,
    skip=['x, y = y, x % y', 'while y > 0', 'return x', 'def gcd', 'n = len(nums)', 'pre = []', 'pre_first = {}', 'suf = []', 'suf_first = {}',
          'v = nums[index]', 'g_list.append', 'm <<= 1', 'while m < n', 'f = [0]', 'for index, v in enumerate(nums):\n            f[m',
          'p >>= 1', 'length >>= 1', 'f[p >> 1] = gcd', 'p = length + index', 'f[p] = gcd', 'p = index + m', 'f[p] = 0', 'f[p] = v',
          'p = 1', 'other = 0', 'p |= 1', 'p <<= 1', 'x = gcd(other', 'other = x', 'for index in range(length)', 'while length >= 1', 'length = m >> 1',
          'while p > 1', 'while p < m', 'm = 1', 'g = 0', 'f[m + index] = v', 'suf.reverse',
          32, 'for index in range(start', 'if g not in first', 'if index == 0', 'if index == n - 1', 'if p == index', 'if index == p', 'continue'],
    max_steps=100,
    views=[
        dict(type='array', var='nums', label='nums', h=190, cell=90, pointers={'index': 'blue'},
             color=lambda S, k, v: 'blue' if k == S.get('index') and S.get('_line', 0) >= 46 else None),
        dict(type='array', var=lambda S: S['pre'] if S.get('pre') else [], label='pre：前缀 gcd', h=120, cell=70),
        dict(type='array', var=lambda S: S['suf'] if S.get('suf') else [], label='suf：后缀 gcd', h=120, cell=70),
        dict(type='map', var=lambda S: S['pre_first'] if S.get('pre_first') else {}, label='pre_first：前缀 gcd 首次出现的位置', h=90,
             fmt=lambda k, v: f'{k} → {v}'),
        dict(type='map', var=lambda S: S['suf_first'] if S.get('suf_first') else {}, label='suf_first：后缀 gcd 在整个数组中最后出现的位置', h=90,
             fmt=lambda k, v: f'{k} → {v}'),
    ],
    watch=['index', 'g', 'pre_g', 'suf_g', ('score', "score", 'green'), ('res', 'res', 'green')],
    captions={
        'generate(0, n, 1, pre, pre_first)': '正向扫一遍：`pre[i]` = `nums[:i+1]` 的 gcd，`pre_first` 记每种 gcd 首次出现的下标',
        'generate(n - 1, -1, -1, suf, suf_first)': '反向扫一遍：`suf` 倒着收集，`suf_first` 记每种后缀 gcd 在整个数组里最靠右的下标（它们出现时的最小后缀起点）',
        'g = gcd(g, v)': lambda S, B, r: (lambda ng: f'第 `{S.index}` 个数 `{S.v}`：`g = gcd({B.g}, {S.v}) = {ng}`' + (f'，`{ng}` 第一次出现 → 记下位置 `{S.index}`' if ng not in B.first else f'，`{ng}` 之前出现过，不更新'))(math.gcd(B.g, S.v)),
        'first[g] = index': '`first[{g}] = {index}`',
        'res = max(0, suf_first': '不删元素：前后缀 gcd 都要等于整体 gcd `g = {f[1]}`；合法分割点在 `pre_first[g]` 到 `suf_first[g] - 1` 之间，共 `max(0, {suf_first[f[1]]} - {pre_first[f[1]]})` = =={res}== 个',
        'for index, v in enumerate(nums):': lambda S, B, r: ('每个位置都试过删除了' if B.get('index') == S.index and 'pre_g' in B else f'枚举删除 `nums[{S.index}] = {S.v}`'),
        'pre_g = 0': '`index == 0`，删第一个元素：左边没有元素，`pre_g = 0`（gcd(0, x) = x）',
        'pre_g = pre[index - 1]': '左边剩下前缀的 gcd：`pre_g = pre[{index - 1}] = {pre_g}`',
        'suf_g = 0': '`index == n - 1`，删最后一个元素：右边没有元素，`suf_g = 0`',
        'suf_g = suf[index + 1]': '右边剩下后缀的 gcd：`suf_g = suf[{index + 1}] = {suf_g}`',
        'g = gcd(pre_g, suf_g)': lambda S, B, r: f'删掉后整个数组的 gcd：`g = gcd({S.pre_g}, {S.suf_g}) = {math.gcd(S.pre_g, S.suf_g)}`',
        'if g == pre_g and g == suf_g': lambda S, B, r: ('情况 1：两边 gcd 都等于 `g` → `pre_first[g]` 与 `suf_first[g]` 在 `index` 两侧' if S.g == S.pre_g and S.g == S.suf_g else f'两边不是都等于 `g = {S.g}`（`pre_g = {S.pre_g}`，`suf_g = {S.suf_g}`）'),
        'res = max(res, suf_first[g] - pre_first[g] - 1)': '情况 1：位置被删掉少一个：`{suf_first[g]} - {pre_first[g]} - 1` → `res` = =={res}==',
        'if g != pre_g and g != suf_g': lambda S, B, r: ('情况 2：两边都不等于 `g`（gcd 只会越做越小）→ 不可能有合法分割点，跳过' if S.g != S.pre_g and S.g != S.suf_g else f'至少一边等于 `g = {S.g}`，要用线段树继续找'),
        'if g == pre_g:': lambda S, B, r: (f'`pre_g = {S.pre_g}` 等于 `g` → 情况 3：分割点只能在 `index` 左侧，线段树找最大的 `p`，使 `arr[p:]` 的 gcd 等于 `g`' if S.g == S.pre_g else f'`suf_g = {S.suf_g}` 等于 `g` 而 `pre_g` 不等 → 情况 4：分割点只能在右侧，线段树找最小的 `p`，使 `arr[:p+1]` 的 gcd 等于 `g`'),
        'if f[p << 1 | 1] == g': '看右孩子区间的 gcd：`{f[p << 1 | 1]}` 是否等于 `g = {g}`（删掉的位置已置 0）',
        'p -= m': '从线段树节点转回数组下标：`p = {p}`（被删位置是 `{index}`，若重合要移开一位）',
        'if x == g': lambda S, B, r: (f'右孩子并上 `other` 的 gcd：`x = {S.x}` 等于 `g` → `p` 走到右孩子' if S.x == S.g else f'`x = {S.x}` 不等于 `g = {S.g}` → 右孩子整段要算进后缀（`other = {S.x}`），`p` 走到左孩子'),
        'if x != g': lambda S, B, r: (f'左孩子并上 `other` 的 gcd：`x = {S.x}` 不等于 `g` → 左边不够，`p` 走到右孩子，`other = {S.x}`' if S.x != S.g else f'`x = {S.x}` 等于 `g` → 左孩子已经够了，`p` 留在左孩子'),
        'p -= 1': '`p` 与被删位置重合，向前移一位：`p = {p}`',
        'score = p - pre_first[g]': '情况 3：分割点在 `pre_first[g] = {pre_first[g]}` 到 `p - 1` 之间 → `score = {p} - {pre_first[g]}` = =={score}==',
        'p += 1': '`p` 与被删位置重合，向后移一位：`p = {p}`',
        'score = suf_first[g] - p': '情况 4：分割点在 `p` 到 `suf_first[g] - 1` 之间 → `score = {suf_first[g]} - {p}` = =={score}==',
        'res = max(res, score)': '`res = max({B.res}, {score}) = {res}`',
        'return res': '最多的有效分割位置：`{res}`',
    },
    cards=dict(
        one_liner='先算前后缀 gcd，再枚举删哪个元素，线段树二分找边界',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['最多删掉一个元素，剩下数组 `arr` 的分割点 `i` 有效当且仅当 `gcd(arr[:i+1]) == gcd(arr[i+1:])`',
                 '求 `arr` 的最大可能有效分割点个数（得分）',
                 '示例：`[10,30,15,10]` → `2`；本视频：`[2,2,3]` → `1`（删掉 3）'],
        quote='若pre[index]等于suf[index + 1]，而整个数组的最大公约数又可以写作gcd(pre[index], suf[index + 1])，那么就说明pre[index]与suf[index + 1]都恰好等于整个数组的最大公约数。',
        quote_src='—— yiduobo 题解原文',
        idea=['不删元素：两边 gcd 都等于整体 `g`，合法分割点是 `pre_first[g]` 到 `suf_first[g]-1`，共 `max(0, suf_first[g] - pre_first[g])` 个',
              '删 `nums[index]` 后分四种情况：两边都等于 `g`（直接算）、都不等于（跳过）、只有一边等于（要找边界）',
              '只有一边等于时，用线段树二分（把被删位置置 0 再自底向上更新）找出另一侧边界 `p`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`gcd(0, x) = x`：删首尾元素时用 0 占位',
                 '`res` 下界是 0：`pre_first[g]` 可能在 `suf_first[g]` 右边',
                 '线段树里用 0 占掉被删位置，找到 `p` 后要把它改回原值',
                 '`p` 与被删位置重合时要向内移一位',
                 '原文已是 Python 3 可运行写法（无整数除法/print），无需改动'],
    ),
)
