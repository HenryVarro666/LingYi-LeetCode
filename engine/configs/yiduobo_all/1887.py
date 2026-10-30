CONFIG = dict(
    num=1887, title='使数组元素相等的减少操作次数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='计数 + 从大到小累加',
    tags=['六、分组循环', '难度分 1428'],
    code='''
class Solution(object):
    def reductionOperations(self, nums):

        cnt_dict = {}
        for num in nums:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        res = 0
        cnt = 0
        for num in sorted(cnt_dict.keys(), reverse=True):
            res += cnt
            cnt += cnt_dict[num]
        
        return res
''',
    call='Solution().reductionOperations([5,1,3,3,5,1])',
    expect=6,
    views=[
        dict(type='array', var='nums', h=200, label='nums',
             color=lambda S, i, v: 'green' if ('cnt' in S and 'num' in S and v == S['num'] and S['_line'] >= 9) else ('yellow' if 'cnt' not in S and 'num' in S and v == S['num'] else None)),
        dict(type='map', var='cnt_dict', h=260, label='cnt_dict（值 → 出现次数）'),
        dict(type='text', fn=lambda S: (f"从大到小：当前 `{S['num']}`，上面更大的数共 ==`{S['cnt']}`== 个，每个都要多走一步" if 'cnt' in S and 'res' in S and S['_line'] >= 9 else '')),
    ],
    watch=['num', ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'cnt_dict = {}': '先建一张表，统计每个数出现几次',
        'for num in nums': '取下一个数：`num = {num}`',
        'cnt_dict[num] = ': '数 `{num}` 出现次数记为 `{cnt_dict[num]}`',
        'res = 0': '`res` 累计操作次数',
        'cnt = 0': '`cnt`：比当前数更大的元素个数，开始时一个都没有',
        'for num in sorted': lambda S, B, r: ('不同的值都处理完了，循环结束' if B.get('cnt') == S['cnt'] and S['_line']==10 and B.get('num') == S['num'] and S['cnt']==sum(S['cnt_dict'].values()) else f'从大到小枚举不同的值：`num = {S["num"]}`'),
        'res += cnt': '每个更大的数都要被降到 `{num}`，各算一次操作：`res` += `{cnt}` → =={res}==',
        'cnt += cnt_dict[num]': '`{num}` 以后也会被降到下一档，所以并入 `cnt`：`cnt` = =={cnt}==',
        'return res': '全部降到最小值，共 ==`{res}`== 次操作',
    },
    cards=dict(
        one_liner='最大值出现 k 次，就要 k 次操作降到次大值',
        complexity='时间 `O(n + k log k)`，空间 `O(k)`（k 为不同值个数）',
        problem=['每次把最大值（下标最小的）降成次大值，问把数组全变相等要几次',
                 '示例：`[5,1,3]` → `3`；`[1,1,1]` → `0`',
                 '本视频：`[5,1,3,3,5,1]` → `6`'],
        quote='某一时刻，若数组中的最大值出现了k次，那么就需要执行k次操作让这些数变成次大值',
        quote_src='—— yiduobo 题解原文',
        idea=['用 `cnt` 记录「已经处理过的更大元素」个数',
              '从大到小遍历不同的值，先把 `cnt` 加到答案，再把当前值的次数并进 `cnt`',
              '操作后最大值变成次大值，所以次大值的个数也要累加进 `cnt`'],
        summary=['时间 `O(n + k log k)`，空间 `O(k)`',
                 '==先 `res += cnt`，再 `cnt += 次数==`：最大的那一档自己不用降（`cnt` 初值 0）',
                 '最小值那一档也会累加，但不再有后续档，不影响答案',
                 '本质是「每个数是第几小」之和，灵神排序后遍历同理'],
    ),
)
