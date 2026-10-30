def _cnt(S):
    return max(min(S['min_i'], S['max_i']) - S['i0'], 0)


CONFIG = dict(
    num=2444, title='统计定界子数组的数目', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='枚举右端点 · 三个位置', tags=['三指针', '难度分 2093'],
    code='''
class Solution:
    def countSubarrays(self, nums: List[int], minK: int, maxK: int) -> int:
        ans = 0
        min_i = max_i = i0 = -1
        for i, x in enumerate(nums):
            if x == minK:
                min_i = i  # 最近的 minK 位置
            if x == maxK:
                max_i = i  # 最近的 maxK 位置
            if not minK <= x <= maxK:
                i0 = i  # 子数组不能包含 nums[i0]
            ans += max(min(min_i, max_i) - i0, 0)
        return ans
''',
    call='Solution().countSubarrays([1,3,5,2,7,5,1,5,4], 1, 5)',
    expect=7,
    views=[
        dict(type='text', size=30, fn=lambda S: (f"以 `i={S['i']}` 结尾：左端点 `[{S['i0'] + 1}, {min(S['min_i'], S['max_i'])}]` → ==`{_cnt(S)}`== 个" if 'i' in S and S['_line'] >= 12 else f"找 minK=`{S['minK']}` 和 maxK=`{S['maxK']}` 都出现、且没有越界数的子数组")),
        dict(type='array', var='nums', h=320, pointers={'i': 'green', 'min_i': 'cyan', 'max_i': 'orange', 'i0': 'red'},
             window=('i0 + 1', 'min(min_i, max_i)'),
             color=lambda S, idx, v: ('red' if not S['minK'] <= v <= S['maxK'] else 'cyan' if v == S['minK'] else 'orange' if v == S['maxK'] else None) if 'minK' in S else None,
             dim=lambda S, idx, v: 'i' in S and idx > S['i']),
    ],
    watch=[('i', 'i', 'green'), ('min_i', 'min_i', 'cyan'), ('max_i', 'max_i', 'orange'), ('i0', 'i0', 'red'), ('ans', 'ans', 'green')],
    captions={
        'min_i = max_i = i0': '三个位置都设为 -1：`min_i` 最近的 minK，`max_i` 最近的 maxK，`i0` 最近的越界元素',
        'for i, x in enumerate': '枚举子数组右端点 `i = {i}`，`x = {x}`',
        'if x == minK': lambda S, B, r: (f'`{S.x} == minK`：刷新最近的 minK 位置 → `min_i = {S.i}`' if S.x == S.minK else f'`{S.x} != minK`，`min_i` 不变（{S.min_i}）'),
        'if x == maxK': lambda S, B, r: (f'`{S.x} == maxK`：刷新最近的 maxK 位置 → `max_i = {S.i}`' if S.x == S.maxK else f'`{S.x} != maxK`，`max_i` 不变（{S.max_i}）'),
        'if not minK <= x <= maxK': lambda S, B, r: (f'`{S.x}` 不在 `[{S.minK}, {S.maxK}]` 内：任何包含它的子数组都不合法 → `i0 = {S.i}`' if not S.minK <= S.x <= S.maxK else f'`{S.x}` 在范围内，`i0` 不变（{S.i0}）'),
        'ans += max': '左端点要在 `[i0+1, min(min_i, max_i)]`：`min({min_i}, {max_i}) - ({i0}) = {min(min_i, max_i) - i0}`，负数当 0 → 加 `{max(min(min_i, max_i) - i0, 0)}`，`ans` = =={ans}==',
        'return ans': '共 `{ans}` 个定界子数组',
    },
    cards=dict(
        one_liner='枚举右端点：左端点在 [i0+1, min(minI,maxI)] 都合法',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['子数组最小值 `== minK` 且最大值 `== maxK` 叫定界子数组，求个数',
                 '示例：`[1,3,5,2,7,5]`，`minK=1, maxK=5` → `2`',
                 '本视频：`[1,3,5,2,7,5,1,5,4]` → `7`'],
        quote='从特殊到一般。首先考虑一个简单的情况，nums 的所有元素都在 [minK,maxK] 范围内。',
        quote_src='—— 灵茶山艾府题解',
        idea=['特殊情况：只数同时包含 minK 和 maxK 的子数组，左端点在 `[0, min(minI,maxI)]`',
              '再加一个 `i0`：最近的范围外元素，左端点必须在 `i0` 右边',
              '以 i 结尾的合法个数 `min(minI,maxI) - i0`，小于 0 时取 0'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '三个位置初始化为 -1，兼容“还没遇到”的情况',
                 '易错：差为负说明 `i0` 之后两个值没凑齐，必须取 `max(…, 0)`',
                 '灵神还给了不调用 max/min 的更快写法，思路一样',
                 '相似题：795 区间子数组个数'],
    ),
)
