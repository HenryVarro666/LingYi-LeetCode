CONFIG = dict(
    num=3731, title='找出缺失的元素', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希集合 · 枚举区间',
    tags=[],
    code='''
class Solution:
    def findMissingElements(self, nums: List[int]) -> List[int]:
        st = set(nums)
        return [i for i in range(min(nums) + 1, max(nums)) if i not in st]
''',
    call='Solution().findMissingElements([7,3,9,4])',
    expect=[5, 6, 8],
    views=[
        dict(type='array', var='nums', label='nums', cell=84),
        dict(type='set', var='st', label='st（nums 转成的哈希集合）', fmt=lambda x: str(x)),
        dict(type='text', fn=lambda S: f"最小值 `{min(S['nums'])}`，最大值 `{max(S['nums'])}`：只需检查它们中间的整数", size=28),
    ],
    watch=['st'],
    captions={
        'st = set(nums)': '把 `nums` 转成哈希集合 `st`：之后判断「某个数在不在 nums 里」只要 ==O(1)==',
        'return [i for': '最小值 `{min(nums)}` 和最大值 `{max(nums)}` 一定在 nums 里，所以只枚举 `[{min(nums)+1}, {max(nums)-1}]`：不在 `st` 里的 `i` 就是缺失的，收集起来 → `{ret}`',
    },
    cards=dict(
        one_liner='区间两端一定在，只检查中间的数在不在集合里',
        complexity='时间 `O(D)`，空间 `O(n)`，`D = max − min`',
        problem=['`nums` 原本是某个范围内的所有整数，现在可能缺了几个（元素互不相同）',
                 '范围的最小值、最大值仍在 `nums` 里',
                 '按从小到大返回缺失的整数；示例：`[1,4,2,5]` → `[3]`',
                 '本视频：`[7,3,9,4]` → `[5,6,8]`'],
        quote='设 nums 的最小值和最大值分别为 m 和 M。枚举在 [m+1, M-1] 中的整数，如果不在 nums 中，加入答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`m` 和 `M` 本身一定存在，只需枚举 `[m+1, M-1]`',
              '数组里查一个数要 `O(n)`，所以先转成哈希集合',
              '一行列表推导式：`i not in st` 的就留下'],
        after=[dict(heading='逐个枚举 [4, 8]', lines=[
            '`4`：在 `st` 里 → 不是缺失的', '`5`：不在 `st` 里 → ==加入答案==', '`6`：不在 `st` 里 → ==加入答案==',
            '`7`：在 `st` 里 → 跳过', '`8`：不在 `st` 里 → ==加入答案==，枚举结束'])],
        result='缺失的是 `5, 6, 8`，按枚举顺序天然有序 ✓',
        summary=['时间 `O(D)`（`D` 是最大值减最小值），空间 `O(n)`',
                 '`range(min+1, max)` 右开，正好排除最大值',
                 '易错：不要对 `nums` 本身判断 `in`，列表查找是 `O(n)`',
                 '枚举顺序就是升序，不需要再排序'],
    ),
)
