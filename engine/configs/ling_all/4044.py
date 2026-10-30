def _wins(S):
    """返回 (窗口1 下标列表, 窗口2 下标列表)，与 sum1/sum2 当前包含的元素一致"""
    if 'i' not in S or 'sum1' not in S:
        return [], []
    i, n, m = S['i'], S['n'], S['m']
    ln = S.get('_line', 0)
    hi = i - 1 if ln == 6 else i          # for 行：本轮还没入
    lo = max(0, hi - n + 1) if hi >= n - 1 else 0
    if hi >= n - 1 and ln == 6:
        lo = hi - n + 2                    # 上一轮已经出过
    a = lo + (1 if ln in (20, 21) else 0)
    b = lo + m + (1 if ln == 21 else 0)
    w1 = [j % n for j in range(a, hi - m + 1)]
    w2 = [j % n for j in range(b, hi + (0 if ln == 8 else 1))]
    return w1, w2


def _col(S, j, v):
    w1, w2 = _wins(S)
    if j in w1:
        return 'cyan'
    if j in w2:
        return 'pink'
    return None


def _txt(S):
    w1, w2 = _wins(S)
    if not w1 and not w2:
        return '两个长为 `n/2` 的窗口一起向右滑（下标 `% n` 实现循环）'
    nums = S['nums']
    a = '+'.join(str(nums[j]) for j in w1) or '0'
    b = '+'.join(str(nums[j]) for j in w2) or '0'
    return f"前半 `{a}` = =={S['sum1']}==　后半 `{b}` = =={S['sum2']}=="


def _rot(S):
    if 'left' not in S or S['left'] < 0 or S.get('_line') in (6, 8, 9):
        return None
    l = S['left']
    return S['nums'][l:] + S['nums'][:l]


CONFIG = dict(
    num=4044, title='统计好循环移位的数量', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='两个定长滑动窗口同时滑',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1418'],
    code='''
class Solution:
    def countGoodRotations(self, nums: list[int]) -> int:
        n = len(nums)
        m = n // 2
        ans = sum1 = sum2 = 0
        for i in range(m, n * 2 - 1):
            # 1. 入
            sum1 += nums[(i - m) % n]
            sum2 += nums[i % n]

            left = i - n + 1
            if left < 0:  # 尚未形成第一个窗口
                continue

            # 2. 更新答案
            if sum1 > sum2:
                ans += 1

            # 3. 出
            sum1 -= nums[left]
            sum2 -= nums[(left + m) % n]
        return ans
''',
    call='Solution().countGoodRotations([1,2,3,4,5,6])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（青 = 前半窗口 sum1，粉 = 后半窗口 sum2）', h=240, cell=110,
             color=_col),
        dict(type='array', var=_rot, label='当前循环移位（左半 vs 右半）', h=200, cell=90, index=False,
             color=lambda S, j, v: 'cyan' if j < S['n'] // 2 else 'pink'),
        dict(type='text', h=100, size=30, fn=_txt),
    ],
    watch=['n', 'm', ('i', 'i', 'blue'), ('left', 'left'), ('sum1', 'sum1', 'cyan'), ('sum2', 'sum2', 'pink'),
           ('ans', 'ans', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'm = n // 2': '每个窗口长 `m = n / 2 = {m}`',
        'ans = sum1 = sum2 = 0': '`sum1`：前半窗口和；`sum2`：后半窗口和',
        'for i in range': lambda S, B, ret: (f'`i = {S.i}`：后半窗口右端到 `{S.i % S.n}`，前半窗口右端到 `{(S.i - S.m) % S.n}`'
                                            if 'i' not in B or S.i != B.i else '共 n 个循环移位，滑完了'),
        'sum1 += nums[(i - m) % n]': '1. 入：前半窗口加入 `nums[{(i - m) % n}] = {nums[(i - m) % n]}` → `sum1 = {sum1}`',
        'sum2 += nums[i % n]': '1. 入：后半窗口加入 `nums[{i % n}] = {nums[i % n]}` → `sum2 = {sum2}`',
        'left = i - n + 1': '当前循环移位的起点 `left = {i} − {n} + 1 = {left}`',
        'if left < 0': lambda S, B, ret: (f'`left = {S.left} < 0`：两个窗口还没装满' if S.left < 0
                                          else f'从下标 `{S.left}` 开始的循环移位成形了'),
        'continue': '继续入',
        'if sum1 > sum2': lambda S, B, ret: (f'2. 更新：`{S.sum1} > {S.sum2}`，前半==严格大于==后半 → 好循环移位' if S.sum1 > S.sum2
                                             else f'2. 更新：`{S.sum1} ≤ {S.sum2}`，不是好循环移位'),
        'ans += 1': '`ans` → {ans}',
        'sum1 -= nums[left]': '3. 出：`nums[{left}] = {nums[left]}` 离开前半窗口 → `sum1 = {sum1}`',
        'sum2 -= nums[(left + m) % n]': '3. 出：`nums[{(left + m) % n}] = {nums[(left + m) % n]}` 从后半窗口移到前半 → `sum2 = {sum2}`',
        'return ans': '好循环移位共 =={ans}== 个',
    },
    max_steps=70,
    cards=dict(
        one_liner='把循环移位看成两个相邻的定长窗口一起向右滑',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['偶数长度数组 `nums`，把一个前缀移到末尾得到循环移位',
                 '若前 `n/2` 个元素之和==严格大于==后 `n/2` 个之和，就是好循环移位，求个数',
                 '示例：`[1,2,3,4,5,6]` → `3`'],
        quote='视作==两个长为 n/2 的定长滑动窗口==同时向右滑动。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['任意循环移位都是 `nums + nums` 的子数组，用 `% n` 代替拼接',
              '前半窗口右端 `(i − m) % n`，后半窗口右端 `i % n`',
              '每轮：入 → 比较 `sum1 > sum2` → 出'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`i` 只到 `2n − 2`：恰好 n 个循环移位，不重复统计',
                 '后半窗口出去的元素 `nums[(left + m) % n]` 正好进入前半窗口',
                 '方法一：`nums + nums` 前缀和，判断 `2·s[i − n/2] > s[i] + s[i − n]`'],
    ),
)
