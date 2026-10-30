def _txt(S):
    if 'sum_set' not in S:
        return '先排序，再从两端向中间配对：`nums[left] + nums[right]`'
    return f"已见过的两数之和 `sum_set` = =={sorted(S['sum_set'])}==，共 {len(S['sum_set'])} 种"


CONFIG = dict(
    num=2465, title='不同的平均值数目', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='排序 + 左右双指针 · 集合去重',
    tags=[],
    code='''
class Solution(object):
    def distinctAverages(self, nums):

        nums.sort()
        left = 0
        right = len(nums) - 1
        sum_set = set()
        while left < right:
            sum_set.add(nums[left] + nums[right])
            left += 1
            right -= 1
        
        return len(sum_set)
''',
    call='Solution().distinctAverages([9,1,4,0,3,5,6,2])',
    expect=2,
    views=[
        dict(type='text', fn=_txt, size=28, h=90),
        dict(type='array', var='nums', label='nums（排序后，蓝 = left，粉 = right）', cell=100, h=230,
             pointers={'left': 'blue', 'right': 'pink'},
             color=lambda S, i, v: ('blue' if i == S['left'] else 'pink' if i == S['right'] else None) if 'right' in S else None,
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right'])),
        dict(type='set', var='sum_set', label='sum_set（两数之和）', fmt=lambda x: str(x), h=160),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('len(sum_set)', 'len(sum_set)', 'green')],
    captions={
        'nums.sort()': '从小到大排序：`{nums}`，最小的在最左、最大的在最右',
        'left = 0': '`left` 指向当前最小值',
        'right = len': '`right = {right}` 指向当前最大值',
        'sum_set = set()': '`sum_set` 存每一对的和：平均值不同 ⇔ 两数之和不同，==不用除以 2==',
        'while left < right': lambda S, B, r: (f'`{S.left} < {S.right}`：还剩一对，继续' if S.left < S.right else f'`{S.left} >= {S.right}`：数都配完了 → 结束'),
        'sum_set.add': lambda S, B, r: (f'这一轮删掉最小 `{S.nums[S.left]}` 和最大 `{S.nums[S.right]}`，和 `{S.nums[S.left] + S.nums[S.right]}` 入集合 → `{sorted(S.sum_set)}`'
                                        + ('（这个和已经有了，集合不增加）' if len(S.sum_set) == len(B.sum_set) else '')),
        'left += 1': '最小值删掉了，`left` → `{left}`',
        'right -= 1': '最大值删掉了，`right` → `{right}`',
        'return len(sum_set)': '集合里有 `{len(sum_set)}` 个不同的和 → 返回 `{len(sum_set)}`',
    },
    cards=dict(
        one_liner='排序后两端往中间走，两数之和放进集合',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每轮删掉当前最小值和最大值，计算它们的平均值，直到数组为空',
                 '返回得到的 ==不同平均值== 的个数',
                 '本视频：`[9,1,4,0,3,5,6,2]` → 排序后配对和为 9、7、7、7 → `2`'],
        quote='只需将数组从小到大进行排序，然后从两边向中间遍历，每次取当前遍历到的两个数求和并加入到集合中。遍历完成后集合的大小即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序之后，==最小值在最左、最大值在最右==，每轮刚好取两端',
              '`left`、`right` 从两头向中间走，一轮处理一对',
              '集合自动去重，最后 `len(sum_set)` 就是答案'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '原文用求和代替平均值，两数和相同当且仅当平均值相同',
                 '循环条件 `left < right`：长度为偶数，刚好配完',
                 '对比灵神：灵神一行生成式搞定，yiduobo 用显式双指针，更直观'],
    ),
)
