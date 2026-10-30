def _col(S, i, v):
    ln = S.get('_line')
    if ln in (12, 13, 14) and 'index' in S and 'num' in S:
        if i == S['index']:
            return 'yellow'
        if i == S['index'] - S['num']:
            return 'blue'
    if ln in (28, 29, 32, 33) and 'index' in S and i == S['index']:
        return 'orange'
    if ln in (28, 29, 32, 33) and 'index' in S and i < S['index']:
        return 'green'
    return None


def _txt(S):
    ln = S.get('_line')
    if ln in (12, 13, 14) and 'num' in S and 'index' in S:
        return f'`f[{S["index"]}] += f[{S["index"] - S["num"]}]`：不选 `{S["num"]}` 的方案 + 选了它的方案'
    if ln and ln >= 26 and 'res' in S and 'index' in S:
        return f'`res` = 总数 − 坏分区，已减到 f[{S["index"]}]：当前 res = =={S["res"]}=='
    return '`f[j]` = 选若干数、和为 `j` 的方案数（`j < k`），倒序更新省掉 i 维'


CONFIG = dict(
    num=2518, title='好分区的数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='逆向计数 · 01 背包 + 快速幂',
    tags=['数学算法', '难度分 2415'],
    code='''
class Solution(object):
    def countPartitions(self, nums, k):

        if sum(nums) < k + k:
            return 0
        
        f = [0] * k
        f[0] = 1
        mod = 10 ** 9 + 7
        for num in nums:
            for index in range(k - 1, num - 1, -1):
                f[index] += f[index - num]
                if f[index] >= mod:
                    f[index] -= mod
        
        def quickPow(base, x):
            if x == 1:
                return base
            
            p = quickPow(base, x // 2)
            p *= p
            if x & 1:
                p *= base
            return p % mod

        res = quickPow(2, len(nums))
        for index in range(k):
            res -= f[index]
            if res < 0:
                res += mod
            
            res -= f[index]
            if res < 0:
                res += mod
        
        return res
''',
    call='Solution().countPartitions([1, 2, 3, 4], 4)',
    expect=6,
    skip=['range(k - 1', 'if f[index] >= mod', 'f[index] -= mod', 'if res < 0', 'res += mod', 'def quickPow', 'mod = 10'],
    views=[
        dict(type='array', var='nums', label='nums', h=140, cell=70,
             color=lambda S, i, v: 'blue' if 'num' in S and v == S['num'] and S.get('_line') in (10, 12) else None),
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='array', var='f', label='f[j]：和为 j 的方案数（j < k）', h=200, cell=100, color=_col),
        dict(type='calls', h=170),
    ],
    watch=[('num', 'num', 'blue'), ('index', 'index', 'yellow'), ('k', 'k', 'pink'), ('res', 'res', 'green')],
    captions={
        'if sum(nums) < k + k': '`sum = {sum(nums)}`，`k + k = {k + k}`：和不够两个 k，根本分不出好分区，先返回 0',
        'f = [0] * k': '`f[j]`：选若干数使和为 j 的方案数，j 只取 `0 ~ k-1`（不合法的那一侧）',
        'f[0] = 1': '空集合，和为 0，1 种',
        'for num in nums': lambda S, B, r: (f'处理第 `{S.num}` 个数' if S.get('num') != B.get('num') or S.get('num') is None else '所有数处理完，`f` 里是和 `< k` 的方案数'),
        'f[index] += f[index - num]': '`f[{index}] += f[{index - num}]` → =={f[index]}==：选 {num}，前面凑 {index - num}；倒序避免重复用 {num}',
        'if x == 1': lambda S, B, r: f'快速幂：`x = {S.x}`' + ('，递归到底' if S.x == 1 else '，对半拆'),
        'return base': '`x = 1`，返回 `{base}`',
        'p = quickPow': '`x = {B.x}`：先算一半，进入 `quickPow(2, {B.x // 2})`',
        'p *= p': '`p` 平方：`p = {p}`',
        'if x & 1': lambda S, B, r: f'`x = {S.x}`：' + ('奇数，还要多乘一个 base' if S.x & 1 else '偶数，不用补乘'),
        'return p % mod': '`2^{x} = {p % mod}`',
        'res = quickPow': '总方案数 `2^n = 2^{len(nums)}` = =={res}==',
        'for index in range(k)': lambda S, B, r: (f'枚举 `index = {S.index}`，减去 f[{S.index}]（两次）' if S.get('index') != B.get('index') or S.get('index') is None else '坏分区减完'),
        'res -= f[index]': lambda S, B, r: f'`res` 减去 `f[{S.index}] = {S.f[S.index]}` → {S.res}' + ('（第一组和为 index 的坏分区）' if S['_line'] == 28 else '（对称：第二组和为 index，再减一次）'),
        'return res': '总数 − 坏分区 = =={res}==',
    },
    max_steps=80,
    cards=dict(
        one_liner='k 很小，倒着数不合法的划分再用 2^n 去减',
        complexity='时间 `O(nk)`，空间 `O(k)`',
        problem=['把数组分成两部分，==每部分的和都不小于 k==',
                 '问可行的划分方案数，对 `10^9+7` 取余',
                 '示例：`[1,2,3,4], k=4` → `6`'],
        quote='注意到题目中的k取值范围比较小，因此可以考虑逆向求解，也就是求出所有不合法的划分方法，然后使用划分的总方案数减去不合法的划分方法得到最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['这是标准 01 背包，但数值太大，不能按和开数组',
              '`f[i][j]`：前 i 个数选若干，和为 j 的方案数，j 只到 `k-1`',
              '滚动数组 + 倒序省掉 i 维；总数 `2^n` 用快速幂求出'],
        summary=['时间 `O(nk)`，空间 `O(k)`',
                 '易错：`sum < 2k` 必须先返回 0，否则 p、q 互补会重复计数',
                 '易错：减法后若小于 0 要加回 `mod`，所以两次减都单独判断',
                 '原文为 Python 2 写法，快速幂里 `x / 2` 已改为 `x // 2`',
                 '对比灵神：他用 `pow(2, n, MOD)` 和 `sum(f) * 2` 一步减完'],
    ),
)
