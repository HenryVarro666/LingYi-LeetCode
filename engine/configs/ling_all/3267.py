CONFIG = dict(
    num=3267, title='统计近似相等数对 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右维护左 · 暴力交换两次',
    tags=['常用枚举技巧', '回溯', '难度分 2545'],
    code='''
POW10 = [10 ** i for i in range(7)]

class Solution:
    def countPairs(self, nums: List[int]) -> int:
        nums.sort()
        ans = 0
        cnt = defaultdict(int)
        for x in nums:
            st = {x}  # 不交换
            a = list(map(int, str(x)))[::-1]
            m = len(a)
            for i in range(m):
                for j in range(i + 1, m):
                    if a[i] == a[j]:  # 小优化
                        continue
                    y = x + (a[j] - a[i]) * (POW10[i] - POW10[j])
                    st.add(y)  # 交换一次
                    a[i], a[j] = a[j], a[i]
                    for p in range(i + 1, m):
                        for q in range(p + 1, m):
                            st.add(y + (a[q] - a[p]) * (POW10[p] - POW10[q]))  # 交换两次
                    a[i], a[j] = a[j], a[i]
            ans += sum(cnt[v] for v in st)
            cnt[x] += 1
        return ans
''',
    call='Solution().countPairs([102, 12, 21])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（已排序；蓝 = 当前 x）', cell=100, h=150,
             color=lambda S, i, v: 'blue' if 'x' in S and v == S['x'] else None),
        dict(type='array', var='a', label='a = x 的数位（低位在左，下标 = 10 的幂次）', cell=100, h=190,
             pointers={'i': 'blue', 'j': 'pink', 'p': 'orange', 'q': 'cyan'}),
        dict(type='set', var='st', label='st = x 交换至多两次能变成的数', h=150, fmt=lambda x: str(x), font=30),
        dict(type='map', var='cnt', label='cnt = 左边各数出现次数', h=130, fmt=lambda k, v: f'{k}: {v}', font=30),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'nums.sort()': '==先排序==：位数少的在前。右边的 `102` 能变成 `12`，反过来不行',
        'for x in nums': lambda S, B, r: '所有数都枚举完了' if 'x' in B and B['x'] == S.x and S.cnt[S.x] > 0 and sum(S.cnt.values()) == len(S.nums) else f'枚举右边的 `x = {S.x}`，左边已经枚举过的数记在 `cnt` 里',
        'st = {x}': '`st` 装 `x` 交换至多两次能变成的所有数，用集合==去重==，避免同一个 `nums[i]` 被算多次。先放入「不交换」的 `{x}`',
        'a = list(map(int, str(x)))': '拆数位并反转：`a = {a}`，低位在左，`a[i]` 对应 `10^i`',
        'if a[i] == a[j]': lambda S, B, r: (f'`a[{S.i}] = a[{S.j}] = {S.a[S.i]}`：交换不改变 `x` → 跳过' if S.a[S.i] == S.a[S.j]
                                           else f'`a[{S.i}] = {S.a[S.i]} ≠ a[{S.j}] = {S.a[S.j]}`：交换会改变数值'),
        'y = x + (a[j]': '交换 `a[{i}]`、`a[{j}]`：`y = x + ({a[j]}-{a[i]})*({10**i}-{10**j})` = =={y}==，O(1) 算出，不转字符串。再真换这两位，枚举第二次交换',
        'st.add(y)': '`{y}` 加入 `st`（交换一次）',
        'st.add(y + (a[q]': '第二次交换 `p={p}`、`q={q}` → 数值 `{y + (a[q] - a[p]) * (10**p - 10**q)}` 加入 `st`（交换两次）',
        'ans += sum': '左边有多少个数在 `st` 里：`sum(cnt[v] for v in st)` → `ans` 从 `{B.ans}` 变成 =={ans}==',
        'cnt[x] += 1': '`x` 变成「左边的数」：`cnt[{x}]` = {cnt[x]}',
        'return ans': '近似相等的数对一共 `{ans}` 个',
    },
    skip=['for i in range', 'for j in range', 'for p in range', 'for q in range', 'm = len(a)', 'a[i], a[j] = a[j], a[i]', 'ans = 0', 'cnt = defaultdict'],
    max_steps=95,
    cards=dict(
        one_liner='枚举右边的数，暴力交换数位，数左边有几个等于它',
        complexity='时间 `O(n log n + n log^4 U)`，空间 `O(n + log^4 U)`',
        problem=['正整数数组 `nums`，一个数可以交换其中两个数位，==至多两次==',
                 '`nums[i]` 与 `nums[j]`（`i < j`）能变成相等则为近似相等（可有前导 0）',
                 '数出近似相等数对的个数',
                 '示例：`[1,10,100]` → `3`；本视频：`[102,12,21]`'],
        quote='核心思想：枚举 j 并暴力交换 nums[j] 中的数位。设交换后的数字为 x，统计左边有多少个 nums[i] 等于 x。',
        quote_src='—— 灵茶山艾府题解',
        idea=['「枚举右，维护左」：右边的 `x` 交换后的所有结果放进集合去重，到左边的计数表里查',
              '`100` 在左、`1` 在右就找不到 → 先 ==排序==，位数少的在前',
              '交换用公式算：`x + (a[j]-a[i])·(10^i − 10^j)`，O(1) 得新数'],
        summary=['时间 `O(n log n + n log^4 U)`，空间 `O(n + log^4 U)`',
                 '必须先排序：保证左边的数不比 `x` 位数多，前导 0 才能被覆盖',
                 '第二次交换的 `p` 从 `i+1` 起，避免重复；`a[i]==a[j]` 时直接 `continue`',
                 '灵神还给了优化前的字符串写法，以及 meet in the middle + bitset 的写法'],
    ),
)
