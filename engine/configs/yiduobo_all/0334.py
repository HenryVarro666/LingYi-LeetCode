CONFIG = dict(
    num=334, title='递增的三元子序列', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='两个变量 first / second', tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def increasingTriplet(self, nums):

        if len(nums) < 3:
            return False

        first = nums[0]
        second = None
        for num in nums[1:]:
            if second is None:
                if num > first:
                    second = num
                else:
                    first = num
            else:
                if num > second:
                    return True
                if num <= first:
                    first = num
                else:
                    second = num

        return False
''',
    call='Solution().increasingTriplet([2,1,5,0,4,6])',
    expect=True,
    views=[
        dict(type='array', var='nums', h=220, label='nums（黄色 = 当前 num）',
             color=lambda S, i, v: 'yellow' if 'num' in S and v == S['num'] else None),
        dict(type='text', size=34, fn=lambda S: (f"`first = {S['first']}`（长 1 的最小结尾），`second = {S['second']}`（长 2 的最小结尾）" if 'first' in S else '')),
    ],
    watch=[('num', 'num', 'yellow'), ('first', 'first', 'blue'), ('second', 'second', 'pink')],
    captions={
        'len(nums) < 3': '不足 3 个数，肯定凑不出三元组',
        'first = nums[0]': '`first`：长度为 1 的上升子序列里最小的末尾，先取 `{first}`',
        'second = None': '`second`：长度为 2 的上升子序列里最小的末尾，还没有',
        'if second is None': lambda S, B, r: ('还没有长度 2 的序列：先看 `num` 能不能接在 `first` 后面' if S.second is None
                                              else '已有长度 2 的序列：`num` 先和 `second` 比'),
        'if num > first': lambda S, B, r: (f'`{S.num} > {S.first}`：能接在 first 后面 → 得到长度 2 的序列' if S.num > S.first
                                           else f'`{S.num} <= {S.first}`：接不上，只能当更小的开头'),
        'second = num': '`second = {second}`：长度 2 的序列末尾记为 `{num}`',
        'first = num': '`first` 更新为更小的 `{first}`：后面更容易接上',
        'if num > second': lambda S, B, r: (f'`{S.num} > second = {S.second}`：==第三个数找到了== → 长度 3' if S.num > S.second
                                            else f'`{S.num} <= second = {S.second}`：还凑不成 3 个'),
        'if num <= first': lambda S, B, r: (f'`{S.num} <= first = {S.first}`：比长 1 的末尾还小 → 更新 first' if S.num <= S.first
                                            else f'`first < {S.num} <= second`：可让 second 变小'),
        'return True': '存在长度为 3 的上升子序列 → ==返回 True==',
        'return False': '扫描结束没出现，返回 False',
    },
    cards=dict(
        one_liner='first、second 两个变量，一遍扫描就够',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['判断数组里是否存在长度为 3 的递增子序列',
                 '进阶要求 `O(n)` 时间、`O(1)` 空间',
                 '示例：`[2,1,5,0,4,6]` → `True`'],
        quote='只需要通过两个变量first与second分别表示当前长度为1和长度为2的上升子序列中最小的末尾元素。',
        quote_src='—— yiduobo 题解原文',
        idea=['新来的 x 有三种情况：`x > second` 直接成功',
              '`x <= first`：更新 first；否则 `first < x <= second`：更新 second',
              '每个数最多比较两次'],
        summary=['时间 `O(n)`，空间 `O(1)`，满足进阶要求',
                 '`second` 初始为 None，要先判断它是否已有值',
                 '更新 first 不会破坏已有的 second',
                 '原文已是 Python 3 可运行的写法，无需修改',
                 '对比灵神：灵神用通用的 g 数组加二分，这里直接展开成两个变量'],
    ),
)
