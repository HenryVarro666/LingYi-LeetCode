def _t(S):
    if 'min_num' in S and 'g' in S:
        mn = S['min_num']
        return f"`g = {S['g']}`，目前最小的合格数 `min_num = {mn}`" if mn is not None else f"`g = {S['g']}`，还没找到合格的数（`min_num = None`）"
    if 'g' in S:
        return f"到目前为止 numsDivide 的最大公约数 `g = {S['g']}`"
    return '先求 numsDivide 所有数的最大公约数 g'


CONFIG = dict(
    num=2344, title='使数组可以被整除的最少删除次数', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='最大公约数 + 两趟遍历',
    tags=['灵神题单', '数学算法', '难度分 1641'],
    code='''
class Solution(object):
    def minOperations(self, nums, numsDivide):

        g = numsDivide[0]
        for num in numsDivide[1:]:
            x, y = num, g
            while y:
                x, y = y, x % y
            
            g = x
        
        min_num = None
        for num in nums:
            if g % num == 0:
                if min_num is None or min_num > num:
                    min_num = num
        
        if min_num is None:
            return -1
        
        res = 0
        for num in nums:
            if num < min_num:
                res += 1
        
        return res
''',
    call='Solution().minOperations([2,3,2,4,3], [6,9,3])',
    expect=2,
    views=[
        dict(type='array', var='numsDivide', h=150, label='numsDivide'),
        dict(type='array', var='nums', h=170, label='nums',
             color=lambda S, i, v: ('green' if 'g' in S and S.get('min_num') is not None and v == S['min_num'] else None)),
        dict(type='text', fn=_t, h=110),
    ],
    watch=['g', 'x', 'y', 'min_num', 'res'],
    captions={
        'g = numsDivide[0]': '先拿第一个数当 `g = {g}`，后面逐个和它求最大公约数',
        'x, y = num, g': '把 numsDivide 的下一个数 `{x}` 并进来：辗转相除求 `gcd({x}, {y})`，`g` 要同时整除两者',
        'while y': '`y = {y}`：不为 0 就继续',
        'x, y = y, x % y': '`(x, y)` → `({x}, {y})`，即 `gcd(x, y) = gcd(y, x % y)`',
        'g = x': 'y 为 0，x 就是公约数：`g = {g}`',
        'min_num = None': '准备第一趟遍历：找 nums 里能整除 g 的最小数',
        'if g % num == 0': '`{g} % {num} = {g % num}` → ' + '{"==能整除，是候选==" if g % num == 0 else "不能整除，跳过"}',
        'if min_num is None or': '`min_num` 为 None 或比 `{num}` 大才更新：现在 `min_num = {min_num}`',
        'min_num = num': '`min_num = {min_num}`',
        'if min_num is None': lambda S, B, r: '没有任何数能整除 g → 无解，返回 `-1`' if S.min_num is None else f'找到了：`min_num = {S.min_num}`。比它小的数都得删',
        'if num < min_num': lambda S, B, r: f'`{S.num} < {S.min_num}` → ' + ('比最小合格数小，必须删掉' if S.num < S.min_num else '不比它小，保留'),
        'res += 1': '删除计数 `res = {res}`',
        'return res': '最少删除 `{res}` 个',
    },
    cards=dict(
        one_liner='最小元素该是 g 的因子：先求 g，再数比它小的',
        complexity='时间 `O(m log U + n)`，空间 `O(1)`',
        problem=['给两个正整数数组 `nums` 和 `numsDivide`，可以从 `nums` 删任意个元素',
                 '要使 `nums` 的最小元素能整除 `numsDivide` 的所有元素，求最少删除次数，不行返回 `-1`',
                 '本视频：`[2,3,2,4,3]`，`[6,9,3]` → `2`'],
        quote='实际上每次执行的删除操作都应该删除最小值……能被numsDivide中所有数整除的最大整数，必然是numsDivide中所有数的最大公约数，不妨记为g。',
        quote_src='—— yiduobo 题解原文',
        idea=['删除只会删最小值，所以目标是：找 `nums` 中最小的、能整除 `g` 的数',
              '`g` 用辗转相除，逐个并入 `numsDivide` 的元素',
              '第一趟遍历找 `min_num`，找不到就 `-1`；第二趟数比它小的个数'],
        summary=['时间 `O(m log U + n)`，空间 `O(1)`',
                 '易错：`min_num` 找不到时要返回 `-1`，不能直接去数',
                 '相同的数（如两个 2）都要计入删除数，所以用 `<` 不是 `<=`',
                 '原文已是可直接运行的写法，只删去了类型说明；示例取 `[6,9,3]` 缩短步数'],
    ),
)
