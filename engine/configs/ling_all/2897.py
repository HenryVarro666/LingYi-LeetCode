CONFIG = dict(
    num=2897, title='对数组执行操作使平方和最大', difficulty='Hard', category='位运算',
    author='灵茶山艾府', technique='按位统计 · 把 1 聚集到一个数', tags=['位运算', '贪心与思维', '难度分 2301'],
    code='''
class Solution:
    def maxSum(self, nums: List[int], k: int) -> int:
        m = max(nums).bit_length()
        cnt = [0] * m
        for x in nums:
            for i in range(m):
                cnt[i] += x >> i & 1
        ans = 0
        for _ in range(k):
            x = 0
            for i in range(m):
                if cnt[i]:
                    cnt[i] -= 1
                    x |= 1 << i
            ans += x * x
        return ans % (10 ** 9 + 7)
''',
    call='Solution().maxSum([2,6,5,8], 2)',
    expect=261,
    views=[
        dict(type='text', fn=lambda S: (f"本轮组装的数 x = =={S['x']}== = `{bin(S['x'])[2:]}`" if 'x' in S and 'ans' in S and S.get('_line', 0) >= 10 else ''), h=60),
        dict(type='array', var='nums', label='nums', h=170),
        dict(type='array', var='cnt', label='cnt[i]：第 i 位上还剩多少个 1', h=200,
             pointers={'i': 'blue'}, color=lambda S, i, v: 'green' if v > 0 else None),
    ],
    watch=['m', ('x', 'x', 'cyan'), ('ans', 'ans', 'green'), 'k'],
    captions={
        'm = max': '最大数决定位数：`m = {m}`',
        'cnt = [0]': '`cnt[i]` 统计所有数在第 i 位上有几个 1',
        'cnt[i] += x >> i & 1': '`{x}` 的第 {i} 位是 {x >> i & 1} → `cnt[{i}]` = {cnt[i]}',
        'for _ in range(k)': '开始组装第几个数（共 `k = {k}` 个）',
        'x = 0': '新组装一个数 `x = 0`',
        'if cnt[i]': lambda S, B, r: (f'第 {S.i} 位还剩 `{S.cnt[S.i]}` 个 1 → 取一个' if S.cnt[S.i] else f'第 {S.i} 位已经没有 1 了，跳过'),
        'cnt[i] -= 1': '从第 {i} 位拿走一个 1：`cnt[{i}]` → {cnt[i]}',
        'x |= 1 << i': '把它放进 `x`：加上 `2^{i}`，`x` = =={x}==',
        'ans += x * x': '1 越聚集平方和越大：`ans` += `{x}²` → =={ans}==',
        'return ans': '取模后返回：`{ans} % (10^9+7)` = {ans % (10 ** 9 + 7)}',
    },
    cards=dict(
        one_liner='操作等价于交换比特位，把 1 聚集到少数几个数里',
        complexity='时间 `O(n log U)`，空间 `O(log U)`',
        problem=['对 `(nums[i], nums[j])` 同时做 AND 与 OR，任意次',
                 '最后选 `k` 个数，求平方和最大值（模 `10^9+7`）',
                 '示例：`[2,6,5,8]`，`k=2` → `261`'],
        quote='操作等价于：把一个数的 0 和另一个数的同一个比特位上的 1 交换。相当于把 1 都聚集在一个数中，比分散到不同的数更好。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每个比特位上 1 的个数不会变，只能在数之间移动',
              '总和不变时，两数越悬殊平方和越大：$(x+d)^2+(y-d)^2 > x^2+y^2$'.replace('$', ''),
              '统计 `cnt`，循环 `k` 次，每次从每一位各取一个 1 拼成最大的数'],
        summary=['时间 `O(n log U)`，空间 `O(log U)`',
                 '易错：最后才对答案取模，Python 不怕溢出',
                 '位数 `m` 用最大数的 `bit_length` 即可',
                 '均值不等式思想：和固定，差越大平方和越大'],
    ),
)
