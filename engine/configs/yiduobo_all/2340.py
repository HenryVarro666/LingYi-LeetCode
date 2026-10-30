CONFIG = dict(
    num=2340, title='生成有效数组的最少交换次数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='最小值移到最前 · 最大值移到最后',
    tags=[],
    code='''
class Solution(object):
    def minimumSwaps(self, nums):

        ma = mi = 0
        n = len(nums)
        for index in range(1, n):
            if nums[index] < nums[mi]:
                mi = index
            if nums[index] >= nums[ma]:
                ma = index
        
        res = mi + len(nums) - 1 - ma
        if ma < mi:
            res -= 1
        return res
''',
    call='Solution().minimumSwaps([3,4,5,5,3,1])',
    expect=6,
    views=[
        dict(type='text', fn=lambda S: (f"最小值在下标 `{S['mi']}`：移到最前要 =={S['mi']}== 次；最大值在下标 `{S['ma']}`：移到最后要 =={len(S['nums']) - 1 - S['ma']}== 次"
                                       if 'mi' in S and 'n' in S else '')),
        dict(type='array', var='nums', pointers={'mi': 'blue', 'ma': 'pink'}, h=300,
             color=lambda S, i, v: ('blue' if i == S['mi'] else 'pink' if i == S['ma'] else None) if 'mi' in S else None),
        dict(type='text', fn=lambda S: ('`ma < mi`：最大值在最小值左边，两者会交叉换位一次，重复算了 1 次' if 'res' in S and S['ma'] < S['mi'] else ''), size=26),
    ],
    watch=[('mi', 'mi', 'blue'), ('ma', 'ma', 'pink'), ('res', 'res', 'green')],
    captions={
        'ma = mi = 0': '`mi` 记最小值的下标、`ma` 记最大值的下标，先都指向第 0 个',
        'n = len': '`n = {n}`',
        'for index': '从下标 `{index}` 开始往后看',
        'if nums[index] < nums[mi]': '`nums[{index}] = {nums[index]}` 是否 ==严格小于== 当前最小 `nums[{mi}] = {nums[mi]}`？严格小于 → 保留==最靠左==的最小值',
        'mi = index': '出现更小的数：`mi` → {mi}',
        'if nums[index] >= nums[ma]': '`nums[{index}] = {nums[index]}` 是否 ==大于等于== 当前最大 `nums[{ma}] = {nums[ma]}`？带等号 → 保留==最靠右==的最大值',
        'ma = index': '最大值（含相等）更靠右了：`ma` → {ma}',
        'res = mi': '最小值移到最前：`mi = {mi}` 次；最大值移到最后：`n-1-ma = {n - 1 - ma}` 次 → `res = {res}`',
        'if ma < mi': lambda S, B, r: (f'`ma = {S.ma} < mi = {S.mi}`：最大值在最小值左边，两个数会==互相交换一次==，这一次被算了两遍'
                                        if S.ma < S.mi else f'`ma = {S.ma} > mi = {S.mi}`：两条移动路线不交叉，不用修正'),
        'res -= 1': '重复的一次要扣掉：`res` → {res}',
        'return res': '最少交换 `{res}` 次',
    },
    cards=dict(
        one_liner='最小值走到最前、最大值走到最后，交叉时少算 1 次',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次可交换相邻两个数，要让数组满足：==最小值在最前、最大值在最后==',
                 '最小值或最大值有多个时，只要有一个到位就行',
                 '示例：`[3,4,5,5,3,1]` → `6`'],
        quote='为了使得交换次数最少，就应该将==首次出现的最小值==以及==最后一次出现的最大值==分别移动到数组的首部和尾部。',
        quote_src='—— yiduobo 题解原文',
        idea=['选最左的最小值（离队首最近）、最右的最大值（离队尾最近）',
              '次数 = `mi + (n - 1 - ma)`',
              '若 `mi > ma`：两个数在路上会交换一次，这次被算了两遍，答案减 1'],
        summary=['时间 `O(n)`，空间 `O(1)`，一次遍历',
                 '最小值用 `<`（取最左），最大值用 `>=`（取最右），比较符号不能写反',
                 '原文变量名是 `ma < mi` 时减 1：即最大值在最小值左边',
                 '原文 Python 2 写法在 Python 3 下无需改动'],
    ),
)
