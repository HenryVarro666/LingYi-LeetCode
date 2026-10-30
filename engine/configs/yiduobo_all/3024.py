def _tri(S):
    n = S['nums']
    if S['_line'] <= 4:
        return '先排序，再比较两条短边与最长边'
    return f'`{n[0]}`  `{n[1]}`  `{n[2]}`：两短边之和 `{n[0]}+{n[1]}={n[0]+n[1]}`，最长边 `{n[2]}`'


CONFIG = dict(
    num=3024, title='三角形类型', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='排序 · 逐类判断',
    code='''
class Solution(object):
    def triangleType(self, nums):

        nums.sort()
        if nums[0] + nums[1] <= nums[2]:
            return "none"
        
        if nums[0] == nums[1]:
            if nums[0] == nums[2]:
                return "equilateral"
            else:
                return "isosceles"
        elif nums[0] == nums[2] or nums[1] == nums[2]:
            return "isosceles"
        else:
            return "scalene"
''',
    call='Solution().triangleType([5,3,5])',
    expect='isosceles',
    views=[
        dict(type='array', var='nums', label='nums', h=300, cell=120,
             color=lambda S, i, v: ('pink' if i == 2 else 'blue') if S['_line'] >= 5 else None),
        dict(type='text', fn=_tri, size=34),
    ],
    watch=[('nums', 'nums', 'blue')],
    captions={
        'nums.sort()': '排序后 `nums = {nums}`，最后一个是最长边',
        'if nums[0] + nums[1] <= nums[2]': lambda S, B, r: (
            f'两短边之和 `{S.nums[0] + S.nums[1]}` ≤ 最长边 `{S.nums[2]}` → ==不能构成三角形=='
            if S.nums[0] + S.nums[1] <= S.nums[2] else
            f'两短边之和 `{S.nums[0] + S.nums[1]}` > 最长边 `{S.nums[2]}` → 能构成三角形，接着判断类型'),
        'if nums[0] == nums[1]': lambda S, B, r: (
            '`nums[0] == nums[1]`：最小两边相等，再看第三边' if S.nums[0] == S.nums[1]
            else '`nums[0] ≠ nums[1]`：转去看最大边是否和某一边相等'),
        'if nums[0] == nums[2]:': '`nums[0] == nums[2]`？最小等于最大 → 三边全相等',
        'elif nums[0] == nums[2] or nums[1] == nums[2]': lambda S, B, r: (
            '最大边和另一条边相等 → ==恰好两边相等==' if (S.nums[0] == S.nums[2] or S.nums[1] == S.nums[2])
            else '最大边和另两条都不等 → 三边互不相同'),
        'return "equilateral"': '返回 =="equilateral"==',
        'return "isosceles"': '返回 =="isosceles"==',
        'return "scalene"': '返回 =="scalene"==',
        'return "none"': '返回 =="none"==',
    },
    cards=dict(
        one_liner='先判能不能成三角形，再依次判等边、等腰',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`nums` 是三条边长，判断能否构成三角形及其类型',
                 '三边全等 `equilateral`，恰两边等 `isosceles`，互不等 `scalene`，不成立 `none`',
                 '本视频：`[5,3,5]` → `"isosceles"`'],
        quote='先通过两短边之和是否大于第三边判断能否形成三角形，如果不是，返回none',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后，最长边在末尾，只比较 `nums[0] + nums[1]` 与 `nums[2]`',
              '合法后：先判等边，再判等腰，都不是就是不等边',
              '每一类都单独写出来，分支清晰'],
        after=[dict(heading='四种结果对照', lines=['`[3,3,3]` → 等边：`nums[0] == nums[1] == nums[2]`',
                                                 '`[3,3,5]` 或 `[3,5,5]` → 等腰',
                                                 '`[3,4,5]` → 不等边：三边互不相同',
                                                 '`[1,2,3]` → `none`：`1 + 2 <= 3`'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '`<=` 不能写成 `<`：两短边之和等于最长边时退化为线段',
                 '有两种路径会得到 isosceles：`nums[0]==nums[1]` 或最大边与另一边相等',
                 '原文为 Python 2 风格，在 Python 3 下无需修改，逐字使用'],
    ),
)
