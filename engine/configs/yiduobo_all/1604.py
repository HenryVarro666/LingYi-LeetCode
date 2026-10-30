def _tl(S):
    td = S.get('time_dict')
    if td is None:
        return '先按人分组，把打卡时间换算成分钟'
    if 'name' in S and 'index' in S and S.get('_line', 0) >= 17 and 'time_list' in S:
        t, i = S['time_list'], S['index']
        return f'`{t[i]} − {t[i - 2]} = {t[i] - t[i - 2]}`，一小时内打卡不超过 60 分钟' + ('，==触发警告==' if t[i] - t[i - 2] <= 60 else '')
    return '各人的打卡时间（分钟）：' + str(td)


CONFIG = dict(
    num=1604, title='警告一小时内使用相同员工卡大于等于三次的人', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希分组 + 排序 + 隔一个比较',
    tags=[],
    code='''
class Solution(object):
    def alertNames(self, keyName, keyTime):

        time_dict = {}
        n = len(keyName)
        for index in range(n):
            name = keyName[index]
            hour, minute = keyTime[index].split(':')
            if name not in time_dict:
                time_dict[name] = []
            time_dict[name].append(int(hour) * 60 + int(minute))
        
        res = []
        for name in sorted(time_dict.keys()):
            if len(time_dict[name]) < 3:
                continue
            time_list = sorted(time_dict[name])
            for index in range(2, len(time_list)):
                if time_list[index] - time_list[index - 2] <= 60:
                    res.append(name)
                    break
        
        return res
''',
    call="Solution().alertNames(['a','a','a','b','b','a','b'], ['10:00','10:40','11:00','09:00','12:00','09:30','13:00'])",
    expect=['a'],
    views=[
        dict(type='array', var='keyTime', label='keyTime（打卡时间，蓝 = 正在记录的一条）', cell=100, h=150,
             index=False, color=lambda S, i, v: 'blue' if S.get('_line', 99) < 12 and S.get('index') == i else None),
        dict(type='array', var='keyName', label='keyName（对应的人）', cell=100, h=150,
             index=False, color=lambda S, i, v: 'blue' if S.get('_line', 99) < 12 and S.get('index') == i else None),
        dict(type='map', var='time_dict', label='time_dict（人 → 打卡分钟数）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=26),
        dict(type='array', var='time_list', label='time_list（排序后；比较 index 与 index−2）', cell=84, h=230,
             pointers={'index': 'blue', 'index - 2': 'pink'}),
        dict(type='text', h=90, size=28, fn=_tl),
    ],
    watch=[('name', 'name', 'blue'), ('index', 'index', 'orange'), ('res', 'res', 'green')],
    captions={
        'time_dict = {}': '`time_dict` 记录每个人的所有打卡时间',
        'n = len': '`n = {n}` 条记录',
        'for index in range(n)': lambda S, B, r: ('分组结束' if B.get('index') == S.index else f'处理第 `{S.index}` 条记录'),
        'name = keyName': '这条记录的人是 `{name}`',
        'hour, minute': '时间 `{keyTime[index]}` 拆成时 `{hour}`、分 `{minute}`',
        'if name not in': lambda S, B, r: (f'`{S.name}` 还没有记录 → 先建一个空列表' if S.name not in B.get('time_dict', {})
                                          else f'`{S.name}` 已有记录，直接追加'),
        'time_dict[name] = []': '新人建空列表',
        'time_dict[name].append': '时间换成分钟 `{hour}×60+{minute}`，加入 `{name}` 的列表：`{time_dict[name]}`',
        'res = []': '`res` 保存被警告的人',
        'for name in sorted': lambda S, B, r: ('所有人都检查完了' if B.get('name') == S.name and 'res' in B and 'time_list' in B else f'按名字字典序处理 `{S.name}`（题目要求答案按字典序）'),
        'if len(time_dict[name]) < 3': lambda S, B, r: (f'`{S.name}` 只有 `{len(S.time_dict[S.name])}` 次打卡，少于 3 次 → 不可能被警告'
                                                       if len(S.time_dict[S.name]) < 3 else f'`{S.name}` 有 `{len(S.time_dict[S.name])}` 次打卡 ≥ 3，要检查'),
        'continue': '跳过这个人',
        'time_list = sorted': '把 `{name}` 的时间从小到大排序：`{time_list}`',
        'for index in range(2': lambda S, B, r: ('这个人的打卡都看完了，没有触发警告' if B.get('index') == S.index and B.get('name') == S.name and 'time_list' in B and S.get('_line') == 18 and B.get('time_list') == S.time_list and B.get('index', 0) >= 2 else f'从第 3 条开始，看 `index = {S.index}` 与前两条'),
        'if time_list[index]': lambda S, B, r: (f'`{S.time_list[S.index]} − {S.time_list[S.index - 2]} = {S.time_list[S.index] - S.time_list[S.index - 2]}` ≤ 60 '
                                                f'→ 这三次打卡都在一小时内，==触发警告=='
                                                if S.time_list[S.index] - S.time_list[S.index - 2] <= 60 else
                                                f'`{S.time_list[S.index]} − {S.time_list[S.index - 2]} = {S.time_list[S.index] - S.time_list[S.index - 2]}` > 60 → 不在一小时内，继续看下一个'),
        'res.append(name)': '`{name}` 加入答案：`{res}`',
        'break': '这个人已确定，不用再看了',
        'return res': '被警告的人：=={ret}==',
    },
    max_steps=140,
    cards=dict(
        one_liner='排序后只需比较「当前」和「上上次」打卡的间隔',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`keyName[i]` 在 `keyTime[i]`（HH:MM）刷了一次员工卡',
                 '同一个人一小时内刷卡 ≥ 3 次就会收到警告；不跨天',
                 '按名字字典序返回被警告的人',
                 '本视频：a 在 10:00、10:40、11:00 刷卡 → `["a"]`'],
        quote='对每个员工记录其打卡的时间，并按打卡的时间从小到大进行排序，然后从第二条记录开始向后一趟扫描，每次对比当前打卡时间与上上次的打卡时间的间隔，若这个间隔在一小时内，说明这三次打卡的时间在一小时内。',
        quote_src='—— yiduobo 题解原文',
        idea=['先按人分组，把 `HH:MM` 换算成分钟',
              '每个人的时间排序；三次打卡在一小时内 ⇔ 相隔一个的两次相差 `≤ 60`',
              '遍历名字用 `sorted`，答案自然按字典序'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：时间是 `HH:MM` 字符串，要先转分钟再比较',
                 '易错：间隔 `≤ 60` 含等于，恰好 60 分钟也算一小时内',
                 '不跨天，所以不用处理 23:xx 到 00:xx',
                 '原文为 Python 2 风格，本题无需改动'],
    ),
)
