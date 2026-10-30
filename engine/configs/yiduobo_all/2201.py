CONFIG = dict(
    num=2201, title='统计可以提取的工件', difficulty='Medium', category='网格图',
    author='yiduobo', technique='二维前缀和',
    tags=[],
    code='''
class Solution(object):
    def digArtifacts(self, n, artifacts, dig):

        max_r = max_c = 0
        for r1, c1, r2, c2 in artifacts:
            max_r = max(max_r, r2)
            max_c = max(max_c, c2)
        
        f = [[0] * (max_c + 1) for _ in range(max_r + 1)]

        for r, c in dig:
            if r <= max_r and c <= max_c:
                f[r][c] = 1
        
        s = [[0] * (max_c + 1) for _ in range(max_r + 1)]
        for r in range(max_r + 1):
            for c in range(max_c + 1):
                if r == 0:
                    if c == 0:
                        s[r][c] = f[r][c]
                    else:
                        s[r][c] = s[r][c - 1] + f[r][c]
                elif c == 0:
                    s[r][c] = s[r - 1][c] + f[r][c]
                else:
                    s[r][c] = s[r - 1][c] + s[r][c - 1] - s[r - 1][c - 1] + f[r][c]
        

        res = 0
        for r1, c1, r2, c2 in artifacts:
            if r1 == 0:
                if c1 == 0:
                    now_s = s[r2][c2]
                else:
                    now_s = s[r2][c2] - s[r2][c1 - 1]
            elif c1 == 0:
                now_s = s[r2][c2] - s[r1 - 1][c2]
            else:
                now_s = s[r2][c2] - s[r2][c1 - 1] - s[r1 - 1][c2] + s[r1 - 1][c1 - 1]
            
            if now_s == (r2 - r1 + 1) * (c2 - c1 + 1):
                res += 1
        
        return res
''',
    call='Solution().digArtifacts(3, [[0,0,0,0],[0,1,1,1],[2,1,2,2]], [[0,0],[0,1],[1,1],[2,1]])',
    expect=2,
    views=[
        dict(type='text', h=60, fn=lambda S: (
            f"工件 `({S['r1']},{S['c1']})~({S['r2']},{S['c2']})`：挖到 =={S['now_s']}== 格，面积 =={(S['r2']-S['r1']+1)*(S['c2']-S['c1']+1)}==" if 'now_s' in S and 'r2' in S and 'r1' in S and S['_line'] >= 30
            else '')),
        dict(type='grid', var='f', label='f：1 = 已挖开', cursors=[('r', 'c', 'yellow', '(r,c)')], h=280,
             color=lambda S, i, j, v: 'green' if v == 1 else None),
        dict(type='grid', var='s', label='s：二维前缀和（左上角到 (r,c) 已挖格数）', cursors=[('r', 'c', 'yellow', '(r,c)')], h=280),
    ],
    watch=['r', 'c', 'r1', 'c1', 'r2', 'c2', 'now_s', ('res', 'res', 'green')],
    skip=['max_r = max(', 'max_c = max('],
    max_steps=90,
    captions={
        'max_r = max_c = 0': '先找出所有工件覆盖的最大行列，只需要建这么大的表',
        'for r1, c1, r2, c2 in artifacts': '读取一个工件的矩形范围',
        'f = [[0]': '`f` 是 `{max_r + 1} × {max_c + 1}` 的全 0 表：1 表示这格已被挖开',
        'f[r][c] = 1': '挖 `({r},{c})`：`f[{r}][{c}] = 1`',
        's = [[0]': '`s[r][c]` 记录左上角到 `(r,c)` 的 ==已挖格数==',
        's[r][c] = f[r][c]': '左上角，没有上方和左方：`s[0][0] = f[0][0]` = {s[r][c]}',
        's[r][c] = s[r][c - 1] + f[r][c]': '第一行：只加左边的前缀和：`s[{r}][{c}] = {s[r][c]}`',
        's[r][c] = s[r - 1][c] + f[r][c]': '第一列：只加上边的前缀和：`s[{r}][{c}] = {s[r][c]}`',
        's[r][c] = s[r - 1][c] + s[r][c - 1]': '上 + 左 − 左上（重复算了一次）+ 自己：`s[{r}][{c}]` = =={s[r][c]}==',
        'res = 0': '`res` 统计可提取的工件数',
        'now_s = s[r2][c2]\n': '',
        'if now_s ==': '已挖 `{now_s}` 格，面积 `{(r2 - r1 + 1) * (c2 - c1 + 1)}`：' + '{"全部裸露 → 可提取" if now_s == (r2 - r1 + 1) * (c2 - c1 + 1) else "还有没挖到的格子 → 不能提取"}',
        'res += 1': '这个工件可以提取：`res` → =={res}==',
        'return res': '一共能提取 `{res}` 个工件',
    },
    cards=dict(
        one_liner='挖过的格子记 1，用前缀和一步算出工件内挖了几格',
        complexity='时间 `O(n² + k)`，空间 `O(n²)`',
        problem=['`n × n` 网格里埋着矩形工件，挖开某些格子后，工件所有格子都露出才能提取',
                 '给出工件的左上、右下坐标和挖掘列表，求能提取几个',
                 '示例：`n=3`，工件 `[0,0,0,0] [0,1,1,1] [2,1,2,2]`，挖 `(0,0) (0,1) (1,1) (2,1)` → `2`'],
        quote='将dig过的位置都置为1，然后计算二维前缀和s。接下来对于每一个工件，就可以利用s来高效地求解这个工件范围内的矩阵和。若这个和恰好等于这个工件覆盖的面积，则说明这个工件可以被提取。',
        quote_src='—— yiduobo 题解原文',
        idea=['挖开的格子标 1，工件内的 1 的个数 == 面积，就是全部裸露',
              '二维前缀和：`s = 上 + 左 − 左上 + 自己`',
              '工件区域的和用四个前缀和加减得到，边界处要分情况处理'],
        summary=['时间 `O(n² + k)`，空间 `O(n²)`（只建到工件覆盖的最大行列）',
                 '易错：第 0 行 / 第 0 列没有 `r-1` 或 `c-1`，要单独分支，否则下标变成 -1',
                 '易错：`dig` 可能超出工件范围，要判断 `r <= max_r and c <= max_c`',
                 '参数 `n` 在代码里其实用不到'],
    ),
)
