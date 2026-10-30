CONFIG = dict(
    num=3961, title='设备评分的最大和', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='一趟找最小次小 + 选接盘设备',
    tags=['灵神题单', '难度分 1880'],
    code='''
class Solution(object):
    def maxRatings(self, units):

        m = len(units)
        if len(units[0]) == 1:
            return sum([units[index][0] for index in range(m)])

        mi_first = None
        mi_second = None

        res = 0
        for index in range(m):
            first = None
            second = None
            for v in units[index]:
                if first is None or first > v:
                    first, second = v, first
                elif second is None or second > v:
                    second = v
        
            if mi_first is None or mi_first > first:
                mi_first = first
            if mi_second is None or mi_second > second:
                mi_second = second
            res += second
        
        return res - mi_second + mi_first
''',
    call='Solution().maxRatings([[5,3,8],[2,6,4],[7,9,1]])',
    expect=13,
    views=[
        dict(type='grid', var='units', h=330, cell=110,
             color=lambda S, i, j, v: ('yellow' if S.get('index') == i and S.get('v') == v and S['_line'] in (14, 15, 16, 17, 18)
                                       else 'cyan' if S.get('index') == i and v == S.get('first') and S['_line'] >= 19
                                       else 'green' if S.get('index') == i and v == S.get('second') and S['_line'] >= 19 else None)),
        dict(type='text', size=32, fn=lambda S: (f"当前设备 最小 `first = {S.get('first')}`，次小 `second = {S.get('second')}`" if 'first' in S else '')),
    ],
    watch=['index', 'first', 'second', ('mi_first', 'mi_first', 'pink'), ('mi_second', 'mi_second', 'cyan'), ('res', 'res', 'green')],
    captions={
        'len(units[0]) == 1': '每台设备只有一个单元：移走会变空，所以不操作',
        'return sum': '答案就是所有 `units[i][0]` 之和',
        'mi_first = None': '`mi_first`：各设备最小值里的最小（接盘设备的新评分）',
        'mi_second = None': '`mi_second`：各设备次小值里的最小（接盘设备损失的评分）',
        'for index in range(m)': lambda S, B, r: ('所有设备都遍历完了' if B.get('index') == S.index else f'遍历设备 `{S.index}`：`{S.units[S.index]}`'),
        'first = None': '准备一趟扫出这台设备的最小 `first` 和次小 `second`',
        'for v in units': lambda S, B, r: ('这台设备扫完了' if B.get('v') == S.v and S.v == S.units[S.index][-1] else f'看单元 `{S.v}`'),
        'if first is None': lambda S, B, r: (f'`{S.v}` 比最小 `{B.first}` 还小 → 它成新最小，旧最小退为次小'
                                            if (B.first is None or B.first > S.v) else f'`{S.v}` 不比最小 `{B.first}` 小，再看能否做次小'),
        'elif second is None': lambda S, B, r: (f'`{S.v}` 比次小 `{B.second}` 小 → 成为新次小'
                                               if (B.second is None or B.second > S.v) else f'`{S.v}` 不比次小 `{B.second}` 小，跳过'),
        'first, second = v, first': '最小=`{first}`，次小=`{second}`',
        'second = v': '次小更新为 `{second}`',
        'mi_first > first': '比较全局最小 `mi_first = {mi_first}` 与这台的最小 `{first}`',
        'mi_second > second': '比较 `mi_second = {mi_second}` 与这台的次小 `{second}`',
        'res += second': '这台设备扔掉最小后评分是次小：`res += {second}` → {res}',
        'return res - mi_second': '让次小最小的设备接盘：`{res} − {mi_second} + {mi_first}` = =={res - mi_second + mi_first}==',
    },
    cards=dict(
        one_liner='每台设备甩掉最小值，全塞给次小值最小的接盘侠',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['设备评分 = 内部单元最小容量，每台设备最多移走一个单元一次',
                 '求评分之和的最大值',
                 '示例：`[[5,3,8],[2,6,4],[7,9,1]]` → `13`'],
        quote='就应该从这m个设备中选出一个接盘，从其他的m - 1个设备中都选出容量最小的那个单元，就这堆拖油瓶都塞给这个接盘的。',
        quote_src='—— yiduobo 题解原文',
        idea=['只有抛掉最小容量，设备得分才可能上涨',
              '被抛掉的最小值要集中祸害同一台，接盘设备得分变成这些最小值中的最小',
              '接盘设备损失自己的次小，所以选次小最小的那台'],
        summary=['时间 `O(mn)`，空间 `O(1)`，一趟遍历找最小次小，不需要排序',
                 '`n = 1` 要特判，否则设备会变空',
                 '最后 `res - mi_second + mi_first`：把接盘设备的次小换成全局最小',
                 '对比灵神：灵神用排序取前两个，本文用 `None` 判空手动维护最小次小'],
    ),
)
