def _col(S, i, v):
    m = S.get('mi')
    if m is None:
        return None
    if v == m:
        return 'green'
    if v % m:
        return 'pink'
    return None


def _text(S):
    if S.get('mi') is None:
        return '第一遍：扫一遍找最小值 `mi` 和它出现的次数 `freq`'
    if 'freq' in S and S.get('_line', 0) <= 11:
        return f'`mi = {S["mi"]}`，出现 `freq = {S["freq"]}` 次'
    return f'第二遍：粉色 = 不是 `{S["mi"]}` 的倍数，绿色 = 最小值'


CONFIG = dict(
    num=3012, title='通过操作使数组长度最小', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='最小值 + 出现次数',
    tags=['灵神题单', '难度分 1833'],
    code='''
class Solution(object):
    def minimumArrayLength(self, nums):

        mi = None
        freq = 0
        for v in nums:
            if mi is None or mi > v:
                mi = v
                freq = 1
            elif mi == v:
                freq += 1
        
        for v in nums:
            if v > mi and v % mi != 0:
                return 1
        
        return (freq + 1) // 2
''',
    call='Solution().minimumArrayLength([2,2,2,2,2,3])',
    expect=1,
    views=[
        dict(type='text', fn=_text, size=30, h=90),
        dict(type='array', var='nums', color=_col, h=300, cell=110),
    ],
    watch=[('mi', 'mi', 'green'), ('freq', 'freq', 'cyan'), 'v'],
    captions={
        'for v in nums': '`for v in nums`：看下一个数',
        'mi = v': '`{v}` 比当前最小值小（或还没有最小值）→ `mi = {mi}`，次数重新记为 1',
        'freq += 1': '又遇到一个最小值 → `freq = {freq}`',
        'if v > mi and v % mi': lambda S, B, r: (f'`{S.v} > {S.mi}` 且 `{S.v} % {S.mi} = {S.v % S.mi}`，非 0 → 成立' if S.v > S.mi and S.v % S.mi
                                                 else f'`{S.v}` 是最小值或是 `{S.mi}` 的倍数 → 不成立，看下一个'),
        'return 1': '`{v}` 不是 `{mi}` 的倍数：`{v} % {mi}` 比 `{mi}` 小，成为唯一最小值，拿它消掉其余所有数 → ==返回 1==',
        'return (freq': '全是最小值的倍数：最小值只能当被模数，其余数被它消掉，`{freq}` 个最小值两两配对 → =={ret}==',
    },
    cards=dict(
        one_liner='先让最小值消掉大数；若有非倍数，就能造出更小的数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['选两个不同下标、值都 > 0，把 `nums[i] % nums[j]` 放到末尾，并删掉这两个数',
                 '求操作任意次后==数组的最小长度==',
                 '示例：`[2,2,2,2,2,3]` → `1`'],
        quote='如果数组中存在某个数不是最小值的倍数，那么就可以先取这两个数进行取模，得到的结果必然小于原来的最小值，也就是说此时得到了一个唯一的新的最小值。',
        quote_src='—— yiduobo 题解原文',
        idea=['`(x, y)` 且 `x < y` 时，取模相当于==消掉 y==，所以最小值能消掉所有大数',
              '有非倍数 `3 % 2 = 1` → 新的唯一最小值，再消掉其余 → 长度 1',
              '全是倍数：最小值若当模数会得到 0（0 不能再算），所以只能当被模数，只剩它们两两相消'],
        summary=['时间 `O(n)`，空间 `O(1)`，两遍扫描：先数最小值，再查倍数',
                 '全是倍数时答案 `(freq + 1) // 2`',
                 '易错：`mi` 用 `None` 起步，最小值次数要在更小值出现时重置为 1',
                 '对比灵神：灵神用 `min` 与 `count`，这里手写一遍扫描同时得到最小值和次数'],
    ),
)
