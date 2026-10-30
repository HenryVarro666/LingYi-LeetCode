CONFIG = dict(
    num=3189, title='得到一个和平棋盘的最少步骤', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='行列分开 · 逐行借车', tags=[],
    code='''
class Solution(object):
    def minMoves(self, rooks):

        n = len(rooks)
        row = [0] * n
        col = [0] * n
        for x, y in rooks:
            row[x] += 1
            col[y] += 1
        
        res = 0
        for index in range(n - 1):
            row[index] -= 1
            res += abs(row[index])
            row[index + 1] += row[index]
            
            col[index] -= 1
            res += abs(col[index])
            col[index + 1] += col[index]
        
        return res
''',
    call='Solution().minMoves([[0,0],[0,1],[0,2],[3,3]])',
    expect=3,
    views=[
        dict(type='array', var='row', label='row（每行的车数，处理后 = 要转交给下一行的车数）', h=170,
             pointers={'index': 'blue'}),
        dict(type='array', var='col', label='col（每列的车数）', h=170, pointers={'index': 'blue'}),
        dict(type='text', fn=lambda S: f"累计移动 `res = {S['res']}`" if 'res' in S else '', size=30),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green'), ('row', 'row', 'cyan'), ('col', 'col', 'orange')],
    captions={
        'n = len': '`n x n` 棋盘上有 `n = {n}` 个车',
        'row = [0]': '`row[i]` 统计第 `i` 行的车数',
        'col = [0]': '`col[i]` 统计第 `i` 列的车数',
        'for x, y in rooks': '看车 `({x}, {y})`',
        'row[x] += 1': '第 `{x}` 行多一个车：`row` = {row}',
        'col[y] += 1': '第 `{y}` 列多一个车：`col` = {col}',
        'res = 0': '行和列互不影响，分开算，累计到 `res`',
        'for index in range': lambda S, B, r: '前 n-1 行/列都交接完，循环结束（最后一行/列的余数必为 0）' if S.index == B.index else f'处理第 `{S.index}` 行和第 `{S.index}` 列，和下一行/列交接',
        'row[index] -= 1': '每行只留 1 个车：多出（或欠）`row[{index}]` = =={row[index]}==',
        'res += abs(row[index])': '多出的车要移到下一行，欠的要从下一行借，各算 `|{row[index]}|` 步：`res` → =={res}==',
        'row[index + 1] += row[index]': '余数交给第 `{index+1}` 行：`row[{index+1}]` → =={row[index+1]}==（负数表示借车）',
        'col[index] -= 1': '每列只留 1 个车：多出（或欠）`col[{index}]` = =={col[index]}==',
        'res += abs(col[index])': '列同理，`|{col[index]}|` 步：`res` → =={res}==',
        'col[index + 1] += col[index]': '余数交给第 `{index+1}` 列：`col[{index+1}]` → =={col[index+1]}==',
        'return res': '最少需要 `{res}` 步',
    },
    cards=dict(
        one_liner='行列互不影响：把多余的车一行一行往下传',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n x n` 棋盘上有 `n` 个车 `rooks[i] = [x, y]`，每步可把一个车水平或竖直移动一格',
                 '求使每行每列恰好一个车的最少步数',
                 '本视频：`[[0,0],[0,1],[0,2],[3,3]]` → `3`'],
        quote='行和列之间是不会互相影响的，因此可以将行和列分开考虑。',
        quote_src='—— yiduobo 题解原文',
        idea=['第 0 行有 `x` 个车，留 1 个，其余 `x-1` 个移到第 1 行；为负就从第 1 行借',
              '每传一次花 `|x-1|` 步，余数累加到下一行，列同理',
              '这是下限，而一步一步移动无额外限制，下限一定能达到'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '行、列各算一遍再相加：行移动不改列，列移动不改行',
                 '==负数表示向下一行借车==，所以取 `abs`',
                 '循环只到 `n-2`：最后一行的余数必为 0',
                 '原文为 Python 2 风格，代码无需修改'],
    ),
)
