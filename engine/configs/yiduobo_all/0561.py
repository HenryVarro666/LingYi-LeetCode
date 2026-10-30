CONFIG = dict(
    num=561, title='数组拆分 I', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='排序 + 隔一个取一个',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def arrayPairSum(self, nums):

        nums = sorted(nums)
        res = 0
        for index in range(0, len(nums), 2):
            res += nums[index]
        return res
''',
    call='Solution().arrayPairSum([6,2,6,5,1,2])',
    expect=9,
    views=[
        dict(type='text', fn=lambda S: (f"相邻两数一组 `({S['nums'][S['index']]}, {S['nums'][S['index']+1]})`，较小的 ==`{S['nums'][S['index']]}`== 计入，累计 `{S['res']}`" if 'index' in S and 'res' in S and S['_line'] >= 7 else '')),
        dict(type='array', var='nums', h=300, pointers={'index': 'yellow'},
             color=lambda S, i, v: ('green' if i % 2 == 0 else 'pink') if 'index' in S and 'res' in S and i % 2 == 0 and i <= S['index'] else (('blue' if i % 2 == 1 and i <= S['index'] + 1 else None) if 'index' in S and 'res' in S else None)),
    ],
    watch=[('index', 'index', 'yellow'), ('res', 'res', 'green')],
    captions={
        'nums = sorted': '从小到大排序：`{nums}`。小的跟小的一组，免得小数拖累大数',
        'res = 0': '`res` 累计每组中较小的数',
        'for index': lambda S, B, r: (f'`index = {S.index}`：排好序后第 `{S.index}` 个数是这一组的较小数' if S.index != B.get('index') else '偶数下标都取完了，循环结束'),
        'res += nums[index]': '组里较小的是 `nums[{index}] = {nums[index]}`，`res` = {res}',
        'return res': '所有偶数项之和 `{res}`',
    },
    cards=dict(
        one_liner='排序后两两分组，所有偶数项之和就是答案',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给定 `2n` 个整数，分成 `n` 对，使每对中较小数之和最大',
                 '示例：`[1,4,3,2]` → `4`（`(1,2)` 和 `(3,4)`）',
                 '本视频：`[6,2,6,5,1,2]` → `9`'],
        quote='小的跟小的一起，大的跟大的一起，免得小的影响了大的。……所有偶数项之和就是最后的答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['每组只算较小数，大数「陪跑」是浪费', '让小数和相近的数组队，浪费最少', '排序后下标 0,2,4,… 的数就是各组较小数'],
        summary=['时间 `O(n log n)`，`sorted` 另开数组，空间 `O(n)`',
                 '下标从 0 开始，每次 +2，取的是偶数下标',
                 '不要取奇数项（那是每组较大数）',
                 '原文为 Python 2 风格，本题无需改动'],
    ),
)
