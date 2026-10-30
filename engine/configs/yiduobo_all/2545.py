CONFIG = dict(
    num=2545, title='根据第 K 场考试的分数排序', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='sorted + lambda 按列排序',
    tags=[],
    code='''
class Solution(object):
    def sortTheStudents(self, score, k):

        return sorted(score, key=lambda d:-d[k])
''',
    call='Solution().sortTheStudents([[10,6,9,1],[7,5,11,2],[4,8,3,15]], 2)',
    expect=[[7, 5, 11, 2], [10, 6, 9, 1], [4, 8, 3, 15]],
    views=[
        dict(type='table', var='score', label='score（原数组不变，sorted 返回新的排好序的列表）', h=300,
             cols=['考试0', '考试1', '考试2', '考试3'],
             color=lambda S, i, j, v: 'yellow' if j == S['k'] else None),
        dict(type='text', fn=lambda S: '排序依据：第 `k` 列取负，数值小的排前面 = 分数高的排前面' if S['_line'] < 5 else '', size=26, h=80),
        dict(type='text', fn=lambda S: 'sorted 的结果：' + str(sorted(S['score'], key=lambda d: -d[S['k']])) if S['_line'] >= 4 else '', size=26, h=80),
    ],
    watch=['k'],
    captions={
        'return sorted': lambda S, B, r: f"`sorted(score, key=lambda d:-d[k])`：每行取第 `{S.k}` 列的负值当关键字，升序即分数从高到低 → `{[x[S.k] for x in r]}`；==不改动 `score`==，返回新列表",
    },
    cards=dict(
        one_liner='一行 sorted：用第 k 列当关键字排序整行',
        complexity='时间 `O(m log m)`，空间 `O(m)`（新列表）',
        problem=['二维数组，每行是一位学生，按第 `k` 列从高到低排行',
                 '示例：`[[3,4],[5,6]]`，`k = 0` → `[[5,6],[3,4]]`',
                 '本视频：`k = 2` 的 3 行 4 列例子'],
        quote='如果使用python的话，直接使用lambda表达式就行了，而对于不具有相关特性的语言，则需要先将第k列单独抽出来，携带着行号一起排序后再将当前的序反向映射回行的下标。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目就是「把第 `k` 列当作关键字，整行排序」',
              'Python 的 `sorted` 可以用 lambda 指定关键字，==一行搞定==',
              '其他语言要抽出第 `k` 列并带上行号排序，再映射回去'],
        after=[dict(heading='关键字怎么排', lines=['每行的第 `2` 列：`9`、`11`、`3`', '取负后：`-9`、`-11`、`-3`，升序是 `-11 < -9 < -3`', '对应行的顺序：第 1 行、第 0 行、第 2 行', '整行跟着关键字移动，行内顺序不变'])],
        summary=['时间 `O(m log m)`，空间 `O(m)`',
                 '`sorted` 返回新列表，不改原数组；灵神用 `score.sort` 原地排序',
                 '关键字取负才是从高到低；也可 `reverse=True`',
                 '原文为 Python 2 风格，本题代码无需改动'],
    ),
)
