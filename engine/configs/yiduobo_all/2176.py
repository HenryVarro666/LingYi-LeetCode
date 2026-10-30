CONFIG = dict(
    num=2176, title='统计数组中相等且可以被整除的数对', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='暴力枚举数对',
    tags=['灵神题单', '数学算法', '难度分 2200'],
    code='''
class Solution(object):
    def countPairs(self, nums, k):

        res = 0
        for i in range(len(nums) - 1):
            for j in range(i + 1, len(nums)):
                if nums[i] == nums[j] and i * j % k == 0:
                    res += 1
        
        return res
''',
    call='Solution().countPairs([3,1,2,2,1,3], 2)',
    expect=3,
    views=[
        dict(type='text', h=80, fn=lambda S: (f"检查数对 `(i, j) = ({S['i']}, {S['j']})`：`nums[{S['i']}] = {S['nums'][S['i']]}`，`nums[{S['j']}] = {S['nums'][S['j']]}`，`i×j = {S['i'] * S['j']}`" if 'j' in S and 'i' in S and S['_line'] >= 6 else (f"换一个 `i = {S['i']}`" if 'i' in S else '枚举所有 `i < j` 的数对'))),
        dict(type='array', var='nums', h=260, label='nums', pointers={'i': 'blue', 'j': 'pink'},
             color=lambda S, i, v: ('blue' if i == S['i'] else 'pink' if i == S['j'] else None) if 'j' in S and 'i' in S else None),
        dict(type='text', h=70, fn=lambda S: f"`k = {S['k']}`，已找到 `res = {S['res']}` 对" if 'res' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    captions={
        'for i in range': lambda S, B, r: (f'`i` 取 `{S.i}`，右边的 `j` 从 `{S.i + 1}` 开始' if S.res == B.get('res') and B.get('i') != S.i else '`i` 枚举完了，退出循环'),
        'for j in range': lambda S, B, r: (f'`j = {S.j}`：和 `nums[{S.i}]` 配对' if B.get('j') != S.j or B.get('i') != S.i else f'`i = {S.i}` 的 `j` 都试完了'),
        'if nums[i] == nums[j]': '`nums[{i}] = {nums[i]}` 对 `nums[{j}] = {nums[j]}`，`{i}×{j} = {i*j}`，`% {k} = {i * j % k}` → {"==两个条件都满足==" if nums[i] == nums[j] and i * j % k == 0 else ("值不相等" if nums[i] != nums[j] else "乘积不是 k 的倍数")}',
        'res += 1': '数对 `({i}, {j})` 满足条件，`res` = =={res}==',
        'return res': '一共 `{res}` 对',
    },
    max_steps=70,
    cards=dict(
        one_liner='数据很小，直接把每一对 (i, j) 都查一遍',
        complexity='时间 `O(n²)`，空间 `O(1)`',
        problem=['数对 `(i, j)`：`i < j`，`nums[i] == nums[j]`，且 `i × j` 能被 `k` 整除',
                 '示例：`nums = [3,1,2,2,1,3]`，`k = 2` → `3` 对'],
        quote='由于题目的数据规模很小，因此可以直接暴力枚举每一组i和j，若满足nums[i] = nums[j]且i * j是k的倍数，那么就将答案加上1。',
        quote_src='—— yiduobo 题解',
        idea=['两层循环枚举 `i < j`，两个条件同时满足才计数',
              '`i = 0` 时 `0 % k == 0`，所以不用特殊处理',
              '作者提到更好的做法：按数值收集后转成 2183 题的做法'],
        summary=['时间 `O(n²)`，本题 `n ≤ 100` 足够',
                 '易错点：`i` 只到 `len(nums) - 2`，`j` 从 `i + 1` 开始，避免重复和自配对',
                 '更大数据范围见 2183 题（用 gcd 与因子计数）'],
    ),
)
