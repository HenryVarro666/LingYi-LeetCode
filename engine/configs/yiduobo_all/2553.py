
def _cur(S):
    nums, res = S['nums'], S.get('res', [])
    cum = 0
    for i in range(len(nums) - 1, -1, -1):
        cum += len(str(nums[i]))
        if cum > len(res):
            return i
    return -1


CONFIG = dict(
    num=2553, title='分割数组中数字的数位', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='模 10 除 10 逐位分离 · 倒着遍历',
    tags=[],
    code='''
class Solution(object):
    def separateDigits(self, nums):

        res = []
        for x in nums[::-1]:
            while x:
                res.append(x % 10)
                x //= 10
        
        res.reverse()
        return res
''',
    call='Solution().separateDigits([13, 25, 83, 77])',
    expect=[1, 3, 2, 5, 8, 3, 7, 7],
    views=[
        dict(type='array', var='nums', label='nums（倒着遍历 nums[::-1]）', h=220,
             color=lambda S, i, v: 'blue' if i == _cur(S) else None,
             dim=lambda S, i, v: i > _cur(S)),
        dict(type='array', var='res', label='res（倒序放入，最后 reverse）', h=240,
             color=lambda S, i, v: 'green' if i == len(S['res']) - 1 and S['_line'] == 7 else None),
    ],
    watch=[('x', 'x', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 用来收集拆出的数位',
        'for x in nums': '倒着遍历，当前数 `x = {x}`',
        'while x': lambda S, B, r: (f'`x = {S.x}` 非 0，继续分离' if S.x else '`x` 变成 0，这个数分离完，取前一个数'),
        'res.append': '`{x} % 10 = {x % 10}`：取出个位 → `{res}`',
        'x //= 10': '`x //= 10`，去掉个位，`x` 变成 `{x}`',
        'res.reverse()': '数组倒着走、数位也是倒着出，==整体翻转一次==就是正序 → `{res}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='倒着处理每个数，最后只需翻转一次',
        complexity='时间 `O(n log U)`，空间 `O(n log U)`',
        problem=['把每个数的各位拆开，按原顺序放入数组',
                 '示例：`[7,1,3,9]` → `[7,1,3,9]`',
                 '本视频：`[13,25,83,77]` → `[1,3,2,5,8,3,7,7]`'],
        quote='单个数字分离出的结果是倒序的，为了方便处理，在这里可以从后往前遍历这些数字并进行逐位分离，这样一来就只需最后进行一次总的翻转操作就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['模 10 除 10：每次拿到一个数的个位，所以单个数拆出来是倒序',
              '让数组也倒着遍历 `nums[::-1]`',
              '整个 `res` 恰好是目标的逆序，最后 `reverse()` 一次即可'],
        summary=['时间 `O(n log U)`，`U` 为数组最大值',
                 '易错：`while x` 要在 `x` 为 0 时停止；本题 `x >= 1`，不会有 0',
                 '原文为 Python 2 写法，`x /= 10` 已改为 `x //= 10`',
                 '对比灵神：灵神用 `reversed(nums)`，思路相同；另给了转字符串的写法'],
    ),
)
