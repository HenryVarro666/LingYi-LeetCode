def _f(S):
    return S.get('f')


def _s(S):
    return S.get('s')


CONFIG = dict(
    num=2201, title='统计可以提取的工件', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='二维前缀和',
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
    call='Solution().digArtifacts(3, [[0,0,0,0],[0,1,1,1],[1,2,2,2]], [[0,0],[0,1],[1,1],[1,2]])',
    expect=2,
    views=[
        dict(type='grid', var='f', label='f（1 = 挖过；黄框 = 当前格）', cell=90, h=300,
             color=lambda S, i, j, v: 'green' if v else None, cursors=[('r', 'c', 'yellow')]),
        dict(type='grid', var='s', label='s（二维前缀和）', cell=90, h=300,
             color=lambda S, i, j, v: 'blue' if (S.get('_line') and i == S.get('r') and j == S.get('c')) else None),
        dict(type='text', h=70, size=28, fn=lambda S: (f"工件 ({S['r1']},{S['c1']})-({S['r2']},{S['c2']})：面积 {(S['r2']-S['r1']+1)*(S['c2']-S['c1']+1)}，挖到 {S['now_s']}" if 'now_s' in S and 'r1' in S else '')),
    ],
    watch=[('r', 'r', 'blue'), ('c', 'c', 'pink'), ('now_s', 'now_s', 'orange'), ('res', 'res', 'green')],
    captions={
        'max_r = max(max_r, r2)': '所有工件到过的最大行 `max_r` = {max_r}',
        'max_c = max(max_c, c2)': '最大列 `max_c` = {max_c}，只需要处理这么大的网格',
        'f = [[0]': '先建全 0 的网格 `f`：{max_r+1} 行 {max_c+1} 列',
        'f[r][c] = 1': '挖过的 `({r},{c})` 置 1',
        's = [[0]': '`s[r][c]` 表示左上角到 (r,c) 这个矩形里挖过的格数',
        'if r == 0': '看是不是第 0 行：第 0 行没有上一行可加',
        'if c == 0': '看是不是第 0 列',
        's[r][c] = s[r][c - 1] + f[r][c]': '第 0 行：只加左边 → `s[{r}][{c}]` = =={s[r][c]}==',
        's[r][c] = s[r - 1][c] + f[r][c]': '第 0 列：只加上边 → `s[{r}][{c}]` = =={s[r][c]}==',
        's[r][c] = s[r - 1][c] + s[r][c - 1] - s[r - 1][c - 1]': '上 + 左 − 左上（重叠加了两次）+ 自己 → `s[{r}][{c}]` = =={s[r][c]}==',
        's[r][c] = f[r][c]': '左上角 → `s[0][0]` = {s[r][c]}',
        30: '检查工件 `({r1},{c1})-({r2},{c2})`',
        'now_s = s[': '用前缀和求这个矩形内挖到的格数 `now_s` = =={now_s}==',
        'if now_s ==': lambda S, B, r: (f"面积 {(S['r2']-S['r1']+1)*(S['c2']-S['c1']+1)}，挖到 {S['now_s']}："
                                        + ('相等 → 整个工件露出来了' if S['now_s'] == (S['r2']-S['r1']+1)*(S['c2']-S['c1']+1) else '不相等 → 还有格子没挖到')),
        'res += 1': '这个工件可以提取，`res` = =={res}==',
        'return res': '一共 `{res}` 个工件可以提取',
    },
    cards=dict(
        one_liner='把挖过的格子记成 1，用前缀和数工件里挖到几格',
        complexity='时间 `O(n²+m)`，空间 `O(n²)`',
        problem=['网格里埋着矩形工件，挖开 `dig` 的格子', '工件所有格子都被挖到才能提取，求可提取的数量',
                 '示例：3 个工件，挖 4 格 → `2`'],
        quote='若这个和恰好等于这个工件覆盖的面积，则说明这个工件可以被提取。',
        quote_src='—— yiduobo 题解原文',
        idea=['挖过的位置置 1，其余为 0，算二维前缀和 `s`', '工件矩形内的和 = 四个前缀和做容斥', '和等于面积，说明每格都挖过'],
        summary=['时间 `O(n²+m)`，空间 `O(n²)`（代码只开到工件用到的最大行列）',
                 '容斥时要分 r1==0、c1==0 的边界情况，防止下标 −1',
                 '工件最多 4 格，所以直接查哈希表也行（灵神写法）'],
    ),
)
