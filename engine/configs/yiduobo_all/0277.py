_G = [[1,1,0,1,0], [0,1,1,1,0], [0,0,1,1,0], [0,0,0,1,0], [1,0,0,1,1]]

CONFIG = dict(
    num=277, title='搜寻名人', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='淘汰候选人 · 3n 次 knows',
    tags=['灵神题单·图论算法', '灵神题单·贪心与思维'],
    setup='''
graph = [[1,1,0,1,0],
         [0,1,1,1,0],
         [0,0,1,1,0],
         [0,0,0,1,0],
         [1,0,0,1,1]]
def knows(a, b):
    return bool(graph[a][b])
''',
    code='''
class Solution(object):
    def findCelebrity(self, n):

        candidate = 0
        flag = False

        while not flag:
            flag = True
            for p in range(candidate + 1, n):
                if knows(candidate, p):
                    candidate = p
                    flag = False
                    break
        
        for p in range(n):
            if p != candidate and (knows(candidate, p) or not knows(p, candidate)):
                return -1
        
        return candidate
''',
    call='Solution().findCelebrity(5)',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: ('`graph[行][列]` = 行号的人是否认识列号的人（1 = 认识）。候选人 `' + str(S['candidate']) + '`'
                                        if 'candidate' in S else '`graph[行][列]` = 行号的人是否认识列号的人（1 = 认识）')),
        dict(type='grid', var=lambda S: _G, label='', h=430, values=True,
             rows=['0', '1', '2', '3', '4'], cols=['0', '1', '2', '3', '4'],
             cursors=[('candidate', 'p', 'yellow', 'knows(c,p)')],
             color=lambda S, i, j, v: ('green' if i == S.get('candidate') and S['_line'] >= 15 else None)),
    ],
    watch=[('candidate', 'candidate', 'yellow'), ('p', 'p', 'blue'), 'flag'],
    captions={
        'candidate = 0': '先假设 `0` 号是名人候选人',
        5: '`flag` 表示这一轮候选人有没有被推翻',
        'while not flag': '`flag = {flag}`：{"还没确认候选人，开始一轮扫描" if not flag else "候选人没再变，淘汰阶段结束"}',
        'flag = True': '先假定这一轮候选人不会变',
        'for p in range(candidate': '检查 `{p}` 号（`candidate = {candidate}`）',
        'if knows(candidate, p)': lambda S, B, r: (f'`knows({S.candidate}, {S.p})` = {bool(_G[S.candidate][S.p])}：'
              + ('候选人认识 p → ==候选人不可能是名人==' if _G[S.candidate][S.p] else '候选人不认识 p，p 暂时留着，继续往后看')),
        'candidate = p': '`candidate` 认识别人 → 出局；它和 p 之间的人也都被淘汰过。新候选人 =={candidate}==',
        12: '候选人换了 → `flag = False`，要从新候选人后面重新扫',
        'break': '直接跳出 for，进入下一轮',
        'for p in range(n)': '核验阶段：检查 `{p}` 号（候选人 `{candidate}`）',
        'if p != candidate and': lambda S, B, r: (f'核验 `{S.p}` 号：' + ('是候选人自己，跳过' if S.p == S.candidate else
              f'`knows(c,p)` = {bool(_G[S.candidate][S.p])}，`knows(p,c)` = {bool(_G[S.p][S.candidate])}：' +
              ('出现矛盾 → 返回 -1' if (_G[S.candidate][S.p] or not _G[S.p][S.candidate]) else '他认识候选人，候选人不认识他 → 通过'))),
        'return -1': '核验失败：没有名人，返回 `-1`',
        'return candidate': '所有人都认识 `{candidate}`，`{candidate}` 谁也不认识 → ==名人是 {candidate}==',
    },
    cards=dict(
        one_liner='knows(x, y) 为真，x 一定不是名人；为假，y 一定不是名人',
        complexity='时间 `O(n)`，`knows` 调用约 `3n` 次，空间 `O(1)`',
        problem=['n 个人，名人 ==被所有人认识、自己谁也不认识==',
                 '只能调用 `knows(a, b)`：a 是否认识 b，找出名人编号，没有返回 `-1`',
                 '本视频：n = 5，名人是 `3`'],
        quote='若某一时刻knows(p, candidate)为false，那么说明candidate不是要找的答案……candidate + 1到p - 1这些人都不会是名人。',
        quote_src='—— yiduobo 题解原文',
        idea=['`knows(candidate, p)` 为真：==candidate 认识别人，不可能是名人==，候选人换成 `p`',
              '被跳过的人在前面的检测里也已经被排除，所以每个人只扫一次',
              '最后再用 `2n` 次 `knows` 核验候选人'],
        summary=['时间 `O(n)`：淘汰阶段 `n` 次，核验阶段 `2n` 次',
                 '淘汰阶段只能选出==唯一可能的候选人==，必须再核验一遍',
                 '核验要同时查两个方向：所有人认识他，他不认识任何人',
                 '原文代码已是 Python 3 写法，未做修改；`knows` 在 setup 里按示例矩阵定义'],
    ),
)
