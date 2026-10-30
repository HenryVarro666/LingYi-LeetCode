CONFIG = dict(
    num=2923, title='找到冠军 I', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='候选冠军一趟遍历',
    tags=[],
    code='''
class Solution(object):
    def findChampion(self, grid):

        res = 0
        for index in range(1, len(grid)):
            if grid[index][res] == 1:
                res = index
        
        return res
''',
    call='Solution().findChampion([[0,1,0,1],[0,0,0,0],[1,1,0,1],[0,1,0,0]])',
    expect=2,
    views=[
        dict(type='grid', var='grid', label='grid[a][b]=1 表示 a 队胜 b 队（黄格 = 当前对决）', cursors=[('index', 'res', 'yellow', '')], h=260,
             color=lambda S, i, j, v: ('green' if v == 1 and S.get('index') == i and j == S.get('res') and S['_line'] >= 7 else None)),
        dict(type='text', size=32, h=60, fn=lambda S: f"候选冠军：=={S['res']}== 号队" if 'res' in S else ''),
    ],
    watch=[('index', 'index', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = 0': '候选冠军先定为 0 号队',
        'if grid[index][res]': lambda S, B, ret: f"让 {S['index']} 队对候选 {S['res']} 队：`grid[{S['index']}][{S['res']}]` = {S['grid'][S['index']][S['res']]} → " + ('当前队伍获胜' if S['grid'][S['index']][S['res']] == 1 else '候选冠军获胜，继续比下一个'),
        'res = index': '当前队伍赢了候选，由传递性它也赢过之前所有被候选击败的队 → 候选改为 `{index}`',
        'return res': '一趟比完，候选冠军就是冠军：=={res}== 号队',
    },
    cards=dict(
        one_liner='谁赢了谁当候选，传递性保证一趟遍历够用',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['n 支队伍两两比赛过，`grid[i][j]==1` 表示 i 队胜 j 队',
                 '胜负关系有传递性，求没人能击败的冠军队伍',
                 '示例：`[[0,0,1],[1,0,1],[0,0,0]]` → `1`；视频演示 4 队'],
        quote='若候选冠军获胜，那么则继续向后比较；反之若当前队伍获胜，那么根据传递性，当前队伍一定也胜过了之前的所有队伍。',
        quote_src='—— yiduobo 题解',
        idea=['题目保证两两比过、有传递性，所以一定存在冠军',
              '候选获胜就保留，当前队伍获胜就替换候选',
              '被换下的候选和它击败的队伍，都不可能是冠军'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '==比较的是 `grid[index][res]`==：当前队伍对候选，顺序别写反',
                 '依赖传递性；2924 不保证两两比过，要改用入度统计'],
    ),
)
