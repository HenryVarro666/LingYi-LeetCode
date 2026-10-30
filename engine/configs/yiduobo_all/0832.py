CONFIG = dict(
    num=832, title='翻转图像', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='逐行倒序扫描 · 顺便取反',
    tags=[],
    code='''
class Solution(object):
    def flipAndInvertImage(self, A):

        res = []
        for line in A:
            res.append([])
            for index in range(len(line) - 1, -1, -1):
                res[-1].append(1 - line[index])
        
        return res
''',
    call='Solution().flipAndInvertImage([[1,1,0],[1,0,1],[0,0,0]])',
    expect=[[1, 0, 0], [0, 1, 0], [1, 1, 1]],
    views=[
        dict(type='grid', var='A', label='A（蓝框 = 正在读的格子）', cell=84, h=300,
             cursors=[('A.index(line) if "line" in _inner else None', 'index if "index" in _inner else None', 'blue', '')]),
        dict(type='grid', var=lambda S: S['res'] if 'res' in S else None, label='res（新矩阵，每格 = 1 − 原值）', cell=84, h=300),
    ],
    watch=[('index', 'index', 'blue'), ('line', 'line', 'pink')],
    captions={
        'res = []': '`res` 保存答案矩阵',
        'for line in A': '逐行处理：`line = {line}`',
        'res.append([])': '答案里==新起一行==，后面的值都追加到这一行末尾',
        'for index in range': '从后往前扫描 `line`：`index = {index}`',
        'res[-1].append': '水平翻转：倒着读；取反：`1 − {line[index]}` = `{1 - line[index]}` → 追加到新行',
        'return res': '全部行处理完，返回 `{ret}`',
    },
    cards=dict(
        one_liner='倒着读每一行，读到的值用 1 减掉',
        complexity='时间 `O(n²)`，空间 `O(n²)`（答案矩阵）',
        problem=['给定 0/1 方阵 `A`：先把每行==水平翻转==，再==取反==（0↔1）',
                 '示例：`[[1,1,0],[1,0,1],[0,0,0]]`',
                 '→ `[[1,0,0],[0,1,0],[1,1,1]]`'],
        quote='对于A中的每行，首先在答案矩阵中新起一行，然后从后往前一趟扫描A中的当前行，将1减去当前值加入到答案矩阵中新加入这一行的末尾即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['翻转 = 从后往前读，取反 = `1 − 值`，两步合成一趟扫描',
              '每行先 `res.append([])`，再往 `res[-1]` 追加',
              '不改原矩阵，直接生成新矩阵'],
        summary=['时间 `O(n²)`，空间 `O(n²)`',
                 '易错：先翻转再取反与先取反再翻转结果相同，但别漏掉任何一步',
                 '`1 - x` 是 0/1 取反的简写',
                 '本题题面库中缺失，题意按 LeetCode 832 补写；原文无需改动'],
    ),
)
