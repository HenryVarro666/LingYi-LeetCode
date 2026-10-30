CONFIG = dict(
    num=750, title='角矩阵的数量', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='逐行枚举 + 列对哈希表',
    code='''
class Solution(object):
    def countCornerRectangles(self, grid):

        m = len(grid)
        n = len(grid[0])

        cnt = {}
        res = 0
        for i in range(m):
            pos = []
            for j in range(n):
                if grid[i][j] == 1:
                    for p in pos:
                        key = p * n + j
                        res += cnt.get(key, 0)
                        cnt[key] = cnt.get(key, 0) + 1
                        
                    pos.append(j)
        
        return res
''',
    call='Solution().countCornerRectangles([[1,1,0],[1,1,1],[0,1,1]])',
    expect=2,
    max_steps=110,
    skip=['for j in range(n)'],
    views=[
        dict(type='grid', var='grid', label='grid（黄框 = 当前格，绿 = pos 中的 1）', cell=96, h=330,
             cursors=[('i', 'j', 'yellow', '(i,j)')],
             color=lambda S, i, j, v: 'green' if v == 1 and i == S.get('i') and j in S.get('pos', []) else None),
        dict(type='map', var='cnt', label='cnt（键 = 列对 p*n+j，即 p-j；值 = 之前有多少行含这一对）', fmt=lambda k, v: f"{k // 3}-{k % 3}: {v}", h=130, font=28),
        dict(type='text', h=60, size=30,
             fn=lambda S: f"本行已有的 1 所在列 `pos = {S['pos']}`，累计矩形 `res` = =={S['res']}==" if 'pos' in S else ''),
    ],
    watch=['i', 'j', 'pos', 'key', ('res', 'res', 'green')],
    captions={
        'cnt = {}': '`cnt`：记录「列对 (p, j)」在之前的行里一共出现了几次',
        'res = 0': '`res` 累计角矩阵数量',
        'for i in range(m)': '处理第 `{i}` 行',
        'pos = []': '`pos` 存本行已经遇到的值为 1 的列',
        'for j in range(n)': '看第 `{j}` 列',
        'if grid[i][j] == 1': '`grid[{i}][{j}] = {grid[i][j]}` {"是 1，可以和本行前面的 1 组成列对" if grid[i][j] == 1 else "是 0，跳过"}',
        'for p in pos': '`pos = {pos}`：{"取出 pos 里的下一个列，和第 " + str(j) + " 列配对；取完就结束循环" if pos else "本行前面还没有 1，没有列对可配"}',
        'key = p * n + j': '列对 `({p}, {j})` 编码成 `{key}`（`p * n + j`，不会重复）',
        'res += cnt.get': '这对列在上面 `{cnt.get(key, 0)}` 行里都是 1，每行都能和本行组成一个矩形 → `res` = =={res}==',
        'cnt[key] =': '本行也含这对列，次数 +1：`cnt[{key}] = {cnt[key]}`，留给下面的行用',
        'pos.append(j)': '把第 `{j}` 列记入 `pos`，后面的列要和它配对',
        'return res': '一共 `{res}` 个角矩阵',
    },
    cards=dict(
        one_liner='逐行找 1 的列对，用哈希表数这对列之前出现过几次',
        complexity='时间 `O(m·n²)`，空间 `O(n²)`',
        problem=['`grid` 只含 0 和 1',
                 '角矩阵：四个不同位置 `(x1,y1)(x1,y2)(x2,y1)(x2,y2)` 的值都为 1',
                 '统计角矩阵的个数',
                 '示例：`[[1,1,0],[1,1,1],[0,1,1]]` → `2`'],
        quote='可以使用一个哈希表储存每一行中值都为1的列的组合，那么对于后续的行，就只需要先找出行中值为1的列，然后两两枚举这些列并到哈希表中查找形成的角矩阵数量，最后更新哈希表即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举两行里同时为 1 的两列，就是一个矩形',
              '按行往下扫：本行每个列对 `(p, j)`，之前出现过 `c` 次就新增 `c` 个矩形',
              '哈希表把列对编码成 `p * n + j`，处理完一对再让次数加一'],
        summary=['时间 `O(m·n²)`，空间 `O(n²)`',
                 '易错点：先 `res += cnt.get(key, 0)`，再更新 `cnt`，否则会把本行自己算进去',
                 '列对编码 `p * n + j` 中 `p < j`，保证同一对只有一个键',
                 '原文为 Python 2 风格，在 Python 3 下无需修改即可运行'],
    ),
)
