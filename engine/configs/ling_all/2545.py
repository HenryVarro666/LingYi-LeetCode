_ORIG = [[10, 6, 9, 1], [7, 5, 11, 2], [4, 8, 3, 15]]


CONFIG = dict(
    num=2545, title='根据第 K 场考试的分数排序', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='自定义排序 · key 取负',
    tags=[],
    code='''
class Solution:
    def sortTheStudents(self, score: List[List[int]], k: int) -> List[List[int]]:
        score.sort(key=lambda row: -row[k])
        return score
''',
    call='Solution().sortTheStudents([[10,6,9,1],[7,5,11,2],[4,8,3,15]], 2)',
    expect=[[7, 5, 11, 2], [10, 6, 9, 1], [4, 8, 3, 15]],
    views=[
        dict(type='text', fn=lambda S: '每行的 key = `-row[k]`：' + '，'.join(f"第{i}行 `{-r[2]}`" for i, r in enumerate(_ORIG)) + '；key 小的排前面', size=28, h=90),
        dict(type='table', var='score', label='score（每行是一位学生，第 k = 2 列是排序依据）', h=420,
             cols=['考试0', '考试1', '考试2', '考试3'],
             color=lambda S, i, j, v: 'yellow' if j == S['k'] else None),
    ],
    watch=['k', ('score', 'score', 'blue')],
    captions={
        'score.sort': '`sort` 用 `key=lambda row: -row[k]` 给每行算 key：第 `{k}` 列的值取负，所以==从小到大排 key 就是从大到小排分数==。原地排序，`score` 变成 `{score}`',
        'return score': '`score` 已被原地排好：第 `{k}` 列依次为 `{[r[k] for r in score]}`，返回它',
    },
    cards=dict(
        one_liner='key 取负：升序排序就变成按第 k 列降序',
        complexity='时间 `O(m log m)`，空间 `O(1)`（忽略排序栈开销）',
        problem=['`score[i][j]` 是第 `i` 位学生第 `j` 场的分数，数值互不相同',
                 '按第 `k` 场分数从高到低对行排序并返回',
                 '示例：`k = 2` → `[[7,5,11,2],[10,6,9,1],[4,8,3,15]]`'],
        quote='自定义排序，按照每一行的下标为 k 的元素从大到小排序。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`list.sort(key=...)` 对每一行算一个 key，再按 key 从小到大排',
              '想要分数从大到小：==key 取负==，`-row[k]`',
              '整行跟着一起移动，所以不用额外映射行号'],
        after=[dict(heading='key 怎么起作用', lines=['每行的第 `2` 列：`9`、`11`、`3`', '取负后：`-9`、`-11`、`-3`，从小到大是 `-11, -9, -3`', '对应行的顺序：第 1 行、第 0 行、第 2 行', '`sort` 原地调整，行内元素不变'])],
        summary=['时间 `O(m log m)`，`m` 是学生数；比较的是 key，与列数无关',
                 '`sort` 是原地修改并返回 `None`，所以单独写 `return score`',
                 '分数互不相同，不用考虑并列时的稳定性',
                 '也可写 `reverse=True`，key 直接用 `row[k]`'],
    ),
)
