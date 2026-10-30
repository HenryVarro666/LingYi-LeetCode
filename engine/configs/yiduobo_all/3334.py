import math

N0 = [2, 4, 8]

CONFIG = dict(
    num=3334, title='数组的最大因子得分', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='数据小 · 枚举移除 + 暴力算 gcd/lcm',
    tags=['动态规划', '数学算法', '专题：前后缀分解', '难度分 1519'],
    code='''
class Solution(object):
    def maxScore(self, nums):
        
        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        def calc(nums):
            if not nums:
                return 0
            
            g = nums[0]
            l = nums[0]
            for v in nums[1:]:
                g = gcd(g, v)
                l = l // gcd(l, v) * v
            
            return g * l
        
        res = calc(nums)
        for index in range(len(nums)):
            res = max(res, calc(nums[:index] + nums[index + 1:]))
        
        return res
''',
    call=f'Solution().maxScore({N0!r})',
    expect=32,
    skip=['while y:', 'x, y = y, x % y', 'def gcd', 'def calc'],
    views=[
        dict(type='text', size=26, h=70, fn=lambda S: (
            f"子数组 `{S['nums']}`：目前 gcd = =={S['g']}==，lcm = =={S['l']}==" if 'g' in S and 'l' in S and S.get('_line', 0) >= 14
            else '先算整个数组，再逐个去掉一个元素重算')),
        dict(type='array', var='nums', label='当前在算的数组（calc 的参数 nums）', h=170, cell=90,
             color=lambda S, i, v: 'blue' if S.get('_line', 0) >= 14 and i == 0 else None),
        dict(type='text', size=26, h=60, fn=lambda S: f"当前最大得分 `res` = =={S['res']}==" if 'res' in S else ''),
    ],
    watch=[('g', 'g', 'cyan'), ('l', 'l', 'orange'), ('v', 'v', 'pink'), ('res', 'res', 'green')],
    captions={
        'if not nums': lambda S, B, r: ('空数组，得分为 0' if not S.nums else f'数组 `{S.nums}` 非空，继续算'),
        'return x': 'gcd 算完，返回 =={ret}==',
        'return 0': '空数组：因子得分为 0',
        'g = nums[0]': '`g` 和 `l` 先取首个元素：一个数的 gcd、lcm 都是它自己',
        'l = nums[0]': '`l` 也先取 `nums[0]` = {l}',
        'for v in nums[1:]': lambda S, B, r: f'依次并入下一个数 `v = {S.v}`' if 'v' in S else '数组只有一个数，不用循环',
        'g = gcd(g, v)': lambda S, B, r: f'`g = gcd({S.g}, {S.v})` = =={math.gcd(S.g, S.v)}==：辗转相除求最大公约数',
        'l = l // gcd': lambda S, B, r: f'`l = {S.l} // gcd({S.l}, {S.v}) × {S.v}` = =={S.l // math.gcd(S.l, S.v) * S.v}==：lcm = a ÷ gcd × b，先除后乘',
        'return g * l': '子数组得分 `g × l = {g} × {l}` = =={ret}==',
        'res = calc(nums)': '`res` = 不移除任何元素的得分 = =={res}==',
        'for index in range': '枚举移除下标 `index`：数据规模小（n ≤ 100），暴力重算就够',
        'res = max(': '去掉下标 `{index}` 的元素，重算剩下的得分，和 `res` 比大小取大',
        'return res': '最大因子得分 =={ret}==',
    },
    cards=dict(
        one_liner='n ≤ 100：枚举去掉哪个，剩下的直接算',
        complexity='时间 `O(n² log U)`，空间 `O(n)`',
        problem=['因子得分 = 数组所有元素的 ==LCM × GCD==，空数组为 0',
                 '最多移除一个元素，求最大因子得分',
                 '示例：`[2,4,8,16]` → `64`；本视频：`[2,4,8]` → `32`（移除 2）'],
        quote='由于题目的数据规模比较小，因此可以先计算不移除任意元素时的因子得分，接下来再一趟遍历，枚举移除掉的元素，对于剩下的子数组计算因子得分并更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`calc(nums)`：空数组返回 0，否则 `g`、`l` 取首元素，逐个并入',
              '`gcd` 用辗转相除；`lcm(a,b) = a // gcd(a,b) * b`',
              '先算整个数组，再枚举 `nums[:index] + nums[index+1:]` 重算并取最大'],
        summary=['时间 `O(n² log U)`，空间 `O(n)`；`n ≤ 100`、`nums[i] ≤ 30` 完全够用',
                 '易错：移除一个元素只剩 1 个数时，得分是 `x × x`',
                 '`lcm` 先除后乘：`l // gcd(l, v) * v`',
                 '本题原文代码无需改动；视频里为缩短时长，跳过了辗转相除的内部循环',
                 '对比灵神：灵神用前后缀 gcd/lcm 数组，时间降到 `O(n log U)`'],
    ),
)
