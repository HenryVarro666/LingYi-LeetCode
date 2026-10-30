CONFIG = dict(
    num=689, title='三个无重叠子数组的最大和', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='窗口和 + 左右最大位置',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def maxSumOfThreeSubarrays(self, nums, k):

        f = [0]
        for index in range(k):
            f[0] += nums[index]
        for index in range(k, len(nums)):
            f.append(f[-1] + nums[index] - nums[index - k])
        
        left_max = [0]
        for index in range(1, len(f)):
            if f[index] > f[left_max[-1]]:
                left_max.append(index)
            else:
                left_max.append(left_max[-1])
        
        right_max = [len(f) - 1]
        for index in range(len(f) - 1, -1, -1):
            if f[index] >= f[right_max[-1]]:
                right_max.append(index)
            else:
                right_max.append(right_max[-1])
        
        right_max.reverse()

        max_sum = 0
        max_pos = []

        for index in range(k, len(f) - k):
            left_pos = left_max[index - k]
            right_pos = right_max[index + k]
            if f[left_pos] + f[right_pos] + f[index] > max_sum:
                max_sum = f[left_pos] + f[right_pos] + f[index]
                max_pos = [left_pos, index, right_pos]
        
        return max_pos
''',
    call='Solution().maxSumOfThreeSubarrays([1,2,1,2,6,7,5,1], 2)',
    expect=[0, 3, 5],
    views=[
        dict(type='array', var='nums', h=125, label='nums（k = 2）', cell=70,
             color=lambda S, i, v: ('yellow' if 'max_pos' in S and 'index' in S and S['max_pos'] and i in [p + d for p in S['max_pos'] for d in range(S['k'])] else None)),
        dict(type='array', var='f', pointers={'index': 'blue'}, h=165, label='f：从 i 起长 k 的窗口和', cell=70),
        dict(type='array', var='left_max', pointers={'index': 'cyan'}, h=165, label='left_max：f[0..i] 最大值的位置', cell=70),
        dict(type='array', var='right_max', pointers={'index': 'orange'}, h=165, label='right_max：f[i..] 最大值的位置', cell=70),
        dict(type='text', h=70, fn=lambda S: (f"中间段 `{S['index']}`：左 `{S['left_pos']}`，右 `{S['right_pos']}` → `{S['f'][S['left_pos']]} + {S['f'][S['index']]} + {S['f'][S['right_pos']]}` = =={S['f'][S['left_pos']] + S['f'][S['index']] + S['f'][S['right_pos']]}==" if 'right_pos' in S and S.get('_line', 0) >= 32 else '')),
    ],
    watch=[('index', 'index', 'blue'), ('max_sum', 'max_sum', 'green'), ('max_pos', 'max_pos', 'yellow')],
    captions={
        'f = [0]': '`f[0]` 先用来累加第一个长 `k` 的窗口',
        'f[0] += nums[index]': '`f[0]` 累加 `nums[{index}]` → {f[0]}',
        'f.append(': '窗口右移一格：加进 `nums[{index}]`，去掉 `nums[{index - k}]` → `f` 末尾 =={f[-1]}==',
        'left_max = [0]': '`left_max[i]`：前缀里窗口和最大的起点，第 0 个就是 0',
        'if f[index] > f[left_max[-1]]': '`f[{index}] = {f[index]}` 对比当前最大 `f[{left_max[-1]}] = {f[left_max[-1]]}`：==严格大于==才换（字典序最小）',
        'left_max.append(index)': '更大，最大位置换成 `{index}`',
        'left_max.append(left_max[-1])': '不更大，沿用前面的位置 `{left_max[-1]}`',
        'right_max = [': '`right_max` 从右往左建，最后一个窗口先放进去',
        'if f[index] >= f[right_max[-1]]': '`f[{index}] = {f[index]}` 对比 `f[{right_max[-1]}] = {f[right_max[-1]]}`：==大于等于==就换，让位置尽量靠前',
        'right_max.append(index)': '位置换成 `{index}`',
        'right_max.append(right_max[-1])': '沿用右边的位置 `{right_max[-1]}`',
        'right_max.reverse()': '倒着建的，翻转后 `right_max[i]` 就对应从 `i` 起的后缀',
        'for index in range(k, len(f) - k)': '枚举中间段起点 `{index}`：左边至少留 `k` 个，右边也要留 `k` 个',
        'left_pos = ': '第一段只能在 `[0, {index - k}]` 里选 → `left_max[{index - k}] = {left_pos}`',
        'right_pos = ': '第三段只能在 `[{index + k}, ..]` 里选 → `right_max[{index + k}] = {right_pos}`',
        'if f[left_pos]': '三段和 `{f[left_pos] + f[right_pos] + f[index]}` 对比目前最大 `{max_sum}`：==严格大于==才更新',
        'max_sum = f[left_pos]': '更新最大和 `{max_sum}`',
        'max_pos = [': '记录三段起点 `{max_pos}`',
        'return max_pos': '三段起点 `{max_pos}`，总和 `{max_sum}`',
    },
    cards=dict(
        one_liner='只枚举中间段，左右两段用预处理好的最大位置直接查',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['在 `nums` 里选 3 段互不重叠、长度都为 `k` 的子数组，使总和最大',
                 '返回三段的起点；有多解时返回字典序最小的',
                 '本视频：`[1,2,1,2,6,7,5,1]`，`k=2` → `[0,3,5]`'],
        quote='到了这里，我们就只需要枚举第二段的起始位置index，那么第一段的起始位置就是left_max[index - k]，而第三段的起始位置则是right_max[index + k]，最终的时间复杂度就优化到了O(n)。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用滑动窗口算出 `f[i]`：以 `i` 起头的长 `k` 窗口和',
              '`left_max` / `right_max` 记录前缀 / 后缀里 `f` 最大的位置',
              '枚举中间段 `index`，左右两段位置 O(1) 查表；比较符号一严一松，保证字典序最小'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`left_max` 用严格大于，`right_max` 用大于等于：都是为了位置靠前',
                 '中间段范围 `[k, len(f)-k)`，保证左右都放得下',
                 '`right_max` 倒着建后要 `reverse`，下标才对得上',
                 '`right_max` 因循环多放了一项，长度比 `f` 多 1，不影响查询',
                 '原文本身就是 Python 3 可运行的写法，未做修改'],
    ),
)
