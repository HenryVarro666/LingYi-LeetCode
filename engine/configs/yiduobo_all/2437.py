def _now(S):
    if 'time' not in S:
        return ''
    t = S['time']
    l, r = S.get('left'), S.get('right')
    return f"小时 `{t[:2]}` → {'?' if l is None else l} 种；分钟 `{t[3:]}` → {'?' if r is None else r} 种"


CONFIG = dict(
    num=2437, title='有效时间的数目', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='小时 / 分钟分情况讨论',
    tags=[],
    code='''
class Solution(object):
    def countTime(self, time):

        if time[0] == '?':
            if time[1] == '?':
                left = 24
            elif time[1] < '4':
                left = 3
            else:
                left = 2
        elif time[1] == '?':
            if time[0] == '2':
                left = 4
            elif time[0] > '2':
                left = 0
            else:
                left = 10
        elif int(time[0]) * 10 + int(time[1]) > 23:
            left = 0
        else:
            left = 1
        
        if time[3] == '?':
            if time[4] == '?':
                right = 60
            else:
                right = 6
        elif time[3] > '5':
            right = 0
        elif time[4] == '?':
            right = 10
        else:
            right = 1
        
        return left * right
''',
    call='''[Solution().countTime("?5:0?"), Solution().countTime("2?:??"), Solution().countTime("?1:3?")]''',
    expect=[20, 240, 30],
    views=[
        dict(type='text', fn=_now, size=26),
        dict(type='string', var='time', label='time（0 1 是小时，3 4 是分钟）', cell=100),
        dict(type='text', fn=lambda S: f"left × right = {S['left']} × {S['right']} = =={S['left'] * S['right']}==" if 'left' in S and 'right' in S and S['_line'] >= 35 else '', size=28),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink')],
    captions={
        4: '先看小时的十位是不是 `?`',
        5: '十位是 `?`：再看个位是不是 `?`',
        6: '两位都是 `?` → 00 到 23，共 ==24== 种',
        7: lambda S, B, r: (f"个位 `{S.time[1]}` < 4：十位可取 0、1、2" if S.time[1] < '4' else f"个位 `{S.time[1]}` ≥ 4：十位只能取 0、1（24 以上不行）"),
        8: '十位取 0、1、2，共 ==3== 种',
        10: '十位只能取 0、1，共 ==2== 种',
        11: '十位是数字，个位是 `?`：要看十位是几',
        12: lambda S, B, r: (f"十位 = 2：个位只能 0 到 3" if S.time[0] == '2' else "十位不是 2，继续判断"),
        13: '`2?` 只有 20、21、22、23，共 ==4== 种',
        14: lambda S, B, r: (f"十位 `{S.time[0]}` > 2：小时已经超过 23，无解" if S.time[0] > '2' else "十位小于 2：个位随便取"),
        15: '这个小时本身就无效 → ==0== 种',
        17: '十位 0 或 1，个位随便 → ==10== 种',
        18: lambda S, B, r: f"没有 `?`：小时 `{S.time[:2]}` {'> 23，无效' if int(S.time[:2]) > 23 else '≤ 23，有效'}",
        21: '小时确定且有效 → ==1== 种',
        23: '再看分钟的十位是不是 `?`',
        24: '分钟十位是 `?`：再看个位',
        25: '两位都是 `?` → 00 到 59，共 ==60== 种',
        27: '十位可取 0 到 5，个位已确定 → ==6== 种',
        28: lambda S, B, r: (f"分钟十位 `{S.time[3]}` > 5：无解" if S.time[3] > '5' else f"分钟十位 `{S.time[3]}` ≤ 5，没问题"),
        29: '分钟本身无效 → ==0== 种',
        30: '十位合法，个位是 `?`',
        31: '个位随便 → ==10== 种',
        33: '分钟确定且有效 → ==1== 种',
        'return left * right': '小时 `{left}` × 分钟 `{right}` = ==`{ret}`==',
    },
    cards=dict(
        one_liner='小时、分钟互相独立，分情况数完再相乘',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`"hh:mm"` 里的 `?` 可以换成 0 到 9，求能得到多少个有效时间（00:00 到 23:59）',
                 '示例：`"?5:00"` → `2`；`"0?:0?"` → `100`',
                 '本视频依次算：`"?5:0?"` → 20，`"2?:??"` → 240，`"?1:3?"` → 30'],
        quote='小时的十位上为问号，个位上是数字。此时需要判断个位上数字与是否小于4，若小于，那么十位上就可以取0、1、2，共3种可能，否则只能取0和1，共2种可能。',
        quote_src='—— yiduobo 题解原文',
        idea=['原文说暴力也可行，但他选择==分情况讨论==：小时、分钟互不影响',
              '小时按「十位 / 个位是不是 `?`」分 4 种，分钟同样 4 种',
              '最后 `left * right`'],
        result='三个示例依次得到 `[20, 240, 30]` ✓',
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：`?` 在十位、个位时上限不同：十位看个位是否 < 4，个位看十位是否 = 2',
                 '字符串比较 `time[1] < \'4\'` 是按字符比较，数字字符顺序与数值一致',
                 '数字本身已超界（如小时 > 23）要置 0'],
    ),
)
