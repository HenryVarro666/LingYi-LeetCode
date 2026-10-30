A1 = [5, 3, 9, 2, 6]
A2 = [2, 8, 4, 7, 1]


def _ix(S):
    return S['index'] if 'index' in S else None


def _text(S):
    if 'f1' not in S:
        return '拆成两问：nums2 的段换进 nums1，或 nums1 的段换进 nums2'
    return (f'问题1：`f1` = =={S["f1"]}==，`max_f1` = {S["max_f1"]}，`s1 + max_f1` = {S["s1"] + S["max_f1"]}'
            f'\n问题2：`f2` = =={S["f2"]}==，`max_f2` = {S["max_f2"]}，`s2 + max_f2` = {S["s2"] + S["max_f2"]}')


def _cap_f(S, B, ret):
    return (f'`diff = nums1 − nums2 = {S.diff}`；`f1 -= diff` → {S.f1}（换进 nums2 的段对 nums1 的增益），'
            f'`f2 += diff` → {S.f2}')


def _cap_neg(name):
    def fn(S, B, ret):
        v = S[name]
        if B[name] < 0 if name in B else v < 0:
            return f'`{name} < 0`：前面拖后腿，舍去，==重新开始== → 0'
        return f'`{name} = {v}` 不小于 0，保留'
    return fn


CONFIG = dict(
    num=2321, title='拼接数组的最大分数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='两个最大子段和（f1 / f2 同时滚动）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1791'],
    code='''
class Solution(object):
    def maximumsSplicedArray(self, nums1, nums2):

        max_f1 = max_f2 = 0
        f1 = f2 = 0
        s1 = s2 = 0
        for index in range(len(nums1)):
            s1 += nums1[index]
            s2 += nums2[index]

            diff = nums1[index] - nums2[index]
            f1 -= diff
            f2 += diff

            if f1 < 0:
                f1 = 0
            if f2 < 0:
                f2 = 0

            max_f1 = max(max_f1, f1)
            max_f2 = max(max_f2, f2)

        return max(s1 + max_f1, s2 + max_f2)
''',
    call=f'Solution().maximumsSplicedArray({A1}, {A2})',
    expect=30,
    skip=['max_f1 = max_f2 = 0', 'f1 = f2 = 0', 's1 = s2 = 0', 's1 += nums1', 's2 += nums2'],
    views=[
        dict(type='text', fn=_text, size=24, h=100),
        dict(type='array', var='nums1', label='nums1', cell=96, h=200,
             pointers={'index': 'blue'}, color=lambda S, i, v: 'blue' if S.get('index') == i else None),
        dict(type='array', var='nums2', label='nums2', cell=96, h=200,
             color=lambda S, i, v: 'pink' if S.get('index') == i else None),
        dict(type='array', var=lambda S: [S['nums2'][i] - S['nums1'][i] for i in range(len(S['nums1']))],
             label='nums2 − nums1', cell=96, h=190,
             color=lambda S, i, v: 'green' if v > 0 else 'orange'),
    ],
    watch=[('f1', 'f1', 'blue'), ('f2', 'f2', 'pink'), ('max_f1', 'max_f1', 'cyan'), ('max_f2', 'max_f2', 'orange'),
           ('s1', 's1', 'blue'), ('s2', 's2', 'pink')],
    captions={
        'diff = nums1': '`diff = nums1[{index}] − nums2[{index}] = {nums1[index]} − {nums2[index]} = {diff}`',
        'f1 -= diff': '问题1 的单点增益是 `−diff`：`f1` {B.f1} → =={f1}==',
        'f2 += diff': '问题2 的增益恰好反号：`f2` {B.f2} → =={f2}==',
        'if f1 < 0': lambda S, B, r: (f'`f1 = {S.f1} < 0`：前面是累赘 → 舍去' if S.f1 < 0 else f'`f1 = {S.f1}` ≥ 0：保留，继续拼'),
        'if f2 < 0': lambda S, B, r: (f'`f2 = {S.f2} < 0`：前面是累赘 → 舍去' if S.f2 < 0 else f'`f2 = {S.f2}` ≥ 0：保留，继续拼'),
        'f1 = 0': '`f1` 清零：从下一个位置重新开始一段',
        'f2 = 0': '`f2` 清零：从下一个位置重新开始一段',
        'max_f1 = max': '`max_f1 = max({B.max_f1}, {f1}) = {max_f1}`',
        'max_f2 = max': '`max_f2 = max({B.max_f2}, {f2}) = {max_f2}`',
        'return max': '`max(s1 + max_f1, s2 + max_f2) = max({s1} + {max_f1}, {s2} + {max_f2})` = =={ret}==',
    },
    cards=dict(
        one_liner='拆成两个对称问题，各做一次最大子段和',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['交换 `nums1`、`nums2` 的同一段（至多一次），分数取两数组和的较大者',
                 '求最大分数',
                 '本视频：`[5,3,9,2,6]` 与 `[2,8,4,7,1]` → `30`'],
        quote='s = sum(nums1) + diff[l] + diff[l + 1] + ... + diff[r]，由于sum(nums1)是个常量，那么为了使得s最大，实际上就是要让diff[l] + ... + diff[r]最大，可以发现这就是非常熟悉的最大子段和问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['问题1：用 `nums2` 的某段替换 `nums1` 的对应段，使 `nums1` 之和最大',
              '问题2：反过来，两者对称，`diff` 刚好相反',
              '一趟遍历同时滚动 `f1`、`f2`，最后取 `max(s1 + max_f1, s2 + max_f2)`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`f` 小于 0 就清零，`max_f` 初值为 0 → ==允许不交换==',
                 '`f1 -= diff` 和 `f2 += diff` 符号相反，别写反',
                 '对比灵神：灵神把一次计算封装成 `solve` 调两遍；这里把两遍合进同一个循环'],
    ),
)
