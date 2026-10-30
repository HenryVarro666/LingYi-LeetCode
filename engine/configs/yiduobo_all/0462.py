def _text(S):
    if 'final_num' in S:
        return f'中位数 `{S["final_num"]}`：各数到它的距离累加，当前 `res = {S.get("res", 0)}`'
    if 'k' in S:
        return f'快速选择：找第 `k = {S["k"]}` 小的数（区间 `[{S["left"]}, {S["right"]}]`）'
    return '目标：把所有数移到 ==中位数== —— 先用快速选择找到它'


CONFIG = dict(
    num=462, title='最小操作次数使数组元素相等 II', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='两数取区间间推出中位数 + 快速选择',
    tags=[],
    code='''
import random
class Solution(object):
    def minMoves2(self, nums):

        final_num = self.search(nums, 0, len(nums) - 1, (len(nums) + 1) // 2)
        res = 0
        for num in nums:
            res += abs(num - final_num)

        return res

    def search(self, nums, left, right, k):
        if left == right:
            return nums[left]

        mid = nums[(left + right) // 2]
        i = left
        j = right
        while i <= j:
            while i <= right and nums[i] < mid:
                i += 1
            while j >= left and nums[j] > mid:
                j -= 1
            if i <= j:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
                j -= 1

        if j - left + 1 >= k:
            return self.search(nums, left, j, k)
        elif i - left >= k:
            return nums[left + k - 1]
        else:
            return self.search(nums, i, right, k - (i - left))
''',
    call='Solution().minMoves2([2, 1, 3, 5, 4])',
    expect=6,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='array', var='nums', h=190,
             pointers={'i': 'blue', 'j': 'pink'}, window=('left', 'right'),
             dim=lambda S, i, v: 'left' in S and 'right' in S and not (S['left'] <= i <= S['right']),
             color=lambda S, i, v: 'yellow' if 'mid' in S and v == S['mid'] and S['left'] <= i <= S['right'] else None),
        dict(type='calls', h=260, hide=('minMoves2',)),
    ],
    watch=['left', 'right', 'k', 'mid', 'i', 'j', ('res', 'res', 'green')],
    captions={
        'final_num = self.search': '先找中位数：第 `k = (n+1)//2` 小的数，用快速选择',
        'if left == right': lambda S, B, r: ('区间只剩一个数，它就是第 `k` 小' if S.left == S.right
                                             else f'区间 `[{S.left}, {S.right}]` 还有多个数，继续分区'),
        'mid = nums': '取区间中间的数当枢轴：`mid = {mid}`',
        'while i <= j': lambda S, B, r: (f'`i = {S.i}`、`j = {S.j}` 还没交叉，继续分区' if S.i <= S.j else f'`i = {S.i} > j = {S.j}`：分区完成，左边 ≤ mid，右边 ≥ mid'),
        'nums[i] < mid': lambda S, B, r: (f'`nums[{S.i}] = {S.nums[S.i]} < mid = {S.mid}`：已在左边，`i` 右移' if S.i <= S.right and S.nums[S.i] < S.mid
                                          else f'`nums[{S.i}] = {S.nums[S.i]} ≥ mid`：`i` 停下，它该去右边'),
        'i += 1': '`i` → {i}',
        'nums[j] > mid': lambda S, B, r: (f'`nums[{S.j}] = {S.nums[S.j]} > mid = {S.mid}`：已在右边，`j` 左移' if S.j >= S.left and S.nums[S.j] > S.mid
                                          else f'`nums[{S.j}] = {S.nums[S.j]} ≤ mid`：`j` 停下，它该去左边'),
        23: '`j` 左移 → {j}',
        27: '`j` → {j}',
        'if i <= j': lambda S, B, r: (f'`i = {S.i} ≤ j = {S.j}`：两个都停在错的一侧 → 交换' if S.i <= S.j else '`i > j`：不用交换'),
        'nums[i], nums[j] =': '交换 `nums[i]` 与 `nums[j]` → `{nums}`，两个指针各向内走一步',
        'if j - left + 1 >= k': '左半有 `j − left + 1 = {j - left + 1}` 个数，`k = {k}`：{"==第 k 小在左半==" if j - left + 1 >= k else "第 k 小不在左半"}',
        'elif i - left >= k': '`i − left = {i - left}` 个数 ≤ mid，{"≥ k：==第 k 位已被 mid 及左边覆盖，直接取 `nums[left + k − 1]`==" if i - left >= k else "< k：第 k 小在右半"}',
        'return self.search(nums, left, j, k)': '只递归左半 `[left, j]`',
        'return self.search(nums, i, right': '只递归右半，`k` 减去左边已经排除的 `i − left` 个',
        'return nums[left + k - 1]': '找到了：第 `k` 小 = `{nums[left + k - 1]}`',
        'res += abs': '`res += |{num} − {final_num}|` → {res}',
        'return res': '最少操作 `{res}` 次',
    },
    cards=dict(
        one_liner='先推出目标是中位数，再用快速选择 O(n) 找它',
        complexity='时间 `O(n)`（平均），空间 `O(log n)`',
        problem=['每次操作使一个数加 1 或减 1',
                 '求让所有元素相等的最少操作次数',
                 '示例：`[1,2,3]` → `2`；本视频：`[7,1,9,2,4,8,3]` → `6`'],
        quote='将所有数移动到nums[len / 2]时，所需的步数之和最少。于是题目现在就转化为了对于一个n个数的数组，如何求其中位数是多少。',
        quote_src='—— yiduobo 题解原文',
        idea=['先看两个数 `a < b`：目标 `x` 在 `[a, b]` 内，步数恒为 `b − a`，最小',
              '排好序后从两头配对：每一对的目标区间都包含中间那个数',
              '所以目标取中位数；用第 215 题的快速选择找第 `(n+1)//2` 小的数'],
        summary=['时间 `O(n)`（平均），空间 `O(log n)`（递归栈）',
                 '快速选择：分区后只递归含第 `k` 小的那一侧',
                 '易错点：`k` 是第几小（从 1 数），取值 `(n+1)//2`',
                 '原文为 Python 2 写法，`/` 做整数除法的 3 处（`(len(nums) + 1) / 2`、`(left + right) / 2` 等）已改为 `//`',
                 '对比灵神：灵神直接排序取 `n//2`，yiduobo 用快速选择省掉排序'],
    ),
)
