CONFIG = dict(
    num='LCS 02', title='完成一半题目', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='按出现次数从大到小贪心',
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
    call='Solution().halfQuestions([1,5,1,3,4,5,2,5,3,3,8,6])',
    expect=2,
    views=[
        dict(type='array', var='questions', label='questions（知识点类型）', h=170, cell=64),
        dict(type='map', var='cnt_dict', h=260, font=26, fmt=lambda k, v: f'类型 {k}：{v} 题'),
        dict(type='text', fn=lambda S: (f"按题数从大到小：{sorted(S['cnt_dict'].values(), reverse=True)}，目标 `n` = =={S['n']}==" if 'n' in S and 'now' in S else ''), size=26),
    ],
    watch=['n', 'q', 'cnt', ('now', 'now', 'blue'), ('res', 'res', 'green')],
    captions={
        'n = len': '每人选一题、共 `{n}` 位 → 需要选出 `{n}` 道题，`n = {n}`（整数除法）',
        'for q in questions': '看下一道题，类型 `q = {q}`',
        'cnt_dict[q] =': '类型 `{q}` 的题数变为 `{cnt_dict[q]}`',
        'now = 0': '`now`：目前已选的题数',
        'res = 0': '`res`：目前用了几种知识点类型',
        'for cnt in sorted': '取题数最多的未选类型：这一类有 `{cnt}` 道',
        'now += cnt': '全选这一类：`now` = =={now}==',
        'res += 1': '又多用一种类型：`res` = =={res}==',
        'if now >= n': '`now = {now}` {">=" if now >= n else "<"} `n = {n}` → {"够 n 道了，停止" if now >= n else "还不够，继续选下一多的类型"}',
        'return res': '至少需要 =={res}== 种知识点类型',
    },
    cards=dict(
        one_liner='优先选题数最多的类型，用最少的类型凑够一半题',
        complexity='时间 `O(n + k log k)`，空间 `O(k)`（k 为类型数）',
        problem=['`2N` 道题，每道有知识点类型；每位扣友选不同的一题，共选 `N` 道',
                 '求被选的 `N` 道题至少涉及多少种知识点类型',
                 '示例：`[1,5,1,3,4,5,2,5,3,3,8,6]` → `2`（选类型 3 和 5）'],
        quote='为了最终选择的知识点最少，那么就应该优先选择对应题目数量最多的知识点。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用字典统计每种类型的题数',
              '题数从大到小排序，一趟累加，找最小的 `k` 使前 `k` 种题数之和 `>= N`',
              '这个 `k` 就是答案'],
        summary=['时间 `O(n + k log k)`，空间 `O(k)`',
                 '判断条件是 `now >= n`，等于也够，不要写成 `>`',
                 '原文为 Python 2 写法，`len(questions) / 2` 已改为 `//`（整数除法）'],
    ),
)
