CONFIG = dict(
    num=747, title='至少是其他数字两倍的最大数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='一趟扫描找最大和次大',
    code='''
class Solution(object):
    def dominantIndex(self, nums):

        first = second = None
        for index, num in enumerate(nums):
            if first is None:
                first = index
            elif second is None:
                if num > nums[first]:
                    second = first
                    first = index
                else:
                    second = index
            elif num > nums[first]:
                second = first
                first = index
            elif num > nums[second]:
                second = index
        
        if second is None or nums[first] >= nums[second] + nums[second]:
            return first
        
        return -1
''',
    call='Solution().dominantIndex([3,6,1,0,2])',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 最大 first，粉 = 次大 second，黄框 = 当前 index）', cell=100, h=230,
             pointers={'index': 'yellow'},
             color=lambda S, i, v: 'blue' if S.get('first') == i else 'pink' if S.get('second') == i else None),
        dict(type='text', h=70, size=34,
             fn=lambda S: (f"最大 `{S['nums'][S['first']]}`，次大 `{S['nums'][S['second']]}`，次大的两倍 = =={2*S['nums'][S['second']]}=="
                           if S.get('first') is not None and S.get('second') is not None
                           else ('只见到一个数' if S.get('first') is not None else ''))),
    ],
    watch=[('first', 'first', 'blue'), ('second', 'second', 'pink'), 'index', 'num'],
    captions={
        'first = second = None': '`first` 记最大数的下标，`second` 记次大数的下标，一开始都还没有',
        'for index, num': '看第 `{index}` 个数 `{num}`',
        'if first is None': '`first` 还是空？{"是，第一个数先当最大" if B.first is None else "不是，往下比较"}',
        8: '`second` 还是空？{"是，这是第二个数，要和最大比较" if second is None else "不是，已经有最大和次大，继续比较"}',
        9: '`{num} > {nums[first]}`？{"更大" if num > nums[first] else "不更大"}，{"它当最大，原来的最大降为次大" if num > nums[first] else "它只能当次大"}',
        'second = first': '原来的最大退位当次大：`second = {second}`',
        'first = index': '新的最大是下标 `{first}`（值 {nums[first]}）',
        'second = index': '次大是下标 `{second}`（值 {nums[second]}）',
        14: '`{num} > {nums[first]}`？{"成立：新的最大，旧最大变次大" if num > nums[first] else "不成立，不是最大，再看能不能当次大"}',
        17: '`{num} > {nums[second]}`？{"成立：比次大更大，替换次大" if num > nums[second] else "不成立：不影响最大和次大"}',
        'if second is None or': '只要最大数 >= 次大数的两倍，它就至少是其他所有数的两倍：`{nums[first]} >= {nums[second]}+{nums[second]}` → {"成立" if nums[first] >= nums[second] + nums[second] else "不成立"}',
        'return first': '满足条件，返回最大数的下标 `{first}`',
        'return -1': '不满足，返回 `-1`',
    },
    cards=dict(
        one_liner='只需比较最大数和次大数：最大数 >= 次大数的两倍',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定数组 `nums`，其中最大的数唯一',
                 '判断最大数是否至少是其他每个数的两倍，是则返回它的下标，否则返回 `-1`',
                 '示例：`[3,6,1,0,2]` → `1`（6 >= 2×3）'],
        quote='可以一趟扫描，在找出最大数的同时顺便也找出第二大的数，然后就只需要判断最大数是否至少是第二大数的两倍即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['比第二大的数都不小于两倍，就比其他所有数都不小于两倍',
              '扫描时维护最大和次大的下标，新数更大就让位，次大跟着更新',
              '只有一个元素时没有次大，直接成立'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：新数成为最大时，旧最大要先赋给 `second` 再改 `first`',
                 '只有一个数时 `second is None`，直接返回下标',
                 '原文为 Python 2 风格，在 Python 3 下无需修改即可运行'],
    ),
)
