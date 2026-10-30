NUMS = [1, 3, 2, 5, 4]
K = 4


def _cost(S):
    return (S['nums'][S['max_q'][0]] - S['nums'][S['min_q'][0]]) * (S['right'] - S['left'] + 1)


def _info(S):
    if 'right' not in S or not S.get('max_q') or not S.get('min_q'):
        return ''
    mx, mn = S['nums'][S['max_q'][0]], S['nums'][S['min_q'][0]]
    c = (mx - mn) * (S['right'] - S['left'] + 1)
    ok = '≤' if c <= K else '>'
    return f"窗口 [{S['left']}, {S['right']}]：`({mx} − {mn}) × {S['right'] - S['left'] + 1}` = =={c}== {ok} k={K}"


CONFIG = dict(
    num=3835, title='开销小于等于 K 的子数组数目', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='滑窗 + 双单调队列',
    tags=['常用数据结构', '难度分 1759'],
    code='''
class Solution:
    def countSubarrays(self, nums: List[int], k: int) -> int:
        min_q = deque()
        max_q = deque()
        ans = left = 0
        for right, x in enumerate(nums):
            # 1. 入：元素进入窗口
            while min_q and x <= nums[min_q[-1]]:
                min_q.pop()
            min_q.append(right)

            while max_q and x >= nums[max_q[-1]]:
                max_q.pop()
            max_q.append(right)

            # 2. 出：如果窗口不满足要求，左端点离开窗口
            # 只需改下面这行代码，其余逻辑和 2762 题完全一致
            while (nums[max_q[0]] - nums[min_q[0]]) * (right - left + 1) > k:
                left += 1
                if min_q[0] < left:
                    min_q.popleft()
                if max_q[0] < left:
                    max_q.popleft()

            # 3. 更新答案
            ans += right - left + 1
        return ans
''',
    call=f'Solution().countSubarrays({NUMS}, {K})',
    expect=8,
    views=[
        dict(type='text', size=26, h=55, fn=_info),
        dict(type='array', var='nums', label='nums', pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), h=200,
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right'])),
        dict(type='queue', var='max_q', label='max_q（下标:值，队首 = 窗口最大）', fmt=lambda i: f'{i}:{NUMS[i]}', h=110),
        dict(type='queue', var='min_q', label='min_q（下标:值，队首 = 窗口最小）', fmt=lambda i: f'{i}:{NUMS[i]}', h=110),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('x', 'x', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'min_q = deque()': '`min_q` 存下标，值从队首到队尾==严格递增==，队首就是窗口最小值',
        'max_q = deque()': '`max_q` 存下标，值从队首到队尾==递减==，队首就是窗口最大值',
        'ans = left = 0': '`ans` 统计合法子数组数，`left` 是窗口左端点',
        'for right, x': lambda S, B, r: ('`nums` 枚举完了，循环结束' if B.get('right') == S.right
                                          else f'枚举右端点 `right = {S.right}`，新元素 `x = {S.x}` 进窗口'),
        'while min_q and x <= nums[min_q[-1]]': lambda S, B, r: (
            f'队尾 `{S.nums[S.min_q[-1]]} ≥ x = {S.x}` → 它比 x 更靠左又不更小，永远当不了最小值，弹出'
            if S.min_q and S.x <= S.nums[S.min_q[-1]] else '队尾比 `x` 小（或队列空）→ 停止弹出'),
        'min_q.pop()': '弹出 `min_q` 队尾',
        'min_q.append(right)': '`right = {right}` 入 `min_q`，保持队列单调',
        'while max_q and x >= nums[max_q[-1]]': lambda S, B, r: (
            f'队尾 `{S.nums[S.max_q[-1]]} ≤ x = {S.x}` → 它又早又小，永远当不了最大值，弹出'
            if S.max_q and S.x >= S.nums[S.max_q[-1]] else '队尾比 `x` 大（或队列空）→ 停止弹出'),
        'max_q.pop()': '弹出 `max_q` 队尾',
        'max_q.append(right)': '`right = {right}` 入 `max_q`，保持队列单调',
        'while (nums[max_q[0]]': lambda S, B, r: (
            f'开销 `({S.nums[S.max_q[0]]} − {S.nums[S.min_q[0]]}) × {S.right - S.left + 1}` = =={_cost(S)}== '
            + (f'> k={S.k} → 窗口太大，要缩小' if _cost(S) > S.k else f'≤ k={S.k} → 窗口合法')),
        'left += 1': '开销超了：==窗口越短开销越小==，`left` 右移到 `{left}`',
        'if min_q[0] < left': lambda S, B, r: (f'`min_q` 队首下标 `{S.min_q[0]}` < left → 已离开窗口，出队' if S.min_q[0] < S.left
                                                  else f'`min_q` 队首下标 `{S.min_q[0]}` 还在窗口内，保留'),
        'min_q.popleft()': '`min_q` 队首出队',
        'if max_q[0] < left': lambda S, B, r: (f'`max_q` 队首下标 `{S.max_q[0]}` < left → 已离开窗口，出队' if S.max_q[0] < S.left
                                                  else f'`max_q` 队首下标 `{S.max_q[0]}` 还在窗口内，保留'),
        'max_q.popleft()': '`max_q` 队首出队',
        'ans += right - left + 1': '以 `right` 结尾、左端点在 `[left, right]` 的子数组全部合法：`+{right - left + 1}` → ans = =={ans}==',
        'return ans': '共有 `{ret}` 个开销 ≤ k 的子数组',
    },
    max_steps=110,
    cards=dict(
        one_liner='越短越合法：右端点右移，窗口超标就缩左端点',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['子数组开销 = `(最大值 − 最小值) × 长度`，数有多少个子数组开销 `≤ k`',
                 '示例：`nums = [1,3,2], k = 4` → `5`',
                 '本视频：`nums = [1,3,2,5,4], k = 4` → `8`'],
        quote='本题只需把 2762 题的 while 循环条件改成 `(nums[maxQ[0]] - nums[minQ[0]]) * (right - left + 1) > k` 即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['套 2762 的模板：枚举右端点 `right`，维护合法的最小 `left`',
              '两个单调队列：`max_q` 取窗口最大、`min_q` 取窗口最小，队首即答案',
              '「入 → 出 → 更新答案」三步；子数组越短开销越小，所以合法性具有单调性',
              '`ans += right - left + 1`：以 `right` 结尾的合法子数组个数'],
        summary=['时间 `O(n)`：每个元素最多入队出队各两次（两个队列）',
                 '队列存==下标==而不是值，才能判断队首是否已离开窗口',
                 '出窗口判断是 `min_q[0] < left`，且 max/min 两个队列都要判断',
                 '用 `>` 缩窗：条件变了只改循环条件，其余同 2762；对照 yiduobo 的「left 固定、右端点往外扩」',
                 '原文可直接运行，无改动'],
    ),
)
