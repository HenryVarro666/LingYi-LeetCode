CONFIG = dict(
    num=414, title='第三大的数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='一趟扫描维护前三大',
    code='''
class Solution(object):
    def thirdMax(self, nums):

        first = nums[0]
        second = third = None
        pos = 1
        while pos < len(nums) and nums[pos] == first:
            pos += 1
        if pos == len(nums):
            return first

        if nums[pos] < first:
            second = nums[pos]
        else:
            second = first
            first = nums[pos]

        for num in nums[pos + 1:]:
            if num == first or num == second:
                continue
            if num > first:
                third = second
                second = first
                first = num
            elif num > second:
                third = second
                second = num
            elif third is None or num > third:
                third = num

        if third is None:
            return first
        
        return third
''',
    call='Solution().thirdMax([3, 2, 2, 5, 1, 0])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums', cell=84, pointers={'pos': 'pink'},
             color=lambda S, i, v: 'blue' if 'num' in S and 'pos' in S and i == S['pos'] + 1 + S.get('_k', -99) else None),
        dict(type='text', fn=lambda S: f"第一大 `{S.get('first')}`　第二大 `{S.get('second')}`　第三大 `{S.get('third')}`" if 'first' in S else '', size=34),
        dict(type='text', fn=lambda S: f"当前数 `num = {S['num']}`" if 'num' in S else '', size=28),
    ],
    watch=[('first', 'first', 'green'), ('second', 'second', 'cyan'), ('third', 'third', 'orange'), ('num', 'num', 'blue')],
    captions={
        'first = nums[0]': '先把 `first` 设成第一个数 `{first}`',
        'second = third = None': '`second`、`third` 还没有，用 `None` 表示',
        'pos = 1': '`pos` 往后找第一个和 `first` 不同的数',
        'while pos < len(nums)': lambda S, B, r: (f'`nums[{S.pos}] = {S.nums[S.pos]}` 等于 `first` → 重复，跳过' if S.pos < len(S.nums) and S.nums[S.pos] == S.first else '遇到了不同的数（或到头了）'),
        'pos += 1': '`pos` → {pos}',
        'if pos == len(nums)': lambda S, B, r: ('全是同一个数，没有第三大，返回最大值' if S.pos == len(S.nums) else '找到了不同的数，可以建立前两名'),
        'if nums[pos] < first': lambda S, B, r: (f'`{S.nums[S.pos]} < {S.first}`：它是第二大' if S.nums[S.pos] < S.first else f'`{S.nums[S.pos]} > {S.first}`：它成为第一大，原来的第一变第二'),
        'second = nums[pos]': '`second` = =={second}==',
        'second = first': '原第一大 `{first}` 降为第二',
        'first = nums[pos]': '`first` = =={first}==',
        'for num in nums[pos + 1:]': '继续扫描下一个数 `num = {num}`',
        'if num == first or num == second': lambda S, B, r: (f'`{S.num}` 已经是前两名之一 → 重复，==跳过==' if S.num == S.first or S.num == S.second else f'`{S.num}` 不重复，继续比较'),
        'continue': '重复的数不能算新的名次',
        'if num > first': lambda S, B, r: (f'`{S.num} > {S.first}` → 新的第一大，前三名整体后移' if S.num > S.first else f'`{S.num} < {S.first}`，不是第一'),
        'third = second': '第二名降为第三：`third = {third}`',
        'second = first': '第一名降为第二：`second = {second}`',
        'first = num': '`first` = =={first}==',
        'elif num > second': lambda S, B, r: (f'`{S.num} > {S.second}` → 新的第二大' if S.num > S.second else f'`{S.num} < {S.second}`，不是第二'),
        'second = num': '`second` = =={second}==',
        'elif third is None or num > third': lambda S, B, r: ('`third` 还空着 → 直接占位' if S.third is None else (f'`{S.num} > {S.third}` → 更新第三大' if S.num > S.third else f'`{S.num} <= {S.third}`，不够大，丢弃')),
        'third = num': '`third` = =={third}==',
        'if third is None': lambda S, B, r: ('不同的数不足三个 → 返回最大的' if S.third is None else '凑够了三个不同的数'),
        'return first': '没有第三大 → 返回 `{first}`',
        'return third': '第三大的数是 `{third}`',
    },
    cards=dict(
        one_liner='一趟扫描，只维护三个名次：first、second、third',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['返回数组中第三大的==不同==的数；不存在第三大就返回最大的数',
                 '重复的数只算一个名次',
                 '示例：`[2,2,3,1]` → `1`；本视频：`[3,2,2,5,1,0]` → `2`'],
        quote='比较基础的题目。一趟扫描，维护住这三个数即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先跳过开头与 `nums[0]` 相同的数，建立 `first`、`second`',
              '之后每个数：与前两名相等就忽略；更大就把名次往后挤',
              '`third` 用 `None` 表示还不存在，最后判断返回哪个'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：重复的数不占名次，必须先判 `num == first or num == second`',
                 '易错：`third` 为 `None` 时不能直接比较大小',
                 '不同的数少于三个时，返回最大值 `first`'],
    ),
)
