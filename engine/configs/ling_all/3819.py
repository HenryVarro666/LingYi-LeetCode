CONFIG = dict(
    num=3819, title='非负元素轮替', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='取出非负数 + 双指针填回（j 从 k 起）', tags=[],
    code='''
class Solution:
    def rotateElements(self, nums: List[int], k: int) -> List[int]:
        # 取出非负数
        a = [x for x in nums if x >= 0]
        m = len(a)

        # 双指针，把 a 填入 nums，跳过负数
        j = k
        for i, x in enumerate(nums):
            if x >= 0:
                nums[i] = a[j % m]
                j += 1
        return nums
''',
    call='Solution().rotateElements([5,4,-9,6,2], 2)',
    expect=[6, 2, -9, 5, 4],
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue'}, label='nums', h=220,
             color=lambda S, k, v: 'red' if v < 0 else None),
        dict(type='array', var='a', pointers={'j % m': 'pink'}, label='a（非负数）', h=220),
    ],
    watch=['k', 'm', 'j', 'i', 'x'],
    captions={
        'a = [x for': '取出所有非负数，保持顺序：`a = {a}`',
        'm = len(a)': '非负数共 `m = {m}` 个',
        'j = k': '不用真的轮替：向左转 `k` 位后的第一个数就是 `a[k]`，所以 `j` 从 `k = {k}` 开始',
        'for i, x in enumerate': lambda S, B, r: f'看 `nums[{S.i}] = {S.x}`',
        'if x >= 0': lambda S, B, r: (f'`{S.x} >= 0` → 非负，这个位置要被覆盖' if S.x >= 0 else f'`{S.x}` 是负数 → ==原地不动==，跳过'),
        'nums[i] = a[j % m]': '`nums[{i}]` 填 `a[{j} % {m}] = a[{j % m}]` = =={nums[i]}==（`% m` 实现循环）',
        'j += 1': '`j` → {j}，下一个非负位置取 `a` 里的下一个数',
        'return nums': '处理后的数组 =={ret}==',
    },
    cards=dict(
        one_liner='非负数轮替 = 填回时把读指针从 k 开始，并对 m 取模',
        complexity='时间 `O(n)`，空间 `O(m)`，`m` 为非负数个数',
        problem=['非负数按顺序向左循环轮替 `k` 位，负数位置不动', '轮替后的非负数依次填回原来非负的位置', '示例：`[5,4,-9,6], k=2` → `[6,5,-9,4]`；本视频：`[5,4,-9,6,2], k=2`'],
        quote='无需轮替，直接把双指针的 j 初始化成 k，即 a 轮替后的第一个数。',
        quote_src='—— 灵茶山艾府题解 写法二',
        idea=['`a` 是非负数的列表，长度 `m`', '向左轮替 `k` 位后，第一个数是 `a[k % m]`', '遍历 `nums`，遇到非负位置就读 `a[j % m]` 并让 `j` 加一，负数位置直接跳过'],
        summary=['时间 `O(n)`，空间 `O(m)`', '易错点：`m` 可能为 0，但这时 `nums` 里没有非负数，不会进入 `a[j % m]`', '`k` 可能大于 `m`，所以要取模',
                 '写法一：先 `k %= len(a)`，`a = a[k:] + a[:k]` 真的轮替，再双指针填回；写法二省掉了轮替'],
    ),
)
