CONFIG = dict(
    num=3769, title='二进制反射排序', difficulty='Easy', category='位运算',
    author='yiduobo', technique='先算反射值，再双关键字排序', tags=['灵神题单', '难度分 1364'],
    code='''
class Solution(object):
    def sortByReflection(self, nums):

        r = {}
        for v in set(nums):
            digits = []
            x = v
            while x:
                digits.append(x % 2)
                x //= 2

            x = 0
            for d in digits:
                x = x * 2 + d

            r[v] = x

        return sorted(nums, key=lambda d:(r[d], d))
''',
    call='Solution().sortByReflection([6, 5, 3, 6])',
    expect=[3, 6, 6, 5],
    views=[
        dict(type='text', size=26, fn=lambda S: (f"当前数 `v = {S['v']}`，二进制从低位到高位取出：`{S['digits']}`" if 'v' in S and 'digits' in S else '')),
        dict(type='array', var='digits', h=150, label='digits（低位在前）', color=lambda S, i, v: 'cyan'),
        dict(type='text', size=26, fn=lambda S: (f"拼回数字：`x = x*2 + d` → ==x = {S['x']}==" if 'd' in S and S.get('_line', 0) >= 14 else '')),
        dict(type='map', var='r', fmt=lambda k, v: f'{k} → {v}', h=230),
        dict(type='array', var='nums', h=150, label='nums'),
    ],
    watch=[('v', 'v', 'blue'), ('x', 'x', 'yellow'), ('digits', 'digits', 'cyan'), ('r', 'r', 'green')],
    captions={
        'for v in set(nums)': '相同的数反射值也相同，所以对去重后的 `v = {v}` 只算一次',
        'digits.append(x % 2)': '取出最低位 `{x} % 2`，放进 `digits` → `{digits}`（先取出的是低位）',
        'x //= 2': '右移一位：`x` 变成 `{x}`；为 0 时二进制取完',
        'while x': lambda S, B, r: (f'`x = {S.x}` 非 0，还有高位没取' if S.x else '`x = 0`，所有二进制位都取完了'),
        'x = x * 2 + d': '按顺序把 `digits` 当作新的二进制：`x*2 + {d}` = =={x}==，==先取出的低位成了新数的高位==',
        'r[v] = x': '`v = {v}` 的反射值是 `{x}`，记入 `r`',
        'return sorted': '`r[d]` 作第一关键字、`d` 作第二关键字排序 → `{ret}`',
    },
    max_steps=80,
    cards=dict(
        one_liner='先算出每个数的反射值，再用「反射值，原值」排序',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['二进制反射 = 把正整数二进制按顺序反转后转回十进制',
                 '按反射值升序排序，反射值相同则按原值升序',
                 '示例：`[3,6,5,8]` → `[8,3,6,5]`；本视频：`[6,5,3,6]`'],
        quote='先对nums一趟遍历，按照题目描述计算出每个nums[index]对应的反射值r[index]，接下来以r[index]为第一关键字，nums[index]为第二关键字对nums进行排序即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['不停取 `x % 2`、`x //= 2`，低位先进 `digits`',
              '再从头扫 `digits`：`x = x*2 + d`，==先进的低位变成高位==，这就是反转',
              '用字典 `r` 存每个值的反射值，`sorted` 的 key 取 `(r[d], d)`'],
        summary=['时间 `O(n log n)`（含排序），空间 `O(n)`',
                 '反转的是「去掉前导零」的二进制，所以 `while x` 取到 0 就停',
                 '`set(nums)` 去重：相同的数只算一次反射值',
                 '原文为 Python 2 风格，除法已是 `//`，无需修改'],
    ),
)
