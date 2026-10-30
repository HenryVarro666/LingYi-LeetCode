NUMS = [1, -2, -3, -1, 7, -5]


def _cur(S):
    return S['nums'].index(S['v']) if 'v' in S and S['_line'] != 13 else None


def _txt(S):
    if 'v' not in S or _cur(S) is None:
        return '去掉异常值后，剩下元素之和 = ==2 × 特殊数字之和=='
    s, v = S['s'], S['v']
    if (s - v) % 2:
        return f"`s − v = {s} − ({v}) = {s - v}` 是==奇数==，不可能是两倍"
    h = (s - v) // 2
    return f"`s − v = {s - v}`，特殊数字之和应为 `{h}`：`freq[{h}] = {S['freq'][h]}`" + ('，且 ==等于 v== → 需要出现 ≥ 2 次' if h == v else '')


CONFIG = dict(
    num=3371, title='识别数组中的最大异常值', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举异常值 · 哈希计数',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1644'],
    code='''
from collections import Counter

class Solution(object):
    def getLargestOutlier(self, nums):
        
        s = sum(nums)
        freq = Counter(nums)
        res = None
        for v in nums:
            if (s - v) % 2 == 0 and (freq[(s - v) // 2] > 1 or (freq[(s - v) // 2] == 1 and (s - v) // 2 != v)):
                if res is None or res < v:
                    res = v
        return res
''',
    call=f'Solution().getLargestOutlier({NUMS})',
    expect=7,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 尝试作为异常值的 v，粉 = 需要的特殊数字之和）', h=210,
             pointers={_cur: 'blue'}, pointer_labels={_cur: 'v'},
             color=lambda S, i, v: ('blue' if i == _cur(S) else
                                    'pink' if _cur(S) is not None and (S['s'] - S['v']) % 2 == 0 and v == (S['s'] - S['v']) // 2 else None)),
        dict(type='map', var='freq', label='freq（每种数字出现的次数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=34),
        dict(type='text', h=90, size=29, fn=_txt),
    ],
    watch=['s', ('v', 'v', 'blue'), ('res', 'res', 'green')],
    captions={
        's = sum(nums)': '`s = {s}`：所有元素之和',
        'freq = Counter': '`freq` 记录每种数字出现的次数',
        'res = None': '`res = None`：还没有找到异常值',
        'for v in nums': lambda S, B, r: (f'检测 `v = {S.v}` 能否作为异常值' if _cur(S) is not None and (B.get('v') != S.v or B.get('_line') == 2) else ('遍历结束' if B.get('v') == S.v else f'检测 `v = {S.v}` 能否作为异常值')),
        'if (s - v) % 2 == 0': lambda S, B, r: (
            f'`s − v = {S.s - S.v}` 是奇数 → 不行' if (S.s - S.v) % 2 else
            (lambda h: (f'`(s − v) // 2 = {h}` 不在数组中 → 不行' if S.freq[h] == 0 else
                        f'`{h}` 恰好等于 v 且只出现 1 次：==和与异常值不能共用一个位置== → 不行' if h == S.v and S.freq[h] == 1 else
                        f'特殊数字之和 `{h}` 存在（出现 {S.freq[h]} 次）→ `{S.v}` ==可以==是异常值'))((S.s - S.v) // 2)),
        'if res is None or res < v': lambda S, B, r: ('第一个合法的异常值' if S.res is None else (f'`{S.res} < {S.v}` → 更大，更新' if S.res < S.v else f'`{S.v}` 不比 `{S.res}` 大，不更新')),
        'res = v': '`res = {res}`',
        'return res': '最大异常值为 `{res}`',
    },
    cards=dict(
        one_liner='枚举谁是异常值：剩下的和必须是某个数的两倍',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n − 2` 个特殊数字，一个是它们的==和==，一个是==异常值==',
                 '求可能的最大异常值（下标要不同，值可以相同）',
                 '示例：`[2,3,5,10]` → `10`；`[1,1,1,1,1,5,5]` → `5`',
                 f'本视频：`{NUMS}` → `7`'],
        quote='若v是异常值，那么剩下元素之和就是s − v，这个值是特殊数字之和的两倍，因此 ==s − v 必须是偶数，且 (s − v) // 2 必须在 freq 中出现过==。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举每个 `v` 作为异常值，剩下元素之和 `s − v` = 2 × 特殊数字之和',
              '`(s − v) // 2` 必须在数组里，用 `freq` 判断',
              '若 `(s − v) // 2 == v`，它要==至少出现两次==（v 自己占掉一次）'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`(s − v) // 2 == v` 时 `freq` 必须 `≥ 2`',
                 '先判断奇偶，再查哈希表',
                 '`freq` 是 `Counter`，查不存在的键返回 0，不会报错',
                 '原文为 Python 2 风格，代码无需改动即可运行'],
    ),
)
