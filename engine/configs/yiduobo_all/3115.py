CONFIG = dict(
    num=3115, title='质数的最大距离', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='先列出质数表 + 前后各扫一遍',
    tags=['灵神题单·数学算法', '难度分 1294'],
    code='''
class Solution(object):
    def maximumPrimeDifference(self, nums):

        prime = set()
        for v in range(2, 101):
            x = 2
            flag = True
            while x * x <= v:
                if v % x == 0:
                    flag = False
                    break
                x += 1
            
            if flag:
                prime.add(v)
        
        n = len(nums)
        for index in range(n):
            if nums[index] in prime:
                first = index
                break
        
        for index in range(n - 1, -1, -1):
            if nums[index] in prime:
                last = index
                break
        
        return last - first
''',
    call='Solution().maximumPrimeDifference([4, 1, 9, 2, 8, 6, 3, 8, 9])',
    expect=3,
    skip=['for v in range(2, 101)', 'x = 2', 'flag = True', 'while x * x', 'if v % x', 'flag = False',
          'x += 1', 'if flag', 'prime.add(v)', 'break'],
    views=[
        dict(type='set', var='prime', label='prime（1 到 100 里的质数，共 25 个）', h=220, font=22,
             fmt=lambda x: str(x)),
        dict(type='array', var='nums', label='nums（箭头 = index；蓝 = first，粉 = last，绿 = 质数）', cell=84, h=240,
             pointers={'index': 'blue'},
             color=lambda S, k, v: ('blue' if k == S.get('first') else 'pink' if k == S.get('last') else
                                    ('green' if v in S['prime'] else None)) if 'prime' in S else None),
    ],
    watch=['index', ('first', 'first', 'blue'), ('last', 'last', 'pink')],
    captions={
        'prime = set()': '先把 1 到 100 里的质数全找出来放进集合 `prime`：每个 `v` 试除 `2 .. sqrt(v)`，没有因子就是质数（这段循环不逐步演示）',
        'n = len(nums)': '`nums` 里的数都在 1 到 100 之间，查 `prime` 就知道是不是质数',
        'for index in range(n):': '从左往右扫，找最靠前的质数：`index = {index}`',
        'if nums[index] in prime': lambda S, B, r: (f'`nums[{S.index}] = {S.nums[S.index]}`' +
                                                    (' ==在 prime 里== → 质数' if S.nums[S.index] in S.prime else ' 不在 prime 里 → 继续')),
        'first = index': '最靠前的质数下标：`first = {first}`，找到就停',
        'for index in range(n - 1, -1, -1)': '再从右往左扫，找最靠后的质数：`index = {index}`',
        'last = index': '最靠后的质数下标：`last = {last}`，找到就停',
        'return last - first': '`last − first` = `{last} − {first}` = =={ret}==',
    },
    cards=dict(
        one_liner='先把质数表备好，再找最靠前和最靠后的质数',
        complexity='时间 `O(n)`（建表为常数），空间 `O(1)`',
        problem=['给整数数组 `nums`，元素大小在 1 到 100 之间',
                 '求两个质数在 `nums` 中==下标之差的最大值==（可以是同一个）',
                 '示例：`[4,2,9,5,3]` → `3`；`[4,8,2,8]` → `0`'],
        quote='由于nums中元素的范围很小，于是可以先找出1到100中的所有质数，接下来只需对nums进行一趟遍历，找出其中最靠前和最靠后的质数，然后计算二者下标之差即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['元素范围只有 1 到 100：先用试除法把质数存进集合 `prime`',
              '正着扫一遍得 `first`，倒着扫一遍得 `last`，各自遇到质数就 `break`',
              '最大距离 = `last - first`，只有一个质数时两者相等，答案为 0'],
        summary=['时间 `O(n)`，建质数表 `O(100 × 10)` 为常数，空间 `O(1)`',
                 '易错：==1 不是质数==，所以 `v` 从 2 开始建表',
                 '`while x * x <= v` 试除到根号 v 即可',
                 '原文本身可直接在 Python 3 运行，未做修改',
                 '对比灵神：灵神把筛出的 `not_prime` 当数组直接下标查询；这里用集合 `in` 查询'],
    ),
)
