CONFIG = dict(
    num=3876, title='构造奇偶一致的数组 II', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='分类讨论 + 最小奇偶数', tags=['灵神题单', '难度分 1444'],
    code='''
class Solution:
    def uniformArray(self, nums1: List[int]) -> bool:
        # 计算最小偶数、最小奇数
        mn = [inf] * 2
        for x in nums1:
            mn[x % 2] = min(mn[x % 2], x)

        # 只有偶数，或者偶数 >= 最小的偶数 > 最小的奇数
        # 只有奇数的情况蕴含在 mn[0] > mn[1] 中
        return mn[1] == inf or mn[0] > mn[1]
''',
    call='Solution().uniformArray([8, 3, 6, 5, 4])',
    expect=True,
    views=[
        dict(type='array', var='nums1', label='nums1', h=230,
             color=lambda S, i, v: ('green' if v % 2 == 1 else 'blue') if 'x' in S and v == S['x'] else None),
        dict(type='array', var='mn', label='mn[0]=最小偶数，mn[1]=最小奇数', h=230, cell=120),
        dict(type='text', fn=lambda S: f"最小偶数 `{S['mn'][0]}`，最小奇数 `{S['mn'][1]}`" if 'mn' in S else ''),
    ],
    watch=['x', ('最小偶数', 'mn[0]', 'blue'), ('最小奇数', 'mn[1]', 'green')],
    captions={
        'mn = [inf]': '`mn[0]` 记最小偶数，`mn[1]` 记最小奇数，先都设为无穷',
        'mn[x % 2] = min': '`x={x}` 是{"奇" if x % 2 else "偶"}数 → 更新 `mn[{x % 2}] = min({B.mn[x % 2]}, {x}) = {mn[x % 2]}`',
        'return': '奇偶都有时：奇数无法变偶数（最小奇数没有更小的奇数可减），偶数要减最小奇数，所以要求最小偶数 > 最小奇数：`{mn[0]} > {mn[1]}` → =={ret}==',
    },
    cards=dict(
        one_liner='奇数没法变偶数，偶数只能减最小奇数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums2[i]` 可取 `nums1[i]`，或 `nums1[i]-nums1[j]`（差必须 ≥ 1）',
                 '问能否让 `nums2` 全奇或全偶',
                 '示例：`[8,3,6,5,4]` → `true`'],
        quote='可以把奇数都变成偶数吗？注意奇数只能减去奇数才能变成偶数，那么最小的奇数要减去谁呢？我们无法满足 nums1[i] - nums1[j] >= 1 的要求。',
        quote_src='—— 灵茶山艾府题解',
        idea=['本来就全奇或全偶：直接照抄',
              '奇偶都有：奇变偶做不到（最小奇数无人可减）',
              '偶变奇：都减最小奇数 `x`，要求每个偶数 > x，即最小偶数 > 最小奇数'],
        summary=['只需一次遍历求最小偶数、最小奇数',
                 '`mn[1] == inf` 表示全偶；全奇时 `mn[0]=inf > mn[1]`，已被后半句蕴含',
                 '示例 2：`[2,3]`，2 > 3 不成立 → `false`',
                 '难点在分类讨论，代码本身极短'],
    ),
)
