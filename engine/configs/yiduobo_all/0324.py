def P(v, lo, hi):
    return f'{v} if {lo} <= _line <= {hi} else None'


def _phase(S):
    ln = S['_line']
    if ln <= 30:
        k = S.get('k')
        if S.get('mid_num') is not None:
            return f'阶段 1：快速选择找中位数，已找到 mid_num = =={S["mid_num"]}=='
        return f'阶段 1：快速选择，在 `[l, r]` 里找第 `{k}` 小的数（中位数）'
    if ln <= 46:
        return f'阶段 2：三路划分：小于 `{S["mid_num"]}` 的放最前（蓝），等于的放中间（绿），大于的放后面'
    if ln <= 51:
        return '阶段 3：全部减去最小值，保证没有负数，再记下最大值 `max_num`'
    if ln <= 69:
        return '阶段 4：按「小的放偶数位、大的放奇数位」沿换位环搬运；加 `max_num+1` 当作已搬运标记（紫）'
    return '阶段 5：减掉标记，加回最小值，还原'


def _col(S, i, v):
    ln = S['_line']
    mm = S.get('mid_num')
    if 32 <= ln <= 46 and mm is not None:
        if i <= S.get('equal_pos', -1) and i > S.get('small_pos', -1):
            return 'green'
        if i <= S.get('small_pos', -1):
            return 'blue'
        return None
    if 53 <= ln <= 69 and S.get('max_num') is not None and v > S['max_num']:
        return 'purple'
    return None


def _dim(S, i, v):
    ln = S['_line']
    if ln <= 30 and 'l' in S and 'r' in S:
        return not (S['l'] <= i <= S['r'])
    return False


CONFIG = dict(
    num=324, title='摆动排序 II', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='快速选择 + 三路划分 + 原地换位环',
    tags=['贪心算法'],
    code='''
class Solution(object):
    def wiggleSort(self, nums):

        l = 0
        r = len(nums) - 1
        k = (len(nums) + 1) // 2
        while l <= r:
            if l == r:
                mid_num = nums[l]
                break

            mid = nums[(l + r) // 2]
            i = l
            j = r
            while i <= j:
                while i <= r and nums[i] < mid: i += 1
                while j >= l and nums[j] > mid: j -= 1
                if i <= j:
                    nums[i], nums[j] = nums[j], nums[i]
                    i += 1
                    j -= 1

            if j - l + 1 >= k:
                r = j
            elif i - l >= k:
                mid_num = nums[l + k - 1]
                break
            else:
                k -= i - l
                l = i

        small_pos = -1
        equal_pos = -1
        for index, num in enumerate(nums):
            if num > mid_num:
                continue
            elif num == mid_num:
                nums[index] = nums[equal_pos + 1]
                nums[equal_pos + 1] = mid_num
                equal_pos += 1
            else:
                nums[index] = nums[equal_pos + 1]
                nums[equal_pos + 1] = nums[small_pos + 1]
                nums[small_pos + 1] = num
                small_pos += 1
                equal_pos += 1

        min_num = min(nums)
        for index in range(len(nums)):
            nums[index] -= min_num
        max_num = max(nums)

        for index in range(len(nums)):
            if nums[index] <= max_num:
                now = index
                prev_num = nums[index]
                while True:
                    if now <= (len(nums) - 1) // 2:
                        next_pos = ((len(nums) - 1) // 2 - now) * 2
                    else:
                        next_pos = (len(nums) - 1 - now) * 2 + 1
                    
                    if next_pos == index:
                        break
                    prev_num, nums[next_pos] = nums[next_pos], prev_num
                    nums[next_pos] += max_num + 1
                    now = next_pos

                nums[index] = prev_num + max_num + 1

        for index in range(len(nums)):
            nums[index] -= max_num + 1 
            nums[index] += min_num
''',
    setup='nums = [1,1,2]',
    call='Solution().wiggleSort(nums)\nnums',
    expect=[1,2,1],
    views=[
        dict(type='text', h=70, fn=_phase),
        dict(type='array', var='nums', h=240, label='nums', cell=84,
             pointers={P('l', 4, 30): 'blue', P('r', 4, 30): 'pink', P('i', 12, 30): 'yellow', P('j', 12, 30): 'orange',
                       P('index', 34, 46): 'yellow', P('small_pos', 34, 46): 'blue', P('equal_pos', 34, 46): 'green',
                       P('index', 49, 73): 'yellow', P('now', 55, 69): 'pink', P('next_pos', 59, 69): 'orange'},
             pointer_labels={P('l', 4, 30): 'l', P('r', 4, 30): 'r', P('i', 12, 30): 'i', P('j', 12, 30): 'j',
                             P('index', 34, 46): 'index', P('small_pos', 34, 46): 'small_pos', P('equal_pos', 34, 46): 'equal_pos',
                             P('index', 49, 73): 'index', P('now', 55, 69): 'now', P('next_pos', 59, 69): 'next_pos'},
             color=_col, dim=_dim),
    ],
    watch=['k', 'mid_num', 'min_num', 'max_num', 'prev_num'],
    skip=[13, 14, 20, 21, 27, 33, 36, 40, 45, 49, 50, 55, 57, 64, 67, 72, 73],
    max_steps=130,
    captions={
        'k = (len(nums) + 1) // 2': '要找第 `k = {k}` 小的数，也就是中位数',
        'while l <= r': '在 `[l, r] = [{l}, {r}]` 里继续找中位数',
        'if l == r': lambda S, B, r: (f'范围只剩一个数 → 它就是中位数 `nums[{S.l}] = {S.nums[S.l]}`' if S.l == S.r else '范围里还有多个数，继续划分'),
        'mid_num = nums[l]': '中位数 `mid_num = {mid_num}`',
        'mid = nums[': '取中间的数当基准 `mid = {mid}`，像快排一样左右划分',
        'i = l': '`i` 从左、`j` 从右向中间扫',
        'while i <= r and nums[i] < mid': '`i` 右移，跳过小于基准的数，停在 `i = {i}`（`nums[i] ≥ mid`）',
        'while j >= l and nums[j] > mid': '`j` 左移，跳过大于基准的数，停在 `j = {j}`（`nums[j] ≤ mid`）',
        'if i <= j': lambda S, B, r: (f'`i = {S.i} ≤ j = {S.j}`：两边都卡住了 → 交换' if S.i <= S.j else f'`i = {S.i} > j = {S.j}`：划分完成，`[l, j]` 都 ≤ 基准，`[i, r]` 都 ≥ 基准'),
        'nums[i], nums[j] = nums[j], nums[i]': '交换 `nums[i]` 与 `nums[j]`：{nums}',
        'if j - l + 1 >= k': lambda S, B, r: (f'左半有 `j - l + 1 = {S.j - S.l + 1}` ≥ k = {S.k} 个 → 第 k 小在左半，只留 `[l, j]`' if S.j - S.l + 1 >= S.k
                                              else f'左半只有 `{S.j - S.l + 1}` 个 < k = {S.k}，第 k 小不在左半'),
        'r = j': '右边界缩到 `r = {r}`',
        'elif i - l >= k': lambda S, B, r: (f'`l ~ i-1` 共 `{S.i - S.l}` ≥ k = {S.k} 个，中间夹着的全是基准 → 第 k 小就是基准' if S.i - S.l >= S.k
                                            else f'`l ~ i-1` 只有 `{S.i - S.l}` < k = {S.k} 个 → 第 k 小在右半'),
        'mid_num = nums[l + k - 1]': '第 k 小就是 `nums[{l + k - 1}] = {mid_num}`，中位数找到，退出',
        'k -= i - l': '左边 `{B.i - B.l}` 个都比它小，丢掉；还要在右半找第 `k = {k}` 小',
        'l = i': '左边界右移到 `l = {l}`',
        'small_pos = -1': '三路划分：`small_pos` 是「小于」那段的末尾，`equal_pos` 是「等于」那段的末尾',
        'if num > mid_num': lambda S, B, r: (f'`{S.num} > mid_num = {S.mid_num}`：大于 → 留在后面不动' if S.num > S.mid_num
                                             else f'`{S.num} > {S.mid_num}`？否'),
        'continue': '大于中位数的先不管，它会被前面的小数挤到后面',
        'elif num == mid_num': lambda S, B, r: (f'`{S.num} == mid_num`：等于 → 放进「等于」段' if S.num == S.mid_num
                                                else f'`{S.num} < mid_num = {S.mid_num}`：小于 → 放进最前面的「小于」段'),
        38: '把 `equal_pos + 1` 位置的数换到当前位置：{nums}',
        39: '当前位置的中位数放到「等于」段末尾：{nums}',
        40: '`equal_pos` → {equal_pos}，「等于」段多了一个',
        42: '把「等于」段下一个位置的数挪到当前位置：{nums}',
        43: '再把「小于」段下一个位置的数挪到「等于」段新位置：{nums}',
        44: '小数 `{num}` 放到「小于」段末尾：{nums}',
        45: '`small_pos` → {small_pos}，「小于」段多了一个',
        46: '`equal_pos` → {equal_pos}，「等于」段整体后移一格',
        'min_num = min(nums)': '最小值 `min_num = {min_num}`：下一步全部减去它，数就都非负了',
        'nums[index] -= min_num': '`nums[{index}]` 减去 min_num → {nums}',
        'max_num = max(nums)': '已全部减去 min_num：{nums}。最大值 `max_num = {max_num}`：一个数 `+max_num+1` 就一定大于 max_num，可当「已搬运」标记',
        'if nums[index] <= max_num': lambda S, B, r: (f'`nums[{S.index}] = {S.nums[S.index]} ≤ max_num = {S.max_num}`：还没搬运 → 从它开始走一个换位环' if S.nums[S.index] <= S.max_num
                                                      else f'`nums[{S.index}] = {S.nums[S.index]} > max_num`：已被搬运过（带标记）→ 跳过'),
        'now = index': '`now` 记录当前所在位置，沿换位环走',
        'prev_num = nums[index]': '手里拿起 `prev_num = {prev_num}`，它要搬到别处',
        'if now <= (len(nums) - 1) // 2': lambda S, B, r: (f'`now = {S.now}` 在前半（小数）→ 去偶数位，越靠中间越靠边' if S.now <= (len(S.nums) - 1) // 2
                                                          else f'`now = {S.now}` 在后半（大数）→ 去奇数位，越靠中间越靠边'),
        'next_pos = ((len(nums) - 1) // 2 - now) * 2': '目标位置 `next_pos = {next_pos}`',
        'next_pos = (len(nums) - 1 - now) * 2 + 1': '目标位置 `next_pos = {next_pos}`',
        'if next_pos == index': lambda S, B, r: (f'`next_pos = {S.next_pos}` 回到起点 `index` → 环走完了，退出' if S.next_pos == S.index
                                                 else f'`next_pos = {S.next_pos}` ≠ `index = {S.index}`：环还没闭合，继续搬'),
        'break': lambda S, B, r: ('找到中位数，退出快速选择' if S['_line'] < 30 else '换位环走完，退出'),
        'prev_num, nums[next_pos] = nums[next_pos], prev_num': '手里的数放到 `next_pos`，把原来的数拿起：`prev_num = {prev_num}`',
        'nums[next_pos] += max_num + 1': '给刚放下的数 `+max_num+1` 打标记（变紫）：{nums}',
        'now = next_pos': '`now` → {now}，继续搬手里的数',
        'nums[index] = prev_num + max_num + 1': '最后手里的数放回起点，同样打标记：{nums}',
        71: lambda S, B, r: (f'全部还原完毕：{S.nums}，满足 `nums[0] < nums[1] > nums[2] ...`' if B.get('index') == S.index
                             else ('最后一步：每个数先减 `max_num+1` 去掉标记，再加回 `min_num` 还原' if S.index == 0
                                  else f'前 {S.index} 个数已还原：{S.nums}')),
    },
    cards=dict(
        one_liner='找中位数，三路划分，再用换位环原地交错摆放',
        complexity='时间 `O(n)`（期望），空间 `O(1)`',
        problem=['无序数组 `nums`，原地重排成 `nums[0] < nums[1] > nums[2] < nums[3]...`',
                 '题目保证一定有解',
                 '本视频：`[1,1,2]`',
                 '→ `[1,2,1]`'],
        quote='我们需要将所有小于mid_num的数放在数组的左侧，而大于mid_num的数放在数组右侧。……计算出每个数应该放置的位置，那么这些数之间会形成若干个交换的环。',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素做法：排序后从中间截断，一左一右交错合并；中间的数放更靠边的位置',
              '其实只要「小的一半」「大的一半」：快速选择找中位数，三路划分',
              '交错放置时每个数的目标位置固定，形成换位环：逐环搬运，加 `max_num+1` 当已搬运标记'],
        summary=['时间期望 `O(n)`，空间 `O(1)`（原地）',
                 '易错：==相等的数不能相邻==，所以中间的数要放到更靠边的位置',
                 '标记用「加 `max_num+1`」，所以要先减最小值保证非负',
                 '原文为 Python 2 写法，`/` 做整数除法的 4 处已改为 `//`'],
    ),
)
