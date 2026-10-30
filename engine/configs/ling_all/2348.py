CONFIG = dict(
    num=2348, title='全 0 子数组的数目', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='越短越合法 · 记录上个非 0 位置',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1316'],
    code='''
class Solution:
    def zeroFilledSubarray(self, nums: List[int]) -> int:
        ans = 0
        last = -1
        for i, x in enumerate(nums):
            if x:
                last = i  # 记录上一个非 0 元素的位置
            else:
                ans += i - last
        return ans
''',
    call='Solution().zeroFilledSubarray([1,3,0,0,2,0,0,4])',
    expect=6,
    views=[
        dict(type='array', var='nums', pointers={'last': 'pink', 'i': 'blue'}, h=300,
             window=('last+1', 'i'),
             color=lambda S, i, v: 'pink' if 'last' in S and i == S['last'] and v != 0 else None),
        dict(type='text', h=120, fn=lambda S: f"右端点 `i = {S['i']}`：左端点可取 `last+1 … i`，共 `{S['i']} − ({S['last']}) = {S['i']-S['last']}` 个" if 'i' in S and S['nums'][S['i']] == 0 else ''),
    ],
    watch=['i', ('last', 'last', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累计全 0 子数组的个数',
        'last = -1': '`last` 记录上一个非 0 元素的位置；一开始没有，设为 -1 才能兼容开头就是 0 的情况',
        'if x': lambda S, B, r: (f'`nums[{S.i}] = {S.x}` 非 0 → 任何包含它的子数组都不合法' if S.x else f'`nums[{S.i}] = 0` → 可以作为全 0 子数组的右端点'),
        'last = i': '窗口左端点被推到它后面：`last = {last}`，窗口从 `{last + 1}` 开始',
        'ans += i - last': '右端点为 `{i}`，左端点可以是 `{last + 1}…{i}`，共 `{i} − {last}` = =={i - last}== 个 → `ans = {ans}`',
        'return ans': '所有右端点都统计完，一共 =={ret}== 个全 0 子数组',
    },
    cards=dict(
        one_liner='枚举右端点，左端点只能在上一个非 0 之后',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定整数数组 `nums`，统计全为 0 的连续子数组个数',
                 '示例：`[1,3,0,0,2,0,0,4]` → `6`'],
        quote='记录上一个非零数字的位置 last。那么 last+1 就是窗口的左端点。当子数组右端点在 i 时，子数组左端点可以是 last+1,last+2,…,i，一共有 i-last 个，加入答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['属于「越短越合法」型滑动窗口：右端点右移，左端点只会不动或右移',
              '遇到非 0，窗口整体越过它：`last = i`',
              '遇到 0，以它为右端点的合法子数组有 `i - last` 个，直接累加'],
        after=[dict(heading='另一种写法：增量法', lines=['`cnt0` 统计连续 0 的个数', '每多一个 0，右端点为 i 的子数组比 i-1 多一个', '把 `cnt0` 加到答案里，遇非 0 清零'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`last` 初值 -1，才能处理 `[0,0,0,...]` 开头就是 0 的情况',
                 '只在 `nums[i] == 0` 时累加，非 0 只更新 `last`',
                 '同类题：1513 仅含 1 的子串数、413 等差数列划分'],
    ),
)
