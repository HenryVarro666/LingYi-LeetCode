CONFIG = dict(
    num=1051, title='高度检查器', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='排序后逐位对比',
    code='''
class Solution(object):
    def heightChecker(self, heights):

        return sum([1 if x != heights[index] else 0 for index, x in enumerate(sorted(heights))])
''',
    call='Solution().heightChecker([1,1,4,2,1,3])',
    expect=3,
    views=[
        dict(type='array', var='heights', label='heights（当前站队顺序）', h=200),
        dict(type='text', size=34, fn=lambda S: '排序后：`' + str(sorted(S['heights'])) + '`' if 'heights' in S else ''),
        dict(type='text', size=34, fn=lambda S: '逐位不同的位置：`' + str([i for i, (a, b) in enumerate(zip(sorted(S['heights']), S['heights'])) if a != b]) + '`' if 'heights' in S else ''),
    ],
    watch=['heights'],
    captions={
        'return sum': lambda S, B, ret: ('把 `heights` 排序得到目标顺序 `' + str(sorted(S.heights)) + '`，逐位和当前顺序比较：'
                                          + '、'.join(f'第{i}位 {a}≠{b}' for i, (a, b) in enumerate(zip(sorted(S.heights), S.heights)) if a != b)
                                          + f'，不同的位置共 =={ret}== 个'),
    },
    cards=dict(
        after=[dict(heading='逐位对比（示例）', lines=['当前 `[1,1,4,2,1,3]`', '排序 `[1,1,1,2,3,4]`', '第 2、4、5 位不同 → 共 3 人要移动', '相同位置的人不用动，不同的才要换'])],
        before=[dict(heading='为什么直接排序', lines=['站好之后的队伍是唯一的：按身高非递减', '所以最终每个位置该站谁已经确定', '站错位置的人数 = 至少要移动的人数'])],
        one_liner='排好序的队伍，和现在的队伍比，有几个位置不同',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['学生按身高排成一队，要求按非递减顺序站好',
                 '返回至少需要移动的学生数（即当前顺序与期望顺序不同的位置数）',
                 '示例：`[1,1,4,2,1,3]` → `3`'],
        quote='实际上就是要求当前顺序heights与最后有序的sorted_heights之间有多少位置上不同，那么只需要将heights排序得到sorted_heights，然后逐位对比即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['期望的站位就是 `sorted(heights)`',
              '某个位置上现在的人和期望的人身高不同，这个位置上的人就必须被换走',
              '用列表推导式逐位比较，不同记 1，最后 `sum` 求和'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错点：比较的是==同一位置==上的身高，不是比较集合或数字个数',
                 '原文代码一行写完，没有改动（只是加了示例输入）',
                 '值域很小时可改用计数排序做到 `O(n)`'],
    ),
)
