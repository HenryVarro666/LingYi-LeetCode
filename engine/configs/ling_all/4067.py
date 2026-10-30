def _txt(S):
    if 'left' not in S:
        return ''
    if 'i' not in S:
        return '`cnt[v]`：窗口里「两数之和 = v」与「两数之差 = v」的对数之和'
    i, left = S['i'], S['left']
    return f'窗口 `[{left}, {i}]`：长度 =={i - left + 1}==；答案 `ans` = =={S["ans"]}=='


CONFIG = dict(
    num=4067, title='数对和受限的最长子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='滑动窗口 · 维护两数之和/差计数', tags=[],
    code='''
class Solution:
    def maxSubarray(self, nums: list[int]) -> int:
        mx = max(nums)
        cnt = [0] * (mx * 2 + 1)
        ans = left = 0

        # 枚举有效子数组的右端点为 i，那么左端点 left 最小是多少？
        for i, x in enumerate(nums):
            # x 进入窗口前，先判断：
            # 如果窗口中有两数之和等于 x，或者两数之差等于 x，那么必须缩小窗口
            while cnt[x] > 0:
                y = nums[left]
                left += 1
                for z in nums[left: i]:
                    cnt[y + z] -= 1
                    cnt[abs(y - z)] -= 1

            # x 进入窗口
            for y in nums[left: i]:
                cnt[x + y] += 1
                cnt[abs(x - y)] += 1

            # 用子数组 [left, i] 的长度更新答案的最大值
            ans = max(ans, i - left + 1)

        return ans
''',
    call='Solution().maxSubarray([2,3,5,3,2,1])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（框 = 窗口 [left, i]）', pointers={'left': 'blue', 'i': 'pink'},
             window=('left', 'i'), h=200),
        dict(type='array', var='cnt', label='cnt[v]：窗口内 两数之和 = v 与 两数之差 = v 的对数', pointers={'x': 'yellow'}, h=230,
             cell=70, color=lambda S, i, v: 'orange' if v > 0 else None),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    skip=['for z in nums[left: i]', 'for y in nums[left: i]'],
    max_steps=100,
    watch=[('left', 'left', 'blue'), ('i', 'i', 'pink'), ('x', 'x', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'cnt = [0]': '`cnt[v]` 合并记录窗口内「和为 v」「绝对差为 v」的数对个数，最大和是 `2 × mx`',
        'for i, x in enumerate': lambda S, B, r: ('右端点都枚举完了，循环结束' if 'i' in B and B['i'] == S['i'] else f'枚举右端点 `i = {S.i}`，新元素 `x = {S.x}`，先看它能不能进窗口'),
        'while cnt[x] > 0': lambda S, B, r: (
            f'`cnt[{S.x}] = {S.cnt[S.x]} > 0`：窗口里有两数之和或之差等于 {S.x} → ==x 进来就会无效==，必须缩小窗口'
            if S.cnt[S.x] > 0 else f'`cnt[{S.x}] = 0`：窗口里凑不出 {S.x} → 可以进入'),
        'y = nums[left]': '要移出的元素 `y = nums[{left}] = {y}`',
        'left += 1': '`left` → {left}：窗口缩小',
        'cnt[y + z] -= 1': '`y` 离开：它和窗口里 `z = {z}` 的和 `{y + z}` 少了一对 → `cnt[{y + z}]` = {cnt[y + z]}',
        'cnt[abs(y - z)] -= 1': '同时它和 `z` 的差 `{abs(y - z)}` 也少了一对 → `cnt[{abs(y - z)}]` = {cnt[abs(y - z)]}',
        'cnt[x + y] += 1': '`x` 进窗口：和 `y = {y}` 的和 `{x + y}` 多了一对 → `cnt[{x + y}]` = {cnt[x + y]}',
        'cnt[abs(x - y)] += 1': '差 `{abs(x - y)}` 也多一对 → `cnt[{abs(x - y)}]` = {cnt[abs(x - y)]}',
        'ans = max': '窗口 `[{left}, {i}]` 有效，长度 `{i - left + 1}`：`ans = max({B.ans}, {i - left + 1}) = {ans}`',
        'return ans': '最长有效子数组长度 =={ans}==',
    },
    cards=dict(
        one_liner='越长越容易出现 a+b=c，所以滑动窗口：新数进来前先查它会不会造成冲突',
        complexity='时间 `O(n^2 + U)`，空间 `O(U)`',
        problem=['子数组里不能有三个不同下标满足 `nums[i] + nums[j] == nums[k]`，求最长的有效子数组',
                 '示例：`[2,3,5,3,2,1]` → `3`（`[3,5,3]`）'],
        quote='子数组越长，元素越多，越容易满足 nums[i] + nums[j] = nums[k]。反之，子数组越短，元素越少，越难满足上式。有这样的性质，可以用滑动窗口解决。',
        quote_src='—— 灵茶山艾府题解',
        idea=['新元素 x 要么当「和」k：窗口里有两数之和 = x；要么当加数 i/j：窗口里有两数之差 = x',
              '`cnt[v]` 记录窗口内和为 v、差为 v 的对数，进出窗口时各更新一遍',
              '`cnt[x] > 0` 就左移 `left`，直到 x 能放进来'],
        summary=['时间 `O(n^2 + U)`：`left` 只增不减，每个元素最多进出一次，各花 `O(n)` 维护 `cnt`',
                 '易错：差要取绝对值；和最大可达 `2 × max`，数组要开 `2mx + 1`',
                 '写法一把和/差拆成 `cnt_s`、`cnt_d` 两个数组，写法二合并成一个 `cnt`（本视频）',
                 '这是 3Sum 的形式（x + y - z = 0），目前没有 `O(n^(2-ε))` 的算法'],
    ),
)
