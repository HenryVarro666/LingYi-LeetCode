CONFIG = dict(
    num=3618, title='根据质数下标分割数组', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='筛法 + 一趟遍历',
    tags=['灵神题单·数学算法', '数学算法', '难度分 1227'],
    code='''
class Solution(object):
    def splitArray(self, nums):
        
        n = len(nums)
        prime = [True] * n
        prime[0] = False
        if n > 1:
            prime[1] = False
        x = 2
        while x < n:
            if prime[x]:
                for y in range(x + x, n, x):
                    prime[y] = False
            x += 1
        
        res = 0
        for index in range(n):
            if prime[index]:
                res += nums[index]
            else:
                res -= nums[index]
        
        return abs(res)
''',
    call='Solution().splitArray([2,3,4,5,-1,7,0,6])',
    expect=18,
    views=[
        dict(type='array', var='prime', label='prime[i]：下标 i 是不是质数', h=190, cell=90,
             pointers={'x': 'blue'}, color=lambda S, i, v: 'pink' if v else None),
        dict(type='array', var='nums', label='nums（粉 = 质数下标，进 A）', h=190, cell=90,
             pointers={'index': 'cyan'}, color=lambda S, i, v: 'pink' if S['prime'][i] and 'res' in S else None),
        dict(type='text', size=30, h=100, fn=lambda S: f"`res = sum(A) − sum(B) = {S['res']}`" if 'res' in S else '先筛质数：划掉质数 `x` 的倍数'),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('index', 'index', 'cyan'), ('res', 'res', 'green')],
    max_steps=70,
    captions={
        'n = len': '`n = {n}`，下标范围 `0 ~ {n-1}`，只需筛这么大',
        'prime = [True]': '先假设每个下标都是质数',
        'prime[0] = False': '下标 `0` ==不是质数==',
        'if n > 1': '`n > 1` 才有下标 1，避免越界',
        'prime[1] = False': '下标 `1` ==也不是质数==',
        'x = 2': '从最小的质数 `2` 开始筛',
        'while x < n': lambda S, B, r: (f'`x = {S.x} < {S.n}`：继续筛' if S.x < S.n else f'`x = {S.x}` 到头了，筛完'),
        'if prime[x]': lambda S, B, r: (f'`{S.x}` 还没被划掉 → 是质数，划掉它的倍数' if S.prime[S.x] else f'`{S.x}` 已被划掉（合数），它的倍数早被划过'),
        'for y in range': lambda S, B, r: f'枚举 `{S.x}` 的倍数 `range({2*S.x}, {S.n}, {S.x})`，当前 `y = {S.y}`（走完则结束）',
        'prime[y] = False': '`{y}` 是 `{x}` 的倍数 → 合数',
        'x += 1': '`x` → {x}',
        'res = 0': '筛完了。`res` 记录 `sum(A) − sum(B)`',
        'for index in range': lambda S, B, r: ('所有下标都看完了' if 'index' in B and B.index == S.index else f'看下标 `{S.index}`：`prime[{S.index}] = {S.prime[S.index]}`'),
        'if prime[index]': lambda S, B, r: (f'下标 `{S.index}` 是质数 → 元素 `{S.nums[S.index]}` 属于 A，加上' if S.prime[S.index] else f'下标 `{S.index}` 不是质数 → 元素 `{S.nums[S.index]}` 属于 B，减去'),
        'res += nums': '`res` += `{nums[index]}` → =={res}==',
        'res -= nums': '`res` −= `{nums[index]}` → =={res}==',
        'return abs': 'A 和 B 的差可能为负，取绝对值：`abs({res})` = =={ret}==',
    },
    cards=dict(
        one_liner='先筛出下标范围内的质数，再一趟遍历加减',
        complexity='时间 `O(n log log n)`，空间 `O(n)`',
        problem=['`nums` 中==质数下标==的元素放入 `A`，其余放入 `B`',
                 '求 `|sum(A) − sum(B)|`',
                 '示例：`[2,3,4]` → `1`；`[-1,5,7,0]` → `3`',
                 '本视频：`[2,3,4,5,-1,7,0,6]` → `18`'],
        quote='n的规模不算小，因此在这里需要先通过筛法，找出1到n中所有的质数。接下来只需一趟遍历，根据当前下标是否为质数计算A和B的数组和，然后返回这两者差的绝对值即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n` 可达 `10^5`，逐个试除太慢，先按 `n` 的大小筛一遍',
              '筛法：遇到质数 `x`，把 `x+x, x+2x, …` 都划掉',
              '遍历下标：质数就加，否则就减，最后取绝对值'],
        summary=['筛法 `O(n log log n)`，遍历 `O(n)`，空间 `O(n)`',
                 '易错点：==`prime[0]`、`prime[1]` 要设为 False==，`n = 1` 时没有下标 1',
                 '易错点：差值取绝对值',
                 '对比灵神：灵神预先筛到 `10^5` 并用 `isqrt` 限制 `i`，yiduobo 按 `n` 现筛，`x` 枚举到 `n−1`'],
    ),
)
