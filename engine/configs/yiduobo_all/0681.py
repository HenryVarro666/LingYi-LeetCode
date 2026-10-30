def _tm(S):
    nl = S.get('num_list')
    if nl is None:
        return ''
    return f'当前时间位：`{nl[0]}{nl[1]}:{nl[2]}{nl[3]}`（只能用原来出现过的数字）'


def _up(S):
    if 'upper' not in S or S['_line'] < 9 or S['_line'] in (10, 12, 13, 15, 17):
        return ''
    return f'`check_pos = {S["check_pos"]}` 的上限 `upper = {S["upper"]}`：这一位必须 `< {S["upper"]}`'


CONFIG = dict(
    num=681, title='最近时刻', difficulty='Medium', category='模拟',
    author='yiduobo', technique='从低位到高位找更大的替代数字',
    code='''
class Solution(object):
    def nextClosestTime(self, time):

        num_list = [int(time[0]), int(time[1]), int(time[3]), int(time[4])]
        mi = min(num_list)

        for check_pos in range(3, -1, -1):
            if check_pos == 3:
                upper = 10
            elif check_pos == 2:
                upper = 6
            elif check_pos == 1:
                if num_list[0] == 2:
                    upper = 4
                else:
                    upper = 10
            else:
                upper = 3

            candidate = [num for num in num_list if num_list[check_pos] < num < upper]
            if candidate:
                num_list[check_pos] = min(candidate)
                for index in range(check_pos + 1, 4):
                    num_list[index] = mi
                return '%d%d:%d%d' % (num_list[0], num_list[1], num_list[2], num_list[3])
        
        return '%d%d:%d%d' % (mi, mi, mi, mi)
''',
    call="Solution().nextClosestTime('13:59')",
    expect='15:11',
    views=[
        dict(type='string', var='time', label='time（给定时间）', cell=80, h=150, index=False),
        dict(type='array', var='num_list', label='num_list = [时十位, 时个位, 分十位, 分个位]', cell=100, h=250,
             pointers={'check_pos': 'blue'}),
        dict(type='array', var='candidate', label='candidate（比当前位大、又不超上限的数字）', cell=80, h=170),
        dict(type='text', h=70, size=28, fn=_tm),
        dict(type='text', h=70, size=28, fn=_up),
    ],
    watch=[('check_pos', 'check_pos', 'blue'), 'upper', ('mi', 'mi', 'green'), 'candidate'],
    captions={
        'num_list = [': '把时间里的 4 个数字收集起来：`{num_list}`',
        'mi = min': '`mi` = 最小数字 `{mi}`：跨位后低位都补它，时间最小',
        'for check_pos': '从==低位到高位==找：这一位能不能换成更大的数字',
        'if check_pos == 3': lambda S, B, r: '`check_pos = {}`，是分钟个位吗？{}'.format(S.check_pos, '是' if S.check_pos == 3 else '不是'),
        'elif check_pos == 2': lambda S, B, r: '是分钟十位吗？{}'.format('是' if S.check_pos == 2 else '不是'),
        'elif check_pos == 1': lambda S, B, r: '是小时个位吗？{}'.format('是' if S.check_pos == 1 else '不是，就是小时十位'),
        'if num_list[0] == 2': lambda S, B, r: ('小时十位是 2 → 小时个位不能超过 3' if S.num_list[0] == 2 else '小时十位不是 2 → 个位可到 9'),
        'upper = 10': '这一位上限 `upper = 10`（数字 0~9）',
        'upper = 6': '分钟十位上限 `upper = 6`（最大 59）',
        'upper = 4': '小时 `2x`，个位上限 `upper = 4`（最大 23）',
        'upper = 3': '小时十位上限 `upper = 3`（最大 2x）',
        'candidate = [': '候选 = 满足 `{num_list[check_pos]} < num < {upper}` 的数字：`{candidate}`',
        'if candidate': lambda S, B, r: ('有候选 → 这一位可以换，取最小的更大值' if S.candidate else '没有候选 → 这一位换不了，继续看更高一位'),
        'num_list[check_pos] = min': '这一位换成候选里最小的 `{num_list[check_pos]}`，让时间只大一点点',
        'num_list[index] = mi': '右边第 `{index}` 位补最小数字 `{mi}`',
        'return \'%d%d:%d%d\' % (mi': '每一位都换不了 → 只能跨天，全用最小数字：`{ret}`',
        'return': '得到答案 `{ret}`',
    },
    cards=dict(
        one_liner='从低位往高位找：谁能换成更大的数字，右边就补最小',
        complexity='时间 `O(1)`（固定 4 位），空间 `O(1)`',
        problem=['给一个 `HH:MM` 时间，用它出现过的数字（可重复用）组成==下一个最近的合法时间==',
                 '可以跨天，答案仍是 `HH:MM`',
                 '示例：`19:34` → `19:39`；本视频：`13:59` → `15:11`'],
        quote='若收集到的candidate不为空，说明在当前的check_pos存在某种替代方案。此时就应该选择candidate中的最小值来替代check_pos这一位的值，同时将check_pos右侧的所有位都置为num_list中的最小值。',
        quote_src='—— yiduobo 题解原文',
        idea=['把 4 个数字放进 `num_list`，从分钟个位向高位逐位检查',
              '每位有上限：分个位 `10`、分十位 `6`、时个位 `4` 或 `10`、时十位 `3`',
              '找到能换大的位：换成最小的更大值，右边全补 `mi`',
              '都换不了 → 跨天，全部用 `mi`'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '低位先试：只让时间变大尽可能少',
                 '小时个位的上限要看十位是不是 `2`（`24` 不合法）',
                 '`mi` 一定 `≤ 2`，补到任何位都不会越界',
                 '原文为 Python 2 风格，无需任何改动即可在 Python 3 运行'],
    ),
)
