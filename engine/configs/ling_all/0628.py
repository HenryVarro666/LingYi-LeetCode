def _cand(S):
    if 'max1' not in S:
        return '答案只有两种候选：==最大三个数的积==，或 ==最小两个数 × 最大数=='
    a, b, c, m1, m2 = S['max1'], S['max2'], S['max3'], S['min1'], S['min2']
    if abs(a) == float('inf') or abs(b) == float('inf') or abs(c) == float('inf'):
        return f'候选一 `max1·max2·max3`：还没凑够三个数；候选二 `min1·min2·max1`：还没凑够'
    return f'候选一 `{a}×{b}×{c}` = =={a*b*c}==　候选二 `{m1}×{m2}×{a}` = =={m1*m2*a}=='


CONFIG = dict(
    num=628, title='三个数的最大乘积', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='一次遍历维护前三大/前二小',
    tags=['贪心与思维', '乘积贪心'],
    code='''
class Solution:
    def maximumProduct(self, nums: List[int]) -> int:
        min1 = min2 = inf
        max1 = max2 = max3 = -inf

        for x in nums:
            # 维护最小值和次小值
            if x < min1:
                min2 = min1
                min1 = x
            elif x < min2:
                min2 = x

            # 维护前三大
            if x > max1:
                max3 = max2
                max2 = max1
                max1 = x
            elif x > max2:
                max3 = max2
                max2 = x
            elif x > max3:
                max3 = x

        return max(max1 * max2 * max3, min1 * min2 * max1)
''',
    call='Solution().maximumProduct([-10, 2, -8, 3, 1, -1])',
    expect=240,
    views=[
        dict(type='text', fn=_cand, h=90),
        dict(type='array', var='nums', h=260, label='nums（绿 = 前三大，粉 = 前二小）',
             color=lambda S, i, v: ('yellow' if S.get('x') == v and S.get('_line') in (8, 12, 13, 17, 20, 23) and False else
                                    'green' if v in (S.get('max1'), S.get('max2'), S.get('max3')) else
                                    'pink' if v in (S.get('min1'), S.get('min2')) else None)),
    ],
    watch=[('min1', 'min1', 'pink'), ('min2', 'min2', 'pink'), ('max1', 'max1', 'green'),
           ('max2', 'max2', 'green'), ('max3', 'max3', 'green'), ('x', 'x', 'yellow')],
    captions={
        'min1 = min2 = inf': '最小、次小先设成 ==正无穷==，任何数都比它小',
        'max1 = max2 = max3 = -inf': '前三大先设成 ==负无穷==，任何数都比它大',
        'for x in nums': '取下一个数 `x = {x}`',
        'if x < min1': '`x < min1`（{x} < {min1}）→ {"成立" if x < min1 else "不成立"}：比最小还小才成为新的最小',
        'elif x < min2': '`x < min2`（{x} < {min2}）→ {"成立" if x < min2 else "不成立"}：不是最小，但比次小小才更新次小',
        'if x > max1': '`x > max1`（{x} > {max1}）→ {"成立" if x > max1 else "不成立"}：比最大还大才成为新的最大',
        'elif x > max2': '`x > max2`（{x} > {max2}）→ {"成立" if x > max2 else "不成立"}：不是最大，但比次大大才更新次大',
        'elif x > max3': '`x > max3`（{x} > {max3}）→ {"成立" if x > max3 else "不成立"}：只比第三大大才更新第三大',
        'min1 = x': '`min1 = {x}`：x 是新的最小',
        'min2 = x': '`min2 = {x}`：最小不变，x 是新的次小',
        'max1 = x': '`max1 = {x}`：x 是新的最大',
        'max2 = x': '`max2 = {x}`：最大不变，x 是新的次大',
        'max3 = x': '`max3 = {x}`：x 是新的第三大',
        'return max': lambda S, B, ret: f'两个候选取大：`{S.max1}×{S.max2}×{S.max3}` = {S.max1*S.max2*S.max3}，`{S.min1}×{S.min2}×{S.max1}` = {S.min1*S.min2*S.max1} → =={ret}==',
    },
    cards=dict(
        one_liner='负负得正：只看「最大三个」和「最小两个+最大一个」',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给整数数组 `nums`，选三个数使乘积最大',
                 '示例：`[1,2,3,4]` → `24`；`[-1,-2,-3]` → `-6`',
                 '本视频：`[-10,2,-8,3,1,-1]` → `240`'],
        quote='综上所述，只需考虑两种情况：1. 选 nums 中最大的三个数。2. 选 nums 中最小的两个数以及最大的一个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['按所选三个数里==负数的个数==分类：0 个、1 个、3 个的最优都等价于「最大三个数」',
              '2 个负数：负负得正，取==最小两个==（绝对值最大）再配最大的一个',
              '所以不用排序，一次遍历维护 5 个数就够'],
        summary=['时间 `O(n)`，空间 `O(1)`，比写法一排序的 `O(n log n)` 更快',
                 '最小值要用 `inf`、最大值要用 `-inf` 初始化，别写反',
                 '更新顺序：先把旧的最大往后挪，再写入新的最大',
                 '另一种写法：排序后 `max(nums[-3]*nums[-2]*nums[-1], nums[0]*nums[1]*nums[-1])`'],
    ),
)
