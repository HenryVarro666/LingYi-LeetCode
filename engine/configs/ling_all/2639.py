G = [[-15, 1, 3], [15, 7, 12], [5, 6, -2]]


def _cell(S, i, j, v):
    if 'ans' not in S:
        return None
    if j == len(S['ans']):
        return 'blue'
    return None


def _txt(S):
    if 'col' not in S:
        return ''
    col = S['col']
    j = len(S['ans'])
    return f"第 {j} 列：`max = {max(col)}`，`min = {min(col)}`，`max(max//10, -min)` = =={max(max(col) // 10, -min(col))}=="


CONFIG = dict(
    num=2639, title='查询网格图中每一列的宽度', difficulty='Easy', category='网格图',
    author='灵茶山艾府', technique='只算列最值的位数',
    tags=[],
    code='''
class Solution:
    def findColumnWidth(self, grid: List[List[int]]) -> List[int]:
        ans = []
        for col in zip(*grid):
            x_len = 1
            x = max(max(col) // 10, -min(col))
            while x:
                x_len += 1
                x //= 10
            ans.append(x_len)
        return ans
''',
    call=f'Solution().findColumnWidth({G})',
    expect=[3, 1, 2],
    views=[
        dict(type='text', fn=_txt, size=30, h=70),
        dict(type='grid', var='grid', color=_cell, h=300),
        dict(type='array', var='ans', label='ans（每列宽度）', h=200),
    ],
    watch=['x_len', 'x', ('ans', 'ans', 'green')],
    captions={
        'for col in zip': lambda S, B, r: f'`zip(*grid)` 把矩阵转置，一次取出一整列：`col = {S.col}`' if len(S.ans) == len(B.get('ans', [])) and len(S.ans) < 3 else '三列都处理完了，退出循环',
        'x_len = 1': '先给 `x_len = 1`：最大位数的数至少有一位',
        'x = max(': '长度只由列最大值或列最小值决定：`max({max(col)}//10, -({min(col)}))` = =={x}==（负号折成多一位）',
        'while x': lambda S, B, r: f'`x = {S.x}` ≠ 0，还没数完位数' if S.x else '`x = 0`，位数数完了',
        'x_len += 1': '多一位：`x_len` = =={x_len}==',
        'x //= 10': '去掉最低位：`x` → {x}',
        'ans.append': '这一列的宽度是 =={x_len}==，加入 `ans`',
        'return ans': '每列宽度：`{ans}`',
    },
    cards=dict(
        one_liner='数字越大越长，一列只需看最大值和最小值',
        complexity='时间 `O(n(m+logU))`，空间 `O(1)`',
        problem=['矩阵一列的宽度 = 这一列数字转成字符串的最大长度（负号算一位）',
                 '返回每一列的宽度',
                 '示例：`[[-15,1,3],[15,7,12],[5,6,-2]]` → `[3,1,2]`'],
        quote='数字的绝对值越大，数字的长度就越长，所以只需要对每一列的最小值或最大值求长度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['负数的负号算一位：取 `max(mx//10, -mn)` 的位数再加一',
              '这样一整列全负、全正也都成立',
              '`0` 的位数当作 0，所以 `x_len` 从 1 开始'],
        summary=['时间 `O(n(m+logU))`，空间 `O(1)`（`zip(*grid)` 不计）',
                 '易错：负数多一位；`0` 的长度是 1，不是 0',
                 '这里用的是方法二的手写位数版本；一行版写法 `len(str(max(max(col), -10*min(col))))`',
                 '方法一则是对每个数都算长度，更慢'],
    ),
)
