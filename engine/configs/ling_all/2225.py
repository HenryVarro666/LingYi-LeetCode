def _res(S):
    if 'players' not in S:
        return ''
    lc = S.get('loss_count')
    if lc is None:
        return '`players` 收集了所有参赛的人；下一步统计谁输了几场'
    zero = sorted(x for x in S['players'] if x not in lc)
    one = sorted(x for x, c in lc.items() if c == 1)
    return f'没输过：=={zero}==　　恰好输一场：=={one}=='


CONFIG = dict(
    num=2225, title='找出输掉零场或一场比赛的玩家', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希集合 + 哈希表计数',
    tags=[],
    code='''
class Solution:
    def findWinners(self, matches: List[List[int]]) -> List[List[int]]:
        players = set(x for m in matches for x in m)
        loss_count = Counter(loser for _, loser in matches)
        return [sorted(x for x in players if x not in loss_count),
                sorted(x for x, c in loss_count.items() if c == 1)]
''',
    call='Solution().findWinners([[1,3],[2,3],[3,6],[5,6],[5,7],[4,5],[4,8]])',
    expect=[[1, 2, 4], [5, 7, 8]],
    views=[
        dict(type='array', var='matches', label='matches（[胜者, 败者]）', cell=110, h=170, font=24),
        dict(type='set', var='players', label='players（所有参赛玩家）', fmt=lambda x: str(x), h=110),
        dict(type='map', var='loss_count', label='loss_count（玩家 → 输的场数）', fmt=lambda k, v: f'{k}: {v}', h=170, font=30),
        dict(type='text', h=90, size=30, fn=_res),
    ],
    watch=[],
    captions={
        'players = set': lambda S, B, r: f'遍历 matches，把胜者、败者的编号都加入哈希集合 → `players = {sorted(S.players)}`',
        'loss_count = Counter': lambda S, B, r: f'只数败者：`loss_count` 记录每个人输的场数 → `{dict(S.loss_count)}`。从没输过的人不会出现在里面',
        'return [sorted(x for x in players': lambda S, B, r: ('两个列表都排好了，返回 `{}`'.format(r) if r is not None else '第一个列表：在 `players` 里、却不在 `loss_count` 里的人 = ==没输过==，排序 → '
                                                          f'`{sorted(x for x in S.players if x not in S.loss_count)}`'),
        'sorted(x for x, c in': lambda S, B, r: ('第二个列表：`loss_count` 里次数恰好为 1 的人 = ==只输一场==，排序 → '
                                                f'`{sorted(x for x, c in S.loss_count.items() if c == 1)}`'),
    },
    cards=dict(
        one_liner='参赛的人减去输过的人 = 没输过；计数等于 1 = 只输一场',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`matches[i] = [胜者, 败者]`，找出没输过的人、恰好输一场的人，各自升序',
                 '只考虑至少打过一场的玩家',
                 '本视频：`[[1,3],[2,3],[3,6],[5,6],[5,7],[4,5],[4,8]]` → `[[1,2,4],[5,7,8]]`'],
        quote='遍历 matches，把所有玩家的编号加入哈希集合 players。遍历 matches，统计 loser 的出现次数，加到哈希表 lossCount 中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['哈希集合 `players` 保证不漏掉只赢不输的人',
              '哈希表只数败者：没出现 = 0 场，值为 1 = 1 场',
              '两个列表分别过滤，再各自排序'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错：没输过的人不在 `loss_count` 里，必须靠 `players` 才能找到',
                 '易错：只统计败者，胜者不计数',
                 '原文还提到可省去 `players`：把胜者以 0 插入 `lossCount`，最后按次数 `< 2` 分到两个列表',
                 '代码用生成器写成两个推导式，Python 3.12 下一行就跑完'],
    ),
)
