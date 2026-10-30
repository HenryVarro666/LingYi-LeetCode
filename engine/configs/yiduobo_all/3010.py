def _pos(S):
    v = S.get('v')
    return S['nums'].index(v, 1) if v is not None and 'nums' in S else None


CONFIG = dict(
    num=3010, title='将数组分成最小总代价的子数组 I', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='一趟遍历维护最小、次小',
    tags=['灵神题单', '难度分 1292'],
    code='''
class Solution(object):
    def minimumCost(self, nums):

        first = second = None
        for v in nums[1:]:
            if first is None or v < first:
                first, second = v, first
            elif second is None or v < second:
                second = v
        
        return nums[0] + first + second
''',
    call='Solution().minimumCost([7,5,4,9,1,6,2])',
    expect=10,
    views=[
        dict(type='array', var='nums', label='nums（绿 = 数组头，蓝 = 当前 v）', cell=100, h=220,
             color=lambda S, i, v: 'green' if i == 0 else ('blue' if i == _pos(S) else None)),
        dict(type='text', h=110, size=32, fn=lambda S: f"最小 `first = {S.get('first')}`，次小 `second = {S.get('second')}`" if 'first' in S else ''),
    ],
    watch=[('v', 'v', 'blue'), ('first', 'first', 'yellow'), ('second', 'second', 'orange')],
    captions={
        'first = second = None': '`first` 记最小、`second` 记次小，一开始都还没有',
        'for v in nums[1:]': lambda S, B, r: ('扫描结束，`nums[1:]` 都看过了' if 'v' in B and B.v == S.v == S.nums[-1] else f'从下标 1 开始扫描：`v = {S.v}`（`nums[0]` 是数组头，不参与比较）'),
        'if first is None or v < first': lambda S, B, r: ('`first` 还是空 → 成立，`v` 直接当最小' if S.first is None else f'`v = {S.v}` < `first = {S.first}`？' + ('成立，它是新的最小' if S.v < S.first else '不成立')),
        'first, second = v, first': '`v` 成为新的最小，原来的最小退位成次小：`first = {first}`，`second = {second}`',
        'elif second is None or v < second': lambda S, B, r: ('`second` 还是空 → 先收下' if S.second is None
                                                             else f'`v = {S.v}` 不比最小小，但比 `second = {S.second}` 小吗？' + ('成立' if S.v < S.second else '不成立')),
        'second = v': '`v` 比次小还小 → `second = {second}`',
        'return nums[0]': '`nums[0] + first + second = {nums[0]} + {first} + {second}` = =={ret}==',
    },
    cards=dict(
        one_liner='划分没有额外限制：挑最小的两个数当另外两段的起点',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 `nums` 分成 3 段连续子数组，每段代价是它的==首个元素==',
                 '求三段代价之和的最小值',
                 '本视频：`[7,5,4,9,1,6,2]` → `10`'],
        quote='题目对子数组的划分没有任何额外的要求，那么为了让总代价最小，就应该选择最小的两个数作为子数组的起点。',
        quote_src='—— yiduobo 题解原文',
        idea=['数组头 `nums[0]` 必是第一段起点',
              '剩下的数里一趟遍历，同时维护最小 `first` 和次小 `second`',
              '遇到更小的数：旧最小退位成次小；介于两者之间：只更新次小'],
        summary=['时间 `O(n)`，空间 `O(1)`，不用排序',
                 '易错：从 `nums[1:]` 开始找，数组头不参与；`first/second` 初始为 `None` 要先判空',
                 '`first, second = v, first` 是同时赋值，次小拿到的是旧的最小',
                 '原文已是可直接运行的写法，无需改动'],
    ),
)
