CONFIG = dict(
    num=1390, title='四因数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='筛法记录最大质因子 + 数论分类',
    tags=['灵神题单', '数学算法', '难度分 1478'],
    code='''
class Solution(object):
    def sumFourDivisors(self, nums):

        max_num = max(nums)

        f = [1] * (max_num + 1)
        now = 2
        while now * now <= max_num:
            if f[now] == 1:
                tmp = now + now
                while tmp <= max_num:
                    f[tmp] = now
                    tmp += now
            now += 1

        res = 0
        for num in nums:
            if f[num] == 1:
                continue
            
            tmp = num // f[num]
            if (f[tmp] == 1 and tmp != f[num]) or (f[tmp] == f[num] and tmp // f[num] == f[num]):
                res += 1 + num + tmp + f[num]
        
        return res
''',
    call='Solution().sumFourDivisors([15, 4, 7, 8])',
    expect=39,
    views=[
        dict(type='array', var='f', h=210, label='f[x]：x 的一个质因子（1 = 质数或 1）', cell=52,
             pointers={'now': 'blue', 'tmp': 'yellow'},
             color=lambda S, i, v: 'green' if 'num' in S and i == S['num'] else None),
        dict(type='array', var='nums', h=180, label='nums',
             color=lambda S, i, v: 'yellow' if 'num' in S and v == S['num'] else None),
    ],
    watch=['max_num', ('now', 'now', 'blue'), ('tmp', 'tmp', 'yellow'), ('res', 'res', 'green')],
    captions={
        'max_num = max': '只需筛到 `max(nums) = {max_num}`',
        'f = [1]': '`f[x]` 记录 x 的一个质因子（取筛到的最大的，不超过 sqrt）；初始 `1` 表示还没有',
        'now = 2': '从最小的质数 `2` 开始筛',
        'while now * now': lambda S, B, r: (f'`{S.now}² = {S.now*S.now} <= {S.max_num}`：继续筛' if S.now*S.now <= S.max_num else f'`{S.now}² > {S.max_num}`：筛完'),
        'if f[now] == 1': lambda S, B, r: (f'`f[{S.now}] == 1`：{S.now} 没有更小的质因子 → 是质数，用它筛倍数' if S.f[S.now] == 1 else f'`f[{S.now}] = {S.f[S.now]}`：合数，不用筛'),
        'tmp = now + now': '从 `2 × now = {tmp}` 开始标记',
        'while tmp <= max_num': '`tmp = {tmp}` 还没超过 `{max_num}`，继续标记',
        'f[tmp] = now': '`{tmp}` 是 `{now}` 的倍数 → `f[{tmp}] = {now}`',
        'tmp += now': '下一个倍数 `tmp = {tmp}`',
        'now += 1': '`now` → {now}',
        'res = 0': '筛好了，开始逐个判断 `nums`',
        'for num in nums': '看 `num = {num}`',
        'if f[num] == 1': lambda S, B, r: (f'`f[{S.num}] == 1`：质数只有 2 个因子 → 跳过' if S.f[S.num] == 1 else f'`f[{S.num}] = {S.f[S.num]}`：合数，继续看是不是恰有 4 个因子'),
        'tmp = num // f[num]': '`tmp = {num} // {f[num]} = {tmp}`：把一个质因子除掉，看剩下的结构',
        'if (f[tmp] == 1': lambda S, B, r: (
            f'满足：`tmp = {S.tmp}` 是质数且 `!= {S.f[S.num]}` → `num = p × q` 恰有 4 个因子' if (S.f[S.tmp] == 1 and S.tmp != S.f[S.num])
            else f'满足：`{S.num} = {S.f[S.num]}³` 是质数的立方 → 恰有 4 个因子' if (S.f[S.tmp] == S.f[S.num] and S.tmp // S.f[S.num] == S.f[S.num])
            else f'`{S.num}` 既不是 `p×q` 也不是 `p³` → 因子数不是 4'),
        'res += 1 + num': '四个因子：`1, {f[num]}, {tmp}, {num}` → `res` = =={res}==',
        'return res': '`res = {res}`',
    },
    skip=['now += 1'],
    max_steps=110,
    cards=dict(
        one_liner='四个因子只有两种形态：p×q 或 p 的立方',
        complexity='时间约 `O(U log log U + n)`，空间 `O(U)`',
        problem=['返回 `nums` 中恰有 4 个因子的整数的因子之和，没有则返回 `0`',
                 '示例：`[21,4,7]` → `32`',
                 '本视频：`[15,4,7,8]` → `39`（15 的 24 + 8 的 15）'],
        quote='为了使得这个式子计算的结果为4，那么一共有两种可能：1、k[0] = 3，且没有其他因数，num是一个完全立方数。2、k[0] = 1且k[1] = 1，num = x[0] * x[1]，x[0]和x[1]都是质数，且不相等。',
        quote_src='—— yiduobo 题解原文',
        idea=['质因数分解 `(k0+1)(k1+1)... = 4`，只能是 `p^3` 或 `p×q`',
              '筛法顺带记下每个数的质因子 `f[num]`',
              '除掉它得 `tmp`：`tmp` 是另一个质数，或 `tmp = f[num]²`'],
        summary=['时间约 `O(U log log U + n)`，空间 `O(U)`',
                 '`f[x] == 1` 表示 x 是质数（或 1），直接跳过',
                 '`p×q` 要求 `p != q`，否则就是平方数，只有 3 个因子',
                 '原文为 Python 2 写法，两处 `/` 整除已改为 `//`'],
    ),
)
