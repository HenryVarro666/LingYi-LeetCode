CONFIG = dict(
    num=1282, title='用户分组', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表 · 按组大小攒人',
    code='''
class Solution(object):
    def groupThePeople(self, groupSizes):

        group_dict = {}
        res = []
        for index, size in enumerate(groupSizes):
            if size not in group_dict:
                group_dict[size] = []
            group_dict[size].append(index)
            if len(group_dict[size]) == size:
                res.append(group_dict[size][:])
                group_dict[size] = []
        
        return res
''',
    call='Solution().groupThePeople([2,1,3,3,3,2])',
    expect=[[1], [2, 3, 4], [0, 5]],
    views=[
        dict(type='array', var='groupSizes', label='groupSizes（第 i 人要在多大的组里）', cell=90, h=190,
             pointers={'index': 'blue'}),
        dict(type='map', var='group_dict', label='group_dict（组大小 → 正在攒的人）', fmt=lambda k, v: f"{k}: {v}", h=220, font=32),
        dict(type='array', var=lambda S: [str(g) for g in S['res']] if 'res' in S else None,
             label='res（已攒满的组）', cell=140, h=170),
    ],
    watch=[('index', 'index', 'blue'), ('size', 'size', 'pink'), ('res', 'res', 'green')],
    skip=['group_dict = {}', 'res = []'],
    captions={
        'for index, size': '第 `{index}` 个人要去大小为 `{size}` 的组',
        'if size not in group_dict': lambda S, B, r: (f"`{S.size}` 还没有对应的组 → 新建" if S.size not in B.group_dict
                                                      else f"`{S.size}` 已有在攒的组 `{S.group_dict[S.size]}`，直接加入"),
        8: '新建大小为 `{size}` 的空组',
        'group_dict[size].append(index)': '把 `{index}` 加入大小 `{size}` 的组：`{group_dict[size]}`',
        'if len(group_dict[size]) == size': lambda S, B, r: (
            f"组内 `{len(S.group_dict[S.size])}` 人 == `{S.size}` → 攒满了" if len(S.group_dict[S.size]) == S.size
            else f"组内 `{len(S.group_dict[S.size])}` 人 < `{S.size}` → 还没满，继续攒"),
        'res.append': '攒满：把组复制一份放进答案 `{res}`（`[:]` 防止后面清空影响答案）',
        12: '清空这个组，下一批同大小的人重新攒',
        'return res': '所有人都分好组：`{res}`',
    },
    cards=dict(
        one_liner='按组大小开桶，桶一满就收走',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`groupSizes[i]` 表示第 `i` 个人所在组的人数',
                 '把 `0..n-1` 分成若干组，每个人所在组的大小恰好等于他要求的数，返回任一方案',
                 '示例：`[2,1,3,3,3,2]` → `[[1],[2,3,4],[0,5]]`（任一合法答案）'],
        quote='使用一个dict，key为组中的人数，而value为一个list，表示当前组内的用户。遍历每个用户，将当前用户加入到对应的组中。若某一时刻组中人数等于key，那么就将组内的用户加入到答案中，并将该组清空。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目只要求组大小达标，不要求谁和谁一组',
              '同样要求大小的人放进同一个桶，桶满就是一个合法组',
              '收走后把桶清空，下一批继续攒'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '加入答案时用 `[:]` 复制一份，因为之后会把桶重新赋成 `[]`',
                 '答案不唯一，视频里的顺序是「谁先攒满谁先出」',
                 '同类思路：按某个属性分桶，桶满即收'],
    ),
)
