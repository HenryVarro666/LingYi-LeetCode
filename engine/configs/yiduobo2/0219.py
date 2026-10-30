NUMS = [1, 2, 3, 1, 2, 3]


def _color(S, i, v):
    if 'index' not in S:
        return None
    if i == S['index']:
        return 'blue'
    num = S.get('num')
    if S['_line'] in (5, 6) and num in S['pos_dict'] and i == S['pos_dict'][num]:
        return 'orange'
    return None


def _formula(S):
    if 'index' not in S:
        return '从左往右扫描，`pos_dict` 维护每个数==最晚一次出现的位置=='
    num, idx = S['num'], S['index']
    d = S['pos_dict']
    if S['_line'] not in (5, 6):
        return f'扫描到 `nums[{idx}] = {num}`'
    if num not in d:
        return f'`{num}` 不在 dict 中'
    diff = idx - d[num]
    return f'`index - pos_dict[{num}] = {idx} - {d[num]} = {diff}` ' + ('`≤ k`' if diff <= S['k'] else f"`> k = {S['k']}`")


def _if_cap(S, B, ret):
    num, idx, d = S.num, S.index, S.pos_dict
    if num not in d:
        return f'`{num}` 不在 dict 中 → 前面没出现过，不用比较'
    diff = idx - d[num]
    if diff <= S.k:
        return f'`{num}` 在 dict 中：差值 `{idx} - {d[num]} = {diff} ≤ k` → 找到了'
    return f'`{num}` 在 dict 中：差值 `{idx} - {d[num]} = {diff} > k = {S.k}` → 不行'


def _upd(S, B, ret):
    num, idx = S.num, S.index
    if num in B.pos_dict:
        return f'把 `pos_dict[{num}]` 从 `{B.pos_dict[num]}` 更新为 `{idx}`：==每扫描一个数都要更新=='
    return f'`pos_dict[{num}] = {idx}`'


CONFIG = dict(
    num=219, title='存在重复元素 II', difficulty='Easy', category='哈希',
    author='yiduobo', technique='dict 维护最晚出现位置 · 一趟扫描',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def containsNearbyDuplicate(self, nums, k):
        pos_dict = {}
        for index, num in enumerate(nums):
            if num in pos_dict and index - pos_dict[num] <= k:
                return True

            pos_dict[num] = index

        return False
''',
    call=f'Solution().containsNearbyDuplicate({NUMS}, 2)',
    expect=False,
    views=[
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='array', var='nums', label='nums（蓝 = index，橙 = pos_dict[num]）', cell=100, h=200,
             pointers={'index': 'blue'}, color=_color,
             dim=lambda S, i, v: 'index' in S and i > S['index']),
        dict(type='map', var='pos_dict', label='pos_dict：数 → 最晚一次出现的位置', h=200, font=34,
             fmt=lambda k, v: f'{k} : {v}'),
    ],
    watch=[('index', 'index', 'blue'), ('num', 'num'), ('k', 'k')],
    captions={
        'pos_dict = {}': '用一个 dict 维护==每个数最晚一次出现的位置==',
        'for index, num in enumerate': lambda S, B, ret: (f'扫描 `nums[{S.index}] = {S.num}`' if 'index' in S and S.index != B.get('index')
                                                          else '扫描完毕'),
        'if num in pos_dict and': _if_cap,
        'return True': '差值 ≤ k → 返回 True',
        'pos_dict[num] = index': _upd,
        'return False': '所有相同的数距离都超过 `k = 2` → 返回 ==False==',
    },
    cards=dict(
        one_liner='dict 记每个数最晚出现的位置，扫描时比较差值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['整数数组 `nums` 和整数 `k`：是否存在两个==不同的下标== `i`、`j`',
                 '满足 `nums[i] == nums[j]` 且 `abs(i - j) <= k`？',
                 '示例：`[1,0,1,1], k = 1` → `true`；`[1,2,3,1,2,3], k = 2` → `false`'],
        quote='用一个dict维护==每个数最晚一次出现的位置==……若当前的nums[index]在dict中，那么就比较index与dict[nums[index]]的差值是否小于等于k即可。',
        quote_src='—— yiduobo 题解',
        idea=['比较基础的题目：一趟扫描 + dict',
              '当前数在 dict 中 → 和它==最晚==出现的位置比较差值',
              '==每扫描一个数都需要把 dict[nums[index]] 更新为 index=='],
        result='三对相同的数距离都是 `3 > k = 2` → 返回 `False` ✓',
        after=[dict(heading='为什么存「最晚」的位置？', lines=[
            '扫描到 `index` 时，候选的相同元素都在左边',
            '离 `index` 最近的就是==最晚出现==的那个：它的差值最小',
            '它都不满足 `≤ k`，更早的位置更不可能满足'])],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '先比较、后更新：顺序反了就会和自己比较，差值为 0',
                 '`k = 0` 时永远是 False（下标必须不同）',
                 '对比灵神：思路相同（枚举右维护左）；灵神另给了定长滑动窗口写法',
                 '原文为 Python 2 风格，仅删去 docstring，代码未改'],
    ),
)
