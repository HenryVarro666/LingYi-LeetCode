def _row(S, k):
    T = S.get('transactions')
    if not T or k >= len(T):
        return ''
    fl = S.get('flag')
    mk = ''
    if S.get('i') == k:
        mk += ' ←i'
    if S.get('j') == k:
        mk += ' ←j'
    bad = fl is not None and fl[k]
    return f"`{k}` `{T[k]}`" + (' ==无效==' if bad else '') + mk


CONFIG = dict(
    num=1169, title='查询无效交易', difficulty='Medium', category='模拟',
    author='yiduobo', technique='暴力枚举 · 两两比较',
    tags=[],
    code='''
class Solution(object):
    def invalidTransactions(self, transactions):

        n = len(transactions)
        flag = [False] * n

        name_dict = {}
        name_cnt= 0
        city_dict = {}
        city_cnt = 0

        tmp_list = []

        for i in range(n):
            name, t, m, city = transactions[i].split(',')
            if int(m) > 1000:
                flag[i] = True
            
            if name not in name_dict:
                name_dict[name] = name_cnt
                name_cnt += 1

            if city not in city_dict:
                name_dict[city] = city_cnt
                city_cnt += 1

            tmp_list.append([name, int(t), city])

        for i in range(n - 1):
            for j in range(i + 1, n):
                if tmp_list[i][0] == tmp_list[j][0] and abs(tmp_list[i][1] - tmp_list[j][1]) <= 60 and tmp_list[i][2] != tmp_list[j][2]:
                    flag[i] = flag[j] = True
        
        res = []
        for i in range(n):
            if flag[i]:
                res.append(transactions[i])
        
        return res
''',
    call='Solution().invalidTransactions(["alice,20,800,mtv", "alice,50,100,beijing", "bob,30,1200,sf"])',
    expect=["alice,20,800,mtv", "alice,50,100,beijing", "bob,30,1200,sf"],
    views=[
        dict(type='text', h=70, size=28, fn=lambda S: _row(S, 0)),
        dict(type='text', h=70, size=28, fn=lambda S: _row(S, 1)),
        dict(type='text', h=70, size=28, fn=lambda S: _row(S, 2)),
        dict(type='array', var='flag', label='flag（True = 无效交易）', cell=100, h=190,
             color=lambda S, k, v: 'red' if v else None),
        dict(type='text', h=120, size=28,
             fn=lambda S: (f"比较 `{S['tmp_list'][S['i']][0]}`/`{S['tmp_list'][S['j']][0]}`，时间差 `{abs(S['tmp_list'][S['i']][1] - S['tmp_list'][S['j']][1])}`，城市 `{S['tmp_list'][S['i']][2]}`/`{S['tmp_list'][S['j']][2]}`"
                           if 'j' in S and 'tmp_list' in S and S['j'] < len(S['tmp_list']) and S['i'] < len(S['tmp_list']) and S.get('_line') else '')),
    ],
    skip=['name_cnt += 1', 'city_cnt += 1', 'name_dict[name] = name_cnt', 'name_dict[city] = city_cnt'],
    watch=['i', 'j', ('flag', 'flag', 'red'), ('res', 'res', 'green')],
    captions={
        'flag = [False]': '`flag[i]` 标记第 i 笔交易是否无效，开始全部 ==False==',
        'name, t, m, city =': '拆开第 {i} 笔交易：名字 `{name}`，时间 `{t}`，金额 `{m}`，城市 `{city}`',
        'if int(m) > 1000': lambda S, B, r: (f"金额 `{S.m}` ==超过 1000== → 无效" if int(S.m) > 1000 else f"金额 `{S.m}` 没超过 1000，这条规则不触发"),
        'flag[i] = True': '第 {i} 笔金额超限 → `flag[{i}] = True`',
        'tmp_list.append': '记下 `[名字, 时间, 城市]`，后面两两比较时用',
        'if tmp_list[i][0] ==': lambda S, B, r: (
            f"第 {S.i} 笔 `{S.tmp_list[S.i][0]}` vs 第 {S.j} 笔 `{S.tmp_list[S.j][0]}`：同名 = {S.tmp_list[S.i][0] == S.tmp_list[S.j][0]}，"
            f"时间差 {abs(S.tmp_list[S.i][1] - S.tmp_list[S.j][1])} ≤ 60 = {abs(S.tmp_list[S.i][1] - S.tmp_list[S.j][1]) <= 60}，"
            f"城市不同 = {S.tmp_list[S.i][2] != S.tmp_list[S.j][2]} → " + ('==三条件都满足==' if (S.tmp_list[S.i][0] == S.tmp_list[S.j][0] and abs(S.tmp_list[S.i][1] - S.tmp_list[S.j][1]) <= 60 and S.tmp_list[S.i][2] != S.tmp_list[S.j][2]) else '不是同一人的可疑组合，跳过')),
        'flag[i] = flag[j] = True': '同名、60 分钟内、不同城市 → ==两笔都无效==：`flag[{i}]`、`flag[{j}]` 置 True',
        'if flag[i]': lambda S, B, r: (f"`flag[{S.i}]` = {S.flag[S.i]}" + ('：无效，收进答案' if S.flag[S.i] else '：有效，跳过')),
        'res.append': '无效交易 `{transactions[i]}` 加入答案（保持原顺序）',
        'return res': '共 {len(res)} 笔无效交易：`{res}`',
    },
    cards=dict(
        one_liner='n 只有 1000，直接两两枚举，满足条件的都标记',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['每条交易是 `"名字,时间,金额,城市"`，满足任一条件即无效：',
                 '① 金额超过 1000',
                 '② 同名、相隔 ==不超过 60 分钟==，且城市不同（两笔都无效）',
                 '返回所有无效交易（顺序任意）'],
        quote='由于题目中给出的交易总数不超过1000，因此我在这里是采用的比较暴力的做法，先逐个枚举交易，将其中金额超过1000的交易加入答案当中，接下来两两枚举交易',
        quote_src='—— yiduobo 题解原文',
        idea=['第一遍：拆分每条交易，金额超 1000 的先标记，同时把 `[名字, 时间, 城市]` 存起来',
              '第二遍：两两枚举 `(i, j)`，同名且时间差 `≤ 60` 且城市不同 → 两笔都标记',
              '最后按下标顺序收集被标记的交易'],
        summary=['时间 `O(n^2)`，`n ≤ 1000` 足够',
                 '时间差是 `<= 60`，包含 60 分钟；两笔交易都要标记，不是只标一笔',
                 '原文里建了名称/城市编号表，但比较时并没有用到（城市还写进了 `name_dict`），不影响结果',
                 '原文已是 Python 3 可运行写法，代码未改动'],
    ),
)
