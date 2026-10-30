CONFIG = dict(
    num=1375, title='二进制字符串前缀一致的次数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='前缀和比对',
    code='''
class Solution(object):
    def numTimesAllBlue(self, light):

        s = 0
        now = 0
        res = 0
        for index, num in enumerate(light):
            s += index + 1
            now += num
            if s == now:
                res += 1
        
        return res
''',
    call='Solution().numTimesAllBlue([3,2,4,1,5])',
    expect=2,
    views=[
        dict(type='array', var='light', pointers={'index': 'blue'}, h=220,
             dim=lambda S, i, v: 'index' in S and i > S['index']),
        dict(type='text', fn=lambda S: f"前 {S['index']+1} 个数之和 `{S['now']}`，1 到 {S['index']+1} 之和 `{S['s']}`" if 'now' in S and 'index' in S else '', size=30, h=80),
    ],
    watch=['index', 'num', ('s', 's', 'cyan'), ('now', 'now', 'orange'), ('res', 'res', 'green')],
    captions={
        's += index + 1': '`s` 是 1 到 `{index + 1}` 的和：`{s}`',
        'now += num': '`now` 是前 `{index + 1}` 个数的和：`{now}`',
        'if s == now': lambda S, B, r: (f'`s = {S.s}` == `now = {S.now}`：前 {S.index+1} 个数恰是 1 到 {S.index+1} 的排列 → ==这一步前缀一致=='
                                        if S.s == S.now else f'`s = {S.s}` != `now = {S.now}`：`now` 偏大，说明还有更大的灯亮着、小的没亮'),
        'res += 1': '前缀一致次数 `res = {res}`',
        'return': '一共 `{ret}` 次',
    },
    cards=dict(
        one_liner='前 k 个数的和恰好等于 1+2+…+k，就是一次前缀一致',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['长度为 n 的灯串初始全灭，第 i 步点亮第 `light[i]` 盏',
                 '若第 k 步后亮的灯恰是 1 到 k，就算一次前缀一致',
                 '本视频：`[3,2,4,1,5]` → `2`'],
        quote='若此时的light[:k]恰好是1到k的一个排列，那么说明k是一个符合题目要求的时刻。',
        quote_src='—— yiduobo 题解原文',
        idea=['light 是 1 到 n 的排列，数字互不相同，亮了的灯不会再灭',
              '直接判排列太慢 → 比较前 k 个数的和与 `(1+k)*k/2`',
              '两边都用累加：`s` 加 `index+1`，`now` 加 `num`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`enumerate` 从 0 开始，所以累加的是 `index + 1`',
                 '依赖「互不相同」：和相等才能推出恰是 1 到 k',
                 '对比灵神：灵神维护前缀最大值，最大值等于 i 即可；这里用和比对',
                 '原文为 Python 2 风格，除删去类型文档字符串外无需改动'],
    ),
)
