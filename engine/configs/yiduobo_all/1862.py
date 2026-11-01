CONFIG = dict(
    num=1862, title='向下取整数对和', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='后缀和 + 筛法式枚举',
    tags=['一、前缀和', '§1.5 进阶', '难度分 2170'],
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
    call='Solution().sumOfFlooredPairs([2, 3, 6])',
    expect=sum(x // y for x in [2, 3, 6] for y in [2, 3, 6]),
    max_steps=110,
    views=[
        dict(type='array', var='sorted_nums', label='sorted_nums（从大到小处理）', pointers={'p': 'blue'}, h=170),
        dict(type='map', var='cnt_dict', label='cnt_dict[x]：数组中 ≥ x 的数的个数', h=200, fmt=lambda k, v: f'{k}→{v}'),
        dict(type='text', h=80, fn=lambda S: (f"除数 `{S['sorted_nums'][S['p']]}`（{S['cnt']} 个），商 `{S['multi']}`：分子 ∈ `[{S['last']}, {S['last'] + S['sorted_nums'][S['p']] - 1}]`" if 30 <= S['_line'] <= 41 and 'multi' in S and 'last' in S and 'cnt' in S and 0 <= S['p'] < len(S['sorted_nums']) else '')),
    ],
    watch=['p', 'cnt', 'multi', ('res', 'res', 'green')],
    captions={
        'sorted_nums = sorted(nums)': '先排序，之后从大到小处理每个除数',
        'max_num = sorted_nums[-1]': '最大值 `{max_num}`，也是 `cnt_dict` 的上界',
        'p = n - 1': '`p` 指向当前要处理的最大数',
        'while p >= 0': '`p = {p}`：{"还有数没处理" if p >= 0 else "全部处理完"}',
        'prev_pos = p - 1': '往左找相同数字的边界，重复数要一起处理',
        'while prev_pos >= 0 and': '{"左边没有数了，边界到头" if prev_pos < 0 else "`sorted_nums[" + str(prev_pos) + "]` " + ("等于" if sorted_nums[prev_pos] == sorted_nums[p] else "不等于") + " `sorted_nums[" + str(p) + "]`"}',
        'prev_pos -= 1': '同样的数，边界左移 → `prev_pos = {prev_pos}`',
        'cnt = p - prev_pos': '这个数一共有 `cnt = {cnt}` 个',
        'for num in range(bound': '把还没记录的更大的值补上 cnt_dict：它们的个数等于比它大一的值的个数',
        'cnt_dict[num] = cnt_dict[num + 1]': '`cnt_dict[{num}] = cnt_dict[{num + 1}] = {cnt_dict[num]}`',
        'cnt_dict[num] = 0': '最大值之上没有数，`cnt_dict[{num}] = 0`',
        'cnt_dict[sorted_nums[p]] = cnt': '`cnt_dict[{sorted_nums[p]}]` 先放入自己的 `cnt = {cnt}` 个',
        'if sorted_nums[p] < max_num': '不是最大值时还要加上更大数的个数',
        'cnt_dict[sorted_nums[p]] += ': '后缀和：`cnt_dict[{sorted_nums[p]}]` = =={cnt_dict[sorted_nums[p]]}==，即数组中 ≥ {sorted_nums[p]} 的数的个数',
        'bound = sorted_nums[p] - 1': '下一轮从 `{bound}` 开始补',
        'last = sorted_nums[p]': '`last` 是当前商 `multi` 对应的区间左端 `multi × 除数`',
        'step = max_num //': '商最大是 `max_num // 除数 = {step}`',
        'while multi < step': '`multi = {multi}`，{"商还没到最大，枚举区间 [last, now)" if multi < step else "到达最大商，退出"}',
        'now = last + sorted_nums[p]': '区间 `[{last}, {now - 1}]` 里的数除以 {sorted_nums[p]} 商都是 `{multi}`',
        'res += cnt * (cnt_dict[last]': '区间内有 `cnt_dict[{last}] - cnt_dict[{now}] = {cnt_dict[last] - cnt_dict[now]}` 个数，除数 {cnt} 个，商 {multi} → `res` = =={res}==',
        'last = now': '`last` 移到下一个区间的左端 {last}',
        'multi += 1': '商加 1 → {multi}',
        'res += cnt * cnt_dict[last] * multi': '最后一个区间 `[{last}, ∞)`：个数 `cnt_dict[{last}] = {cnt_dict[last]}`，商都是 {multi} → `res` = =={res}==',
        'p = prev_pos': '处理下一个不同的数：`p = {prev_pos}`',
    },
    cards=dict(
        one_liner='除数从大到小，边处理边把「≥ x 的个数」存进 cnt_dict',
        complexity='时间 `O(U log U)`，空间 `O(U)`',
        problem=['求所有下标对 `(i, j)` 的 `floor(nums[i] / nums[j])` 之和，结果对 `1e9+7` 取余',
                 '数组长 1e5、值 ≤ 1e5，不能两两枚举',
                 '本视频：`[2,3,6]` → `9`'],
        quote='可以采用类似筛法的思路，枚举除数与向下取整后的结果。……nums中有重复的数，因此在处理时应该将这些数收集起来一起处理。',
        quote_src='—— yiduobo 题解原文',
        idea=['除数 `num`、商 `multi`：被除数在 `[num*multi, num*(multi+1)-1]`',
              '用后缀和 `cnt_dict[x]` = 数组中 ≥ x 的个数，两项相减得区间内个数',
              '除数从大到小，边处理边补 `cnt_dict`；重复的数合并成 `cnt` 一起处理'],
        summary=['原文为 Python 2 写法，`max_num / sorted_nums[p]` 的整数除法已改为 `//`',
                 '时间 `O(U log U)`，空间 `O(U)`',
                 '易错点：重复数必须合并处理；最后一个区间没有上界，要单独加',
                 '对比灵神：灵神用前缀和，yiduobo 用后缀和，顺序从大到小'],
    ),
)
