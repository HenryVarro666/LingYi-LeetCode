CONFIG = dict(
    num=1862, title='向下取整数对和', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='枚举除数与商 + 后缀和',
    tags=['前缀和', '数学算法', '难度分 2170'],
    code='''
class Solution(object):
    def sumOfFlooredPairs(self, nums):

        sorted_nums = sorted(nums)
        n = len(sorted_nums)
        max_num = sorted_nums[-1]
        p = n - 1
        bound = max_num
        mod = 10 ** 9 + 7
        res = 0
        cnt_dict = {}
        while p >= 0:
            prev_pos = p - 1
            while prev_pos >= 0 and sorted_nums[prev_pos] == sorted_nums[p]:
                prev_pos -= 1
            
            cnt = p - prev_pos

            for num in range(bound, sorted_nums[p], -1):
                if num != max_num:
                    cnt_dict[num] = cnt_dict[num + 1]
                else:
                    cnt_dict[num] = 0

            cnt_dict[sorted_nums[p]] = cnt
            if sorted_nums[p] < max_num:
                cnt_dict[sorted_nums[p]] += cnt_dict[sorted_nums[p] + 1]
            bound = sorted_nums[p] - 1

            last = sorted_nums[p]
            multi = 1
            step = max_num // sorted_nums[p]
            while multi < step:
                now = last + sorted_nums[p]
                res += cnt * (cnt_dict[last] - cnt_dict[now]) * multi
                res %= mod
                last = now
                multi += 1
            
            res += cnt * cnt_dict[last] * multi
            res %= mod

            p = prev_pos
        
        return res
''',
    call='Solution().sumOfFlooredPairs([2,3,5])',
    expect=7,
    views=[
        dict(type='array', var='sorted_nums', label='sorted_nums（从大到小处理除数）', h=190,
             pointers={'p': 'blue'},
             color=lambda S, i, v: 'blue' if 'p' in S and i == S['p'] else None,
             dim=lambda S, i, v: 'p' in S and i > S['p']),
        dict(type='map', var='cnt_dict', h=300, fmt=lambda k, v: f'≥{k}: {v}'),
        dict(type='text', fn=lambda S: (
            f"除数 `{S['sorted_nums'][S['p']]}`，商 `{S['multi']}`：数落在 `[{S['last']}, {S['now']-1}]`，个数 `cnt_dict[{S['last']}] − cnt_dict[{S['now']}]`"
            if 'now' in S and 'multi' in S and 'last' in S and S.get('_line', 0) in (31, 32, 33, 34, 35) else '')),
    ],
    skip=['res %= mod', 'mod = ', 'n = len', 'max_num = sorted', 'multi = 1', 'bound = max_num'],
    watch=['p', 'cnt', 'last', 'multi', 'step', ('res', 'res', 'green')],
    captions={
        'while prev_pos >= 0 and': '`sorted_nums[{prev_pos}]` 和 `sorted_nums[{p}]` 相同？{"是 → 重复的数，一起处理" if prev_pos >= 0 and sorted_nums[prev_pos] == sorted_nums[p] else "否 → 这个值的重复个数数完了"}',
        'cnt = p - prev_pos': '数值 `{sorted_nums[p]}` 出现 `cnt = {cnt}` 次：重复的数收集起来==一起当除数==，否则复杂度会退化',
        'for num in range(bound': '补 `cnt_dict`：从 `{bound}` 往下补到 `{sorted_nums[p]+1}`，这些位置没有数，沿用右边的后缀计数',
        'cnt_dict[num] = cnt_dict[num + 1]': '没有数落在 `{num}`，大于等于 `{num}` 的个数和 `{num+1}` 一样：`cnt_dict[{num}] = {cnt_dict[num]}`',
        'cnt_dict[num] = 0': '`{num}` 是最大值右边，没有更大的数：`cnt_dict[{num}] = 0`',
        'cnt_dict[sorted_nums[p]] = cnt': '先放上这个数自己的 `cnt = {cnt}` 个',
        'cnt_dict[sorted_nums[p]] +=': '再加上更大的数：`cnt_dict[{sorted_nums[p]}]` 表示 ==大于等于 {sorted_nums[p]} 的数有 {cnt_dict[sorted_nums[p]]} 个==',
        'bound = sorted_nums[p] - 1': '下一轮要补的上界：`bound = {bound}`',
        'step = max_num': '商最多到 `max_num // {sorted_nums[p]} = {step}`：区间 `[除数×multi, 除数×(multi+1)-1]` 里的数商都是 multi',
        'last = sorted_nums[p]': '`last` 是区间左端 `除数×multi`，从 `{last}` 开始',
        'now = last': '区间右端的下一个位置 `now = {last} + {sorted_nums[p]} = {now}`，区间是 `[{last}, {now-1}]`',
        'res += cnt * (cnt_dict[last]': '商为 `{multi}`：个数 `{cnt_dict[last]} − {cnt_dict[now]}` = {cnt_dict[last]-cnt_dict[now]}，乘除数个数 `{cnt}`、商 `{multi}` → `res = {res}`',
        'last = now': '`last` 移到 `{last}`',
        'multi += 1': '商 `multi → {multi}`',
        'res += cnt * cnt_dict[last] * multi': '最后一段：所有 `>= {last}` 的数（`{cnt_dict[last]}` 个）商都是 `{multi}` → `res = {res}`',
        'p = prev_pos': '换下一个更小的除数：`p = {p}`',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='像筛法：枚举除数和商，用后缀计数数落在区间的数',
        complexity='时间 `O(n + U log U)`，空间 `O(U)`',
        problem=['求所有下标对 `(i, j)` 的 `floor(nums[i] / nums[j])` 之和，对 `1e9+7` 取余',
                 '`n`、`nums[i]` 最大到 `1e5`，不能两两枚举',
                 '示例：`[2,5,9]` → `10`'],
        quote='可以采用类似筛法的思路，枚举除数与向下取整后的结果。大小处于 num * multi 到 num * (multi + 1) - 1 之间的数除以 num 向下取整后的结果才会是 multi。',
        quote_src='—— yiduobo 题解原文',
        idea=['除数 `d`、商 `m`：分子在 `[d*m, d*(m+1)-1]` 内，数它们的个数',
              '用后缀计数：`cnt_dict[x]` = 大于等于 `x` 的个数，区间个数 = `cnt_dict[d*m] − cnt_dict[d*(m+1)]`',
              '除数从大到小处理，边处理边把后缀计数补出来；重复的数一起处理'],
        after=[dict(heading='为什么是调和级数', lines=['除数 `d` 只需枚举 `max/d` 个商', '各个不同的除数加起来是 `U/1 + U/2 + …` ≈ `U ln U`'])],
        summary=['时间 `O(n log n + U log U)`，`U` 是最大值',
                 '重复的数要合并，否则枚举量会超',
                 '最后一段商 `multi` 的区间没有右端，直接取 `cnt_dict[last]`',
                 '原文为 Python 2 写法，`max_num / sorted_nums[p]` 的整数除法已改为 `//`'],
    ),
)
