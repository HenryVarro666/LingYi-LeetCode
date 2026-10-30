POS = ['smart', 'brilliant', 'studious']
NEG = ['not']
REP = ['this student is studious', 'the student is smart', 'this student is not smart', 'not good']
IDS = [3, 2, 5, 1]


def _words(S):
    r = S.get('r')
    return r.split(' ') if r else []


CONFIG = dict(
    num=2512, title='奖励最顶尖的 K 名学生', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='模拟 · 正负词集合 + 排序',
    tags=[],
    code='''
class Solution(object):
    def topStudents(self, positive_feedback, negative_feedback, report, student_id, k):

        pos_set = set(positive_feedback)
        neg_set = set(negative_feedback)

        score_list = []
        for r, id in zip(report, student_id):
            score = 0
            for word in r.split(' '):
                if word in pos_set:
                    score += 3
                elif word in neg_set:
                    score -= 1
            score_list.append([score, id])

        score_list.sort(key=lambda d:(-d[0], d[1]))
        return [info[1] for info in score_list[:k]]
''',
    call=f'Solution().topStudents({POS!r}, {NEG!r}, {REP!r}, {IDS!r}, 2)',
    expect=[2, 3],
    views=[
        dict(type='set', var='pos_set', label='pos_set（正面词）', fmt=lambda x: str(x), h=100, font=26),
        dict(type='set', var='neg_set', label='neg_set（负面词）', fmt=lambda x: str(x), h=100, font=28),
        dict(type='array', var=_words, label='当前评语拆出的单词（绿 = 正面，橙 = 负面）', cell=140, h=200, font=24,
             color=lambda S, i, v: ('green' if v in S.get('pos_set', ()) else 'orange' if v in S.get('neg_set', ()) else None)),
        dict(type='array', var='score_list', label='score_list（[得分, ID]）', cell=130, h=180, font=26),
    ],
    watch=[('id', 'id', 'blue'), ('score', 'score', 'green'), ('word', 'word', 'pink')],
    captions={
        'pos_set = set': '正面词放进集合 `pos_set`，判断一个词是否在里面是 O(1)',
        'neg_set = set': '负面词放进集合 `neg_set`',
        'score_list = []': '`score_list` 存每名学生的 `[得分, ID]`',
        'for r, id in zip': lambda S, B, r: ('所有学生都算完，循环结束' if B.get('id') == S.id and B.get('r') == S.r else f'轮到 ID `{S.id}` 的评语：`{S.r}`'),
        'score = 0': '这名学生的得分从 0 开始',
        'for word in r.split': lambda S, B, r: ('这条评语的词都看完了' if B.get('word') == S.word and B.get('r') == S.r else f'看单词 `{S.word}`'),
        'if word in pos_set': lambda S, B, r: (f'`{S.word}` 在正面集合里 → ==+3==' if S.word in S.pos_set else f'`{S.word}` 不在正面集合，再看负面'),
        'score += 3': '正面词，`score` → =={score}==',
        'elif word in neg_set': lambda S, B, r: (f'`{S.word}` 在负面集合里 → ==-1==' if S.word in S.neg_set else f'`{S.word}` 两个集合都没有 → 不加不减'),
        'score -= 1': '负面词，`score` → =={score}==',
        'score_list.append': '这名学生算完：`[{score}, {id}]` 加入列表',
        'score_list.sort': '按 `(-得分, ID)` 排序：==得分降序，同分 ID 升序== → `{score_list}`',
        'return [info': '取前 `{k}` 个的 ID → =={ret}==',
    },
    cards=dict(
        one_liner='按题目描述一步步算分，最后按两级规则排序取前 k',
        complexity='时间 `O((p+q+n)L + n log n)`，空间 `O((p+q)L + n)`',
        problem=['正面词 +3 分，负面词 -1 分，按评语算每位学生的得分',
                 '得分高者在前，同分 ID 小者在前，返回前 `k` 名的 ID',
                 '示例：`[1,2]` 同为 3 分 → ID 小的 1 在前'],
        quote='很常规的模拟题，题目的数据规模也不大，直接按照题目描述按部就班地计算就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['正、负词分别放进两个集合，逐个单词判断属于哪边',
              '每个学生算出 `[得分, ID]`，装进 `score_list`',
              '`sort(key=lambda d: (-d[0], d[1]))`：得分为第一优先级倒序，ID 为第二优先级顺序'],
        summary=['时间 `O((p+q+n)L + n log n)`',
                 '易错点：用 `if / elif`，一个词至多算一次；两个集合不会有交集',
                 '作者提到 top k 还可用大小为 k 的堆或快速选择优化，这里偷懒直接排序',
                 '对比灵神：灵神用一张哈希表存分数，把 `-得分` 放进元组直接 sorted'],
    ),
)
