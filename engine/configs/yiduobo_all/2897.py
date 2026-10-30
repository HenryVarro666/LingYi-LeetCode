CONFIG = dict(
    num=2897, title='对数组执行操作使平方和最大', difficulty='Hard', category='位运算',
    author='yiduobo', technique='按位计数 · 逐位取 1 组装', tags=['位运算', '贪心与思维', '难度分 2301'],
    code='''
class Solution(object):
    def maxSum(self, nums, k):

        cnt = [0] * 30
        for v in nums:
            p = 0
            while v:
                if v % 2 == 1:
                    cnt[p] += 1
                
                p += 1
                v //= 2
        
        res = 0
        mod = 10 ** 9 + 7
        while k > 0:
            v = 0
            for index in range(30):
                if cnt[index] > 0:
                    cnt[index] -= 1
                    v |= (1 << index)
            
            res += v * v
            res %= mod
            k -= 1
        
        return res
''',
    call='Solution().maxSum([2,6,5,8], 2)',
    expect=261,
    views=[
        dict(type='text', fn=lambda S: (f"当前组装的数 v = =={S['v']}== = `{bin(S['v'])[2:]}`" if 'res' in S and 'v' in S else ''), h=60),
        dict(type='array', var='nums', label='nums', h=150),
        dict(type='array', var='cnt', label='cnt[p]：第 p 位上 1 的个数（共 30 位）', h=200, cell=30, index=True,
             pointers={'index': 'blue'}, color=lambda S, i, v: 'green' if v > 0 else None),
    ],
    watch=[('v', 'v', 'cyan'), ('res', 'res', 'green'), ('k', 'k', 'blue')],
    captions={
        'cnt = [0] * 30': '`cnt[p]` 记录所有数的第 p 位上 1 的数量（题目保证不超过 30 位）',
        'for v in nums': '统计 `{v}` 的每一位',
        'if v % 2 == 1': '末位是 {v % 2} → ' + '{"是 1，计入 cnt" if v % 2 == 1 else "是 0，不计"}',
        'cnt[p] += 1': '第 {p} 位多一个 1：`cnt[{p}]` → {cnt[p]}',
        'v //= 2': '右移一位：`v` → {v}（原文 `/`，Python 3 改 `//`）',
        'while k > 0': '还需组装 `k = {k}` 个数',
        'v = 0': '新组装一个数 `v = 0`',
        'if cnt[index] > 0': lambda S, B, r: (f'第 {S.index} 位还有 {S.cnt[S.index]} 个 1 → 取走一个' if S.cnt[S.index] > 0 else f'第 {S.index} 位没有 1 了，跳过'),
        'cnt[index] -= 1': '取走第 {index} 位的一个 1：`cnt[{index}]` → {cnt[index]}',
        'v |= (1 << index)': '放进 `v`：加上 `2^{index}`，`v` = =={v}==',
        'res += v * v': '把 1 集中到一个数：`res` += `{v}²` → {res}',
        'res %= mod': '取模保持数值不大：`res` = =={res}==',
        'k -= 1': '组装完一个，还剩 `k` = {k}',
        'return res': '最大平方和 `{res}`',
    },
    cards=dict(
        one_liner='AND/OR 操作其实是在数与数之间搬运 1，集中起来最大',
        complexity='时间 `O(30(n + k))`，空间 `O(1)`',
        problem=['选 `i, j`，同时令 `nums[i] = a & b`、`nums[j] = a | b`，可操作任意次',
                 '最终选 `k` 个数求平方和最大（模 `10^9+7`）',
                 '示例：`[2,6,5,8]`，`k=2` → `261`'],
        quote='就应该通过交换操作尽量把1集中在同一个数字上，然后选择top k个这样的数字计算平方和。',
        quote_src='—— yiduobo 题解原文',
        idea=['逐位分析：某位两数相同则无事，不同则 1 被搬到 `or` 的一侧',
              '两数和不变，比较 `(a+t)^2+(b-t)^2` 与 `a^2+b^2`：差为 `2t(a-b)+2t^2 > 0`',
              '所以统计每位 1 的个数，循环 `k` 次，每次每位取一个 1'],
        summary=['时间 `O(30(n+k))`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `v /= 2` 已改为 `v //= 2`',
                 '每轮 `cnt` 都在消耗，后面的数只会更小',
                 '对比灵神：灵神用 `bit_length` 定位数，这里固定 30 位'],
    ),
)
