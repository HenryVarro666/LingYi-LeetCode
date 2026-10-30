CONFIG = dict(
    num=2762, title='不间断子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='滑动窗口 + 单调队列',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1940'],
    code='''
class Solution:
    def continuousSubarrays(self, nums: List[int]) -> int:
        min_q = deque()
        max_q = deque()
        ans = left = 0
        for right, x in enumerate(nums):
            while min_q and x <= nums[min_q[-1]]:
                min_q.pop()
            min_q.append(right)

            while max_q and x >= nums[max_q[-1]]:
                max_q.pop()
            max_q.append(right)

            while nums[max_q[0]] - nums[min_q[0]] > 2:
                left += 1
                if min_q[0] < left:
                    min_q.popleft()
                if max_q[0] < left:
                    max_q.popleft()
            ans += right - left + 1
        return ans
''',
    call='Solution().continuousSubarrays([5,4,2,4,6])',
    expect=10,
    views=[
        dict(type='array', var='nums', pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), h=190,
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right']),
             color=lambda S, i, v: ('green' if (S['min_q'] and i == S['min_q'][0]) or (S['max_q'] and i == S['max_q'][0]) else None) if 'right' in S and 'left' in S and S['left'] <= i <= S['right'] else None),
        dict(type='queue', var='max_q', fmt=lambda i: f'{i}:{[5,4,2,4,6][i]}', label='max_q（下标:值，队首 = 窗口最大）', h=120),
        dict(type='queue', var='min_q', fmt=lambda i: f'{i}:{[5,4,2,4,6][i]}', label='min_q（下标:值，队首 = 窗口最小）', h=120),
        dict(type='text', fn=lambda S: (f"窗口 `[{S['left']}, {S['right']}]`：最大 `{S['nums'][S['max_q'][0]]}` − 最小 `{S['nums'][S['min_q'][0]]}` = =={S['nums'][S['max_q'][0]] - S['nums'][S['min_q'][0]]}==" if S.get('max_q') and S.get('min_q') and 'left' in S else '')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'while min_q and': lambda S, B, r: (f'队尾 `nums[{S.min_q[-1]}] = {S.nums[S.min_q[-1]]}` >= `x = {S.x}`：它以后==不可能再是最小值==，弹掉' if S.min_q and S.x <= S.nums[S.min_q[-1]] else ('min_q 为空，不用弹' if not S.min_q else f'队尾 `{S.nums[S.min_q[-1]]}` < `x = {S.x}`，保留，停止弹出')),
        'min_q.append': '`x = {x}` 入 min_q 队尾，队列里的值从队首到队尾==严格递增==',
        'while max_q and': lambda S, B, r: (f'队尾 `nums[{S.max_q[-1]}] = {S.nums[S.max_q[-1]]}` <= `x = {S.x}`：它以后==不可能再是最大值==，弹掉' if S.max_q and S.x >= S.nums[S.max_q[-1]] else ('max_q 为空，不用弹' if not S.max_q else f'队尾 `{S.nums[S.max_q[-1]]}` > `x = {S.x}`，保留，停止弹出')),
        'max_q.append': '`x = {x}` 入 max_q 队尾，队列里的值从队首到队尾==递减==',
        'while nums[max_q[0]]': lambda S, B, r: (lambda d: f'窗口最大 `{S.nums[S.max_q[0]]}` − 最小 `{S.nums[S.min_q[0]]}` = {d}，' + ('==大于 2，不合法==，要缩小窗口' if d > 2 else '不超过 2，窗口合法'))(S.nums[S.max_q[0]] - S.nums[S.min_q[0]]),
        'left += 1': '差大于 2：`left` 右移到 {left}，==越短越合法==，缩到合法为止',
        'if min_q[0] <': lambda S, B, r: f'min_q 队首下标 `{S.min_q[0]}` ' + (f'< left（{S.left}）：已滑出窗口，移出' if S.min_q[0] < S.left else f'>= left（{S.left}）：仍在窗口内'),
        'if max_q[0] <': lambda S, B, r: f'max_q 队首下标 `{S.max_q[0]}` ' + (f'< left（{S.left}）：已滑出窗口，移出' if S.max_q[0] < S.left else f'>= left（{S.left}）：仍在窗口内'),
        'ans += ': '右端点固定为 {right}，左端点 {left}..{right} 全合法，共 `{right} - {left} + 1` = {right-left+1} 个：`ans` = =={ans}==',
        'return ans': '所有右端点都算完，总数 =={ret}==',
    },
    cards=dict(
        one_liner='枚举右端点，窗口越短越合法：每次加 right-left+1',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['子数组中任意两数的绝对差 `<= 2`，就是「不间断」的',
                 '数出所有不间断子数组的个数',
                 '示例：`[5,4,2,4]` → `8`；本视频：`[5,4,2,4,6]` → `10`'],
        quote='由于子数组越短，越能满足题目要求，所以除了 [left,right]，还有 [left+1,right],……,[right,right] 都是满足要求的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['合法 = 窗口最大值 − 最小值 `<= 2`，用两个单调队列分别维护最大、最小下标',
              '不合法就 `left += 1`，并把滑出窗口的队首弹掉',
              '合法后，以 `right` 结尾的合法子数组恰有 `right-left+1` 个，加进答案'],
        summary=['单调队列让最值查询 `O(1)`，总时间 `O(n)`，与差值上限 2 无关',
                 '队列存==下标==而不是值，才能判断队首是否滑出窗口',
                 '题解方法一用 `Counter` 维护窗口，差值至多 2 所以字典只有 O(1) 个键',
                 '同类题：1438. 绝对差不超过限制的最长连续子数组'],
    ),
)
