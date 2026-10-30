CONFIG = dict(
    num=1574, title='删除最短的子数组使剩余数组有序', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='同向双指针（枚举右端点，移动左端点）',
    tags=['滑动窗口与双指针', '难度分 1932'],
    code='''
class Solution:
    def findLengthOfShortestSubarray(self, arr: List[int]) -> int:
        n = len(arr)
        right = n - 1
        while right and arr[right - 1] <= arr[right]:
            right -= 1
        if right == 0:  # arr 已经是非递减数组
            return 0
        # 此时 arr[right-1] > arr[right]
        ans = right  # 删除 arr[:right]
        left = 0
        while True:  # 枚举 right
            while right == n or arr[left] <= arr[right]:
                ans = min(ans, right - left - 1)  # 删除 arr[left+1:right]
                if arr[left] > arr[left + 1]:
                    return ans
                left += 1
            right += 1
''',
    call='Solution().findLengthOfShortestSubarray([1,2,3,10,4,2,3,5])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"保留 `arr[..{S['left']}]` 和 `arr[{S['right']}..]`，删掉中间 `arr[{S['left'] + 1}:{S['right']}]` 共 =={max(S['right'] - S['left'] - 1, 0)}== 个" if 'left' in S and 'right' in S and S['left'] < len(S['arr']) else (f"最长非递减后缀从 `right = {S['right']}` 开始" if 'right' in S else ''))),
        dict(type='array', var='arr', pointers={'left': 'blue', 'right': 'pink'}, h=330,
             color=lambda S, i, v: (('blue' if i == S['left'] else 'pink' if i == S['right'] else 'red' if S['left'] < i < S['right'] else None) if 'left' in S and 'right' in S else ('pink' if 'right' in S and i >= S['right'] else None))),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'right = n - 1': '先找最长的非递减后缀：`right` 从末尾开始往左',
        'while right and': lambda S, B, ret: (f'`arr[{S.right - 1}] = {S.arr[S.right - 1]}` <= `arr[{S.right}] = {S.arr[S.right]}`：还是非递减 → `right` 左移' if S.right and S.arr[S.right - 1] <= S.arr[S.right] else (f'`arr[{S.right - 1}] = {S.arr[S.right - 1]}` > `arr[{S.right}] = {S.arr[S.right]}`：后缀到此为止' if S.right else '`right` 到了 0：整个数组都是非递减')),
        'right -= 1': '`right` → {right}',
        'if right == 0': '`right` 不为 0 说明数组有逆序，必须删',
        'ans = right': '保底方案：只留后缀 `arr[{right}:]`，删前 `{right}` 个 → `ans = {right}`',
        'left = 0': '`left` 从 0 开始：保留前缀 `arr[0..left]`，它们必须是非递减的',
        'while True': '枚举 `right`：当前后缀从 `{right}` 起',
        'while right == n or': lambda S, B, ret: ('`right == n`：后缀为空，只保留前缀，一定合法' if S.right == len(S.arr) else (f'`arr[left] = {S.arr[S.left]}` <= `arr[right] = {S.arr[S.right]}`：前缀末尾 ≤ 后缀开头，==拼得起来==' if S.arr[S.left] <= S.arr[S.right] else f'`arr[left] = {S.arr[S.left]}` > `arr[right] = {S.arr[S.right]}`：拼不起来 → `right` 右移')),
        'ans = min': '删除 `arr[{left + 1}:{right}]`，长度 `{right} - {left} - 1` = {right - left - 1} → `ans = {ans}`',
        'if arr[left] > arr[left + 1]': lambda S, B, ret: (f'`arr[left] = {S.arr[S.left]}` > `arr[left+1] = {S.arr[S.left + 1]}`：前缀再往右就不是非递减了 → 结束' if S.arr[S.left] > S.arr[S.left + 1] else f'`arr[left] = {S.arr[S.left]}` <= `arr[left+1] = {S.arr[S.left + 1]}`：前缀还能延长'),
        'left += 1': '前缀多保留一个：`left` → {left}（`right` 不用回头）',
        'right += 1': '`arr[left]` 比 `arr[right]` 大，后缀的这个数不能留：删掉它，`right` → {right}',
        'return ans': '最短删除长度 `{ans}`',
    },
    cards=dict(
        one_liner='保留一段前缀和一段后缀，枚举后缀起点、前缀只增不减',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['删除一个子数组（可以为空），使剩下的元素非递减',
                 '求最短要删多长',
                 '示例：`[1,2,3,10,4,2,3,5]` → `3`（删 `[10,4,2]`）'],
        quote='枚举右端点，移动左端点：枚举 right，增大 left 直到 arr[left] > arr[right]。在增大过程中去更新子数组长度的最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['剩下的前缀、后缀各自非递减，并且前缀末尾 ≤ 后缀开头',
              '先求出最长非递减后缀，起点 `right`；`left` 从 0 起往右扩前缀',
              '`arr[left] <= arr[right]` 就能拼，每拼成一次更新答案；否则 `right` 右移丢掉一个'],
        after=[dict(heading='另一种写法', lines=['方法一：枚举 `left`，移动 `right` 直到 `arr[left] <= arr[right]`，思路对称',
                                                '变形题：改最少个数（删子序列）= `n` − 最长非递减子序列'])],
        summary=['时间 `O(n)`，内外层指针都只右移',
                 '`left`、`right` 是开区间 `(left, right)`，删除长度是 `right - left - 1`',
                 '先判断整个数组已非递减，再保证循环一定会因 `arr[left] > arr[left+1]` 结束',
                 '`right == n` 表示后缀为空，要放在 `arr[right]` 之前判断避免越界'],
    ),
)
