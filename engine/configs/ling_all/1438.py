NUMS = [10, 1, 2, 4, 7, 2]

CONFIG = dict(
    num=1438, title='绝对差不超过限制的最长连续子数组', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='滑动窗口 + 两个单调队列',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1672'],
    code='''
class Solution:
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        min_q = deque()
        max_q = deque()
        ans = left = 0

        for i, x in enumerate(nums):
            # 1. 右边入
            while min_q and x <= nums[min_q[-1]]:
                min_q.pop()
            min_q.append(i)

            while max_q and x >= nums[max_q[-1]]:
                max_q.pop()
            max_q.append(i)

            # 2. 左边出
            while nums[max_q[0]] - nums[min_q[0]] > limit:
                left += 1
                if min_q[0] < left:  # 队首不在窗口中
                    min_q.popleft()
                if max_q[0] < left:  # 队首不在窗口中
                    max_q.popleft()

            # 3. 更新答案
            ans = max(ans, i - left + 1)

        return ans
''',
    call='Solution().longestSubarray([10,1,2,4,7,2], 5)',
    expect=4,
    views=[
        dict(type='array', var='nums', pointers={'left': 'blue', 'i': 'pink'}, window=('left', 'i'), h=190,
             dim=lambda S, i, v: 'i' in S and not (S['left'] <= i <= S['i'])),
        dict(type='queue', var='max_q', label='max_q（存下标:值，队首最大，递减）', fmt=lambda k: f'{k}:{NUMS[k]}', h=105),
        dict(type='queue', var='min_q', label='min_q（存下标:值，队首最小，递增）', fmt=lambda k: f'{k}:{NUMS[k]}', h=105),
        dict(type='text', h=60, fn=lambda S: (f"窗口极差：`{S['nums'][S['max_q'][0]]} − {S['nums'][S['min_q'][0]]}` = =={S['nums'][S['max_q'][0]] - S['nums'][S['min_q'][0]]}==，limit = {S['limit']}" if S.get('max_q') and S.get('min_q') else '')),
    ],
    watch=[('left', 'left', 'blue'), ('i', 'i', 'pink'), ('limit', 'limit'), ('ans', 'ans', 'green')],
    captions={
        'min_q = deque()': '`min_q` 维护窗口最小值，`max_q` 维护窗口最大值，==存下标==（要靠下标判断出窗口）',
        'for i, x in enumerate(nums)': '枚举右端点 `i = {i}`，`x = {x}` 进入窗口',
        'while min_q and x <= nums[min_q[-1]]': lambda S, B, r: ('`min_q` 队尾 `{}` >= `x = {}`：队尾不可能再当最小值，==弹出=='.format(S.nums[B.min_q[-1]], S.x) if B.min_q and S.x <= S.nums[B.min_q[-1]]
                                                                  else ('`min_q` 为空或队尾更小，停止弹出')),
        'min_q.pop()': '队尾出队：`min_q` = `{list(min_q)}`',
        'min_q.append(i)': '`i` 入队，`min_q` = `{list(min_q)}`，队首 `{nums[min_q[0]]}` 是窗口最小值',
        'while max_q and x >= nums[max_q[-1]]': lambda S, B, r: ('`max_q` 队尾 `{}` <= `x = {}`：队尾不可能再当最大值，==弹出=='.format(S.nums[B.max_q[-1]], S.x) if B.max_q and S.x >= S.nums[B.max_q[-1]]
                                                                  else ('`max_q` 为空或队尾更大，停止弹出')),
        'max_q.pop()': '队尾出队：`max_q` = `{list(max_q)}`',
        'max_q.append(i)': '`i` 入队，`max_q` = `{list(max_q)}`，队首 `{nums[max_q[0]]}` 是窗口最大值',
        'while nums[max_q[0]] - nums[min_q[0]] > limit': lambda S, B, r: ('极差 `{} − {} = {}` > `limit = {}`：窗口太宽，==收缩左端点=='.format(S.nums[S.max_q[0]], S.nums[S.min_q[0]], S.nums[S.max_q[0]] - S.nums[S.min_q[0]], S.limit)
                                                                          if S.nums[S.max_q[0]] - S.nums[S.min_q[0]] > S.limit
                                                                          else '极差 `{} − {} = {}` <= `limit = {}`：窗口合法'.format(S.nums[S.max_q[0]], S.nums[S.min_q[0]], S.nums[S.max_q[0]] - S.nums[S.min_q[0]], S.limit)),
        'left += 1': '`left` → {left}：左端点右移，扔掉 `nums[{left-1}]`',
        'if min_q[0] < left': lambda S, B, r: ('`min_q` 队首下标 `{}` < `left = {}`：已不在窗口，==出队=='.format(S.min_q[0], S.left) if S.min_q[0] < S.left
                                              else '`min_q` 队首 `{}` 仍在窗口里'.format(S.min_q[0])),
        'if max_q[0] < left': lambda S, B, r: ('`max_q` 队首下标 `{}` < `left = {}`：已不在窗口，==出队=='.format(S.max_q[0], S.left) if S.max_q[0] < S.left
                                              else '`max_q` 队首 `{}` 仍在窗口里'.format(S.max_q[0])),
        'min_q.popleft()': '`min_q` 队首出队：`{list(min_q)}`',
        'max_q.popleft()': '`max_q` 队首出队：`{list(max_q)}`',
        'ans = max(ans, i - left + 1)': '窗口长度 `{i} − {left} + 1 = {i-left+1}`，`ans = max({B.ans}, {i-left+1})` = =={ans}==',
        'return ans': '最长合法窗口长度 `{ans}`',
    },
    cards=dict(
        one_liner='窗口越长极差越大：滑动窗口 + 两个单调队列取最大最小',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给整数数组 `nums` 和 `limit`，求最长连续子数组，其中任意两元素之差 `<= limit`',
                 '即子数组的 ==最大值 − 最小值 <= limit==',
                 '示例：`[10,1,2,4,7,2]`，`limit = 5` → `4`（子数组 `[2,4,7,2]`）'],
        quote='子数组越长，子数组的最大值越大，最小值越小，最大值与最小值的差值越大，越不能满足题目 <= limit 的要求。反之，子数组越短，越满足要求。',
        quote_src='—— 灵茶山艾府题解',
        idea=['有这个单调性，就能用==滑动窗口==：枚举右端点，不满足就收缩左端点',
              '窗口最大、最小值各用一个==单调队列==维护（同 239 题）',
              '队列里存下标，因为要靠下标判断队首是否滑出窗口'],
        summary=['时间 `O(n)`：每个元素在两个队列里至多入队、出队各一次，内层 while 总次数是 `O(n)`',
                 '答疑：队列存下标而不是值，是为了判断队首是否在窗口外',
                 '答疑：出队写 `if` 就够：`left` 每加一，队列里没有重复下标，至多出队一个',
                 '同类题：239 滑动窗口最大值（§4.4 单调队列）'],
    ),
)
