CONFIG = dict(
    num=3963, title='构造恰好一条路径的网格', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='L 形路径',
    tags=['灵神题单', '贪心与思维', '难度分 1311'],
    code='''
class Solution(object):
    def createGrid(self, m, n):
        
        res = []
        for index in range(m - 1):
            res.append('.' + '#' * (n - 1))
        res.append('.' * n)
        return res
''',
    call='Solution().createGrid(4, 5)',
    expect=['.####', '.####', '.####', '.....'],
    views=[
        dict(type='text', fn=lambda S: '路径：先沿第一列向下，再沿最后一行向右（L 形）'),
        dict(type='grid', var=lambda S: [list(r) for r in S['res']] if 'res' in S else [], h=360, label='res',
             color=lambda S, i, j, v: 'green' if v == '.' else None),
    ],
    watch=['m', 'n', 'index'],
    captions={
        'res.append(\'.\' +': '第 `{index}` 行：首格 `.`，其余 `{n-1}` 格 `#` → `{res[-1]}`；这一行只能往下走，不能向右',
        "res.append('.' * n)": '最后一行全是 `.`：从 `({m-1}, 0)` 一路向右到终点',
        'return res': '一条 L 形路径：往下到底再向右，其余全是障碍，路径唯一',
    },
    cards=dict(
        one_liner='把路径留成 L 形，其余全堵上',
        complexity='时间 `O(mn)`，空间 `O(1)`（返回值不计入）',
        problem=['构造 `m * n` 网格，`.` 空格，`#` 障碍',
                 '从 `(0,0)` 只能右移或下移到 `(m-1,n-1)`，路径要恰好一条',
                 '本视频：`m = 4, n = 5`'],
        quote='我在这里选择的是构造L形的路径，即从(0, 0)往下走到(m - 1, 0)，然后向右走到(m - 1, n - 1)。',
        quote_src='—— yiduobo 题解原文',
        idea=['为这条路径留出足够的空格，其他地方全部填障碍物',
              '前 `m-1` 行：首字符 `.`，后面全 `#`',
              '最后一行：全 `.`'],
        summary=['时间 `O(mn)`，空间 `O(1)`（返回值不计入）',
                 '易错：循环只有 `m - 1` 次，最后一行单独加',
                 '对比灵神：灵神选先右后下，L 形方向相反'],
    ),
)
