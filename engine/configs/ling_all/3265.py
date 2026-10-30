CONFIG = dict(
    num=3265, title='统计近似相等数对 I', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='排序 + 哈希表 · 枚举交换一次的所有结果',
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
                    st.add(x + (a[j] - a[i]) * (POW10[i] - POW10[j]))  # 交换一次
            ans += sum(cnt[v] for v in st)
            cnt[x] += 1
        return ans
''',
    call='Solution().countPairs([3,12,30,17,21])',
    expect=2,
    views=[
        dict(type='array', var='nums', h=170, label='nums（排序后，黄 = 当前 x）', color=lambda S, i, v: 'yellow' if 'x' in S and v == S['x'] else None,
             dim=lambda S, i, v: 'x' in S and v > S['x']),
        dict(type='set', var='st', h=170, label='st = x 不交换 / 交换一次能变成的数'),
        dict(type='map', var='cnt', h=220, label='cnt：左边已出现的数的个数'),
    ],
    watch=[('x', 'x', 'yellow'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'POW10 =': '预处理 `10^0 ~ 10^6`，后面用它直接算交换后的数',
        'nums.sort()': '==先排序==：保证左边的数都不大于 x，交换 x 的数位就能覆盖前导 0 的情况',
        'cnt = defaultdict': '`cnt` 记录左边每个数出现的次数',
        'st = {x}': '`st` 装 x 能变成的所有数：先放入不交换的 `{x}`',
        'a = list(map': '把 `{x}` 的数位倒着存：`a = {a}`，`a[i]` 对应 10^i 位',
        'st.add': '交换第 `{i}`、`{j}` 位：`{x}` 变成 `{x + (a[j] - a[i]) * (10**i - 10**j)}`，加入 `st`',
        'ans += sum': '`st` 里每个数在左边出现过几次，就和 x 组成几对：`ans` → =={ans}==',
        'cnt[x] += 1': 'x 处理完，自己放进 `cnt`：`cnt[{x}]` = {cnt[x]}',
    },
    cards=dict(
        one_liner='排序后枚举 x 交换一次能得到的数，去哈希表里数有几个',
        complexity='时间 `O(n log n + n log²U)`，空间 `O(n + log²U)`',
        problem=['一个数交换其中两个数位至多一次，可以变成另一个数，就是近似相等（可有前导 0）',
                 '数对 `i<j`，求近似相等的对数',
                 '示例：`[3,12,30,17,21]` → `2`（3 和 30，12 和 21）'],
        quote='优化后：交换 i、j 两位后的数 = x + (a[j] - a[i]) * (POW10[i] - POW10[j])，不用再拼字符串。',
        quote_src='—— 灵茶山艾府题解（代码思路）',
        idea=['先排序，遍历到 x 时，左边都是不大于 x 的数',
              '枚举 x 交换一次的所有结果放进集合 `st`，用 `cnt` 统计左边有几个等于这些值',
              '交换后的值用数位差公式直接算，省掉字符串拼接（原版先交换再 join）'],
        summary=['时间 `O(n log n + n log²U)`，空间 `O(n + log²U)`',
                 '易错：先排序，否则 x 比左边的数位数少时配不上前导 0 的情况',
                 '`st` 是集合，同一个结果只计一次，避免重复数对',
                 '另一种写法：优化前用 `list(str(x))` 原地交换再还原，思路相同'],
    ),
)
