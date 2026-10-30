CONFIG = dict(
    num=3914, title='使数组非递减需要的最小累计值', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='贪心 · 只改后缀',
    tags=['灵神题单', '常用数据结构', '难度分 1662'],
    code='''
class Solution(object):
    def minOperations(self, nums):
        
        res = 0
        for index in range(1, len(nums)):
            if nums[index] < nums[index - 1]:
                res += nums[index - 1] - nums[index]
        
        return res
''',
    call='Solution().minOperations([3,3,2,1,5,4])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"补齐 `nums[{S['index']}]` 要付：`{S['nums'][S['index']-1]} − {S['nums'][S['index']]}` = ==`{max(S['nums'][S['index']-1]-S['nums'][S['index']],0)}`==" if 'index' in S else ''), size=28),
        dict(type='array', var='nums', label='nums（蓝 = 当前位，粉 = 前一位）', h=230, pointers={'index': 'blue', 'index - 1': 'pink'},
             color=lambda S, i, v: ('blue' if i == S['index'] else 'pink' if i == S['index'] - 1 else None) if 'index' in S else None),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计所有操作的 `x` 之和',
        'for index in range': '考察 `nums[{index}] = {nums[index]}`，前一个是 `nums[{index-1}] = {nums[index-1]}`',
        'if nums[index] < nums[index - 1]': lambda S, B, r: (
            f'`{S.nums[S.index]} < {S.nums[S.index-1]}`：比前一个小 → 前面的修改都已覆盖到这两位，只能再改后缀补差' if S.nums[S.index] < S.nums[S.index - 1]
            else f'`{S.nums[S.index]} >= {S.nums[S.index-1]}`：已经不下降，无需操作'),
        'res += nums[index - 1] - nums[index]': '后缀整体加 `{nums[index-1]} − {nums[index]}`，`res` → =={res}==',
        'return res': '遍历完，所有下降处的差之和就是答案 `{res}`',
    },
    cards=dict(
        one_liner='每次只改一个后缀，下降多少就补多少',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一次操作选任意子数组，每个元素加同一个正整数 `x`',
                 '求让数组非递减所需的 ==`x` 之和== 的最小值',
                 '示例：`[3,3,2,1]` → `2`；`[5,1,2,3]` → `4`'],
        quote='每次修改就应该修改nums中的一个后缀。',
        quote_src='—— yiduobo 题解原文',
        idea=['改 `nums[left..right]` 会让右边元素更可能变小，所以干脆改到末尾',
              '每次都改后缀，则前面的修改对 `nums[i-1]` 和 `nums[i]` 同时生效，比较时相当于没改',
              '于是只看相邻两个数：下降了多少，就加多少'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：只累计下降的差，上升的位置不能抵消',
                 '后缀操作覆盖前面的修改，所以相邻比较互不影响',
                 '对比灵神：灵神用差分数组，取负的差分之和；结论相同',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
