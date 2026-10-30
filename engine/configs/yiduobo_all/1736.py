CONFIG = dict(
    num=1736, title='替换隐藏数字得到的最晚时间', difficulty='Easy', category='字符串',
    author='yiduobo', technique='分情况讨论小时与分钟', tags=[],
    code='''
class Solution(object):
    def maximumTime(self, time):

        time_list = list(time)

        if time_list[0] == '?':
            if time_list[1] == '?':
                time_list[0] = '2'
                time_list[1] = '3'
            elif time_list[1] <= '3':
                time_list[0] = '2'
            else:
                time_list[0] = '1'
        elif time_list[1] == '?':
            if time_list[0] == '2':
                time_list[1] = '3'
            else:
                time_list[1] = '9'
        
        if time_list[3] == '?':
            time_list[3] = '5'
        
        if time_list[4] == '?':
            time_list[4] = '9'
        
        return ''.join(time_list)
''',
    call="Solution().maximumTime('?4:5?')",
    expect='14:59',
    views=[
        dict(type='text', fn=lambda S: '当前：==' + ''.join(S['time_list']) + '==' if 'time_list' in S else '', size=40, h=90),
        dict(type='array', var='time_list', cell=90, h=240,
             color=lambda S, i, v: 'yellow' if v == '?' else None),
    ],
    watch=[('time', 'time'), ('time_list', "''.join(time_list) if 'time_list' in S else ''", 'green')],
    captions={
        "time_list = list(time)": '把字符串拆成字符列表，方便逐位替换：`{time_list}`',
        "if time_list[0] == '?'": lambda S, B, r: ('小时十位是 `?`：要看个位才能定' if S.time_list[0] == '?' else f'小时十位是 `{S.time_list[0]}`，不用替换，改看个位'),
        "if time_list[1] == '?':\n": '个位也是 `?` 吗？是则小时直接取最大 23',
        "elif time_list[1] <= '3'": lambda S, B, r: (f'个位 `{S.time_list[1]}` <= 3 → 十位可以取 ==2==（20~23 都合法）' if S.time_list[1] <= '3' else f'个位 `{S.time_list[1]}` > 3 → 十位取 2 会超过 23，只能取 ==1=='),
        "time_list[0] = '2'": '十位填 `2`：`{"".join(time_list)}`',
        "time_list[0] = '1'": '个位大于 3，十位只能填 `1`：`{"".join(time_list)}`',
        "time_list[1] = '3'": '十位是 2 时个位最大 3：`{"".join(time_list)}`',
        "time_list[1] = '9'": '十位是 0 或 1 时个位最大 9：`{"".join(time_list)}`',
        "elif time_list[1] == '?'": '十位已知，看个位是不是 `?`',
        "if time_list[0] == '2'": '十位是 2 吗？是 2 个位最多 3，否则最多 9',
        "if time_list[3] == '?'": '分钟十位若为 `?`，最大是 5（分钟最大 59）',
        "time_list[3] = '5'": '分钟十位填 `5`',
        "if time_list[4] == '?'": '分钟个位和十位互不限制，若为 `?` 就填 9',
        "time_list[4] = '9'": '分钟个位填 `9`：`{"".join(time_list)}`',
        "return": '拼回字符串 `{ret}`',
    },
    cards=dict(
        one_liner='小时两位互相约束，分钟两位互相独立',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['时间字符串 `hh:mm`，某些位是 `?`，把 `?` 替换成数字',
                 '使结果是最晚的合法时间（`00:00` 到 `23:59`）',
                 '示例：`?4:5?` → `14:59`'],
        quote='24小时表示的时间里面，由于存在20、21、22、23这几个小时，因此小时的两位之间是有某种限制关系的。相对的，分钟的两位取值相对是独立的。',
        quote_src='—— yiduobo 题解原文',
        idea=['小时：`??` 取 23；`?X` 看 X<=3 取 2 否则取 1；`X?` 看 X 是 2 取 3 否则取 9',
              '分钟：十位 `?` 取 5，个位 `?` 取 9，互不影响',
              '每一位只需根据另一位做常数次判断'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：十位 `?`、个位 `4~9` 时十位只能是 1，不是 2',
                 '易错：十位是 2 时个位最大 3，其他情况是 9',
                 '分钟十位最大是 5，不是 9',
                 '原文代码无需修改，直接运行'],
    ),
)
