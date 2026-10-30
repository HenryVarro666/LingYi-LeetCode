CONFIG = dict(
    num=217, title='存在重复元素', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希集合 · 边遍历边查',
    tags=[],
    code='''
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        st = set()
        for x in nums:
            if x in st:
                return True
            st.add(x)
        return False
''',
    call='Solution().containsDuplicate([1,2,3,4,2,5])',
    expect=True,
    views=[
        dict(type='array', var='nums', h=200,
             color=lambda S, i, v: 'blue' if 'x' in S and v == S['x'] else None),
        dict(type='set', var='st', h=260, fmt=lambda x: str(x)),
    ],
    watch=[('x', 'x', 'blue'), ('已见元素', 'sorted(st)', 'green')],
    captions={
        'st = set()': '准备一个空的哈希集合 `st`，记录==已经见过==的数',
        'for x in nums': '依次取出 `x = {x}`',
        'if x in st': lambda S, B, r: (f'`{S.x}` 已经在 `st` 里 → ==见过了，有重复==' if S.x in S.st
                                       else f'`{S.x}` 不在 `st` 里 → 还没见过'),
        'return True': '发现重复，直接返回 `True`，==提前退出==，后面不用看了',
        'st.add(x)': '把 `{x}` 加入集合，留给后面的数去查',
        'return False': '遍历完都没有重复 → 返回 `False`',
    },
    cards=dict(
        one_liner='边遍历边丢进哈希集合，碰到已有的就是重复',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给整数数组 `nums`，某个值出现 ==至少两次== 就返回 `true`',
                 '每个元素都不同则返回 `false`',
                 '示例：`[1,2,3,1]` → `true`；`[1,2,3,4]` → `false`'],
        quote='遍历数组，一边遍历一边把 nums[i] 加到哈希集合中。如果发现 nums[i] 已经在哈希集合中，直接返回 true。这样可以提前退出循环。',
        quote_src='—— 灵茶山艾府题解（写法二）',
        idea=['集合里存的是「前面已经出现过的数」',
              '当前数在集合里 → 它前面出现过 → 重复',
              '不用等扫完整个数组，发现就返回'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '先查再加：==先判断 x in st，再 st.add(x)==，否则自己会和自己重复',
                 '写法一 `len(set(nums)) < len(nums)` 更短，但要扫完全部元素，不能提前退出'],
    ),
)
