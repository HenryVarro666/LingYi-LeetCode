def _txt(S):
    if 'ma' not in S or 'mi' not in S or 'v' not in S:
        return ''
    if S.get('_line', 0) >= 14 and 'diff' in S:
        return f"`v = {S['v']}`：最大位 `ma = {S['ma']}`，最小位 `mi = {S['mi']}`，范围 `diff = {S['diff']}`"
    return f"`v = {S['v']}`：逐位分离，当前 `ma = {S['ma']}`，`mi = {S['mi']}`，剩下 `x = {S['x']}`"


CONFIG = dict(
    num=3982, title='最大数字范围的整数之和', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='模拟 · 模 10 逐位取最大最小', tags=[],
    code='''
class Solution(object):
    def maxDigitRange(self, nums):
        
        ma_diff = 0
        res = 0
        for v in nums:
            ma = 0
            mi = 9
            x = v
            while x:
                d = x % 10
                ma = max(ma, d)
                mi = min(mi, d)
                x //= 10

            diff = ma - mi
            if diff > ma_diff:
                ma_diff = diff
                res = 0
            if diff == ma_diff:
                res += v
        
        return res
''',
    call='Solution().maxDigitRange([5724, 111, 350])',
    expect=6074,
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='array', var='nums', label='nums（蓝 = 当前整数）', cell=110, pointers={'nums.index(v)': 'blue'}, pointer_labels={'nums.index(v)': 'v'},
             color=lambda S, i, k: 'blue' if S.get('v') == k else None, h=230),
        dict(type='text', fn=lambda S: (f"累计 `res = {S['res']}`，最大范围 `ma_diff = {S['ma_diff']}`" if 'res' in S else ''), size=28),
    ],
    watch=[('v', 'v', 'blue'), ('d', 'd', 'pink'), ('ma', 'ma', 'orange'), ('mi', 'mi', 'cyan'), ('ma_diff', 'ma_diff', 'yellow'), ('res', 'res', 'green')],
    captions={
        'ma_diff = 0': '`ma_diff`：目前最大的数字范围',
        5: '`res`：范围等于 `ma_diff` 的数之和',
        'for v in nums': lambda S, B, ret: (f'取 `v = {S.v}`' if S.get('v') is not None and S.v != B.get('v') else '遍历完了'),
        'ma = 0': '`ma = 0`：最大数字的初值',
        'mi = 9': '`mi = 9`：最小数字的初值',
        'x = v': '拷一份 `x = {v}`，用它模 10 除 10 拆数字',
        'while x': lambda S, B, ret: (f'`x = {S.x}` 还没拆完，继续' if S.x else '`x = 0`：每一位都拆完了'),
        'd = x % 10': '`x % 10` 取出最低位 `d = {d}`',
        'ma = max': '最大数字 `ma = max({B.ma}, {d}) = {ma}`',
        'mi = min': '最小数字 `mi = min({B.mi}, {d}) = {mi}`',
        'x //= 10': '`x //= 10` 去掉最低位 → {x}',
        'diff = ma - mi': '数字范围 `diff = {ma} − {mi} = {diff}`',
        'if diff > ma_diff': lambda S, B, ret: (f'`diff = {S.diff} > ma_diff = {S.ma_diff}`：出现更大的范围 → ==更新并清零 res==' if S.diff > S.ma_diff else f'`diff = {S.diff}` 比 `ma_diff = {S.ma_diff}` 大吗？不大'),
        'ma_diff = diff': '`ma_diff` 更新为 {ma_diff}',
        19: '之前累加的数范围不够大，作废 → `res = 0`',
        'if diff == ma_diff': lambda S, B, ret: (f'`diff = {S.diff}`，`ma_diff = {S.ma_diff}`：' + ('相等 → 这个数要加进答案' if S.diff == S.ma_diff else '不相等 → 跳过')),
        'res += v': '`res += {v}` → {res}',
        'return res': '范围最大的数之和 = =={ret}==',
    },
    cards=dict(
        one_liner='直接模拟：模 10 拆数字，对比最大范围再更新答案',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['整数的==数字范围==：最大数字 − 最小数字',
                 '返回所有数字范围等于最大范围的整数之和',
                 '本视频：`[5724,111,350]` → `6074`'],
        quote='直接按照题目要求模拟计算即可。一趟遍历，通过模10除以10的方法得到每一位数字，记录其中的最大值和最小值。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个数 `x % 10` 取最低位，`x //= 10` 去掉它，直到 `x` 为 0',
              '同时维护最大位 `ma` 和最小位 `mi`，范围 `diff = ma − mi`',
              '`diff` 更大就清零 `res`，随后 `diff == ma_diff` 就累加'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '`mi` 初值是 9、`ma` 初值是 0，保证第一位就能更新',
                 '清零后紧跟着的 `if diff == ma_diff` 会把当前数加进去',
                 '原文已是 `//`，无需改写',
                 '对比灵神：灵神用 `str` 取 max/min，yiduobo 用模 10 手工拆位'],
    ),
)
