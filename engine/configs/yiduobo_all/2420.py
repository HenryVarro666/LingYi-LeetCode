CONFIG = dict(
    num=2420, title='找到所有好下标', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='枚举中间位置 + 预处理两侧长度',
    tags=['灵神题单·动态规划', '难度分 1695'],
    code='''
class Solution(object):
    def goodIndices(self, nums, k):

        n = len(nums)
        left = [1]
        for index in range(1, n):
            if nums[index] <= nums[index - 1]:
                left.append(left[-1] + 1)
            else:
                left.append(1)
        
        right = [1]
        for index in range(n - 2, -1, -1):
            if nums[index] <= nums[index + 1]:
                right.append(right[-1] + 1)
            else:
                right.append(1)
        right.reverse()

        res = []
        for index in range(k, n - k):
            if left[index - 1] >= k and right[index + 1] >= k:
                res.append(index)
        
        return res
''',
    call='Solution().goodIndices([2,1,1,1,3,4,1], 2)',
    expect=[2, 3],
    views=[
        dict(type='array', var='nums', label='nums', h=200, cell=80, pointers={'index': 'blue'},
             color=lambda S, j, v: 'green' if j in S.get('res', []) else None),
        dict(type='array', var='left', label='left[i]：以 i 结尾的最长非递增段', h=150, cell=80),
        dict(type='array', var='right', label='right[i]：以 i 开头的最长非递减段（反向构造，最后 reverse）', h=150, cell=80),
    ],
    watch=[('index', 'index', 'blue'), 'k', ('res', 'res', 'green')],
    captions={
        'left = [1]': '`left[index]` 以 `nums[index]` 结尾的最长非递增段，`left[0] = 1`',
        'if nums[index] <= nums[index - 1]': '`nums[{index}] = {nums[index]}` 与前一个 `{nums[index-1]}`：{"不大于前一个，非递增段延长" if nums[index] <= nums[index-1] else "比前一个大，段断开"}',
        'left.append(left[-1] + 1)': '`left[{index}] = left[{index-1}] + 1` = =={left[-1]}==',
        'left.append(1)': '重新开始：`left[{index}] = 1`',
        'right = [1]': '`right[index]` 以 `nums[index]` 开头的最长非递减段：反过来扫，最后再翻转',
        'if nums[index] <= nums[index + 1]': '`nums[{index}] = {nums[index]}` 与后一个 `{nums[index+1]}`：{"不大于后一个，非递减段延长" if nums[index] <= nums[index+1] else "比后一个大，段断开"}',
        'right.append(right[-1] + 1)': '追加 `{right[-1]}`（对应下标 `{index}`，此时 right 还是倒序）',
        'right.append(1)': '追加 1，段断开（对应下标 `{index}`）',
        'right.reverse()': '翻转后 `right[i]` 才与下标 `i` 对齐：`{right}`',
        'for index in range(k, n - k)': '枚举中间位置 `index` 从 `k` 到 `n-k-1`，两侧才有足够的 k 个元素',
        'if left[index - 1] >= k': '`left[{index-1}] = {left[index-1]}`，`right[{index+1}] = {right[index+1]}`，k = {k}：{"两边都 ≥ k，好下标" if left[index-1] >= k and right[index+1] >= k else "有一边不足 k"}',
        'res.append(index)': '`{index}` 是好下标 → `res = {res}`',
        'return res': '好下标：`{res}`',
    },
    cards=dict(
        one_liner='枚举中间位置，两侧的长度提前预处理好',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组 `nums` 和正整数 `k`，下标 `i` 之前 `k` 个元素非递增、之后 `k` 个元素非递减，则为好下标',
                 '按升序返回所有好下标',
                 '示例：`nums = [2,1,1,1,3,4,1], k = 2` → `[2,3]`'],
        quote='对于这类问题，通常的做法是枚举中间的位置，然后检测两侧是否符合要求。',
        quote_src='—— yiduobo 题解原文',
        idea=['`left[index]`：以 `nums[index]` 结尾的最长非递增子数组长度',
              '`right[index]`：以 `nums[index]` 开头的最长非递减子数组长度',
              '两趟遍历都用上一个位置的值递推；之后只需判断 `left[index-1]` 和 `right[index+1]` 是否 ≥ `k`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`right` 是从后往前追加的，==必须 `reverse`== 才与下标对齐',
                 '判断用 `left[index-1]` 和 `right[index+1]`，不含 `index` 自己',
                 '原文为 Python 2 写法，仅删去了类型说明文档字符串',
                 '对比灵神：灵神把前缀压成一个变量 `inc`，yiduobo 两个数组都保留'],
    ),
)
