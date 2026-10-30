CONFIG = dict(
    num=3718, title='缺失的最小倍数', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希集合 + 枚举倍数',
    tags=[],
    code='''
class Solution:
    def missingMultiple(self, nums: List[int], k: int) -> int:
        st = set(nums)
        for x in count(k, k):  # 相当于 range(k, inf, k)
            if x not in st:
                return x
''',
    call='Solution().missingMultiple([8,2,3,4,6], 2)',
    expect=10,
    setup='from itertools import count',
    views=[
        dict(type='array', var='nums', label='nums', cell=80, h=170),
        dict(type='set', var='st', label='st（nums 的集合）', fmt=lambda x: str(x), h=170, font=34),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"枚举倍数 `x = {S['x']}`：{'在集合里 → 继续' if S['x'] in S['st'] else '不在集合里 → 就是答案'}" if 'x' in S else '')),
    ],
    watch=['k', 'x'],
    captions={
        'st = set': '转成哈希集合，判断“在不在”只要 `O(1)`：`st = {st}`',
        'for x in count': '按 `k, 2k, 3k, ...` 从小到大枚举：`x = {x}`',
        'if x not in st': '`{x}` 在集合里吗？ → ' + '{"不在，缺失的最小倍数就是它" if x not in st else "在，继续下一个倍数"}',
        'return x': '`{x}` 是最小的缺失倍数，返回 `{ret}`',
    },
    cards=dict(
        one_liner='把 nums 放进集合，从 k 开始一个个数倍数，第一个不在集合里的就是答案',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给整数数组 `nums` 和整数 `k`',
                 '返回 `nums` 中==缺失的、最小的正整数 k 的倍数==',
                 '示例：`[8,2,3,4,6]`，`k=2` → `10`'],
        quote='为方便查找元素，把 nums 保存到一个哈希集合中。然后枚举 x = k,2k,3k,... 如果 x 不在哈希集合中，返回 x。',
        quote_src='—— 灵茶山艾府题解',
        idea=['集合让“是否存在”变成 `O(1)`',
              '`count(k, k)` 是无限迭代器，相当于 `range(k, inf, k)`',
              '倍数从小到大枚举，第一个缺失的即最小'],
        summary=['时间 `O(n)`：至多枚举 `n + 1` 个倍数，因为 `nums` 只有 `n` 个数',
                 '空间 `O(n)`，存集合',
                 '倍数从 `k` 开始，不是 0（要求正整数）',
                 '`count` 来自 itertools，已在 setup 中导入，作者代码未改',
                 '另一种写法：`next(x for x in count(k, k) if x not in st)`'],
    ),
)
