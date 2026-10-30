def _bits(v, w=4):
    return format(v, '0%db' % w)


def _info(S):
    if 'x' not in S:
        return ''
    i, x = S['i'], S['x']
    nums = S['nums']
    if 'j' in S and S['_line'] in (8, 9, 10, 11) and S['j'] < i:
        j = S['j']
        return f"`x = {_bits(x)}`　`nums[{j}] = {_bits(nums[j])}`　OR = `{_bits(nums[j] | x)}`"
    return f"`x = nums[{i}] = {_bits(x)}`（二进制）"


CONFIG = dict(
    num=3171, title='找到按位或最接近 K 的子数组', difficulty='Hard', category='位运算',
    author='灵茶山艾府', technique='LogTrick · 或值只增不减',
    tags=['灵神题单'],
    code='''
class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        ans = inf
        for i, x in enumerate(nums):
            ans = min(ans, abs(x - k))
            for j in range(i - 1, -1, -1):
                # 只需增加一个判断条件：如果 x 是 nums[j] 的子集，退出循环
                if nums[j] | x == nums[j]:
                    break
                nums[j] |= x
                ans = min(ans, abs(nums[j] - k))
        return ans
''',
    call='Solution().minimumDifference([1,2,1,4,1,3], 6)',
    expect=1,
    views=[
        dict(type='text', fn=_info, size=30, h=60),
        dict(type='array', var='nums', pointers={'i': 'blue', 'j': 'pink'}, window=None, h=240, label='nums（原地改成「以 i 结尾的子数组或值」）',
             color=lambda S, idx, v: ('blue' if idx == S.get('i') else 'pink' if S['_line'] in (8, 9, 10, 11) and idx == S.get('j') else None)),
        dict(type='text', fn=lambda S: f"`k = {S['k']}`　当前最小差 ans = =={S['ans'] if S['ans'] != float('inf') else '∞'}==" if 'ans' in S else '', size=28, h=60),
    ],
    watch=['i', 'x', 'j', ('k', 'k', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = inf': '答案先设成无穷大，之后不断取最小',
        'for i, x in enumerate': lambda S, B, r: (f'`i = {S.i}`：计算右端点为 `{S.i}` 的所有子数组的或值' + (f'，`j` 从 `{S.i-1}` 往左并入 `x`' if S.i else '，左边没有元素') if S.get('i') != B.get('i') else '枚举结束'),
        'ans = min(ans, abs(x - k))': '单个元素也是子数组：`|{x} − {k}| = {abs(x-k)}`，`ans` = {ans}',
        'break': '退出内层循环：`nums[{j}]` 及更左的元素都不用再改了',
        'if nums[j] | x == nums[j]': lambda S, B, r: (f'`nums[{S.j}] | x = {S.nums[S.j]}` 等于它自己 → ==x 已是子集==，再往左也不会变，退出内层循环' if S.nums[S.j] | S.x == S.nums[S.j]
                                                   else f'`{_bits(S.nums[S.j])} | {_bits(S.x)} = {_bits(S.nums[S.j] | S.x)}` ≠ 原值 → 或值会增大，继续并入'),
        'nums[j] |= x': '`nums[{j}]` 增大为 `{nums[j]}`：它现在表示 `[{j}..{i}]` 的或值',
        'ans = min(ans, abs(nums[j] - k))': '`[{j}..{i}]` 的或值 `{nums[j]}`，差 `{abs(nums[j]-k)}`，`ans` = {ans}',
        'return ans': '所有子数组的或值都看过了，最小差 `{ans}`',
    },
    skip=['for j in range'],
    max_steps=90,
    cards=dict(
        one_liner='或值只增不减：x 已是子集就停，每个数最多增大约 30 次',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['在 `nums` 中选连续子数组，使「所有元素按位或」与 `k` 的差绝对值最小',
                 '示例：`nums=[1,3,1,3], k=2` → `1`',
                 '本视频：`[1,2,1,4,1,3], k=6` → `1`'],
        quote='如果 $A_i$ 已经是 $A_j$ 的子集，那么 $A_i$ 必然也是更左边的 $A_0,A_1,\\cdots,A_{j-1}$ 的子集……并入操作不会改变这些集合。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把二进制数看成集合，OR 就是并集；内层循环结束时 `A0 ⊇ A1 ⊇ … ⊇ Ai`',
              '`nums[j] | x == nums[j]` 说明 x 是子集，左边全都不会变 → ==直接 break==',
              '每个数至多从 1 个元素的集合长到 30 个元素，总循环 `O(n log U)`'],
        after=[dict(heading='另一种写法：滑动窗口 + 栈', lines=[
            '或值随窗口变长而增大，可用滑窗',
            '但 OR 没有逆运算，左端点离开时要用「栈」存后缀或值',
            '本视频演示 LogTrick；两种写法都是 `O(n)` ~ `O(n log U)`'])],
        summary=['时间 `O(n log U)`，空间 `O(1)`（原地改 nums）',
                 '易错：单个元素也是子数组，先 `ans = min(ans, abs(x-k))`',
                 '易错：`break` 的条件是 `nums[j] | x == nums[j]`，不是 `x` 等于它',
                 '同类题：1521（AND）、3097、2411，见位运算题单 LogTrick'],
    ),
)
