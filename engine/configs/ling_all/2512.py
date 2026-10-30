POS = ['smart', 'brilliant', 'studious']
NEG = ['not']
REP = ['this student is studious', 'the student is smart', 'this student is not smart', 'not good']
IDS = [3, 2, 5, 1]


def _a(S):
    a = S.get('a')
    if not a:
        return '`score[w]` 为 3 / -1，不在表里的词默认 0（defaultdict）'
    return '排序键 `(-得分, ID)`：' + '，'.join(f'`({x},{i})`' for x, i in a) + '；得分高在前，同分 ID 小在前'


CONFIG = dict(
    num=2512, title='奖励最顶尖的 K 名学生', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表打分 · 元组排序',
    tags=[],
    code='''
class Solution:
    def topStudents(self, positive_feedback: List[str], negative_feedback: List[str], report: List[str], student_id: List[int], k: int) -> List[int]:
        score = defaultdict(int)
        for w in positive_feedback: score[w] = 3
        for w in negative_feedback: score[w] = -1
        a = sorted((-sum(score[w] for w in r.split()), i) for r, i in zip(report, student_id))
        return [i for _, i in a[:k]]
''',
    call=f'Solution().topStudents({POS!r}, {NEG!r}, {REP!r}, {IDS!r}, 2)',
    expect=[2, 3],
    views=[
        dict(type='text', size=26, h=190,
             fn=lambda S: '评语（ID：内容）\n' if False else '；'.join(f'ID `{i}`：{r}' for r, i in zip(S['report'], S['student_id']))),
        dict(type='map', var='score', label='score（词 → 分数）', fmt=lambda k, v: f"'{k}': {v}", h=190, font=30),
        dict(type='text', fn=_a, size=24, h=170),
    ],
    watch=[('k', 'k', 'blue')],
    captions={
        'score = defaultdict': '`score` 把每个评价词映射到分数；没出现过的词取 0',
        'for w in positive_feedback': '正面词 `{positive_feedback}` 全部记 ==3== 分',
        'for w in negative_feedback': '负面词 `{negative_feedback}` 全部记 ==-1== 分',
        'a = sorted': '每位学生：`r.split()` 拆词、查表求和，取负号放进元组 `(-得分, ID)`，一次 `sorted` 同时满足「分高在前、同分 ID 小在前」→ `a = {a}`',
        'return [i': '取 `a` 前 `{k}` 个的 ID → =={ret}==',
    },
    cards=dict(
        one_liner='把词存进哈希表，得分取负再排序，一步搞定两级规则',
        complexity='时间 `O((p+q+n)L + n log n)`，空间 `O((p+q)L + n)`',
        problem=['正面词 +3 分，负面词 -1 分，按评语算每位学生的得分',
                 '按得分从高到低、同分 ID 小者在前，返回前 `k` 名的 ID',
                 '示例：两人都 3 分 → ID 小的排前 `[1,2]`'],
        quote='把 feedback 及其分数存到哈希表 score 中，对每个 report_i，按照空格分割，然后用 score 计算分数之和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['正负词合并进一张 `score` 表：查词 O(1)，不在表里的是 0 分',
              '元组 `(-得分, ID)` 升序 = 得分降序、ID 升序，不用写 `key`',
              '最后切前 `k` 个，取出 ID'],
        summary=['时间 `O((p+q+n)L + n log n)`，`L` 为平均字符串长度',
                 '易错点：得分要取负才能让「分高的排前」；同分靠元组第二项 ID',
                 '`defaultdict(int)` 让陌生词自动 0 分，不需要判断',
                 '对比 yiduobo：用两个集合分别判断正负，再 `sort(key=...)`'],
    ),
)
