def _oi(S):
    """外层循环的 i（进入 strictlyIncreasing 后 i 会被内层同名参数遮住，这里从 nums 重新找第一处逆序）"""
    nums = S['nums']
    for k in range(1, len(nums)):
        if nums[k - 1] >= nums[k]:
            return k
    return S.get('i') if 'a' not in S else None


CONFIG = dict(
    num=1909, title='删除一个元素使数组严格递增', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='找第一处逆序 · 两个都试删（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def canBeIncreasing(self, nums: List[int]) -> bool:
        for i in range(1, len(nums)):
            if nums[i - 1] >= nums[i]:
                return self.strictlyIncreasing(nums, i - 1) or self.strictlyIncreasing(nums, i)
        return True

    def strictlyIncreasing(self, a: List[int], i: int) -> bool:
        a = a[:i] + a[i + 1:]
        return all(a[j - 1] < a[j] for j in range(1, len(a)))
''',
    call='Solution().canBeIncreasing([5,6,1,7,8])',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: (f"从左往右扫：`nums[{S['i']-1}] = {S['nums'][S['i']-1]}`，`nums[{S['i']}] = {S['nums'][S['i']]}`" if S['_line'] <= 4 and 'a' not in S else (f"第一处不递增：下标 `{_oi(S)-1}` 和 `{_oi(S)}`，删掉其中一个" if _oi(S) else '')), size=26),
        dict(type='array', var='nums', label='nums（蓝 = i-1，粉 = i）', h=240,
             color=lambda S, k, v: ('blue' if k == _oi(S) - 1 else 'pink' if k == _oi(S) else None) if _oi(S) else None),
        dict(type='array', var='a', label='删掉一个数之后的 a（黄框 = 相邻已递增）', h=240,
             color=lambda S, k, v: 'green' if S['_line'] >= 10 and k > 0 and S['a'][k-1] < v else None),
    ],
    watch=[('第一处逆序的 i', 'next((k for k in range(1, len(nums)) if nums[k-1] >= nums[k]), None)', 'pink')],
    captions={
        'for i in range(1': '`i = {i}`：看相邻的 `nums[{i-1}]` 和 `nums[{i}]`',
        'if nums[i - 1] >= nums[i]': lambda S, B, ret: (f"`{S.nums[S.i-1]} >= {S.nums[S.i]}` → ==不严格递增==，这两个数必须删掉一个" if S.nums[S.i-1] >= S.nums[S.i] else f"`{S.nums[S.i-1]} < {S.nums[S.i]}` → 还是递增，继续往右"),
        'return self.strictlyIncreasing(nums, i - 1) or': '这对数里必须删一个：先试删左边那个，不行再试删右边那个，有一个行就返回 True',
        'a = a[:i] + a[i + 1:]': '删掉下标 `{i}` 的元素，得到 `{a}`',
        'return all(': lambda S, B, ret: (f"剩下的数相邻都满足 `a[j-1] < a[j]` → ==严格递增== → 返回 True" if ret else "剩下的数里还有相邻逆序 → 这样删不行"),
        'return True': '整个数组本来就严格递增，返回 `True`',
    },
    cards=dict(
        one_liner='只看第一处逆序，两个数各删一次试试',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['恰好删除一个元素，使数组==严格递增==，能就返回 `true`',
                 '本身已严格递增也算 `true`',
                 '示例：`[1,2,10,5,7]` → `true`；`[2,3,1,2]` → `false`'],
        quote='遍历数组 nums，如果中途遇到了 nums[i-1] >= nums[i] 的情况，则肯定要删除这两个元素中的一个，各尝试删除检查一遍即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从左往右扫，第一次遇到 `nums[i-1] >= nums[i]`，这对数里必须删一个',
              '在原数组里分别删掉下标 `i-1`、`i`，各检查一遍是否严格递增',
              '没遇到逆序，数组本来就递增，直接 `true`'],
        result='先删 `6` 得 `[5,1,7,8]` 不行；再删 `1` 得 `[5,6,7,8]` ✓ → True',
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`sort.SliceIsSorted` 对应 “相邻严格递增”的检查）',
                 '时间 `O(n)`，空间 `O(n)`（切片拷贝）',
                 '易错：必须是==严格==递增，相等也算逆序',
                 '遇到第一处逆序就返回：后面哪怕还有逆序，检查时自然会发现'],
    ),
)
