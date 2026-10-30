def _digits(S):
    if 'v' not in S:
        return ''
    return f"当前数的剩余部分：`{S['v']}`，已累加数位和 `s = {S['s']}`"


CONFIG = dict(
    num=3300, title='替换为数位和以后的最小元素', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='一趟遍历 · 逐位分离',
    tags=[],
    code='''
class Solution(object):
    def minElement(self, nums):

        res = None
        for v in nums:
            s = 0
            while v:
                s += v % 10
                v //= 10
            
            if res is None or res > s:
                res = s
                
        return res
''',
    call='Solution().minElement([999, 19, 199])',
    expect=10,
    views=[
        dict(type='array', var='nums', label='nums', h=150),
        dict(type='text', h=90, size=32, fn=_digits),
    ],
    watch=['v', ('s', 's', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = None': '`res` 保存目前最小的数位和，还没有结果所以是 `None`',
        'for v in nums': lambda S, B, r: (f'按题目要求一趟遍历，取下一个元素 `v = {S.v}`' if S.v else '`nums` 已经遍历完，退出循环'),
        's = 0': '`s` 用来累加 `v` 的各位数字',
        'while v': lambda S, B, r: ('`v = %d` 非 0，继续分离数位' % S['v'] if S['v'] else '`v` 已经为 0，数位分离完毕'),
        's += v % 10': '`v % 10` 是个位 ==`{v % 10}`==，加进 `s` → {s}',
        'v //= 10': '`v //= 10` 去掉个位，剩下 `{v}`',
        'if res is None': lambda S, B, r: ('`res` 还是 None，第一个数位和直接作为答案' if B.res is None
                                           else f'比较：`res = {B.res}` 与 `s = {S.s}`，' + ('`s` 更小 → 更新' if B.res > S.s else '`res` 不大于 `s` → 不变')),
        'res = s': '`res` 更新为 =={res}==',
        'return res': '所有元素都处理完，最小数位和 `{res}`',
    },
    cards=dict(
        one_liner='按题意来：每个数逐位分离求和，取最小',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['把 `nums` 每个元素替换为各位数字之和，求替换后的最小元素',
                 '示例：`[999,19,199]` → `[27,10,19]` → `10`',
                 '`1 <= nums.length <= 100`'],
        quote='按照题目要求来做就行了。一趟遍历，对于每个元素先逐位分离并计算数位之和，然后取其中的最小值作为最终答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`v % 10` 得个位，`v //= 10` 去个位，循环到 `v` 为 0',
              '`res` 初值 `None`，第一个数位和直接当答案',
              '之后每算出一个 `s`，比 `res` 小就更新'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '易错点：`s` 每个元素要清零；`res` 用 `None` 判断第一次',
                 '对比灵神：灵神用 `inf` 作初值配合 `min`；这里用 `None` + 比较'],
    ),
)
