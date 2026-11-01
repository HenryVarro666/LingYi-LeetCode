CONFIG = dict(
    num='LCS 02', title='完成一半题目', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='统计后降序累加，找最小 k',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def halfQuestions(self, questions):

        n = len(questions) // 2

        cnt_dict = {}
        for q in questions:
            cnt_dict[q] = cnt_dict.get(q, 0) + 1
        
        now = 0
        res = 0
        for cnt in sorted(cnt_dict.values(), reverse=True):
            now += cnt
            res += 1
            if now >= n:
                break
        
        return res
''',
    call='Solution().halfQuestions([4,4,4,7,7,9,1,2,2,2])',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: (f"累计已选 ==`{S['now']}`== 道题，目标 `{S['n']}`，用了 `{S['res']}` 种知识点" if 'now' in S
                                        else '先统计每种知识点的题数')),
        dict(type='array', var='questions', label='questions', h=140),
        dict(type='map', var='cnt_dict', label='cnt_dict（知识点 → 题数）', h=190),
        dict(type='array', var=lambda S: sorted(S['cnt_dict'].values(), reverse=True) if 'now' in S else [],
             label='题数从大到小', h=170, pointers={'res': 'pink'},
             color=lambda S, i, v: 'green' if i < S.get('res', 0) else None),
    ],
    watch=['n', ('now', 'now', 'yellow'), ('res', 'res', 'green')],
    captions={
        'n = len': '要选 `N = {len(questions)} // 2 = {n}` 道题',
        'for q in questions': '看下一道题，知识点类型 `{q}`',
        'cnt_dict[q] = ': '类型 `{q}` 的题数：`cnt_dict[{q}] = {cnt_dict[q]}`',
        'now = 0': '`now` 累计已选题数',
        'res = 0': '`res` 累计知识点种数',
        'for cnt in sorted': '从题数最多的开始，这一种有 `{cnt}` 道',
        'now += cnt': '选上这个知识点的全部题目：`now` → =={now}==',
        'res += 1': '多用了一种知识点：`res` → {res}',
        'if now >= n': '`now = {now}` vs `n = {n}`：' + '{"已经够了 → 停，res 就是最小的 k" if now >= n else "还不够，继续取下一种"}',
        'break': '前 `{res}` 种已经覆盖 `{now}` 道 ≥ `{n}`，不用再选',
        'return res': '最少 `{res}` 种知识点',
    },
    cards=dict(
        one_liner='找最小的 k：前 k 种知识点的题数和 ≥ N',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`2N` 道题，`questions[i]` 是知识点类型',
                 '每人选不同的一题，共选 `N` 题，求最少涉及几种知识点',
                 '本视频：`[4,4,4,7,7,9,1,2,2,2]` → `2`（要选 5 题）'],
        quote='为了最终选择的知识点最少，那么就应该优先选择对应题目数量最多的知识点。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用字典统计每种知识点的题数',
              '题数从大到小排序，一趟累加',
              '第一次累计 ≥ N 时的种数 k 就是答案'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，`n = len(questions) / 2` 已改为 `//`',
                 '易错点：判断是 `now >= n`（可以刚好等于）',
                 '同类：优先选「一次性覆盖最多」的'],
    ),
)
