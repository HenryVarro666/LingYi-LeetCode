def _pre(S):
    nums = S['nums']
    out, s = [], 0
    for v in nums:
        s += v
        out.append(s)
    return out


def _txt(S):
    nums = S['nums']
    p = _pre(S)
    return ' → '.join(f'{x}' for x in p) + f'    其中 ==0== 出现 {sum(1 for x in p if x == 0)} 次'


CONFIG = dict(
    num=3028, title='边界上的蚂蚁', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='前缀和 · 数 0',
    code='''
class Solution:
    def returnToBoundaryCount(self, nums: List[int]) -> int:
        return sum(s == 0 for s in accumulate(nums))
''',
    call='Solution().returnToBoundaryCount([2,3,-5,4,-4,1])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（每一步的位移）', h=200,
             color=lambda S, i, v: 'pink' if v < 0 else 'blue'),
        dict(type='array', var=_pre, label='accumulate(nums)：蚂蚁每一步后的位置', h=230,
             color=lambda S, i, v: 'green' if v == 0 else None,
             dim=lambda S, i, v: v != 0),
        dict(type='text', fn=lambda S: _txt(S) if 'nums' in S else '', size=34),
    ],
    watch=[('位置序列', _pre, 'blue'), ('回到边界次数', lambda S: sum(1 for x in _pre(S) if x == 0), 'green')],
    captions={
        'return sum': '`accumulate(nums)` 依次给出蚂蚁每一步后的位置 `{_pre(S)}`；==位置等于 0 就是回到了边界==，`s == 0` 为真的个数相加 = =={ret}==',
    },
    cards=dict(
        one_liner='边走边累加，累加值等于 0 就是回到边界',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['蚂蚁从边界出发，`nums[i]` 正数向右、负数向左走 `|nums[i]|` 步',
                 '只在每一步走完后检查，中途穿过边界不算',
                 '示例：`[2,3,-5]` → `1`'],
        quote='一边遍历数组，一边累加元素，如果发现累加值等于 0，说明返回到边界，把答案加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['累加值 = 蚂蚁当前离边界的有符号距离',
              '`accumulate` 生成前缀和，`s == 0` 的个数就是答案',
              '`sum` 把布尔值当 0/1 相加，一行搞定'],
        after=[dict(heading='示例走一遍', lines=['`[2,3,-5,4,-4,1]` 的前缀和：`2, 5, 0, 4, 0, 1`',
                                                 '前缀和为 `0` 的位置有两个：第 3 步和第 5 步',
                                                 '所以蚂蚁一共回到边界 `2` 次，答案 ==2==',
                                                 '注意第 1、2 步都在右侧，没有穿过边界']),
               dict(heading='为什么是前缀和', lines=['蚂蚁位置 = 之前所有位移之和',
                                                      '位移有正有负，正好对应数轴上的左右',
                                                      '所以「回到边界」等价于「前缀和 = 0」'])],
        summary=['时间 `O(n)`，空间 `O(1)`（`accumulate` 是惰性迭代器）',
                 '只统计走完一步后的位置，穿过边界不算，前缀和天然满足',
                 '`nums[i]` 非零，无需考虑原地不动的情况',
                 '本质是「前缀和等于 0 的个数」'],
    ),
)
