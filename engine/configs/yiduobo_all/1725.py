CONFIG = dict(
    num=1725, title='可以形成最大正方形的矩形数目', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟扫描 · 擂台法',
    code='''
class Solution:
    def countGoodRectangles(self, rectangles):

        m = 0
        res = 0
        for l, w in rectangles:
            max_l = min(l, w)
            if m == max_l:
                res += 1
            elif m < max_l:
                m = max_l
                res = 1

        return res
''',
    call='Solution().countGoodRectangles([[5,8],[3,9],[5,12],[16,5]])',
    expect=3,
    views=[
        dict(type='table', var='rectangles', label='rectangles（长, 宽）', h=300,
             values=True, rows=lambda S: [f'#{i}' for i in range(len(S['rectangles']))], cols=['l', 'w'],
             color=lambda S, i, j, v: 'blue' if 'l' in S and S['rectangles'][i] == [S['l'], S['w']] else None),
        dict(type='text', h=80, fn=lambda S: (f"这块最大能切 `min({S['l']}, {S['w']}) = {min(S['l'], S['w'])}`；当前最大边长 `m = {S['m']}`，出现 `{S['res']}` 次"
                                              if 'l' in S else '')),
    ],
    watch=[('l', 'l', 'blue'), ('w', 'w', 'pink'), ('max_l', 'max_l', 'cyan'), ('m', 'm', 'orange'), ('res', 'res', 'green')],
    captions={
        'm = 0': '`m` 记录目前最大的正方形边长',
        'res = 0': '`res` 记录这个最大边长出现的次数',
        'for l, w in': '取一个矩形 `{l} × {w}`',
        'max_l = min': '长宽取小：最大正方形边长 `min({l}, {w})` = =={max_l}==',
        'if m == max_l': lambda S, B, r: (f'`m = {S.m}` 等于 `{S.max_l}`：和纪录并列 → 次数加一' if S.m == S.max_l
                                          else f'`m = {S.m}` ≠ `{S.max_l}`，不并列'),
        'res += 1': '并列最大：`res` → =={res}==',
        'elif m < max_l': lambda S, B, r: (f'`{S.m} < {S.max_l}`：打破纪录' if S.m < S.max_l
                                           else f'`{S.m} > {S.max_l}`：比纪录小，忽略'),
        'm = max_l': '新纪录 `m = {m}`，次数重新从 `1` 开始',
        'res = 1': '新纪录只出现了这一次：`res = 1`',
        'return res': '最大边长 `{m}`，共 `{res}` 个矩形能切出',
    },
    cards=dict(
        one_liner='每个矩形最大正方形边长是 min(长, 宽)，边扫边维护最大值和次数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每个矩形 `[l, w]` 可以切出边长不超过 `min(l, w)` 的正方形',
                 '设能切出的最大正方形边长为 `maxLen`，求有多少个矩形能切出边长为 `maxLen` 的正方形',
                 '示例：`[[5,8],[3,9],[5,12],[16,5]]` → `3`'],
        quote='对于一个矩形而言，可以切割出来的最大正方形边长就是min(l, w)，那么可以一趟扫描遍历所有的矩形，计算出每个矩形能切割的最大正方形边长，然后找出其中的最大值并统计出现次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['矩形 → 边长：`min(l, w)`，问题变成“数组最大值出现几次”',
              '一趟扫描：等于纪录就 `res += 1`；超过纪录就更新 `m` 并把 `res` 重置为 1'],
        summary=['时间 `O(n)`，空间 `O(1)`，不用先求最大值再数第二趟',
                 '更新纪录时 `res` 是置 `1` 而不是累加',
                 '原文为 Python 2 风格，仅把 `Solution(object)` 改为 `Solution`'],
    ),
)
