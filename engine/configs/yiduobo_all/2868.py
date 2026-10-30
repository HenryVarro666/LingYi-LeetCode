def _hl(player):
    def f(S, i, v):
        if 'pre_index' not in S or 'pre_player' not in S:
            return None
        if S['pre_player'] == player and i == S['pre_index']:
            return 'yellow'
        return None
    return f


CONFIG = dict(
    num=2868, title='单词游戏', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='贪心 · 每个首字母只记最大单词',
    tags=['灵神题单·数学算法'],
    code='''
class Solution(object):
    def canAliceWin(self, a, b):
        last = [{}, {}]

        for index in range(1, len(a)):
            last[0][a[index][0]] = index
        for index in range(len(b)):
            last[1][b[index][0]] = index

        def get(pre_player, pre_index, last):
            now_player = 1 - pre_player
            if pre_player == 0:
                pre_list = a
                now_list = b
            else:
                pre_list = b
                now_list = a
            
            pre_char = pre_list[pre_index][0]
            nxt_char = chr(ord(pre_char) + 1)
            for check_char in [pre_char, nxt_char]:
                if check_char in last[now_player] and now_list[last[now_player][check_char]] > pre_list[pre_index]:
                    return last[now_player][check_char]
            
            return -1

        pre_index = 0
        pre_player = 0
        while True:
            now_index = get(pre_player, pre_index, last)
            if now_index == -1:
                return pre_player == 0
            
            pre_index, pre_player = now_index, 1 - pre_player
            print(pre_index, pre_player)
''',
    call='Solution().canAliceWin(["ananas", "atlas", "banban", "cat"], ["aro", "bat", "bz"])',
    expect=True,
    views=[
        dict(type='array', var='a', label='Alice 词表 a（黄 = 上一手出的词）', color=_hl(0), cell=130, h=210),
        dict(type='array', var='b', label='Bob 词表 b', color=_hl(1), cell=130, h=210),
        dict(type='text', fn=lambda S: (f"`last[0] = {S['last'][0]}`  `last[1] = {S['last'][1]}`" if 'last' in S else ''), size=24, h=100),
    ],
    skip=['pre_list = ', 'now_list = ', 'print(', 'while True', 'now_player = 1 - pre_player', 'for index', 'if pre_player == 0', 'nxt_char =', 'for check_char'],
    watch=[('pre_player', 'pre_player', 'blue'), ('pre_index', 'pre_index', 'yellow'), 'now_index'],
    captions={
        'last = [{}, {}]': '`last[p]`：玩家 p 的每个首字母 → 该首字母下==字典序最大==单词的下标',
        'last[0][a[index][0]]': '遍历 Alice 的词（从下标 1 起，`a[0]` 是开局就打出的词）：`last[0] = {last[0]}`',
        'last[1][b[index][0]]': '遍历 Bob 的词：`last[1] = {last[1]}`；词表有序，后写的覆盖前面，留下的就是最大的',
        'now_player = 1 - pre_player': '轮到对手：`now_player = {now_player}`',
        'pre_char = ': '{now_player} 号玩家出词：上一个词 `{pre_list[pre_index]}`，可接首字母 `{pre_char}` 或其后继字母；先试不变的（贪心结论 2）',
        'if check_char in': lambda S, B, r: (f"试首字母 `{S.check_char}`：" + (f"对手有该首字母最大词 `{S.now_list[S.last[S.now_player][S.check_char]]}`，" + ('比 `' + S.pre_list[S.pre_index] + '` 大 → ==可以接==' if S.now_list[S.last[S.now_player][S.check_char]] > S.pre_list[S.pre_index] else '但不比上一个词大 → 不能接') if S.check_char in S.last[S.now_player] else '对手没有这个首字母的词')),
        'return last[now_player]': '接上了：返回该词下标 `{ret}`，出的是该首字母下最大的词',
        'return -1': '两个首字母都接不上，对手无词可出 → 返回 `-1`',
        'pre_index = 0': '开局 Alice 先出 `a[0]`：`pre_index = 0`',
        'pre_player = 0': '`pre_player = 0`：上一手是 Alice，接下来 Bob 出',
        'now_index = get': '轮到下一位出词：对手尝试接上一手',
        'if now_index == -1': lambda S, B, r: ('`-1`：' + ('Bob' if S.pre_player == 0 else 'Alice') + ' 没词可出，输了' if S.now_index == -1 else f'`now_index = {S.now_index}`：接上了，游戏继续'),
        'return pre_player == 0': lambda S, B, r: ('最后出词的是 Alice（`pre_player = 0`）→ Alice 赢 ==True==' if S.pre_player == 0 else '最后出词的是 Bob（`pre_player = 1`）→ Alice 输 ==False=='),
        'pre_index, pre_player = ': '交换回合：`pre_index = {pre_index}`，`pre_player = {pre_player}`',
    },
    cards=dict(
        one_liner='每个首字母只留最大的词，贪心模拟到有人没词可出',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['Alice、Bob 各有一个已排序的词表，Alice 先出她的第一个词',
                 '之后每个人必须出一个==字典序更大==、首字母相同或为上一词首字母后继的词，每词只能用一次',
                 '无词可出的人输；返回 Alice 是否必胜'],
        quote='若存在多个不改变首字符的可用单词，那么就应该选择其中字典序最大的那个。',
        quote_src='—— yiduobo 题解原文',
        idea=['结论 1：同首字母有多个可用词时，直接出最大的，不影响胜负还能加速',
              '结论 2：首字母不变的词和换成后继字母的词都有时，优先首字母不变的',
              '所以每人只需哈希表 `last` 记下每个首字母的最大词下标，然后模拟'],
        summary=['时间 `O(n + m)`，空间 `O(n + m)`',
                 '`last[0]` 从下标 1 开始建：`a[0]` 开局就被用掉了',
                 '要同时判断「同首字母」和「后继首字母」，且都要比上一个词更大',
                 '原文末尾的 `print` 是调试输出，已原样保留（Python 3 写法本就兼容）',
                 '谁先无词可出谁输：返回 `pre_player == 0`'],
    ),
)
