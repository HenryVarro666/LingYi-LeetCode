def _info(S):
    I = S['_inner']
    if 'lower' not in I:
        return '把区间和变成前缀和之差：`sum_list[j] - sum_list[i]` 落在 `[lower, upper]` 内的数对个数'
    if 'mid' not in I:
        return f"区间 `[{I['l']}, {I['r']}]`"
    return f"区间 `[{I['l']}, {I['mid']}]` 与 `[{I['mid'] + 1}, {I['r']}]` 都已排序，`res = {I.get('res')}`"


CONFIG = dict(
    num=327, title='区间和的个数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='前缀和 + 归并排序 · 三指针',
    tags=['灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def countRangeSum(self, nums, lower, upper):

        if not nums:
            return 0

        sum_list = nums[:]
        for index in range(1, len(nums)):
            sum_list[index] += sum_list[index - 1]
        
        return self.mergeSort(0, len(nums) - 1, lower, upper, sum_list)

    def mergeSort(self, l, r, lower, upper, sum_list):
        if l == r:
            if sum_list[l] >= lower and sum_list[l] <= upper:
                return 1
            return 0

        mid = (l + r) // 2
        res = self.mergeSort(l, mid, lower, upper, sum_list) + self.mergeSort(mid + 1, r, lower, upper, sum_list)

        merge_pos = lower_pos = upper_pos = mid + 1
        tmp_list = []
        for index in range(l, mid + 1):
            while merge_pos <= r and sum_list[merge_pos] < sum_list[index]:
                tmp_list.append(sum_list[merge_pos])
                merge_pos += 1
            while lower_pos <= r and sum_list[lower_pos] - sum_list[index] < lower:
                lower_pos += 1
            while upper_pos <= r and sum_list[upper_pos] - sum_list[index] <= upper:
                upper_pos += 1
            
            res += upper_pos - lower_pos
            tmp_list.append(sum_list[index])

        for index in range(len(tmp_list)):
            sum_list[l + index] = tmp_list[index]

        return res
''',
    call='Solution().countRangeSum([-2, 5, -1], -2, 2)',
    expect=3,
    skip=['if l == r', 'if sum_list[l]', 'tmp_list = []', 36, 37],
    max_steps=90,
    views=[
        dict(type='text', fn=_info),
        dict(type='array', var=lambda S: S['_inner'].get('sum_list', S.get('sum_list')),
             label='sum_list（框 = 归并区间，蓝 = 当前 index）', h=210,
             pointers={'lower_pos': 'pink', 'upper_pos': 'orange'},
             color=lambda S, i, v: 'blue' if S['_inner'].get('index') == i and 'mid' in S['_inner'] and i <= S['_inner']['mid'] else None,
             window=('l', 'r')),
        dict(type='array', var='tmp_list', label='tmp_list（归并结果）', h=130),
        dict(type='calls', h=200, hide=('sum_list',)),
    ],
    watch=['l', 'r', 'mid', 'lower_pos', 'upper_pos', ('res', 'res', 'green')],
    captions={
        'sum_list = nums[:]': '先复制一份 `nums`，下面原地改成前缀和',
        'sum_list[index] += ': '`sum_list[{index}]` = 前 `{index + 1}` 个数之和 = =={sum_list[index]}==',
        'return self.mergeSort(0': '区间和 `[i..j]` = `sum_list[j] - sum_list[i-1]`，于是转成对前缀和数对计数；开始分治',
        'return 1': '`l == r`：单个前缀和 `{sum_list[l]}` 本身就是 `nums[0..{l}]` 的区间和（要特判）：`{lower} <= {sum_list[l]} <= {upper}` → 返回 1',
        'return 0': lambda S, B, r: (f'`l == r`：单个前缀和 `{S.sum_list[S.l]}` 本身是 `nums[0..{S.l}]` 的区间和，不在 `[{S.lower}, {S.upper}]` 内 → 返回 0' if S.l == S.r else '空数组，返回 0'),
        'mid = (l + r)': '`mid = ({l} + {r}) // 2 = {mid}`：左半 `[{l}, {mid}]`，右半 `[{mid + 1}, {r}]`',
        'res = self.mergeSort': '两半各自递归完：内部合法数对已数好，且都已排序；`res` = =={res}==',
        'merge_pos = lower_pos': '三个指针都从右半起点出发：`merge_pos` 管归并，`lower_pos` / `upper_pos` 划出合法范围',
        24: lambda S, B, r: f'枚举左半的 `sum_list[{S.index}] = {S.sum_list[S.index]}`，在有序的右半里找 `sum_list[j] - {S.sum_list[S.index]}` 落在 `[{S.lower}, {S.upper}]` 的 j',
        'while merge_pos': lambda S, B, r: (f'归并：右半 `sum_list[{S.merge_pos}] = {S.sum_list[S.merge_pos]}` 比左边的小 → 先放入 `tmp_list`' if S.merge_pos <= S.r and S.sum_list[S.merge_pos] < S.sum_list[S.index] else '右半没有更小的了，归并先停'),
        'tmp_list.append(sum_list[merge_pos])': '右半的 `{sum_list[merge_pos]}` 放入 `tmp_list`',
        'merge_pos += 1': '`merge_pos` → {merge_pos}',
        'while lower_pos': lambda S, B, r: (f'`{S.sum_list[S.lower_pos]} - {S.sum_list[S.index]} = {S.sum_list[S.lower_pos] - S.sum_list[S.index]} < lower = {S.lower}`：太小，`lower_pos` 要右移' if S.lower_pos <= S.r and S.sum_list[S.lower_pos] - S.sum_list[S.index] < S.lower else f'`lower_pos = {S.lower_pos}`：从这里起差值都 >= `lower`'),
        'lower_pos += 1': '`lower_pos` → {lower_pos}（右半有序，前面的差值只会更小）',
        'while upper_pos': lambda S, B, r: (f'`{S.sum_list[S.upper_pos]} - {S.sum_list[S.index]} = {S.sum_list[S.upper_pos] - S.sum_list[S.index]} <= upper = {S.upper}`：还没超，`upper_pos` 可以右移' if S.upper_pos <= S.r and S.sum_list[S.upper_pos] - S.sum_list[S.index] <= S.upper else f'`upper_pos = {S.upper_pos}`：此前的差值都 <= `upper`，这里开始超了'),
        'upper_pos += 1': '`upper_pos` → {upper_pos}',
        'res += upper_pos - lower_pos': '合法的 j 在 `[lower_pos, upper_pos)`：共 `{upper_pos} − {lower_pos}` = =={upper_pos - lower_pos}== 个 → `res` = =={res}==',
        'tmp_list.append(sum_list[index])': '左半的 `{sum_list[index]}` 放入 `tmp_list`；左半有序，下一个 index 的两个指针不回退',
        'sum_list[l + index] = tmp_list[index]': '把有序的 `tmp_list` 写回 `sum_list[{l}..]`，给上一层使用',
        'return res': '`tmp_list` 已写回 `sum_list[{l}..{r}]`，区间有序；其内共 `{res}` 对',
    },
    cards=dict(
        one_liner='前缀和之差落在 [lower, upper]，用归并排序 + 三指针数对',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['数组 `nums`，统计区间和 `S(i, j)` 落在 `[lower, upper]` 内的区间个数（`i <= j`）',
                 '示例：`[-2,5,-1]`，`lower=-2`，`upper=2` → `3`',
                 '三个区间：`[0,0]`、`[2,2]`、`[0,2]`'],
        quote='可以联想到一道经典的分治题求逆序对……这一题也可以如法炮制：设当前归并的两个部分为 left_sum 和 right_sum，先递归求解，再进行二路归并。',
        quote_src='—— yiduobo 题解原文',
        idea=['区间和 = 前缀和之差：数 `lower <= sum[j] - sum[i] <= upper` 的数对',
              '左右两半都已排序：对每个左边的 `sum[i]`，右半满足条件的 j 是一段连续区间 `[lower_pos, upper_pos)`',
              '左半递增，`lower_pos` / `upper_pos` 只会右移，不用回退，一趟扫描'],
        summary=['时间 `O(n log n)`：每层的归并、`lower_pos`、`upper_pos` 各扫一遍',
                 '`l == r` 要特判：单个前缀和本身就是 `nums[0..l]` 的区间和',
                 '`lower_pos` 找第一个 `>= lower`，`upper_pos` 找第一个 `> upper`，个数是 `upper_pos - lower_pos`',
                 '原文为 Python 2 写法，`mid = (l + r) / 2` 已改为 `//`',
                 '同类题：315 计算右侧小于当前元素的个数、493 翻转对'],
    ),
)
