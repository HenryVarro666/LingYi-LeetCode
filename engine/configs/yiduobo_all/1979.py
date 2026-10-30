CONFIG = dict(
    num=1979, title='找出数组的最大公约数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='一趟遍历 + 辗转相除',
    tags=['灵神题单', '数学算法', '难度分 1184'],
    code='''
class Solution(object):
    def findGCD(self, nums):

        ma = mi = nums[0]
        for num in nums[1:]:
            ma = max(ma, num)
            mi = min(mi, num)

        while mi:
            ma, mi = mi, ma % mi
        
        return ma
''',
    call='Solution().findGCD([2,5,6,9,10])',
    expect=2,
    views=[
        dict(type='array', var='nums', pointers={'num': 'blue'}, h=260,
             color=lambda S, i, v: ('cyan' if 'mi' in S and v == S['mi'] and 'num' in S and not S.get('_gcd') else None)),
        dict(type='text', fn=lambda S: (f"辗转相除：`ma = {S['ma']}`，`mi = {S['mi']}`" if 'mi' in S else ''), size=34),
    ],
    watch=[('ma', 'ma', 'orange'), ('mi', 'mi', 'cyan'), 'num'],
    captions={
        'ma = mi = nums[0]': '先拿第一个数当最大也当最小：`{ma}`',
        'for num in nums[1:]': lambda S, B, r: ('数组遍历完，`ma`、`mi` 就是最大、最小值' if 'num' in B and B.num == S.num and S.num == S.nums[-1] else f'看下一个数 `num = {S.num}`'),
        'ma = max': '最大值 `ma = max({B.ma}, {num}) = {ma}`',
        'mi = min': '最小值 `mi = min({B.mi}, {num}) = {mi}`',
        'while mi': lambda S, B, r: (f'`mi = {S.mi}` 不为 0，继续辗转相除' if S.mi else '`mi = 0`：余数为零，此时 `ma` 就是最大公约数'),
        'ma, mi = mi, ma % mi': '`ma, mi = mi, ma % mi`：`({B.ma}, {B.mi})` → `({ma}, {mi})`，较大数换成余数',
        'return ma': '最大数和最小数的最大公约数 = `{ma}`',
    },
    cards=dict(
        one_liner='一趟遍历找最值，再用辗转相除求最大公约数',
        complexity='时间 `O(n + log U)`，空间 `O(1)`',
        problem=['给整数数组 `nums`，求最大数和最小数的==最大公约数==',
                 '示例：`[2,5,6,9,10]` → `gcd(2, 10) = 2`'],
        quote='比较基础的题目，按照题目要求一趟遍历，找出数组中的最大值和最小值，然后求二者的最大公约数即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历一遍，边走边更新 `ma` 和 `mi`',
              '`gcd(a, b) = gcd(b, a % b)`，余数为 0 时停下，剩下的数就是答案'],
        summary=['时间 `O(n + log U)`，空间 `O(1)`',
                 '`ma` 与 `mi` 都从 `nums[0]` 起步，所以循环从 `nums[1:]` 开始',
                 '辗转相除不用关心谁大谁小：若 `mi > ma`，第一轮会自动交换',
                 '原文已是 Python 3 可运行，代码未改动'],
    ),
)
