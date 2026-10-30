CONFIG = dict(
    num=2873, title='有序三元组中的最大值 I', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='枚举中间 j + 前后缀最大值',
    tags=[],
    code='''
class Solution(object):
    def maximumTripletValue(self, nums):

        res = 0
        n = len(nums)

        prefix = [nums[0]]
        for index in range(1, n):
            prefix.append(max(prefix[-1], nums[index]))
        
        suffix = [nums[-1]]
        for index in range(n - 2, -1, -1):
            suffix.append(max(suffix[-1], nums[index]))
        suffix.reverse()

        for j in range(1, n - 1):
            res = max(res, (prefix[j - 1] - nums[j]) * suffix[j + 1])
        
        return res
''',
    call='Solution().maximumTripletValue([6,12,1,2,7])',
    expect=77,
    views=[
        dict(type='text', size=26, fn=lambda S: (
            f"枚举中间 `j = {S['j']}`：`(prefix[{S['j'] - 1}] − nums[{S['j']}]) × suffix[{S['j'] + 1}]` = `({S['prefix'][S['j'] - 1]} − {S['nums'][S['j']]}) × {S['suffix'][S['j'] + 1]}` = =={(S['prefix'][S['j'] - 1] - S['nums'][S['j']]) * S['suffix'][S['j'] + 1]}=="
            if 'j' in S and 1 <= S['j'] <= len(S['nums']) - 2 and S['_line'] >= 16 else '')),
        dict(type='array', var='nums', label='nums', pointers={'j': 'blue'}, h=170,
             color=lambda S, k, v: 'blue' if S.get('j') == k and S['_line'] >= 16 else None),
        dict(type='array', var='prefix', label='prefix[i] = nums[0..i] 的最大值', h=170,
             pointers={'j - 1': 'cyan'} if False else {}),
        dict(type='array', var='suffix', label='suffix[i] = nums[i..n-1] 的最大值（先倒着存，最后 reverse）', h=170),
    ],
    watch=[('index', 'index', 'pink'), ('j', 'j', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res = 0`：负数都不要，答案最小就是 0',
        'prefix = [nums[0]]': '`prefix[i]`：`nums[0..i]` 里的最大值，先放 `nums[0] = {nums[0]}`',
        'prefix.append': '`prefix[{index}] = max({prefix[-2]}, {nums[index]})` = =={prefix[-1]}==',
        'suffix = [nums[-1]]': '`suffix` 从右往左算，先放 `nums[-1] = {nums[-1]}`',
        'suffix.append': '从右往左：`nums[{index}..]` 最大值 = `max({suffix[-2]}, {nums[index]})` = =={suffix[-1]}==',
        'suffix.reverse': '倒着存的，`reverse()` 后 `suffix[i]` 就是 `nums[i..n-1]` 的最大值：`{suffix}`',
        'for j in range': lambda S, B, r: ('`j` 枚举完了，`res` 就是答案' if S.j == (B['j'] if 'j' in B else None) else
                                           f'枚举中间下标 `j = {S.j}`：左边取最大的 `nums[i]`，右边取最大的 `nums[k]`'),
        'res = max': lambda S, B, r: (f'`(prefix[{S.j-1}] − nums[{S.j}]) × suffix[{S.j+1}]` = `({S.prefix[S.j-1]} − {S.nums[S.j]}) × {S.suffix[S.j+1]}` = '
                                      f'{(S.prefix[S.j-1]-S.nums[S.j])*S.suffix[S.j+1]}，`res = max({B.res}, …)` = =={S.res}=='),
        'return res': '最大三元组的值 =={ret}==',
    },
    skip=['n = len'],
    cards=dict(
        one_liner='枚举中间的 j，左边取最大、右边取最大',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['在 `i < j < k` 的三元组里，求 `(nums[i] − nums[j]) × nums[k]` 的最大值', '全是负数则返回 `0`',
                 '示例：`[12,6,1,2,7]` → `77`，即 `(12 − 1) × 7`', '本视频：`[6,12,1,2,7]` → `77`，`j = 1` 时是负数，不计'],
        quote='对于这类三元组的求解，常见的做法是枚举中间元素的下标，本题就是枚举j，然后尝试找出适配j的最优的i和k。',
        quote_src='—— yiduobo 题解原文',
        idea=['元素都是正数、答案只取非负：`nums[i]` 和 `nums[k]` 都应尽量大',
              '于是对每个 `j`，要 `nums[0..j-1]` 的最大值和 `nums[j+1..]` 的最大值',
              '正反各扫一遍得到 `prefix`、`suffix`，再枚举 `j` 更新答案'],
        summary=['时间 `O(n)`，空间 `O(n)`（本题 n ≤ 100，暴力三重循环也行，II 才必须这样）',
                 '易错：`suffix` 是倒着 `append` 的，最后必须 `reverse()`',
                 '`j` 的范围是 `1` 到 `n-2`，保证左右两边都有元素',
                 '原文已是 Python 3 可运行写法，代码未改动'],
    ),
)
