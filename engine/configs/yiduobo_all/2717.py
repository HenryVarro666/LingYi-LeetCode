CONFIG = dict(
    num=2717, title='半有序排列', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='遍历记录 1 和 n 的下标', tags=[],
    code='''
class Solution(object):
    def semiOrderedPermutation(self, nums):

        p1 = p2 = None
        for index in range(len(nums)):
            if nums[index] == 1:
                p1 = index
            if nums[index] == len(nums):
                p2 = index
        
        res = p1 + len(nums) - p2 - 1
        if p1 > p2:
            res -= 1
        return res
''',
    call='Solution().semiOrderedPermutation([2,5,1,3,4])',
    expect=4,
    views=[
        dict(type='array', var='nums', pointers={'index': 'yellow', 'p1': 'blue', 'p2': 'pink'}, h=220,
             color=lambda S, i, v: 'blue' if S.get('p1') == i else 'pink' if S.get('p2') == i else None),
        dict(type='text', h=110, fn=lambda S: (f"`1` 的下标 `p1 = {S['p1']}`，`n` 的下标 `p2 = {S['p2']}`" if S.get('p1') is not None or S.get('p2') is not None else '还没找到 1 和 n')),
    ],
    watch=[('index', 'index', 'yellow'), ('p1', 'p1', 'blue'), ('p2', 'p2', 'pink'), ('res', 'res', 'green')],
    captions={
        'p1 = p2 = None': '先准备两个变量，记录 `1` 和 `n` 的下标',
        'if nums[index] == 1': '`nums[{index}] = {nums[index]}`，是 `1` 吗？{"是，记下 p1" if nums[index] == 1 else "不是"}',
        'p1 = index': '`1` 在下标 `{p1}`，要换到头部需要 `{p1}` 次交换',
        'if nums[index] == len': '`nums[{index}] = {nums[index]}`，是 `n = {len(nums)}` 吗？{"是，记下 p2" if nums[index] == len(nums) else "不是"}',
        'p2 = index': '`n` 在下标 `{p2}`，换到尾部需要 `n - p2 - 1 = {len(nums) - p2 - 1}` 次',
        'res = p1': '直观答案：`p1 + n - p2 - 1 = {p1} + {len(nums)} - {p2} - 1` = =={res}==',
        'if p1 > p2': '`p1 > p2`（{p1} > {p2}）→ {"成立：1 和 n 一定会互相交换一次，这次被算了两遍" if p1 > p2 else "不成立：两者不会相遇，不用修正"}',
        'res -= 1': '重复算的那一次减掉：`res = {res}`',
        'return': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='1 换到头、n 换到尾，两者交叉时多算了一次要减掉',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['排列第一个数是 `1`、最后一个数是 `n` 叫半有序',
                 '每次交换相邻两个元素，求最少操作次数',
                 '示例：`[2,1,4,3]` → `2`'],
        quote='不妨设1的初始下标为p1，n的初始下标为p2，那么将1交换到头部所需的交换次数就是p1，而将n交换到尾部所需的交换次数就是n - p2 - 1，因此直观来看最终答案就是p1 + n - p2 - 1。',
        quote_src='—— yiduobo 题解',
        idea=['一趟遍历，记下 `1` 和 `n` 的下标 `p1`、`p2`',
              '直观答案是 `p1 + n - p2 - 1`',
              '若 `p1 > p2`，它们之间的那次交换被两边各算一次，要 `-1`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '==特别注意 `p1 > p2` 时要减 1==，原文强调的易错点',
                 '尾部要移动的次数是 `n - p2 - 1`，不是 `n - p2`',
                 '其他数字的位置不影响答案'],
    ),
)
