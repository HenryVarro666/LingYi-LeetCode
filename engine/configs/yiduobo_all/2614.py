CONFIG = dict(
    num=2614, title='对角线上的质数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='逐行检测 + 暴力判质数',
    tags=['灵神题单', '难度分 1375'],
    code='''
class Solution(object):
    def diagonalPrime(self, nums):

        def check(x):
            if x == 1:
                return False
            p = 2
            while p * p <= x:
                if x % p == 0:
                    return False
                p += 1
            
            return True

        n = len(nums)
        res = 0
        for i in range(n):
            if nums[i][i] > res and check(nums[i][i]):
                res = nums[i][i]
            if nums[i][n - i - 1] > res and check(nums[i][n - i - 1]):
                res = nums[i][n - i - 1]
        
        return res
''',
    call='Solution().diagonalPrime([[1,2,3],[5,17,7],[9,11,10]])',
    expect=17,
    views=[
        dict(type='text', fn=lambda S: (f"检测 `x = {S['_inner']['x']}`：`p = {S['_inner'].get('p', 2)}`，`p×p = {S['_inner'].get('p', 2) ** 2}`"
                                         if 'x' in S.get('_inner', {}) else ''), size=26),
        dict(type='grid', var='nums', label='nums（蓝 = nums[i][i]，粉 = nums[i][n-i-1]）', cell=110, h=330,
             cursors=[('i', 'i', 'blue'), ('i', 'n - i - 1', 'pink')]),
        dict(type='text', fn=lambda S: f"目前最大的对角线质数 `res = {S['res']}`" if 'res' in S else '', size=28),
    ],
    watch=[('i', 'i', 'blue'), ('res', 'res', 'green')],
    captions={
        'if x == 1': lambda S, B, r: ('`x = 1`：==1 不是质数==，单独排除' if S.x == 1 else f'`x = {S.x}` 不是 1，继续试除'),
        'p = 2': '从 `p = 2` 开始试除',
        'while p * p <= x': lambda S, B, r: (f'`p×p = {S.p * S.p} <= {S.x}`：还需要试除' if S.p * S.p <= S.x
                                              else f'`p×p = {S.p * S.p} > {S.x}`：再往后不会有因子了，停止'),
        'if x % p == 0': '`{x} % {p} = {x % p}` → {"==整除，不是质数==" if x % p == 0 else "不整除"}',
        'return False': lambda S, B, r: ('`x = 1` 不是质数 → `False`' if S.x == 1 else f'`{S.x}` 有因子 `{S.p}` → `False`'),
        'p += 1': '`p` → {p}',
        'return True': '试到 `p×p > x` 都没有因子 → `{x}` 是质数',
        'n = len(nums)': '`n = {n}`：第 `i` 行的对角线元素是 `[i][i]` 和 `[i][n-i-1]`',
        'res = 0': '`res` 记录当前最大的对角线质数',
        'for i in range(n)': '处理第 `{i}` 行',
        'if nums[i][i] > res': lambda S, B, r: (f'`nums[{S.i}][{S.i}] = {S.nums[S.i][S.i]} > res = {S.res}`：可能刷新答案 → 检测质数'
                                                if S.nums[S.i][S.i] > S.res
                                                else f'`nums[{S.i}][{S.i}] = {S.nums[S.i][S.i]} <= res = {S.res}`：==不会刷新答案，不用检测=='),
        'if nums[i][n - i - 1] > res': lambda S, B, r: (f'`nums[{S.i}][{S.n - S.i - 1}] = {S.nums[S.i][S.n - S.i - 1]} > res = {S.res}`：可能刷新答案 → 检测质数'
                                                        if S.nums[S.i][S.n - S.i - 1] > S.res
                                                        else f'`nums[{S.i}][{S.n - S.i - 1}] = {S.nums[S.i][S.n - S.i - 1]} <= res = {S.res}`：不会刷新答案，不用检测'),
        'res = nums[i][i]': '主对角线元素是更大的质数 → `res = {res}`',
        'res = nums[i][n - i - 1]': '副对角线元素是更大的质数 → `res = {res}`',
        'return res': '遍历完所有行，答案 `{res}`',
    },
    cards=dict(
        one_liner='题面已经告诉了对角线位置：每行取两个数，检测质数，更新最大值',
        complexity='时间 `O(n√U)`，空间 `O(1)`',
        problem=['二维数组 `nums`，找位于==至少一条对角线==上的最大质数，没有返回 `0`',
                 '第 `i` 行的对角线元素：`nums[i][i]` 和 `nums[i][n-i-1]`',
                 '本视频：`[[1,2,3],[5,17,7],[9,11,10]]` → `17`'],
        quote='题目描述中已经指明了每一行位于对角线上的数是哪两个，于是只需遍历每行，检测当前行位于对角线上的数是否为质数，如果是，则更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['最多只有 `2n` 个数要检测，不用筛法，==直接暴力试除==就够了',
              '`check(x)`：`x == 1` 不是质数；`p` 从 2 试到 `p*p > x`',
              '先和 `res` 比大小，不会刷新答案的数连检测都省了'],
        summary=['时间 `O(n√U)`，`U` 是对角线上的最大值，空间 `O(1)`',
                 '易错：==1 不是质数==，`check` 里要先排除',
                 '用 `p * p <= x` 作循环条件，避免调用开方函数',
                 '奇数阶矩阵的中心元素在两条对角线上，会被检测两次，结果不变',
                 '原文代码已是 Python 3 可运行写法，未作修改'],
    ),
)
