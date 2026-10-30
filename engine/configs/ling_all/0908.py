CONFIG = dict(
    num=908, title='最小差值 I', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='最大最小值 · 一行公式',
    code='''
class Solution:
    def smallestRangeI(self, nums: List[int], k: int) -> int:
        return max(max(nums) - min(nums) - k * 2, 0)
''',
    call='Solution().smallestRangeI([4,1,9,6,3], 2)',
    expect=4,
    views=[
        dict(type='text', size=34, fn=lambda S: f"最大 `{max(S['nums'])}` − 最小 `{min(S['nums'])}` = =={max(S['nums'])-min(S['nums'])}==；最多缩小 `2k = {2*S['k']}`" if 'nums' in S else ''),
        dict(type='array', var='nums', h=240,
             color=lambda S, i, v: 'pink' if v == max(S['nums']) else 'blue' if v == min(S['nums']) else None),
        dict(type='text', size=34, fn=lambda S: f"答案 = max(`{max(S['nums'])-min(S['nums'])} − {2*S['k']}`, 0) = ==" + str(max(max(S['nums'])-min(S['nums'])-2*S['k'], 0)) + "==" if 'nums' in S else ''),
    ],
    watch=['k', ('max', 'max(nums)', 'pink'), ('min', 'min(nums)', 'blue')],
    captions={
        'return max': '最大值 `{max(nums)}` 往下降 `k`、最小值 `{min(nums)}` 往上升 `k`，差最多缩小 `2k = {k*2}`：`{max(nums)} - {min(nums)} - {k*2} = {max(nums)-min(nums)-k*2}`；差不能为负，和 0 取最大 → =={ret}==',
    },
    cards=dict(
        before=[dict(heading='先看例子', lines=['`[0,10], k = 2`：最大 10 降到 8，最小 0 升到 2', '差 `10 - 0 = 10` 缩成 `8 - 2 = 6`，正好少了 `2k = 4]'.replace('4]','4`')])],
        after=[dict(heading='为什么公式成立', lines=['其他数夹在最大最小之间，调整最大/最小时不会越界', '`max - min <= 2k`：两头可以碰到一起，甚至全变成同一个数 → 答案 0', '`max - min > 2k`：两头各走满 k 步仍有空隙 → 答案 `max - min - 2k`'])],
        one_liner='只看最大和最小：各向中间走 k 步，差最多缩 2k',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每个数最多可以加上 `[-k, k]` 内的任意整数一次',
                 '分数 = 数组最大值 − 最小值，求操作后的最小分数',
                 '示例：`nums = [0,10], k = 2` → `6`；本视频：`[4,1,9,6,3], k = 2` → `4`'],
        quote='`max(max(nums) - min(nums) - k * 2, 0)`',
        quote_src='—— 灵茶山艾府题解代码',
        idea=['分数只由最大值和最小值决定，其余数字可以无视',
              '最大值减 `k`、最小值加 `k`，差最多缩小 `2k`',
              '若差 ≤ `2k`，可以全部变成同一个数，分数为 0'],
        summary=['时间 `O(n)`（求 max/min），空间 `O(1)`',
                 '易错点：差小于 `2k` 时结果不能为负，要和 `0` 取最大',
                 '思考题：至多操作 `m` 次时，只有最大/最小的几个数值得动，需要排序后分类讨论'],
    ),
)
