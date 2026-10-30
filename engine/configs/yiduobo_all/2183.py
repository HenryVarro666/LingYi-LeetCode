CONFIG = dict(
    num=2183, title='统计可以被 K 整除的下标对数目', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='约分 + 筛法预处理倍数个数 · 去重',
    tags=['灵神题单', '数学算法', '难度分 2246'],
    code='''
class Solution(object):
    def countPairs(self, nums, k):

        cnt_list = [0] * (k + 1)
        cnt_list[1] = len(nums)
        num_dict = {}
        for num in nums:
            num_dict[num] = num_dict.get(num, 0) + 1

        max_num = max(nums)
        for num in range(2, k + 1):
            now = num
            while now <= max_num:
                cnt_list[num] += num_dict.get(now, 0)
                now += num

        res = 0
        for num in nums:
            x, y = num, k
            if x < y:
                x, y = y, x
            while y:
                x, y = y, x % y

            tmp = k // x
            res += cnt_list[tmp]
            if num % tmp == 0:
                res -= 1
        
        return res // 2
''',
    call='Solution().countPairs([1,2,3,4,5], 4)',
    expect=4,
    views=[
        dict(type='text', h=80, fn=lambda S: (f"当前 `num = {S['num']}`：`gcd = {S['x']}`" if 'res' in S and 'x' in S and S['_line'] >= 25 else
                                              (f"`num = {S['num']}`：用 `k = {S['k']}` 的倍数筛，更新 `cnt_list[{S['num']}]`" if S['_line'] >= 15 and 'num' in S and 'res' not in S else '先预处理 `cnt_list[t]` = nums 里 t 的倍数的个数'))),
        dict(type='array', var='nums', h=170, label='nums'),
        dict(type='array', var='cnt_list', h=230, label='cnt_list[t]：nums 中是 t 的倍数的个数（下标就是 t）',
             pointers={'tmp': 'yellow'}, color=lambda S, i, v: 'yellow' if 'tmp' in S and i == S['tmp'] and S['_line'] >= 24 else None),
    ],
    watch=[('num', 'num', 'blue'), ('tmp', 'tmp', 'yellow'), ('res', 'res', 'green')],
    skip=['cnt_list = [0]', 'cnt_list[1] = len', 'num_dict = {}', 7, 'num_dict[num] =', 'max_num = max', 'now = num', 'now += num', 'res = 0'],
    max_steps=90,
    captions={
        'cnt_list[num] += num_dict': '`{num}` 的倍数 `{now}` 在 nums 里有 `{num_dict.get(now, 0)}` 个 → `cnt_list[{num}] = {cnt_list[num]}`',
        'while now <= max_num': lambda S, B, r: (f'倍数 `{S.now}` 没超过最大值 `{S.max_num}`，继续数' if S.now <= S.max_num else f'`{S.now} > {S.max_num}`：`cnt_list[{S.num}] = {S.cnt_list[S.num]}` 数完'),
        'for num in range(2, k + 1)': lambda S, B, r: ('`t` 都数完了：`cnt_list` 准备好' if S.num == B.get('num') else f'`t = {S.num}`：数 nums 里 `{S.num}` 的倍数有几个（类似筛法）'),
        'x, y = num, k': '`x = {x}`，`y = {y}`，准备用辗转相除求 `gcd({num}, {k})`',
        'if x < y': '`{x} < {y}`？{"是，交换使 x 为大数" if x < y else "否，不用交换"}',
        'x, y = y, x % y': '辗转相除：`x, y = {x}, {y}`（y 为 0 时 x 就是 gcd）',
        'tmp = k // x': '约分：`tmp = k // gcd = {k} // {x}` = =={tmp}==，另一个数必须是 `{tmp}` 的倍数',
        'res += cnt_list[tmp]': '`nums` 里 `{tmp}` 的倍数有 `{cnt_list[tmp]}` 个 → `res` = =={res}==',
        'if num % tmp == 0': '`{num} % {tmp} == 0`？{"是：num 自己也被算进去了（自己配自己）" if num % tmp == 0 else "否：没有自配"}',
        'res -= 1': '扣掉自配自的一次：`res` = =={res}==',
        'return res // 2': '每一对 `(i, j)` 在 i 和 j 各数了一遍，所以除以 2：`{res} // 2 = {res // 2}`',
    },
    cards=dict(
        one_liner='先约分，再用「倍数个数表」O(1) 查出另一个数有几个',
        complexity='时间 `O(n log n)`，空间 `O(k)`',
        problem=['求满足 `i < j` 且 `nums[i] × nums[j]` 能被 `k` 整除的下标对个数',
                 '`n`、数值、`k` 最大 `10⁵`，不能枚举所有数对',
                 '示例：`nums = [1,2,3,4,5]`，`k = 4` → `4`'],
        quote='可以先将nums[i]和k进行约分，即求出二者的最大公约数g，那么nums[j]就只需要满足是t = k / g的倍数就行了。',
        quote_src='—— yiduobo 题解',
        idea=['先用类似筛法的方式算 `cnt[t]`：`t, 2t, 3t, …` 在 nums 里出现的次数总和',
              '对每个 `num`：`gcd` 约分得 `t = k // gcd`，答案加上 `cnt[t]`',
              '每对会被两端各数一次，自己配自己也可能被数进去：先减自配，最后除以 2'],
        summary=['预处理是调和级数 `O(n log n)`，每个 `num` 求 gcd 是 `O(log k)`',
                 '易错点：`num % tmp == 0` 时要减 1（自己乘自己），最后 `// 2`',
                 '原文为 Python 2 写法，其中 `k / x` 与 `res / 2` 已改为整除 `//`'],
    ),
)
