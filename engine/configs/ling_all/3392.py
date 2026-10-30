def _rows(S):
    n = S['nums']
    return [[n[i - 2], n[i], (n[i - 2] + n[i]) * 2, n[i - 1], '✓' if (n[i - 2] + n[i]) * 2 == n[i - 1] else '-'] for i in range(2, len(n))]


def _txt(S):
    if 'nums' not in S:
        return ''
    n = S['nums']
    k = sum((n[i - 2] + n[i]) * 2 == n[i - 1] for i in range(2, len(n)))
    return f'逐个右端点 `i = 2 … {len(n) - 1}` 检查，满足条件的共 ==' + str(k) + '== 个'


CONFIG = dict(
    num=3392, title='统计符合条件长度为 3 的子数组数目', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='枚举子数组右端点 · 一行 sum',
    tags=[],
    code='''
class Solution:
    def countSubarrays(self, nums: List[int]) -> int:
        return sum((nums[i - 2] + nums[i]) * 2 == nums[i - 1]
                   for i in range(2, len(nums)))
''',
    call='Solution().countSubarrays([1,2,1,4,1,3,1])',
    expect=1,
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='array', var='nums', label='nums', h=170, color=lambda S, k, v: None),
        dict(type='table', var=_rows, label='每个 i 的检查：a = nums[i-2]，b = nums[i-1]，c = nums[i]', h=420,
             rows=lambda S: [f'i={i}' for i in range(2, len(S['nums']))],
             cols=['a', 'c', '(a+c)×2', 'b', '符合'],
             color=lambda S, i, j, v: 'green' if v == '✓' else None),
    ],
    watch=[('len(nums)', 'len(nums)'), ('n − 2 个子数组', 'len(nums) - 2')],
    captions={
        'return sum': lambda S, B, ret: (
            '生成器表达式：`i` 从 2 到 n-1，逐个判断 `(nums[i-2] + nums[i]) * 2 == nums[i-1]`，下表列出每个 `i` 的结果；`sum` 把 `True` 当 1 累加'
            if ret is None else f'`sum` 累加所有 `True`，满足条件的子数组共 =={ret}== 个'),
        'for i in range': '生成器每次取出一个 `i`，算完一个布尔值再取下一个；取完后 `sum` 结束',
    },
    cards=dict(
        after=[dict(heading='为什么用乘法而不是除法', lines=[
            '条件是 `a + c == b / 2`，直接写除法在 Python 里会变成小数',
            '两边同乘 2：`(a + c) * 2 == b`，全程整数比较',
            '负数也成立，例如 `[-1, -2, -1]`：`(-1 + -1) * 2 = -4`，不等于 `-2`'])],
        one_liner='枚举右端点 i，判断 (首+尾)×2 是否等于中间数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数一数长度为 3 的子数组：==第一个数 + 第三个数 = 中间数的一半==',
                 '示例：`[1,2,1,4,1]` → `1`（只有 `[1,4,1]`）',
                 '本视频：`[1,2,1,4,1,3,1]` → `1`'],
        quote='遍历 nums，统计满足 2 ≤ i < n 且 (nums[i-2] + nums[i]) · 2 = nums[i-1] 的 i 的个数，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['长度固定为 3，子数组由右端点 `i` 唯一确定，所以 `i` 从 2 开始',
              '把“和等于一半”写成乘法 `(a + c) * 2 == b`，避免除法和小数',
              '布尔值 `True` 当 1 用，`sum` 直接得到个数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`i` 从 2 开始，`range(2, len(nums))`',
                 '易错：写成 `nums[i-1] / 2` 会有小数，用乘法更稳',
                 '`sum` 里是生成器表达式，逐个产出 True/False'],
    ),
)
