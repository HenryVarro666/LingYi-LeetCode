NUMS = [5, 2, 7, 3, 2]


def _mod_color(S, k, v):
    return {1: 'blue', 2: 'pink'}.get(v % 3)


def _text(S):
    if 's' not in S:
        return '蓝 = 模 3 余 1，粉 = 模 3 余 2；0 表示「还没有」'
    s = S['s']
    if S.get('_line', 0) >= 21:
        r = s % 3
        if r == 1:
            return f'`s = {s}`，`s % 3 = 1`：剔除==一个余 1 的数==，或==两个余 2 的数=='
        if r == 2:
            return f'`s = {s}`，`s % 3 = 2`：剔除==一个余 2 的数==，或==两个余 1 的数=='
        return f'`s = {s}` 能被 3 整除，直接就是答案'
    return f'一趟扫描：累加 `s = {s}`，同时维护==最小的两个==余 1 / 余 2 的数'


def _mod_if(r):
    def f(S, B, ret):
        num = S['num']
        if num % 3 == r:
            return f'`{num} % 3 = {r}` → 用它更新 `min{r}`'
        return f'`{num} % 3 = {num % 3}` ≠ {r}'
    return f


def _first_if(r):
    def f(S, B, ret):
        num, m = S['num'], S[f'min{r}']
        if m[0] == 0:
            return f'`min{r}[0] == 0`：还没有余 {r} 的数 → `{num}` 成为最小的'
        if m[0] > num:
            return f'`min{r}[0] = {m[0]} > {num}`：`{num}` 是新的最小值，旧最小值退为次小'
        return f'`min{r}[0] = {m[0]} ≤ {num}`：不比最小的小，再看次小的'
    return f


def _second_if(r):
    def f(S, B, ret):
        num, m = S['num'], S[f'min{r}']
        if m[1] == 0:
            return f'`min{r}[1] == 0`：次小还空着 → 放 `{num}`'
        if m[1] > num:
            return f'`min{r}[1] = {m[1]} > {num}` → `{num}` 成为新的次小值'
        return f'`min{r}[1] = {m[1]} ≤ {num}`：比最小的两个都大，用不上'
    return f


def _demote(r):
    def f(S, B, ret):
        v = S[f'min{r}'][1]
        if v == 0:
            return f'原来的最小值退为次小：`min{r}[1] = 0`（原来也是空的）'
        return f'原来的最小值 `{v}` 退为次小：`min{r}[1] = {v}`'
    return f


CONFIG = dict(
    num=1262, title='可被三整除的最大和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='贪心：按 s 模 3 的余数剔除最小的数',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def maxSumDivThree(self, nums):
        s = 0
        min1 = [0, 0]
        min2 = [0, 0]
        for num in nums:
            s += num
            if num % 3 == 1:
                if min1[0] == 0 or min1[0] > num:
                    min1[1] = min1[0]
                    min1[0] = num
                elif min1[1] == 0 or min1[1] > num:
                    min1[1] = num
            elif num % 3 == 2:
                if min2[0] == 0 or min2[0] > num:
                    min2[1] = min2[0]
                    min2[0] = num
                elif min2[1] == 0 or min2[1] > num:
                    min2[1] = num

        if s % 3 == 0:
            return s

        res = 0

        if s % 3 == 1:
            if min1[0] > 0:
                res = max(res, s - min1[0])
            if min2[1] > 0:
                res = max(res, s - min2[0] - min2[1])
            return res

        if s % 3 == 2:
            if min2[0] > 0:
                res = max(res, s - min2[0])
            if min1[1] > 0:
                res = max(res, s - min1[0] - min1[1])
            return res
''',
    call=f'Solution().maxSumDivThree({NUMS!r})',
    expect=15,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='array', var='nums', label='nums（蓝 = 余 1，粉 = 余 2）', cell=96, color=_mod_color, h=180),
        dict(type='array', var='min1', label='min1：最小的两个余 1 的数 [最小, 次小]', cell=96,
             color=lambda S, k, v: 'blue' if v else None, h=170),
        dict(type='array', var='min2', label='min2：最小的两个余 2 的数 [最小, 次小]', cell=96,
             color=lambda S, k, v: 'pink' if v else None, h=170),
    ],
    watch=[('num', 'num', 'yellow'), ('s', 's', 'cyan'), ('s % 3', 's % 3'), ('res', 'res', 'green')],
    skip=['min1 = [0, 0]', 'min2 = [0, 0]'],
    captions={
        3: '`s` 累加总和；`min1`、`min2` 记录最小的两个余 1 / 余 2 的数（0 = 还没有）',
        'for num in nums': lambda S, B, ret: ('扫描结束' if 'num' in B and B.num == S['num'] and B.s == S['s']
                                              else f'取出 `num = {S["num"]}`'),
        's += num': '`s` → {s}',
        'if num % 3 == 1': _mod_if(1),
        'elif num % 3 == 2': _mod_if(2),
        'if min1[0] == 0 or': _first_if(1),
        'if min2[0] == 0 or': _first_if(2),
        'elif min1[1] == 0 or': _second_if(1),
        'elif min2[1] == 0 or': _second_if(2),
        'min1[1] = min1[0]': _demote(1),
        'min2[1] = min2[0]': _demote(2),
        'res = 0': '`res = 0`：两种剔除方式都不行时，答案就是 0（一个都不选）',
        'min1[0] = num': '`min1[0] = {num}` → `min1 = {min1}`',
        'min2[0] = num': '`min2[0] = {num}` → `min2 = {min2}`',
        'min1[1] = num': '`min1[1] = {num}` → `min1 = {min1}`',
        'min2[1] = num': '`min2[1] = {num}` → `min2 = {min2}`',
        'if s % 3 == 0': lambda S, B, ret: (f'`{S["s"]} % 3 = {S["s"] % 3}`：不能直接返回，要剔除一些数'
                                            if S['s'] % 3 else f'`{S["s"]}` 能被 3 整除 → 就是答案'),
        'if s % 3 == 1': lambda S, B, ret: (f'`s % 3 = 1`：剔除一个余 1 的，或两个余 2 的（余 2 + 余 2 = 余 1）'
                                            if S['s'] % 3 == 1 else '`s % 3` 不是 1'),
        'if min1[0] > 0': lambda S, B, ret: (f'`min1[0] = {S["min1"][0]}`：存在余 1 的数，可以剔除它'
                                             if S['min1'][0] > 0 else '没有余 1 的数，这条路走不通'),
        'res = max(res, s - min1[0])': '剔除一个余 1 的最小数：`{s} − {min1[0]} = {s - min1[0]}` → `res = {res}`',
        'if min2[1] > 0': lambda S, B, ret: (f'`min2[1] = {S["min2"][1]}`：至少两个余 2 的数，可以剔除两个'
                                             if S['min2'][1] > 0 else '余 2 的数不足两个，这条路走不通'),
        'res = max(res, s - min2[0] - min2[1])': '剔除两个余 2 的最小数：`{s} − {min2[0]} − {min2[1]} = {s - min2[0] - min2[1]}` → ==`res = {res}`==',
        'return res': '返回 =={ret}==：剔除两个小数，反而比剔除一个大数更划算',
    },
    cards=dict(
        one_liner='先求总和 s，再按 s 模 3 的余数，剔除最小的一个或两个数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['整数数组 `nums`（元素都是正数）',
                 '选出若干个数，使它们的和==能被 3 整除==，求最大的和',
                 '示例：`[3,6,5,1,8]` → `18`',
                 '本视频：`[5,2,7,3,2]` → `15`'],
        quote='s模三余一，那么此时我们可以从数组中==剔除一个模三余一的数，或者剔除两个模三余二的数==，原因是两个模三余二的数之和模三是余一的。',
        quote_src='—— yiduobo 题解原文',
        idea=['s 能被 3 整除：s 就是答案',
              's 余 1：剔除一个余 1 的数，或两个余 2 的数；s 余 2 同理对称',
              '为了和最大，剔除==最小的==：一趟扫描维护最小的两个余 1 / 余 2 的数'],
        summary=['时间 `O(n)`，空间 `O(1)`：不用排序，扫描时维护最小两个',
                 '易错：两种剔除方式都要试，取 max（本例剔除 2+2 比剔除 7 好）',
                 '用 0 表示「还没有」：题目保证元素为正数才能这么写',
                 '对比灵神：灵神更推荐「选或不选」DP，换成模 4、模 5 也通用',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
