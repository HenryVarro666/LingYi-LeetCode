CONFIG = dict(
    num=1854, title='人口最多的年份', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='差分字典 + 逐年累加',
    tags=['灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def maximumPopulation(self, logs):

        delta = {}
        for birth, death in logs:
            delta[birth] = delta.get(birth, 0) + 1
            delta[death] = delta.get(death, 0) - 1
        
        ma = 0
        res = None
        now = 0
        for y in range(1950, 2051):
            now += delta.get(y, 0)
            if now > ma:
                ma = now
                res = y
        
        return res
''',
    call='Solution().maximumPopulation([[1951,1957],[1953,1955],[1954,1960]])',
    expect=1954,
    views=[
        dict(type='text', fn=lambda S: (f"第 `{S['y']}` 年：当年变化 `{S['delta'].get(S['y'], 0)}`，在世人数 `now` = =={S['now']}==，最高 `ma` = {S['ma']}" if 'y' in S and 'now' in S else '先把每个人的出生/去世记成 +1 / −1')),
        dict(type='map', var='delta', fmt=lambda k, v: f'{k}: {v:+d}', h=300, label='delta（年份 → 人口变化）'),
        dict(type='text', fn=lambda S: (f"答案 `res` = =={S['res']}==" if S.get('res') else '')),
    ],
    watch=['y', ('now', 'now', 'blue'), ('ma', 'ma', 'orange'), ('res', 'res', 'green')],
    captions={
        'delta[birth] =': '`{birth}` 年出生：这一年起人口 +1 → `delta[{birth}] = {delta[birth]}`',
        'delta[death] =': '`{death}` 年去世：这一年起人口 −1（去世那年不算在世）→ `delta[{death}] = {delta[death]}`',
        'now += delta.get': '`now += delta.get({y}, 0)`：上一年人口加上今年的变化 → ==`{now}`==',
        'if now > ma': lambda S, B, r: f'`{S.now} > {S.ma}`？' + ('成立：今年人口创新高' if S.now > S.ma else '不成立：没超过最高，答案不动（并列取更早的年份）'),
        'ma = now': '更新最高人口 `ma = {ma}`',
        'res = y': '记下年份 `res = {res}`：`>` 严格大于，并列时保留最早的年份',
        'return res': '遍历完 1950–2050，最早的最高人口年份 = `{res}`',
    },
    skip=['for y in range'],
    max_steps=44,
    cards=dict(
        one_liner='dict 只记变化，逐年累加就得到每年的人口',
        complexity='时间 `O(n + 101)`，空间 `O(n)`',
        problem=['`logs[i] = [birth, death]`：第 `i` 个人出生于 `birth`、去世于 `death`',
                 '人在 `[birth, death)` 这些年算在世，去世那年不算',
                 '求在世人数最多的年份，并列取最早；示例 `[[1951,1957],[1953,1955],[1954,1960]]` → `1954`'],
        quote='使用一个dict记录每年人口变化的情况，然后从1950年开始到2050年一趟遍历，通过dict中记录的这一年的人口变化，配合上一年的总人口计算出本年度的总人口，并更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['出生年 `+1`、去世年 `−1`，只记「变化」不记总数',
              '从 1950 扫到 2050，`now` 累加就是当年在世人数',
              '用 `now > ma` 严格大于更新，天然取到最早的年份'],
        summary=['时间 `O(n)` 建 dict，再固定扫 101 年；空间 `O(n)`',
                 '去世年是 `−1`，因为去世那年不算在世',
                 '更新答案要用 `>` 而不是 `>=`，否则并列时会取到更晚的年份',
                 '原文已是 Python 3 可运行的写法，未做改动'],
    ),
)
