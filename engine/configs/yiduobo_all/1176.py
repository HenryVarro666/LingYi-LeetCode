CAL = [1, 3, 2, 6, 4, 1, 5]


def _win(S):
    k = S['k']
    i = S.get('index')
    if i is None:
        return (0, k - 1)
    line = S.get('_line', 0)
    if line <= 12:
        return (i, i + k - 1)
    if line == 13:
        return (i, i + k)
    return (i + 1, i + k)


def _txt(S):
    if 'now' not in S:
        return f"窗口长 `k = {S['k']}`，合法范围 `[{S['lower']}, {S['upper']}]`"
    now = S['now']
    tag = '==高于 upper：+1 分==' if now > S['upper'] else '==低于 lower：−1 分==' if now < S['lower'] else '正常：不加不减'
    return f"窗口和 `now = {now}`（`[{S['lower']}, {S['upper']}]`）：{tag}"


CONFIG = dict(
    num=1176, title='健身计划评估', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='定长滑动窗口',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def dietPlanPerformance(self, calories, k, lower, upper):

        res = 0
        now = sum(calories[:k])

        if now > upper:
            res = 1
        elif now < lower:
            res = -1
        
        for index, c in enumerate(calories[k:]):
            now += c
            now -= calories[index]
            if now > upper:
                res += 1
            elif now < lower:
                res -= 1
        
        return res
''',
    call=f'Solution().dietPlanPerformance({CAL!r}, 3, 7, 10)',
    expect=2,
    views=[
        dict(type='array', var='calories', label='calories', h=230, cell=84,
             window=(lambda S: _win(S)[0], lambda S: _win(S)[1]),
             pointers={'index': 'blue'} ),
        dict(type='text', fn=_txt, size=26, h=70),
    ],
    watch=[('now', 'now', 'cyan'), ('res', 'res', 'green'), 'lower', 'upper'],
    captions={
        'res = 0': '分数 `res` 从 0 开始',
        'now = sum': '先算第一个窗口：前 `{k}` 天卡路里之和 `now = {now}`',
        'if now > upper': lambda S, B, r: f'`now = {S.now}` {">" if S.now > S.upper else "≤"} `upper = {S.upper}` → ' + ('==吃多了，+1 分==' if S.now > S.upper else '没超标，再看低不低'),
        'res = 1': '首个窗口超标 → `res = 1`',
        'elif now < lower': lambda S, B, r: f'`now = {S.now}` {"<" if S.now < S.lower else "≥"} `lower = {S.lower}` → ' + ('==吃少了，−1 分==' if S.now < S.lower else '在范围内，不得分'),
        'res = -1': '首个窗口偏低 → `res = -1`',
        'for index, c in': lambda S, B, r: ('所有天都滑过了，循环结束' if B.get('index') == S.get('index') else f'窗口右移一格：新进来 `c = {S.c}`，要离开的是 `calories[{S.index}]`'),
        'now += c': '新的一天进窗口：`now += {c}` → {now}',
        'now -= calories[index]': '最左一天出窗口：`now -= {calories[index]}` → =={now}==（不用重新求和）',
        'res += 1': '超标：`res` → {res}',
        'res -= 1': '偏低：`res` → {res}',
        'return res': '总分 `{res}`',
    },
    cards=dict(
        one_liner='长度为 k 的窗口右移，进一个、出一个，窗口和 O(1) 更新',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`calories[i]` 是第 i 天的卡路里；每连续 `k` 天算一个窗口和 `T`',
                 '`T < lower` 扣 1 分，`T > upper` 加 1 分，否则 0 分',
                 '本视频：`[1,3,2,6,4,1,5]`，`k=3, lower=7, upper=10` → `2`'],
        quote='非常标准的滑动窗口问题。使用一个长度为k的窗口向后滑动，每一轮滑动都先计算出新的窗口内的卡路里之和，然后与upper和lower的大小关系更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用 `sum(calories[:k])` 算出第一个窗口并打分',
              '之后每一轮：加上新进来的 `c`，减去离开的 `calories[index]`',
              '`calories[k:]` 的第 `index` 个元素进来时，离开的正好是 `calories[index]`'],
        summary=['时间 `O(n)`，空间 `O(1)`（切片会额外复制，思路上不影响）',
                 '第一个窗口要单独处理，循环从第 `k` 个元素开始',
                 '超标 +1、偏低 −1，==相等边界不算==（`>` / `<`）',
                 '同类题：643 子数组最大平均数 I'],
    ),
)
