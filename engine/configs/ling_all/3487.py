CONFIG = dict(
    num=3487, title='删除后的最大子数组元素和', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希集合 · 非负数去重求和',
    code='''
class Solution:
    def maxSum(self, nums: List[int]) -> int:
        st = set(x for x in nums if x >= 0)  # 去掉非负数并去重
        return sum(st) if st else max(nums)
''',
    call='Solution().maxSum([1, 2, -1, -2, 1, 0, -1])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（灰 = 负数，必删；绿 = 非负数）', h=200, cell=84,
             color=lambda S, i, v: 'green' if v >= 0 else None, dim=lambda S, i, v: v < 0),
        dict(type='set', var='st', label='st（非负数去重后的集合）', fmt=lambda x: str(x), h=150),
        dict(type='text', h=80, fn=lambda S: (f"选中的数：`{sorted(S['st'])}`，和 = =={sum(S['st'])}==" if 'st' in S and S['st'] else '')),
    ],
    watch=[('st', 'sorted(st) if "st" in dir() else None', 'green')],
    captions={
        'st = set': '负数留着只会让和变小 → 全部删掉；非负数==去重==后放进集合 `st`：`{sorted(st)}`',
        'return sum(st)': lambda S, B, r: (f'`st` 非空 → 答案是集合里所有数之和 `{sum(S.st)}`' if S.st
                                           else f'`st` 为空，说明全是负数，只能留一个：取最大的 `{max(S.nums)}`'),
    },
    cards=dict(
        one_liner='负数全删，非负数去重后求和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['可以任意删元素（不能删空），再选一个元素互不相同的子数组',
                 '求这个子数组的最大元素和',
                 '示例：`[1,2,-1,-2,1,0,-1]` → `3`（选 `[2, 1]`）'],
        quote='为了让元素和尽量大，负数不能留，可以全部去掉。但如果 nums 中的元素都是负数，题目规定不能全部去掉，此时答案为 nums 中的最大元素。',
        quote_src='—— 灵茶山艾府题解',
        idea=['删除不限个数 → 子数组可以挑出任意一组互不相同的数',
              '有非负数：每个非负数只能选一个，答案 = 非负数去重后的和',
              '全是负数：只能留一个，留最大的（绝对值最小的）'],
        before=[dict(heading='先分两种情况', lines=['有非负数：负数全删，每个非负数只留一个 → 去重求和',
                                                     '全是负数：不能删空，只能留一个 → 取最大值',
                                                     '用哈希集合 `set` 一步完成去重'])],
        after=[dict(heading='另一种写法', lines=['`sum(set(x for x in nums if x >= 0)) or max(nums)`',
                                                  '集合和为 0（空集或只有 0）时落到 `or max(nums)`',
                                                  '全是 0 时 `max(nums)` 也是 0，结果仍正确'])],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：全是负数时 `st` 为空，要返回 `max(nums)`，不能返回 0',
                 '0 属于非负数，可以放进集合，不影响和',
                 '另一种写法：`sum(set(...)) or max(nums)`，原理相同'],
    ),
)
