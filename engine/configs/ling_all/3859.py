def _info(S):
    if 'distinct_limit' not in S:
        return ''
    d = S['distinct_limit']
    s = f"第 {'1' if d == S['k'] else '2'} 次：至少 `{d}` 种不同整数 且 至少 `{S['k']}` 种好整数（出现 ≥ {S['m']} 次）"
    if 'good_numbers' in S and 'cnt' in S:
        s += f"　窗口：`{len(S['cnt'])}` 种数，`{S['good_numbers']}` 个好整数"
    return s


CONFIG = dict(
    num=3859, title='统计包含 K 个不同整数的子数组', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='至少型滑窗相减 · calc(k) − calc(k+1)',
    tags=['难度分 2302'],
    code='''
class Solution:
    def countSubarrays(self, nums, k: int, m: int) -> int:
        # 子数组至少有 distinct_limit 个不同的整数，其中至少有 k 个不同的好整数
        def calc(distinct_limit: int) -> int:
            cnt = defaultdict(int)  # 用来统计不同元素个数
            good_numbers = 0  # 窗口中的好整数（出现至少 m 次的整数）的个数
            ans = left = 0
            for x in nums:
                # 1. 入
                cnt[x] += 1
                if cnt[x] == m:
                    good_numbers += 1

                # 2. 出
                while len(cnt) >= distinct_limit and good_numbers >= k:
                    out = nums[left]
                    if cnt[out] == m:
                        good_numbers -= 1
                    cnt[out] -= 1
                    if cnt[out] == 0:
                        del cnt[out]
                    left += 1

                # 3. 更新答案
                ans += left
            return ans

        return calc(k) - calc(k + 1)
''',
    call='Solution().countSubarrays([1,2,1,2,2], 2, 2)',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = left：left 之前的元素已移出窗口）', pointers={'left': 'blue'},
             dim=lambda S, i, v: 'left' in S and i < S['left'], h=210, cell=100),
        dict(type='map', var='cnt', label='cnt（窗口内各数出现次数）', fmt=lambda k, v: f'{k}: {v}', h=130, font=32),
        dict(type='text', h=100, size=26, fn=_info),
    ],
    watch=[('x', 'x'), ('left', 'left', 'blue'), ('good', 'good_numbers', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'cnt = defaultdict': '新一轮：`distinct_limit = {distinct_limit}`，窗口清空，`good_numbers = 0`',
        'ans = left = 0': '`left` = 满足条件的最大左端点之后的位置，`ans` 累加合法左端点个数',
        'cnt[x] += 1': '右端点 `{x}` 入窗口：`cnt[{x}] = {cnt[x]}`',
        'if cnt[x] == m': lambda S, B, r: (f'`cnt[{S.x}] = {S.m}`：{S.x} 刚好出现 m 次，成为==好整数== → 好整数 +1，`good_numbers` → {S.good_numbers + 1}' if S.cnt[S.x] == S.m
                                            else f'`cnt[{S.x}] = {S.cnt[S.x]}` ≠ m = {S.m}，好整数个数不变'),
        'while len(cnt) >= distinct_limit': lambda S, B, r: (
            f'种类 `{len(S.cnt)}` ≥ {S.distinct_limit} 且好整数 `{S.good_numbers}` ≥ k={S.k}：窗口已满足，尝试缩小左端点（越短越不满足，所以能缩就缩）'
            if len(S.cnt) >= S.distinct_limit and S.good_numbers >= S.k
            else f'种类 `{len(S.cnt)}` 或好整数 `{S.good_numbers}` 没达标（要 ≥ {S.distinct_limit}、≥ {S.k}）：停止缩窗口'),
        'out = nums[left]': '准备移出最左边的 `{out}`',
        'if cnt[out] == m': lambda S, B, r: (f'`cnt[{S.out}] = {S.m}`：移出后它不再是好整数 → 好整数 −1，`good_numbers` → {S.good_numbers - 1}' if S.cnt[S.out] == S.m
                                              else f'`cnt[{S.out}] = {S.cnt[S.out]}` ≠ m，好整数个数不变'),
        'cnt[out] -= 1': '`cnt[{out}]` 减一 → `{cnt[out]}`',
        'if cnt[out] == 0': lambda S, B, r: (f'`cnt[{S.out}] = 0`：窗口里没有它了，删掉' if S.cnt[S.out] == 0 else '还有剩余，不删'),
        'del cnt[out]': '删除 `{out}`，不同整数种类 −1',
        'left += 1': '`left` → {left}',
        'ans += left': '以当前 `x` 为右端点：左端点 `0 .. left-1` 共 =={left}== 个都满足“至少”，`ans` → {ans}',
        'return ans': '本轮至少型计数 `{ans}`',
        'return calc(k)': lambda S, B, r: (f'答案 = `calc({S.k}) − calc({S.k + 1})` = =={r}==' if r is not None else '先后算两轮：`calc(k)` 和 `calc(k+1)`'),
    },
    skip=['for x in nums', 'out = nums[left]', 'good_numbers = 0', 'good_numbers += 1', 'good_numbers -= 1'],
    max_steps=110,
    cards=dict(
        one_liner='“至少” 减 “至少”：减去的那一份必须保持好整数 ≥ k',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组 `nums`，求子数组个数：==恰好== 有 `k` 种不同整数，且每种都==至少出现 `m` 次==',
                 '示例：`nums = [1,2,1,2,2], k = 2, m = 2` → `2`',
                 '满足的子数组：`[1,2,1,2]` 和 `[1,2,1,2,2]`'],
        quote='问题应当拆分为：子数组至少有 k 个不同的整数，其中至少有 k 个不同的好整数；子数组至少有 k+1 个不同的整数，其中至少有 k 个不同的好整数；二者相减，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['“出现至少 m 次的整数” 叫好整数；要求恰有 k 种整数，且全是好整数',
              '错误拆法：第二项写成“至少 k+1 个好整数”，会多算“k+1 种整数、恰 k 个好整数”的子数组',
              '正确：第二项是“至少 k+1 种整数、至少 k 个好整数”，窗口都有单调性，用同一个 `calc`',
              '`ans += left`：右端点固定时，合法的左端点是 `0 .. left-1`'],
        summary=['时间 `O(n)`，两次滑窗各 `O(n)`',
                 '易错：第二轮的限制是 `distinct_limit = k+1`，但好整数仍然是 `>= k`',
                 '好整数个数在 `cnt[x] == m` 时加一，移出时 `cnt[out] == m` 先减一再减计数',
                 '入窗口 → 缩窗口（满足条件才缩）→ 累加 `left`，是“至少型”滑窗的模板',
                 '先做 2962 题理解 `ans += left`'],
    ),
)
