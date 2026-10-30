CONFIG = dict(
    num=2099, title='找到和最大的长度为 K 的子序列', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='下标数组排序',
    tags=['贪心', '排序', '难度分 1447'],
    code='''
class Solution:
    def maxSubsequence(self, nums: List[int], k: int) -> List[int]:
        idx = sorted(range(len(nums)), key=lambda i: nums[i])  # 创建下标数组，对下标数组排序
        idx = sorted(idx[-k:])  # 取前 k 大元素的下标，排序
        return [nums[i] for i in idx]  # 取出 nums 的子序列
''',
    call='Solution().maxSubsequence([-1,5,3,-2,4,3,0,2], 4)',
    expect=[5, 3, 4, 3],
    views=[
        dict(type='array', var='nums', h=200, label='nums',
             color=lambda S, i, v: 'green' if 'idx' in S and S.get('_line', 0) >= 5 and i in S['idx'][-S['k']:] else None),
        dict(type='array', var='idx', h=200, label='idx（下标）'),
    ],
    watch=[('k', 'k', 'blue')],
    captions={
        'idx = sorted(range': '按 `nums[i]` 从小到大给下标排序：`idx` = {idx}，最后 `k` 个就是最大的 `k` 个数的位置',
        'idx = sorted(idx[-k:])': '取末尾 `k` 个下标 `{idx[-k:]}`，但子序列要保持原顺序 → 把下标按从小到大重排：`idx` = {idx}',
        'return': '按下标取值，顺序和原数组一致：=={ret}==',
    },
    cards=dict(
        after=[dict(heading='为什么不直接排序 nums', lines=['排序会打乱位置，而子序列要求 ==保持原顺序==', '给下标排序，值和位置都不丢', '最后再排一次下标，就还原了顺序'])],
        one_liner='给下标排序，取最大的 k 个下标，再还原顺序',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['在 `nums` 中选长度为 `k` 的子序列，使和最大',
                 '子序列必须保持原来的相对顺序，返回任意一个',
                 '示例：`[-1,-2,3,4]`，`k=3` → `[-1,3,4]`'],
        quote='问题相当于选 nums 中最大的 k 个数，这样总和才能最大。但子序列的顺序是不能变的，怎么办？创建一个下标数组 idx，根据 nums[idx[i]] 对 idx 排序。',
        quote_src='—— 灵茶山艾府题解',
        idea=['和最大 = 选最大的 `k` 个数，哪怕是负数也要凑够 `k` 个',
              '直接排序 `nums` 会丢掉顺序，所以改成给下标排序',
              '取最大 `k` 个下标，再按下标升序，就还原了原顺序'],
        summary=['时间 `O(n log n)`，用快速选择可到 `O(n)`',
                 '`idx[-k:]` 取的是最大的 `k` 个，不是最小的',
                 '选完下标后别忘了再排一次序',
                 '专题：贪心 §1.1 从最小/最大开始贪心'],
    ),
)
