CONFIG = dict(
    num=2660, title='保龄球游戏的获胜者', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历模拟', tags=[],
    code='''
class Solution(object):
    def isWinner(self, player1, player2):

        s1 = s2 = 0
        for index in range(len(player1)):
            s1 += player1[index]
            s2 += player2[index]

            if (index > 0 and player1[index - 1] == 10) or (index > 1 and player1[index - 2] == 10):
                s1 += player1[index]
            
            if (index > 0 and player2[index - 1] == 10) or (index > 1 and player2[index - 2] == 10):
                s2 += player2[index]
        
        if s1 > s2:
            return 1
        elif s1 == s2:
            return 0
        else:
            return 2
''',
    call='Solution().isWinner([5,10,3,2], [6,5,7,3])',
    expect=1,
    setup='',
    views=[
        dict(type='array', var='player1', label='player1', pointers={'index': 'blue'}, h=230,
             color=lambda S, i, v: 'yellow' if v == 10 else None),
        dict(type='array', var='player2', label='player2', pointers={'index': 'pink'}, h=230,
             color=lambda S, i, v: 'yellow' if v == 10 else None),
        dict(type='text', size=32, fn=lambda S: f"得分 `s1 = {S['s1']}`　`s2 = {S['s2']}`（黄色格 = 全中 10，使后两轮得分翻倍）" if 's1' in S else ''),
    ],
    watch=[('index', 'index', 'blue'), ('s1', 's1', 'blue'), ('s2', 's2', 'pink')],
    captions={
        's1 = s2 = 0': '两人得分从 0 开始，一趟遍历同时累计',
        6: '玩家 1 第 `{index}` 轮击倒 `{player1[index]}` 个，先按原分累加：`s1` = {s1}',
        7: '玩家 2 第 `{index}` 轮击倒 `{player2[index]}` 个，先按原分累加：`s2` = {s2}',
        'if (index > 0 and player1': lambda S, B, r: f"玩家 1 前两轮里有 10 吗？" + ('有 → 这一轮得分翻倍' if (S.index > 0 and S.player1[S.index - 1] == 10) or (S.index > 1 and S.player1[S.index - 2] == 10) else '没有 → 不翻倍'),
        'if (index > 0 and player2': lambda S, B, r: f"玩家 2 前两轮里有 10 吗？" + ('有 → 这一轮得分翻倍' if (S.index > 0 and S.player2[S.index - 1] == 10) or (S.index > 1 and S.player2[S.index - 2] == 10) else '没有 → 不翻倍'),
        10: '玩家 1 第 `{index}` 轮的得分翻倍：再加一次 `{player1[index]}` → `s1` = =={s1}==',
        13: '玩家 2 第 `{index}` 轮的得分翻倍：再加一次 `{player2[index]}` → `s2` = =={s2}==',
        'if s1 > s2': '比较总分 `s1 = {s1}`，`s2 = {s2}`：玩家 1 更高才返回 1',
        'elif s1 == s2': '总分相同 → 平局，返回 0',
        'return 1': '玩家 1 获胜，返回 `1`',
        'return 0': '平局，返回 `0`',
        'return 2': '玩家 2 获胜，返回 `2`',
    },
    cards=dict(
        one_liner='一趟遍历，前两轮出现全中就把这轮得分翻倍',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['两人各打 `n` 轮，`player[i]` 是第 `i` 轮击倒的瓶数',
                 '若前一轮或前两轮击倒了 10 个，这一轮得分翻倍',
                 '总分高者获胜：玩家 1 赢返回 `1`，玩家 2 赢返回 `2`，平局返回 `0`',
                 '示例：`[5,10,3,2]` 对 `[6,5,7,3]` → `1`'],
        quote='按照题目描述的规则一趟遍历，分别计算两个人的得分，然后根据最终得分确定比赛结果即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['每轮先加原分，再检查 `index-1` 和 `index-2` 是否为 10',
              '满足就把这一轮的分再加一次（等于翻倍）',
              '遍历结束比较 `s1` 与 `s2`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：下标 `index-1`、`index-2` 要先判断 `index > 0`、`index > 1`，避免取到负下标',
                 '本题代码在 Python 3 下无需修改'],
    ),
)
