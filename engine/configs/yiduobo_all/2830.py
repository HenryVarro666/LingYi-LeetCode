OFFERS = [[0, 0, 1], [0, 2, 2], [1, 3, 2], [3, 5, 4]]


def _dict_txt(S):
    d = S.get('end_dict')
    if d is None:
        return '用哈希表 `end_dict` 把 offer 按 end 收集起来'
    return '  |  '.join(f'end={e}: ' + ' '.join(f'({s},{w})' for s, w in lst) for e, lst in sorted(d.items()))


def _cur_txt(S):
    if 'index' not in S:
        return ''
    i = S['index']
    if S['_line'] in (18, 19, 21, 23) and 'start' in S:
        return f'offer `[{S["start"]}, {i}]` 出价 {S["gold"]}：选它的总价 = ==' + str(S['gold'] + (S['f'][S['start'] - 1] if S['start'] else 0)) + '=='
    return f'`f[{i}]` = 房屋 0 到 {i} 能卖出的最大价格'


CONFIG = dict(
    num=2830, title='销售利润最大化', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='按 end 建哈希表 · 线性 DP',
    tags=['灵神题单', '难度分 1851'],
    code='''
class Solution(object):
    def maximizeTheProfit(self, n, offers):

        end_dict = {}
        for start, end, gold in offers:
            if end not in end_dict:
                end_dict[end] = []
            end_dict[end].append([start, gold])
        
        f = []
        for index in range(n):
            if index > 0:
                f.append(f[-1])
            else:
                f.append(0)

            for start, gold in end_dict.get(index, []):
                if start == 0:
                    v = gold
                else:
                    v = gold + f[start - 1]

                f[-1] = max(f[-1], v)
        
        return f[-1]
''',
    call=f'Solution().maximizeTheProfit(6, {OFFERS!r})',
    expect=6,
    skip=['end_dict[end] = []', 'end_dict[end].append', 'if end not in end_dict', 'for start, end, gold in offers'],
    views=[
        dict(type='text', fn=_dict_txt, size=26, h=70),
        dict(type='array', var='f', label='f[i]：房屋 0..i 能卖出的最大价格（黄 = 正在算的末位）', h=300, cell=100,
             pointers={'len(f) - 1': 'blue', 'start - 1 if _line in (18, 19, 21, 23) and start > 0 else None': 'pink'},
             pointer_labels={'len(f) - 1': 'index', 'start - 1 if _line in (18, 19, 21, 23) and start > 0 else None': 'start-1'},
             color=lambda S, i, v: 'yellow' if i == len(S['f']) - 1 else None),
        dict(type='text', fn=_cur_txt, size=28, h=90),
    ],
    watch=['index', ('start', "start if _line >= 17 else '-'", 'pink'), ('gold', "gold if _line >= 17 else '-'"),
           ('v', "v if _line in (19, 21, 23) else '-'", 'yellow'), ('f[-1]', "f[-1] if f else '-'", 'green')],
    captions={
        'end_dict = {}': '`end_dict`：key 是右端点 `end`，value 是这个 end 下所有 `[start, gold]`',
        'f = []': '`f[i]` 表示下标 0 到 `i` 的房屋能卖出的最大价格',
        'for index in range': lambda S, B, r: ('所有房屋位置都算完了' if S.index == B.get('index') else f'开始算 `f[{S.index}]`'),
        'if index > 0': lambda S, B, r: ('`index = 0`：前面没有房屋可继承' if S.index == 0 else f'`index = {S.index} > 0`：可以继承 `f[{S.index - 1}]`'),
        'f.append(f[-1])': '先==无视==房屋 `{index}`：`f[{index}] = f[{index - 1}]` = {f[-1]}',
        'f.append(0)': '`index = 0`：前面没有房屋，边界 `f[0]` 先记为 0',
        'for start, gold in end_dict.get': lambda S, B, r: (f'`end = {S.index}` 的 offer 都看完了' if 'start' in B and 'end' in S and B.get('index') == S.index and (S.start, S.gold) == (B.start, B.gold) and S.index in S.end_dict
                                                              else (f'没有以 {S.index} 结尾的 offer，只能无视' if S.index not in S.end_dict else f'枚举 `end = {S.index}` 的 offer `[{S.start}, {S.index}]`，出价 {S.gold}')),
        'if start == 0': lambda S, B, r: ('`start == 0`：买下就占了最前面，没有更靠前的 f 可加，边界要特殊处理' if S.start == 0
                                          else f'`start = {S.start} > 0`：可以接在 `f[{S.start - 1}]` 后面'),
        19: '`v = gold` = =={v}==',
        21: '`v = {gold} + f[{start - 1}]` = {gold} + {f[start - 1]} = =={v}==',
        'f[-1] = max': '`f[-1] = max({B.f[-1]}, {v})` = =={f[-1]}==',
        'return f[-1]': '答案 `f[-1]` = =={ret}==',
    },
    cards=dict(
        one_liner='f[i] 看 0 到 i：无视房屋 i，或选 end 为 i 的 offer',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['数轴上有 `n` 所房屋，每个 offer 是 `[start, end, gold]`：买下 `[start, end]` 全部房屋',
                 '同一所房屋只能卖一次，求最多卖得多少金币',
                 '示例：`n=5, offers=[[0,0,1],[0,2,2],[1,3,2]]` → `3`'],
        quote='注意到本题中房屋的坐标都处于10^5内，那么就可以利用这一点建立动态规划的状态。令f[i]表示下标位置0到i的所有房屋可以卖出的最大价格。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]` 先初始化为 `f[i - 1]`：==无视==下标 `i` 的房屋',
              '再试每个 `end = i` 的 offer：`f[start - 1] + gold`',
              '用哈希表 `end_dict` 按 end 收集，避免每次遍历所有 offer'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '易错：`start == 0` 时没有 `f[start - 1]`，直接取 `gold`',
                 '这里 `f[-1]` 就是当前正在算的 `f[index]`',
                 '对比灵神：灵神把 f 整体右移一位（`f[0]=0`），省掉了 `start == 0` 的特判'],
    ),
)
