NUMS = [3, 4, 1, 2]


def _txt(S):
    if 'k' not in S:
        if 'index' in S and 'p' in S:
            return f"从 `index = {S['index']}` 起找最长非递减段，截止在 `p = {S['p']}`"
        return '先算 f：f[i] = 从 i 起第一个「比前一个小」的位置'
    if 'start' not in S:
        return f"检验 `k = {S['k']}`：每 {S['k']} 个一块"
    blk = S['nums'][S['start']:S['end'] + 1]
    return f"块 `{blk}`（下标 {S['start']}..{S['end']}），上一块最大值 `pre_ma = {S['pre_ma']}`"


CONFIG = dict(
    num=3886, title='可排序整数求和', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='f 数组 · 枚举因子 · 两种合法形态',
    tags=['灵神题单', '思维题', '难度分 1999'],
    code='''
class Solution(object):
    def sortableIntegers(self, nums):
        
        n = len(nums)
        f = []
        
        index = 0
        while index < n:
            p = index + 1
            while p < n and nums[p] >= nums[p - 1]:
                p += 1
            f.extend([p] * (p - index))
            index = p

        def check(k):
            pre_ma = 0
            for start in range(0, n, k):
                end = start + k - 1
                if f[start] > end:
                    if nums[start] >= pre_ma:
                        pre_ma = nums[end]
                    else:
                        return False
                
                elif f[f[start]] > end and nums[end] <= nums[start]:
                    if nums[f[start]] >= pre_ma:
                        pre_ma = nums[f[start] - 1]
                    else:
                        return False

                else:
                    return False
            
            return True

        res = 0
        k = 1
        while k * k <= n:
            if n % k == 0:
                if check(k):
                    res += k
                if n // k != k and check(n // k):
                    res += n // k
            k += 1
        
        return res
''',
    call=f'Solution().sortableIntegers({NUMS})',
    expect=4,
    max_steps=110,
    skip=['n = len(nums)', 'f = []', 'index = 0', 37],
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='nums', label='nums（蓝框 = 当前块 start..end）', cell=100,
             window=('start', 'end'), pointers={'index': 'blue', 'p': 'pink'}, h=250),
        dict(type='array', var='f', label='f[i]：从 i 起这段非递减序列的终点（下一个不满足的位置）', cell=100, h=220),
    ],
    watch=[('k', 'k', 'blue'), ('pre_ma', 'pre_ma', 'orange'), ('res', 'res', 'green')],
    captions={
        'while index < n': '`index < n`？{"是，再找一段非递减序列" if B.index < B.n else "否，f 算完了"}',
        'p = index + 1': '`p` 从 `index + 1` 开始往右试探',
        'while p < n and': lambda S, B, r: (f'`nums[{B.p}] = {B.nums[B.p]} >= nums[{B.p - 1}] = {B.nums[B.p - 1]}`：==没有下降，p 继续右移==' if (B.p < B.n and B.nums[B.p] >= B.nums[B.p - 1])
                                            else ('`p` 已到末尾，这段到头了' if B.p >= B.n else f'`nums[{B.p}] = {B.nums[B.p]} < nums[{B.p - 1}] = {B.nums[B.p - 1]}`：==出现下降，这段到 p 为止==')),
        'p += 1': '`p → {p}`',
        'f.extend': '`index..p-1` 这一段每个位置的 f 都是 `p = {p}`：`f = {f}`',
        'index = p': '`index = {index}`，接着找下一段',
        'def check': '',
        'pre_ma = 0': '`pre_ma`：上一块的最大值，初始为 0',
        'for start in range': '块的起点 `start`：0、k、2k、……',
        'end = start + k - 1': '当前块 `[{start}, {end}]`，内容 `{nums[start:end + 1]}`',
        'if f[start] > end': lambda S, B, r: (f'`f[{B.start}] = {B.f[B.start]} > end = {B.end}`：块内没有下降，==本身非递减==' if B.f[B.start] > B.end
                                              else f'`f[{B.start}] = {B.f[B.start]} <= end = {B.end}`：块内有下降，不是单段'),
        'if nums[start] >= pre_ma': lambda S, B, r: (f'最小值 `nums[{B.start}] = {B.nums[B.start]}` >= `pre_ma = {B.pre_ma}`：==接得上=='
                                                     if B.nums[B.start] >= B.pre_ma else f'最小值 `nums[{B.start}] = {B.nums[B.start]}` < `pre_ma = {B.pre_ma}`：==接不上，k 不合法=='),
        'pre_ma = nums[end]': '递增块的最大值是末尾：`pre_ma = nums[{end}] = {pre_ma}`',
        'elif f[f[start]] > end': lambda S, B, r: (
            f'下降点后的第二段 `[{B.f[B.start]}, {B.end}]` 是否非递减、且末尾 `{B.nums[B.end]}` <= 首位 `{B.nums[B.start]}`：'
            + ('==是，可以由递增序列循环移位得到==' if (B.f[B.f[B.start]] > B.end and B.nums[B.end] <= B.nums[B.start]) else '==否，k 不合法==')),
        'if nums[f[start]] >= pre_ma': lambda S, B, r: (f'移位后块的最小值是第二段开头 `nums[{B.f[B.start]}] = {B.nums[B.f[B.start]]}`，与 `pre_ma = {B.pre_ma}` 比：'
                                                        + ('==接得上==' if B.nums[B.f[B.start]] >= B.pre_ma else '==接不上，k 不合法==')),
        'pre_ma = nums[f[start] - 1]': '块的最大值是第一段末尾：`pre_ma = nums[{f[start] - 1}] = {pre_ma}`',
        'return False': '`k = {k}` ==不合法==',
        'return True': '所有块都通过：`k = {k}` ==合法==',
        'res = 0': '`res` 累加合法的 k',
        'while k * k <= n': '`k * k = {k * k}` {"<=" if B.k * B.k <= B.n else ">"} `n = {n}`：{"继续枚举" if B.k * B.k <= B.n else "枚举结束"}',
        'if n % k == 0': '`{n} % {k} = {n % k}`：{"是因子，检验 k 和 n // k" if n % k == 0 else "不是因子"}',
        'if check(k)': '检验 `k = {k}`',
        'res += k': '`k = {k}` 合法：`res = {res}`',
        'if n // k != k': '另一个因子 `n // k = {B.n // B.k}`：{"与 k 不同，也要检验" if B.n // B.k != B.k else "和 k 相同，不重复"}',
        'res += n // k': '`n // k` 合法：`res = {res}`',
        'k += 1': '`k → {k}`',
        'return res': '可排序整数之和 `{res}`',
    },
    cards=dict(
        one_liner='每块要么本身非递减，要么「后半段 ≤ 前半段」两段拼成',
        complexity='时间 `O(n log log n)`，空间 `O(n)`',
        problem=['`k` 是 `n` 的因数：把 `nums` 切成长为 `k` 的块，每块可独立循环移位（左移或右移任意次）',
                 '能让整个数组非递减的 `k` 叫可排序整数，求它们的和',
                 '示例：`[3,1,2]` → `3`；本视频：`[3,4,1,2]` → `4`'],
        quote='不妨反过来考虑，一个非递减的子数组在经过若干步左移或者右移操作之后会变成什么。第一种是保持不变；第二种是某个后缀被移动到前面。',
        quote_src='—— yiduobo 题解原文',
        idea=['一块要合法：要么单段非递减，要么由两段非递减拼成，且前半段首位 ≥ 后半段末位',
              '块与块之间：前一块最大值 ≤ 后一块最小值，用 `pre_ma` 记录',
              '先用 f 数组记录每个位置所在非递减段的终点，检验一块只需 O(1)'],
        summary=['时间 `O(n log log n)`，空间 `O(n)`',
                 '易错：两段情形里，块的最小值是 `nums[f[start]]`，最大值是 `nums[f[start] - 1]`',
                 '`n // k != k` 时才检验 `n // k`，避免平方数重复相加',
                 '原文为 Python 2 写法，本题代码无需改动即可在 Python 3 运行',
                 '对比灵神：灵神 `next_dec` 记的是下降点（`nums[j] > nums[j+1]`），yiduobo 的 f 记的是段终点'],
    ),
)
