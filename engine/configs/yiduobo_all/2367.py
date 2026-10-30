CONFIG = dict(
    num=2367, title='等差三元组的数目', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='一趟遍历 + 集合', tags=['三指针'],
    code='''
class Solution(object):
    def arithmeticTriplets(self, nums, diff):
        num_set = set()
        res = 0
        for num in nums:
            if num - diff in num_set and num - diff - diff in num_set:
                res += 1
            num_set.add(num)

        return res
''',
    call='Solution().arithmeticTriplets([0,1,4,6,7,10], 3)',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: (f"当前 `{S['num']}`：往前看 ==`{S['num'] - S['diff']}`== 和 ==`{S['num'] - 2 * S['diff']}`== 是否都见过" if 'num' in S else f"diff = {S['diff']}"), size=30),
        dict(type='array', var='nums', h=200, pointers={'nums.index(num)': 'green'}, pointer_labels={'nums.index(num)': 'num'}),
        dict(type='set', var='num_set', h=200, fmt=lambda x: str(x)),
    ],
    watch=[('num', 'num', 'green'), ('res', 'res', 'green')],
    captions={
        'num_set = set()': '`num_set` 记录已经遍历过的数',
        'res = 0': '`res` 统计三元组个数',
        'for num in nums': '遍历到 `num = {num}`',
        'if num - diff in num_set': lambda S, B, r: (f'`{S.num} - {S.diff} = {S.num - S.diff}` {"在" if S.num - S.diff in S.num_set else "不在"}集合，`{S.num - 2 * S.diff}` {"在" if S.num - 2 * S.diff in S.num_set else "不在"}集合 → {"==两个都在，凑成三元组==" if (S.num - S.diff in S.num_set and S.num - 2 * S.diff in S.num_set) else "不成立"}'),
        'res += 1': '以 `{num}` 为最大项的三元组找到了：`res` → {res}',
        'num_set.add(num)': '==无论成不成立==，都把 `{num}` 放进集合，留给后面的数查',
        'return res': '共 `{res}` 个',
    },
    cards=dict(
        one_liner='一趟遍历，已见过的数放进集合，回头查前两项',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['严格递增数组 `nums` 和 `diff`，数相邻差为 `diff` 的三元组个数',
                 '示例：`[0,1,4,6,7,10]`，`diff=3` → `2`'],
        quote='若num - diff以及num - diff - diff都出现在集合中，说明这三个数就是一组合法的算术三元组。',
        quote_src='—— yiduobo 题解原文',
        idea=['把当前数当作三元组的最大项',
              '它前面的两项 `num-diff`、`num-diff-diff` 一定已经被遍历过，查集合即可',
              '最后不管是否成立，都要把 `num` 加入集合'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：==先查集合再 add==，顺序反了会把当前数自己也算进去',
                 '原文为 Python 2 风格，只删去了函数开头的空行',
                 '对比灵神：灵神还给了不占空间的三指针写法'],
    ),
)
