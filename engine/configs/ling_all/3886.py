NUMS = [3, 4, 1, 2]


def _col(S, i, v):
    if 'l' in S and 'r' in S and 'k' in S and S['_line'] >= 17 and S['l'] <= i <= S['r']:
        return None
    return None


def _txt(S):
    if 'k' not in S:
        return '先预处理 `next_dec`，再枚举 4 的因子 k'
    if 'l' not in S:
        return f"检验 `k = {S['k']}`：把数组切成长 {S['k']} 的块，每块可循环移位"
    k, l, r = S['k'], S['l'], S['r']
    blk = S['nums'][l:r + 1]
    return f"块 `{blk}`（下标 {l}..{r}），上一块最大值 `last_max = {S['last_max']}`"


CONFIG = dict(
    num=3886, title='可排序整数求和', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='next_dec 预处理 · 枚举因子 · 逐块检查',
    tags=['灵神题单', '思维题', '难度分 1999'],
    code='''
class Solution:
    def sortableIntegers(self, nums: List[int]) -> int:
        n = len(nums)
        next_dec = [0] * n  # nums[next_dec[i]] > nums[next_dec[i] + 1]
        next_dec[-1] = p = n
        # 对于每个 i，记录下一个递减的位置
        for i in range(n - 2, -1, -1):
            if nums[i] > nums[i + 1]:
                p = i
            next_dec[i] = p

        def solve(k: int) -> None:
            last_max = 0  # 上一段的最大值
            for r in range(k - 1, n, k):
                l = r - k + 1
                m = next_dec[l]
                if m >= r:
                    # [l, r] 是递增的，最小值为 nums[l]，最大值为 nums[r]
                    # 最小值必须 >= 上一段的最大值
                    if nums[l] < last_max:
                        return
                    last_max = nums[r]
                else:
                    # [l, m] 是第一段，[m+1, r] 是第二段
                    # 第二段必须是递增的，且第二段的最小值必须 >= 上一段的最大值，且第二段的最大值必须 <= 第一段的最小值
                    if next_dec[m + 1] < r or nums[m + 1] < last_max or nums[r] > nums[l]:
                        return
                    last_max = nums[m]
            nonlocal ans
            ans += k  # 满足要求

        ans = 0
        # 枚举 n 的因子 k
        for k in range(1, isqrt(n) + 1):
            if n % k == 0:
                solve(k)
                if k * k < n:
                    solve(n // k)
        return ans
''',
    call=f'Solution().sortableIntegers({NUMS})',
    expect=4,
    max_steps=110,
    skip=['n = len(nums)', 'next_dec = [0] * n'],
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='nums', label='nums（蓝框 = 当前块，粉箭头 = 块内第一段结尾 m）', cell=100,
             window=('l', 'r'), pointers={'m': 'pink'}, h=250),
        dict(type='array', var='next_dec', label='next_dec[i]：从 i 起第一个「后面更小」的位置（n = 没有）', cell=100,
             pointers={'i': 'blue'}, h=250),
    ],
    watch=[('k', 'k', 'blue'), ('last_max', 'last_max', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'next_dec[-1] = p = n': '最后一位后面没有下降：`next_dec[{n - 1}] = {n}`（n 表示「不存在」）',
        'for i in range(n - 2': '从右往左扫，记录每个位置右边第一个「下降点」',
        'if nums[i] > nums[i + 1]': '`nums[{i}] = {nums[i]}` 和 `nums[{i + 1}] = {nums[i + 1]}`：{"==前者更大 → i 本身是下降点=="  if nums[i] > nums[i + 1] else "没有下降，沿用右边的下降点 p"}',
        'p = i': '下降点更新为 `p = {p}`',
        'next_dec[i] = p': '`next_dec[{i}] = {p}`：从 {i} 往右，第一次下降发生在下标 {p}',
        'ans = 0': '预处理完成 `next_dec = {next_dec}`。接下来枚举 n 的因子 k',
        'for k in range': '只枚举到 `isqrt(n)`，每个 k 同时检验 `k` 和 `n // k`',
        'if n % k == 0': '`{n} % {k} = {n % k}`：{"是因子，检验它" if n % k == 0 else "不是因子，跳过"}',
        'solve(k)': '检验 `k = {k}`：切成长 {k} 的块',
        'solve(n // k)': lambda S, B, r: f'`k*k < n`，所以还要检验另一个因子 `n // k = {B.n // B.k}`',
        'last_max = 0': '`last_max` 记录上一块的最大值，==下一块的最小值不能比它小==',
        'for r in range(k - 1': '每块的右端点 `r = k-1, 2k-1, …, n-1`，这里 `k = {k}`',
        'l = r - k + 1': '当前块 `[l, r] = [{l}, {r}]`，内容 `{nums[l:r + 1]}`',
        'm = next_dec[l]': '块内从 l 起第一个下降点 `m = {m}`',
        'if m >= r': lambda S, B, r: (f'`m = {B.m} >= r = {B.r}`：块内没有下降，==本身递增==' if B.m >= B.r
                                      else f'`m = {B.m} < r = {B.r}`：块内在 {B.m} 处下降，==可能是两段递增的循环移位=='),
        'if nums[l] < last_max': lambda S, B, r: (f'最小值 `nums[{B.l}] = {B.nums[B.l]}` < 上一块最大 `{B.last_max}` → ==拼起来不递增，k 不行==' if B.nums[B.l] < B.last_max
                                                  else f'最小值 `nums[{B.l}] = {B.nums[B.l]}` >= 上一块最大 `{B.last_max}`，没问题'),
        'last_max = nums[r]': '递增块的最大值是末尾：`last_max = nums[{r}] = {last_max}`',
        'if next_dec[m + 1] < r': lambda S, B, r: (
            f'第二段 `[{B.m + 1}, {B.r}]` 是否递增、最小值 `{B.nums[B.m + 1]}` 是否 >= 上一块最大 `{B.last_max}`、最大值 `{B.nums[B.r]}` 是否 <= 第一段最小 `{B.nums[B.l]}`：'
            + ('==有一条不满足，k 不行==' if (B.next_dec[B.m + 1] < B.r or B.nums[B.m + 1] < B.last_max or B.nums[B.r] > B.nums[B.l]) else '全部满足')),
        'last_max = nums[m]': '循环移位后，第二段在前、第一段在后：块的最大值是 `nums[{m}]`，`last_max = {last_max}`',
        'ans += k': '所有块都通过：==`k = {k}` 可排序==，`ans = {ans}`',
        'return ans': '可排序整数之和 `{ans}`',
    },
    cards=dict(
        one_liner='每一块要么本身递增，要么是两段递增的循环移位',
        complexity='时间 `O(n log log n)`，空间 `O(n)`',
        problem=['`k` 是 `n` 的因数：把 `nums` 切成长为 `k` 的块，每块可独立循环移位',
                 '能让整个数组非递减的 `k` 叫可排序整数，求它们的和',
                 '示例：`[3,1,2]` → `3`；本视频：`[3,4,1,2]` → `4`（只有 k = 4 可行）'],
        quote='对于一个子数组 a，如果能通过循环移动变成递增的，那么反过来，一个递增数组，通过循环移动，可以变成什么样的数组？子数组 a 本来就是递增的；或者，子数组 a 由两个递增段组成，且第一段的最小值 ≥ 第二段的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['反过来想：递增数组循环移位后，要么不变，要么「两段递增，且前段最小 ≥ 后段最大」',
              '预处理 `next_dec[i]`，O(1) 找到一块里第一次下降的位置 `m`',
              '块与块之间还要满足：本块最小值 ≥ 上一块最大值，用 `last_max` 传递'],
        summary=['时间 `O(n log log n)`：因子的 n/k 之和是 log log n 级',
                 '易错：两段的情形，最小值是 `nums[m+1]`，最大值是 `nums[m]`',
                 '`k = 1` 只有原数组已有序才行；`k = n` 只看整个数组是否是循环移位',
                 '枚举因子只到 `isqrt(n)`，另一个因子 `n // k` 一起检验（`k*k < n` 时）',
                 '`solve` 里用 `nonlocal ans` 在满足时累加 k'],
    ),
)
