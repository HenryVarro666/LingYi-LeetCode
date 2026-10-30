CONFIG = dict(
    num=2601, title='质数减法运算', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='贪心 · 预处理「≤ i 的最大质数」',
    tags=['灵神题单', '数学算法', '难度分 1779'],
    code='''
class Solution(object):
    def primeSubOperation(self, nums):

        f = [None] * 1001
        prime_list = []
        x = 2
        while x <= 1000:
            if f[x] is None:
                prime_list.append(x)
                for y in range(x + x, 1001, x):
                    f[y] = x
            
            x += 1
        
        remove_num = [0, 0]
        p = 0
        for v in range(2, 1001):
            while p + 1 < len(prime_list) and prime_list[p + 1] <= v:
                p += 1
            
            remove_num.append(prime_list[p])
        
        pre = nums[0] - remove_num[nums[0] - 1]
        for v in nums[1:]:
            v -= pre + 1
            if v < 0:
                return False
            
            v -= remove_num[v]
            pre += v + 1
        
        return True
''',
    call='Solution().primeSubOperation([4,9,6,10])',
    expect=True,
    max_events=30000,
    views=[
        dict(type='text', h=80, fn=lambda S: (f"已定好的前一项 `pre = {S['pre']}`；当前 `v = {S['v']}`" if 'pre' in S and 'v' in S and S['_line'] >= 23 else
                                              f"已定好的前一项 `pre = {S['pre']}`" if 'pre' in S else '先用筛法造出 1000 以内的质数，再造 `remove_num`')),
        dict(type='array', var='nums', h=200, label='nums'),
        dict(type='text', h=80, fn=lambda S: (f"`remove_num[i]` = 小于等于 i 的最大质数，例如 `remove_num[7] = {S['remove_num'][7]}`，`remove_num[8] = {S['remove_num'][8]}`" if 'remove_num' in S and len(S['remove_num']) > 8 else '')),
    ],
    watch=[('pre', 'pre', 'green'), ('v', 'v', 'blue')],
    skip=['f[y] = x', 'for y in range', 'x += 1', 'while p + 1', 'p += 1', 'remove_num.append', 'for v in range(2, 1001)',
          'f = [None]', 'prime_list = []', 'x = 2', 'while x <= 1000', 'if f[x] is None', 'prime_list.append', 'remove_num = [0, 0]', 'p = 0'],
    captions={
        'pre = nums[0] - remove_num': 'nums[0] 要尽量小：减去 `<= nums[0]-1` 的最大质数 `{remove_num[B.nums[0] - 1]}` → 首项 `pre = {nums[0]} - {remove_num[nums[0] - 1]} = {pre}`',
        'for v in nums[1:]': lambda S, B, r: ('`nums[1:]` 遍历完了，退出循环' if S.v == B.v else f'取下一个数 `v = {S.v}`'),
        'v -= pre + 1': '要 `v - p > pre`，即 `p <= v - pre - 1`：`v` 先变成 `{v}`（现在 v 表示 p 的上界）',
        'if v < 0': '`{v} < 0`？{"上界为负：这个数已经 ≤ pre，无法再变大 → 返回 False" if v < 0 else "上界不为负，还能操作"}',
        'v -= remove_num[v]': '取 `<= {B.v}` 的最大质数 `{remove_num[B.v]}`，==减得越多结果越小==：剩下 `v = {B.v} - {remove_num[B.v]} = {v}`',
        'pre += v + 1': '新的 `pre = 旧 pre + v + 1 = {pre}`（即 nums[i] 减去质数后的值）',
        'return True': '每个数都处理完，能严格递增 → ==True==',
    },
    cards=dict(
        one_liner='每一项都减去尽量大的质数，让它尽量小',
        complexity='时间 `O(U + n)`，空间 `O(U)`，`U = 1000`',
        problem=['每个下标最多减一次，减去一个 ==严格小于 nums[i]== 的质数',
                 '问能否把 `nums` 变成严格递增数组',
                 '示例：`[4,9,6,10]` → `true`'],
        quote='为了使得后续形成单调递增数组的可能性更大，就应该让 nums[0] 操作后得到的结果尽量的小。',
        quote_src='—— yiduobo 题解',
        idea=['`nums[i] - p[i] > final[i-1]` 变形为 `p[i] <= nums[i] - final[i-1] - 1`',
              '预处理 `remove[i]`：小于等于 i 的最大质数，每项直接查表',
              '若上界 `< 0`，说明 nums[i] 已不超过前一项，直接返回 False'],
        summary=['筛质数 + 双指针造表 `remove_num`，之后每个数 `O(1)` 查表',
                 '易错点：上界为 0 时 `remove_num[0] = 0`，表示一个质数都不减，需要把表头补成 `[0, 0]`',
                 '原文为 Python 2 写法，在 Python 3 下无需修改即可运行'],
    ),
)
