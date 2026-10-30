def _grid(S):
    m, n = S['m'], S['n']
    return ['.' * n] + ['#' * (n - 1) + '.'] * (m - 1)


CONFIG = dict(
    num=3963, title='构造恰好一条路径的网格', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='先右后下的路径',
    tags=['灵神题单', '难度分 1311'],
    code='''
class Solution:
    def createGrid(self, m: int, n: int) -> list[str]:
        return ['.' * n] + ['#' * (n - 1) + '.'] * (m - 1)
''',
    call='Solution().createGrid(4, 5)',
    expect=['.....', '####.', '####.', '####.'],
    views=[
        dict(type='text', fn=lambda S: '路径：第一行全为 `.`，其余每行只有最后一格是 `.`，其余全是 `#`'),
        dict(type='grid', var=lambda S: [list(r) for r in _grid(S)], h=360, label='返回的网格',
             color=lambda S, i, j, v: 'green' if v == '.' else None,
             cursors=[]),
    ],
    watch=['m', 'n'],
    captions={
        "return": '第一行 `.` * {n}，后面 `{m-1}` 行都是 `#` * {n-1} + `.`：只有 ==先向右、再向下== 这一条路，其余格子全是障碍',
    },
    cards=dict(
        before=[dict(heading='构造题的套路', lines=['答案不唯一，只要给出一个满足条件的就行', '先想最简单的形状：一条直线加一条直线', '“全堵死，再挖一条路”比“逐格判断”简单得多'])],
        after=[dict(heading='为什么路径唯一', lines=['路径上的格子只有一条出路：不是右就是下被堵', '第一行向右走到头，再沿最后一列向下', '偏离这条路就会撞上 `#`'])],
        one_liner='全放障碍，再挖出一条路',
        complexity='时间 `O(m+n)`，空间 `O(1)`（返回值不计入）',
        problem=['构造 `m x n` 网格，`.` 空格、`#` 障碍',
                 '从 `(0,0)` 只能右移或下移到 `(m-1,n-1)`，要求恰好一条路径',
                 '本视频：`m = 4, n = 5`'],
        quote='先创建一个全为 # 的网格，然后选任意一条从左上角到右下角的移动路径，把路径上的字符改成 . 号，即可满足要求。',
        quote_src='—— 灵茶山艾府题解',
        idea=['选一条先往右到右上角、再往下到右下角的路径',
              '路径上的格子是 `.`，其余都是 `#`，路径自然唯一',
              'Python 里同一个字符串被引用 `m-1` 次，只需 `O(m+n)`'],
        summary=['时间 `O(m+n)`（Python 共享同一字符串的引用）',
                 '易错：下面 `m-1` 行是 `#` * (n-1) + `.`，不是 `.` 开头',
                 '先往下再往右同样可行；本题是构造题，答案不唯一'],
    ),
)
