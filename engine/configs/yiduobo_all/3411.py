CONFIG = dict(
    num=3411, title='最长乘积等价子数组', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举子数组 + 增量维护 gcd/lcm',
    tags=['数学算法', '难度分 2300'],
    code='''
class Solution(object):
    def maxLength(self, nums):
        
        def calc(gcd, v, lcm):
            x, y = gcd, v
            while y:
                x, y = y, x % y
            nxt_gcd = x

            x, y = lcm, v
            while y:
                x, y = y, x % y
            nxt_lcm = lcm * v // x

            return nxt_gcd, nxt_lcm

        res = 1
        for start in range(len(nums)):
            mul = nums[start]
            gcd = nums[start]
            lcm = nums[start]
            for end in range(start + 1, len(nums)):
                mul *= nums[end]
                gcd, lcm = calc(gcd, nums[end], lcm)
                if gcd * lcm == mul:
                    res = max(res, end - start + 1)
        
        return res
''',
    call='Solution().maxLength([2,3,4,5,6])',
    expect=3,
    max_steps=60,
    views=[
        dict(type='array', var='nums', pointers={'start': 'blue', 'end': 'pink'}, window=('start', 'end'), h=240,
             dim=lambda S, i, v: 'start' in S and 'end' in S and 'res' in S and not (S['start'] <= i <= S['end'])),
        dict(type='text', fn=lambda S: (f"`mul = {S['mul']}`，`gcd × lcm = {S['gcd']} × {S['lcm']} = {S['gcd']*S['lcm']}`" if all(k in S for k in ('mul', 'gcd', 'lcm')) and isinstance(S['gcd'], int) and isinstance(S['lcm'], int) and S['_line'] in (25, 26) else '')),
    ],
    watch=[('start', 'start', 'blue'), ('end', 'end', 'pink'), 'mul', 'gcd', 'lcm', ('res', 'res', 'green')],
    skip=['x, y = y, x % y', 'while y:', 'x, y = gcd, v', 'x, y = lcm, v', 'nxt_gcd = x', 'nxt_lcm = lcm', 'return nxt_gcd'],
    captions={
        'res = 1': '单个数不算数，`res` 初值 1（长度至少 2 的子数组才有意义）',
        'for start in': '枚举起点 `start = {start}`',
        'lcm = nums[start]': '子数组 `[{nums[start]}]`：乘积、gcd、lcm 都从 `{nums[start]}` 起步',
        'mul *= nums[end]': '终点右扩到 `end = {end}`，乘积 ==直接乘上== `{nums[end]}` = {mul}（不用重算）',
        'gcd, lcm = calc': '调用 `calc`：在上一轮基础上，用辗转相除更新 `gcd`，再用 `lcm × v // gcd(lcm, v)` 更新 `lcm`',
        'for end in': '终点 `end` 从 `start + 1` 起逐个右扩',
        'if gcd * lcm': '`{gcd} × {lcm} = {gcd*lcm}` 和 `mul = {mul}`：{"相等，子数组乘积等价" if gcd*lcm == mul else "不相等，不满足"}',
        'res = max': '长度 `end - start + 1 = {end-start+1}`，`res = max({B.res}, {end-start+1}) = {res}`',
        'return res': '全部子数组查完，最长 ==`{res}`==',
    },
    cards=dict(
        one_liner='数据只有 100，枚举所有子数组，增量维护乘积/gcd/lcm',
        complexity='时间 `O(n^2 log U)`，空间 `O(1)`',
        problem=['数组满足 `prod == gcd × lcm` 叫乘积等价',
                 '求 `nums` 里最长的乘积等价子数组',
                 '示例：`[2,3,4,5,6]` → `3`'],
        quote='题目的数据规模较小，因此可以直接暴力枚举所有子数组的起点start以及终点end，然后检测子数组是否为乘积等价数组。',
        quote_src='—— yiduobo 题解',
        idea=['`nums` 长度 ≤ 100，直接 `O(n^2)` 枚举起点终点',
              '`nums[start:end+1]` 的乘积、gcd、lcm 都在 `nums[start:end]` 基础上增量更新',
              'gcd 用辗转相除，lcm = `lcm × v // gcd(lcm, v)`'],
        summary=['时间 `O(n^2 log U)`，空间 `O(1)`',
                 '易错：`res` 初值 1，lcm 更新要用除以 `gcd(lcm, v)` 的结果',
                 '函数参数名 `gcd`、`lcm` 遮蔽了内置函数，原文如此',
                 '更优：滑动窗口 + 两两互质，`O(n log U)`（灵神方法二）'],
    ),
)
