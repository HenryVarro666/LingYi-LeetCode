CONFIG = dict(
    num=1418, title='点菜展示表', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表分桌统计 · 菜名排序定列',
    code='''
class Solution(object):
    def displayTable(self, orders):

        table_dict = {}
        f_set = set()
        for c, t, f in orders:
            t = int(t)
            if t not in table_dict:
                table_dict[t] = []
            table_dict[t].append(f)
            if f not in f_set:
                f_set.add(f)
        
        f_num = len(f_set)
        sorted_f = sorted(list(f_set))
        f_mapping = {f : index + 1 for index, f in enumerate(sorted_f)}
        res = [['Table'] + sorted_f]
        
        for table in sorted(table_dict.keys()):
            tmp = [table] + [0] * f_num
            for f in table_dict[table]:
                tmp[f_mapping[f]] += 1
            
            res.append([str(x) for x in tmp])
        
        return res
''',
    call='Solution().displayTable([["David","3","Ceviche"],["Corina","10","Beef"],["David","3","Fried"],["Carla","5","Water"],["Rous","3","Ceviche"]])',
    expect=[['Table', 'Beef', 'Ceviche', 'Fried', 'Water'], ['3', '0', '2', '1', '0'], ['5', '0', '0', '0', '1'], ['10', '1', '0', '0', '0']],
    views=[
        dict(type='text', fn=lambda S: ('订单 `(顾客, 桌号, 菜)`：' + '  '.join(f"{'==' if S.get('_idx') == i else ''}{o[1]}桌:{o[2]}{'==' if S.get('_idx') == i else ''}" for i, o in enumerate(S['orders']))) if 'orders' in S else '', size=24, h=90),
        dict(type='map', var='table_dict', label='table_dict：桌号 → 点过的菜', fmt=lambda k, v: f'{k}桌: {v}', h=230),
        dict(type='set', var='f_set', label='f_set：出现过的菜', h=120),
        dict(type='text', fn=lambda S: (f"列顺序 `sorted_f` = {S['sorted_f']}" if 'sorted_f' in S else ''), size=24, h=60),
        dict(type='table', var='res', label='res：展示表（第一行是表头）', cell=150, h=300),
    ],
    watch=[('t', 't', 'blue'), ('f', 'f', 'pink'), ('table', 'table', 'cyan'), ('tmp', 'tmp', 'green')],
    captions={
        'table_dict = {}': '`table_dict`：桌号 → 这张桌点的菜列表',
        'f_set = set()': '`f_set`：所有出现过的菜名，用来确定列',
        'for c, t, f in orders': lambda S, B, r: ('订单都处理完了，开始整理表头' if sum(len(v) for v in S.table_dict.values()) == len(S.orders)
                                                  else f'取下一条订单：顾客 `{S.c}`，桌 `{S.t}`，菜 `{S.f}`（顾客名用不上）'),
        't = int(t)': '桌号原本是字符串，转成数字 `{t}`，后面才能按数值排序（`10` 应排在 `5` 后面）',
        'if t not in table_dict': lambda S, B, r: (f'桌 `{S.t}` 还没出现过 → 先建一个空列表' if S.t not in S.table_dict else f'桌 `{S.t}` 已有记录'),
        'table_dict[t] = []': '桌 `{t}` 开始记录 → `{table_dict}`',
        'table_dict[t].append': '把 `{f}` 记到桌 `{t}`：`{table_dict[t]}`',
        'if f not in f_set': lambda S, B, r: (f'`{S.f}` 是新菜 → 加入集合' if S.f not in S.f_set else f'`{S.f}` 已在集合里'),
        'f_set.add': '集合加入 `{f}` → 现有 {len(f_set)} 种菜',
        'f_num = len': '一共 `{f_num}` 种菜，也就是展示表的数据列数',
        'sorted_f = sorted': '菜名按字典序排序 → `{sorted_f}`，这就是表头里菜的顺序',
        'f_mapping = ': '菜名 → 列号（从 1 开始，0 号列留给桌号）：`{f_mapping}`',
        'res = [[': '表头 = `Table` + 排好序的菜名：`{res[0]}`',
        'for table in sorted': lambda S, B, r: ('所有桌都处理完了' if len(S.res) - 1 == len(S.table_dict) else f'按桌号从小到大处理：桌 `{S.table}`'),
        'tmp = [table]': '这一行先填桌号，其余每种菜计数 0：`{tmp}`',
        'for f in table_dict': lambda S, B, r: (f'桌 `{S.table}` 的菜都数完了' if sum(S.tmp[1:]) == len(S.table_dict[S.table]) else f'数桌 `{S.table}` 点的下一道菜：`{S.f}`'),
        'tmp[f_mapping[f]] += 1': '`{f}` 在第 `{f_mapping[f]}` 列 → 计数加一：`{tmp}`',
        'res.append': '这一行全部转成字符串，加入答案：`{res[-1]}`',
        'return res': '返回展示表，共 `{len(res)}` 行（1 行表头 + {len(res) - 1} 张桌）',
    },
    cards=dict(
        one_liner='先按桌分组记菜，再给菜名排序定列，最后按桌号逐行计数',
        complexity='时间 `O(n + m log m + T log T + T·m)`，空间 `O(n + T·m)`（`m` 菜种数，`T` 桌数）',
        problem=['`orders[i] = [顾客名, 桌号, 菜名]`，输出点菜展示表',
                 '第一行是 `Table` 加上所有菜名（字典序）；之后每行是桌号和这桌各菜的份数',
                 '行按桌号数值升序；表里的数字都是字符串',
                 '示例（缩短菜名）：5 条订单 → 3 张桌、4 种菜'],
        quote='直接一趟扫描，分桌子统计每张桌子点到菜，并记录下所有点的菜的集合。接下来对集合中的菜按字典序进行排序，这里得到的顺序就是最终答案中菜的排列顺序。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟扫描：`table_dict` 记每桌点了什么菜，`f_set` 收集所有菜名',
              '菜名排序后建 `f_mapping`：菜名 → 列号，表头也就定下来了',
              '桌号升序遍历，每桌用 `[桌号] + [0]*菜数` 当一行，点到的菜在对应列 +1'],
        summary=['时间 `O(n + m log m + T log T + T·m)`，空间 `O(n + T·m)`',
                 '易错：桌号要先 `int()` 再排序，字符串排序会让 `10` 排在 `5` 前面',
                 '易错：列号从 1 开始（`index + 1`），第 0 列是桌号',
                 '易错：输出里的数字（含桌号）都要转成字符串',
                 '原文已是 Python 3 可运行的写法，未做改动'],
    ),
)
