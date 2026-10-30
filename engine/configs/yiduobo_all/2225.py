CONFIG = dict(
    num=2225, title='找出输掉零场或一场比赛的玩家', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表计败场 · 按序遍历玩家',
    tags=[],
    code='''
class Solution(object):
    def findWinners(self, matches):

        candidate = set()
        cnt_dict = {}
        for winner, loser in matches:
            candidate.add(winner)
            candidate.add(loser)
            cnt_dict[loser] = cnt_dict.get(loser, 0) + 1
        
        res = [[], []]
        for index in sorted(list(candidate)):
            cnt = cnt_dict.get(index, 0)
            if cnt <= 1:
                res[cnt].append(index)
        
        return res
''',
    call='Solution().findWinners([[1,3],[2,3],[3,6],[5,6],[5,7],[4,5],[4,8]])',
    expect=[[1, 2, 4], [5, 7, 8]],
    views=[
        dict(type='array', var='matches', label='matches（[胜者, 败者]）', cell=110, h=170, font=24,
             color=lambda S, i, v: 'yellow' if S.get('loser') is not None and v == [S.get('winner'), S.get('loser')] and S['_line'] in (7, 8, 9, 10) else None),
        dict(type='set', var='candidate', label='candidate（出场过的玩家）', fmt=lambda x: str(x), h=100),
        dict(type='map', var='cnt_dict', label='cnt_dict（败者 → 输的场数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=30),
        dict(type='text', h=90, size=30, fn=lambda S: (
            f"`res[0]`（没输过）= =={S['res'][0]}==　`res[1]`（输一场）= =={S['res'][1]}==" if 'res' in S else '')),
    ],
    watch=[('index', 'index', 'yellow'), ('cnt', 'cnt', 'orange')],
    captions={
        'candidate = set()': '`candidate` 收集所有出场的玩家（去重）',
        'cnt_dict = {}': '`cnt_dict` 统计每个玩家输了几场',
        'for winner, loser in matches': lambda S, B, r: ('所有比赛都看完了' if 'loser' in B and (S.winner, S.loser) == (B.winner, B.loser) else f'这场 `{S.winner}` 胜 `{S.loser}`'),
        'candidate.add(winner)': '胜者 `{winner}` 也是出场玩家',
        'candidate.add(loser)': '败者 `{loser}` 也是出场玩家',
        'cnt_dict[loser] =': '败者 `{loser}` 输的场数 +1 → `{cnt_dict[loser]}`',
        'res = [[], []]': '`res[cnt]` 的下标正好是败场数：`res[0]` 没输过，`res[1]` 输一场',
        'for index in sorted': lambda S, B, r: ('玩家都枚举完了' if 'index' in B and S.index == B.index else f'题目要求递增，所以按从小到大枚举：`index = {S.index}`'),
        'cnt = cnt_dict.get': lambda S, B, r: (f'`{S.index}` 在 `cnt_dict` 里没有 → 没输过，`cnt = 0`' if S.cnt == 0
                                               else f'`{S.index}` 输了 `{S.cnt}` 场'),
        'if cnt <= 1': lambda S, B, r: (f'`cnt = {S.cnt} ≤ 1` → 符合要求' if S.cnt <= 1
                                        else f'`cnt = {S.cnt} > 1`：输得太多，跳过'),
        'res[cnt].append(index)': '`{index}` 放进 `res[{cnt}]` → `{res}`',
        'return res': '返回 `{res}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='败场数 0 或 1，直接当下标放进 res',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`matches[i] = [胜者, 败者]`，找出没输过的人、恰好输一场的人，各自升序',
                 '示例：10 场比赛 → `[[1,2,10],[4,5,7,8]]`',
                 '本视频：`[[1,3],[2,3],[3,6],[5,6],[5,7],[4,5],[4,8]]` → `[[1,2,4],[5,7,8]]`'],
        quote='使用哈希表统计每个玩家输掉的场次，然后从小到大遍历出现的所有玩家，利用哈希表判断当前玩家是否没输过或者只输了一场，然后更新答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历 matches：胜者败者都进 `candidate`，败者败场 +1',
              '玩家按编号从小到大枚举，所以答案天然有序，不用再排',
              '败场数 `cnt` 为 0 或 1 时，直接 `res[cnt].append(index)`'],
        summary=['时间 `O(n log n)`（只排序一次玩家），空间 `O(n)`',
                 '易错：没输过的人不在 `cnt_dict`，要用 `.get(index, 0)`',
                 '`cnt` 只可能是 0 或 1 才会下标访问 `res`，所以先判断 `cnt <= 1`',
                 '对比灵神：灵神用 Counter + 两次推导式各排一次；本文只排一次、边枚举边分组',
                 '原文为 Python 2 风格，代码一字未改'],
    ),
)
