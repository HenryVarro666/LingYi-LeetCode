CONFIG = dict(
    num=2260, title='必须拿起的最小连续卡牌数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表记录最后出现位置',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1365'],
    code='''
class Solution(object):
    def minimumCardPickup(self, cards):

        res = -1
        last_pos = {}
        for index, card in enumerate(cards):
            if card in last_pos:
                if res == -1 or index - last_pos[card] + 1 < res:
                    res = index - last_pos[card] + 1
            
            last_pos[card] = index
        
        return res
''',
    call='Solution().minimumCardPickup([3,4,2,3,4,7,2,7])',
    expect=3,
    views=[
        dict(type='array', var='cards', label='cards（框 = 当前卡牌与它上一次出现之间）', h=230,
             pointers={'index': 'blue'},
             color=lambda S, i, v: ('pink' if 'card' in S and S['last_pos'].get(S['card']) == i and i != S['index'] else 'blue' if i == S.get('index') else None),
             window=(lambda S: S['last_pos'].get(S['card']) if 'card' in S and S['last_pos'].get(S['card']) != S['index'] else None, 'index'),
             dim=lambda S, i, v: 'index' in S and i > S['index']),
        dict(type='map', var='last_pos', label='last_pos（卡牌值 → 最后一次出现的下标）', fmt=lambda k, v: f'{k}: {v}', h=170, font=34),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"上一张 `{S['card']}` 在下标 {S['last_pos'][S['card']]}：长度 `{S['index']} − {S['last_pos'][S['card']]} + 1` = =={S['index'] - S['last_pos'][S['card']] + 1}=="
                           if 'card' in S and S['card'] in S['last_pos'] and S['last_pos'][S['card']] != S['index'] else
                           '`last_pos` 只记最后一次出现：离当前最近的同值卡牌才可能最短')),
    ],
    watch=[('index', 'index', 'blue'), ('card', 'card'), ('res', 'res', 'green')],
    captions={
        'res = -1': '`res = -1`：还没找到匹配，先按“无解”处理',
        'last_pos = {}': '`last_pos` 记录每种卡牌==最后一次==出现的位置',
        'for index, card': lambda S, B, r: (f'看第 {S.index} 张卡牌：`{S.card}`' if B.get('index') != S.index else '所有卡牌都看完了'),
        'if card in last_pos': lambda S, B, r: (f'`{S.card}` 之前在下标 {S.last_pos[S.card]} 出现过 → 可以组成一段匹配' if S.card in S.last_pos
                                               else f'`{S.card}` 第一次出现，左边没有能和它匹配的牌'),
        'if res == -1 or': lambda S, B, r: (f'长度 `{S.index} − {S.last_pos[S.card]} + 1 = {S.index - S.last_pos[S.card] + 1}`，' +
                                           ('第一次找到匹配 → 更新' if S.res == -1 else
                                            (f'比 `res = {S.res}` 更短 → 更新' if S.index - S.last_pos[S.card] + 1 < S.res else f'不比 `res = {S.res}` 短 → 不更新'))),
        'res = index - last_pos': '`res` 更新为 =={res}==：首尾相同的最短一段',
        'last_pos[card] = index': '把 `{card}` 的最后位置改成 {index}：==以后的牌只需要和最近这张比==',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='最优的一段首尾相同、中间没有同值牌：只和上一次出现比',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`cards[i]` 是卡牌的值，值相同的两张牌==匹配==',
                 '求包含一对匹配卡牌的==最短连续子数组==长度，没有返回 `-1`',
                 '示例：`[3,4,2,3,4,7]` → `4`；本视频：`[3,4,2,3,4,7,2,7]` → `3`'],
        quote='对于任意位置的卡牌cards[index]，只需要找到其左侧==最后一次出现的相同卡牌==，然后使用这两个位置间的距离更新答案就能找到最优解。',
        quote_src='—— yiduobo 题解原文',
        idea=['若中间还有与头尾相同的牌，换成它和尾部就得到==更短==的合法段',
              '所以每张牌只需和它左边==最近==的同值牌配对',
              '哈希表存“最后一次出现的位置”，一趟遍历边查边更新'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '长度是 `index − last_pos[card] + 1`，别忘了 ==+1==',
                 '`res == -1` 表示还没答案，需单独判断，不能直接取 min',
                 '先用旧位置更新答案，==再==覆盖成当前位置',
                 '原文为 Python 2 风格，代码无需改动即可运行'],
    ),
)
