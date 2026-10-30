CONFIG = dict(
    num=3688, title='偶数的按位或运算', difficulty='Easy', category='位运算',
    author='yiduobo', technique='一趟遍历 · 特判第一个偶数',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def evenNumberBitwiseORs(self, nums):
        
        res = None
        for v in nums:
            if v % 2 == 0:
                if res is None:
                    res = v
                else:
                    res |= v
        
        if res is None:
            res = 0
        return res
''',
    call='Solution().evenNumberBitwiseORs([1,8,16,3])',
    expect=24,
    views=[
        dict(type='array', var='nums', label='nums', h=170,
             color=lambda S, i, v: ('green' if v % 2 == 0 else 'pink') if 'v' in S and v == S['v'] else None,
             dim=lambda S, i, v: v % 2 == 1),
        dict(type='text', h=120, size=34,
             fn=lambda S: ('`res` = 还没有偶数（None）' if S.get('res') is None else f"`res` = `{S['res']:08b}` = =={S['res']}==") if 'res' in S else ''),
    ],
    watch=['v', ('res', 'res', 'green')],
    captions={
        'res = None': '`res` 先设成 `None`，表示「还没遇到偶数」，这样才能区分第一个偶数',
        'for v in nums': lambda S, B, r: (f'取下一个数 `v = {S.v}`' if S.v != B.get('v') else '遍历完了'),
        'if v % 2 == 0': lambda S, B, r: (f'`{S.v} % 2 == 0` → 偶数' if S.v % 2 == 0 else f'`{S.v} % 2 = 1` → 奇数，跳过'),
        'if res is None': lambda S, B, r: (f'遍历完了，`res = {S.res}` 不是 `None`，不用补 0' if S['_line'] == 12 else '`res` 还是 `None`：这是第一个偶数' if S.res is None else f'`res = {S.res}` 已有值：可以直接做 OR'),
        'res = v': '第一个偶数直接赋给 `res` = =={res}==',
        'res |= v': '`{B.res:b} | {v:b}` → `{res:b}` = =={res}==',
        'res = 0': '一个偶数都没遇到，按题意返回 0',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='一趟遍历，偶数 OR 起来；没有偶数就返回 0',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['返回 `nums` 里所有偶数的按位或',
                 '没有偶数时返回 `0`',
                 '示例：`[1,2,3,4,5,6]` → `6`；本视频用 `[1,8,16,3]` → `24`'],
        quote='一趟遍历，按题目要求计算偶数的按位或结果即可。注意不要忘了特别处理第一个偶数以及没有偶数的情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['`res = None` 表示还没见过偶数', '第一个偶数直接赋值，之后用 `|=` 累积',
              '遍历完 `res` 仍是 `None` → 返回 0'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文是 Python 2 风格，在 Python 3 下可直接运行，未做改动',
                 '易错：忘了处理 `None`，对 `None` 做 `|=` 会报错',
                 '对比灵神：灵神用 0 当初值（0 | x = x），省掉两处特判'],
    ),
)
