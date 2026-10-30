CONFIG = dict(
    num=3745, title='三元素表达式的最大值', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='排序 · 取最大两个和最小一个',
    tags=['贪心与思维', '从最小/最大开始贪心', '难度分 1218'],
    code='''
class Solution:
    def maximizeExpressionOfThree(self, nums: List[int]) -> int:
        nums.sort()
        return nums[-1] + nums[-2] - nums[0]
''',
    call='Solution().maximizeExpressionOfThree([-2,0,5,-2,4])',
    expect=11,
    views=[
        dict(type='array', var='nums', label='nums（排序后：a、b 取最大两个，c 取最小）', h=300,
             color=lambda S, i, v: ('green' if i >= len(S['nums']) - 2 else 'red' if i == 0 else None) if S['_line'] >= 4 else None),
        dict(type='text', size=34, h=140,
             fn=lambda S: (f"`a + b − c` = `{S['nums'][-1]} + {S['nums'][-2]} − ({S['nums'][0]})` = =={S['nums'][-1] + S['nums'][-2] - S['nums'][0]}==" if S['_line'] >= 4 else '')),
    ],
    watch=[('nums', 'nums', 'cyan')],
    captions={
        'nums.sort': '要让 `a + b − c` 最大：a、b 越大越好，c 越小越好 → 先==从小到大排序==：`{nums}`',
        'return nums[-1]': 'a = `nums[-1]` = `{nums[-1]}`，b = `nums[-2]` = `{nums[-2]}`，c = `nums[0]` = `{nums[0]}` → =={ret}==',
    },
    cards=dict(
        one_liner='a、b 取最大的两个，c 取最小的一个',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['从 `nums` 里选下标互不相同的三个数 `a`、`b`、`c`',
                 '使 `a + b - c` 最大，返回这个最大值',
                 '本视频：`[-2,0,5,-2,4]` → `11`'],
        quote='要让 a+b-c 尽量大，a 和 b 要尽量大，c 要尽量小。把 nums 从小到大排序，取 a=nums[n-1], b=nums[n-2], c=nums[0]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`a + b − c`：加的越大越好，减的越小越好',
              '排序后，最大两个在末尾，最小一个在开头',
              '三个下标天然不同（n ≥ 3），直接代入'],
        after=[dict(heading='优化：不排序也行', lines=['题解提到：手动维护前二大（或用堆）和最小值', '写法：`sum(nlargest(2, nums)) - min(nums)`', '时间从 `O(n log n)` 降到 `O(n)`，思路不变：大的加、小的减'])],
        summary=['时间 `O(n log n)`，空间 `O(1)`（忽略排序栈）',
                 '`c` 是负数时 `− c` 反而变大，公式不用分情况',
                 '题解的优化写法：`sum(nlargest(2, nums)) - min(nums)`，一次遍历 `O(n)`',
                 '本视频演示题解里的排序写法，逻辑完全相同'],
    ),
)
