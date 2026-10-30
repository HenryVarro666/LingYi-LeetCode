NUMS = [0, 1, 1, 1, 0, 1, 1, 0, 1]


def _color(S, i, v):
    if 'right' in S and S['left'] <= i <= S['right'] and v == 0:
        return 'red' if S['cnt0'] > 1 else 'orange'
    return None


CONFIG = dict(
    num=1493, title='删掉一个元素以后全为 1 的最长子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='不定长滑窗：至多一个 0',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        ans = cnt0 = left = 0
        for right, x in enumerate(nums):
            # 1. 入，nums[right] 进入窗口
            cnt0 += 1 - x  # 维护窗口中的 0 的个数
            while cnt0 > 1:  # 不符合题目要求
                # 2. 出，nums[left] 离开窗口
                cnt0 -= 1 - nums[left]  # 维护窗口中的 0 的个数
                left += 1
            # 3. 更新答案，注意不是 right-left+1，因为我们要删掉一个数
            ans = max(ans, right - left)
        return ans
''',
    call=f'Solution().longestSubarray({NUMS})',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums（框 = 窗口，橙 = 窗口里的 0，红 = 多出来的 0）', h=260,
             pointers={'left': 'pink', 'right': 'blue'}, window=('left', 'right'), color=_color),
        dict(type='text', h=90, size=28,
             fn=lambda S: (f"窗口长 `{S['right'] - S['left'] + 1}`，含 `{S['cnt0']}` 个 0 → 删一个数后长 =={S['right'] - S['left']}=="
                           if 'right' in S else '删除前的子数组==至多有一个 0==')),
    ],
    watch=[('left', 'left', 'pink'), ('right', 'right', 'blue'), ('x', 'x'), ('cnt0', 'cnt0', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = cnt0 = left = 0': '`cnt0`：窗口中 0 的个数；`left`：窗口左端点',
        'for right, x in': lambda S, B, r: ('遍历结束' if B.get('right') == S.right else f'右端点 `right = {S.right}`，`x = {S.x}`'),
        'cnt0 += 1 - x': lambda S, B, r: (f'`x = 0` 进入窗口 → `cnt0 = {S.cnt0}`' if S.x == 0 else f'`x = 1` 进入窗口，`cnt0` 不变 = {S.cnt0}'),
        'while cnt0 > 1': lambda S, B, r: (f'`cnt0 = {S.cnt0} > 1`：两个 0 ==删不完==，窗口不合法' if S.cnt0 > 1
                                           else f'`cnt0 = {S.cnt0} ≤ 1`：删掉这个 0（或一个 1）后全是 1，合法'),
        'cnt0 -= 1 - nums[left]': lambda S, B, r: (f'`nums[{S.left}] = 0` 离开窗口 → `cnt0 = {S.cnt0}`' if S.nums[S.left] == 0
                                                   else f'`nums[{S.left}] = 1` 离开窗口，`cnt0` 不变'),
        'left += 1': '缩小窗口：`left` → {left}',
        'ans = max': '删掉一个数后长 `right − left = {right - left}` → `ans = {ans}`',
        'return ans': '最长 =={ans}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='删除后全是 1 ⇔ 删除前==至多一个 0==',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制数组 `nums` ==必须删掉一个元素==，求删除后最长的全 1 子数组长度',
                 '示例：`[1,1,0,1]` → `3`；`[1,1,1]` → `2`（必须删一个）',
                 '本视频：`[0,1,1,1,0,1,1,0,1]` → `5`'],
        quote='删除后，子数组只有 1，也就是没有 0。那么删除之前呢？至多有一个 0。所以问题相当于：求最长子数组的长度（减一），满足子数组==至多有一个 0==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['子数组越长 0 越多 → 右端点增大，左端点只会右移，符合滑窗',
              '三步：==入==（维护 cnt0）→ ==出==（cnt0 > 1 时缩左端点）→ ==更新答案==',
              '必须删一个数，所以答案用 `right − left` 而不是 `+1`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：全是 1 时也必须删一个 → `right − left` 自动处理',
                 '`1 − x` 把 “是不是 0” 写成 0/1，省掉 if',
                 '推广：至多 k 个 0 → 1004. 最大连续 1 的个数 III'],
    ),
)
