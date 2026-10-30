CONFIG = dict(
    num=2923, title='找到冠军 I', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='打擂台',
    tags=[],
    code='''
class Solution:
    def findChampion(self, grid: List[List[int]]) -> int:
        ans = 0
        for i, row in enumerate(grid):
            if row[ans]:
                ans = i
        return ans
''',
    call='Solution().findChampion([[0,0,1,0,1],[1,0,1,1,1],[0,0,0,0,1],[1,0,1,0,1],[0,0,0,0,0]])',
    expect=1,
    views=[
        dict(type='grid', var='grid', label='grid[i][j]=1 表示 i 队比 j 队强', cursors=[('i', 'ans', 'yellow', '(i,ans)')], h=330,
             color=lambda S, i, j, v: ('green' if v == 1 and S.get('i') == i and j == S.get('ans') and S['_line'] >= 6 else None)),
        dict(type='text', size=32, h=60, fn=lambda S: f"当前擂主 =={S['ans']}== 号队" if 'ans' in S else ''),
    ],
    watch=[('i', 'i', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '先假设 0 号队是冠军（擂主）',
        'if row[ans]': lambda S, B, ret: f"`grid[{S['i']}][{S['ans']}] = {S['grid'][S['i']][S['ans']]}`：" + (f"{S['i']} 队比擂主 {S['ans']} 队强 → 挑战成功" if S['grid'][S['i']][S['ans']] else f"{S['i']} 队打不过擂主 {S['ans']} 队 → 擂主不变"),
        'ans = i': '擂主换成 `{i}` 号队：它比之前的擂主强，传递性保证它也比 `[1, i-1]` 里的队强',
        'return ans': '没有人能再击败擂主，冠军是 =={ans}== 号队',
    },
    cards=dict(
        one_liner='擂主不断被更强的队伍取代，打一圈就是冠军',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`grid[i][j]=1` 表示 i 队比 j 队强，否则 j 队更强，没有平手',
                 '没有任何队伍比它强的队伍是冠军，强弱关系有传递性',
                 '示例：`[[0,1],[0,0]]` → `0`'],
        quote='假设冠军是 ans=0，我们从 i=1 开始遍历，寻找可以击败 ans 的队伍，也就是 grid[i][ans]=1。',
        quote_src='—— 灵茶山艾府题解（方法三：打擂台）',
        idea=['若 `grid[i][ans] = 1`，i 比擂主强，擂主换成 i',
              '`[1, i-1]` 中没有比 0 强的队，更别说比 i 强，所以不用回头',
              '一遍扫完，剩下的擂主就是冠军'],
        summary=['打擂台 `O(n)`；另两种写法：行和等于 `n-1`（横看成岭）、整列全 0（侧成峰），都是 `O(n^2)`',
                 '==判断的是 `row[ans]`，不是 `row[i]`==：看 i 有没有赢过擂主',
                 '依赖「保证有冠军」和传递性，换成有向图（2924）就不能这样做'],
    ),
)
