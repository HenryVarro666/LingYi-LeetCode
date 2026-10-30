A = [21, 18, 18, 18, 31]
B_ = [34, 32, 16, 16, 17]


def _flag(a, b):
    return 1 if a > b else 0 if a == b else -1


def _rowA(S):
    return list(S['temperatureA'])


def _text(S):
    if 'index' not in S:
        return '先给每天算趋势：当天比前一天高 1，相等 0，低 -1'
    i = S['index']
    fa = _flag(S['temperatureA'][i], S['temperatureA'][i - 1])
    fb = _flag(S['temperatureB'][i], S['temperatureB'][i - 1])
    return (f"第 `{i}` 天：A `{S['temperatureA'][i - 1]}→{S['temperatureA'][i]}` = `{fa}`；"
            f"B `{S['temperatureB'][i - 1]}→{S['temperatureB'][i]}` = `{fb}`　→ " + ('==相同==' if fa == fb else '==不同=='))


def _col(S, i, v):
    if 'index' not in S:
        return None
    idx = S['index']
    if i == idx:
        return 'yellow'
    if i == idx - 1:
        return 'blue'
    return None


CONFIG = dict(
    num='LCP 61', title='气温变化趋势', difficulty='Easy', category='模拟',
    author='yiduobo', technique='逐天比较 · cnt 计连续',
    tags=[],
    code='''
class Solution(object):
    def temperatureTrend(self, temperatureA, temperatureB):

        n = len(temperatureA)
        res = 0
        cnt = 0
        for index in range(1, n):
            if temperatureA[index] > temperatureA[index - 1]:
                flagA = 1
            elif temperatureA[index] == temperatureA[index - 1]:
                flagA = 0
            else:
                flagA = -1
            
            if temperatureB[index] > temperatureB[index - 1]:
                flagB = 1
            elif temperatureB[index] == temperatureB[index - 1]:
                flagB = 0
            else:
                flagB = -1
            
            if flagA == flagB:
                cnt += 1
            else:
                res = max(res, cnt)
                cnt = 0
        
        return max(res, cnt)
''',
    call=f'Solution().temperatureTrend({A!r}, {B_!r})',
    expect=2,
    views=[
        dict(type='array', var='temperatureA', label='temperatureA', pointers={'index': 'yellow'}, h=200, color=_col),
        dict(type='array', var='temperatureB', label='temperatureB', pointers={'index': 'yellow'}, h=200, color=_col),
        dict(type='text', fn=_text, size=28, h=130),
    ],
    watch=[('index', 'index', 'yellow'), 'flagA', 'flagB', ('cnt', 'cnt', 'cyan'), ('res', 'res', 'green')],
    captions={
        'n = len': '`n = {n}` 天，趋势要比相邻两天，所以从下标 1 开始',
        'res = 0': '`res` 记已结束的各段里最长的',
        6: '`cnt` 记当前这一段趋势相同的天数',
        'for index': lambda S, B, r: ('遍历完成。注意最后一段还没和 `res` 比较' if 'index' in B and S.index == B.index
                                      else f'看第 `{S.index}` 天与前一天'),
        'if temperatureA[index] >': 'A：`{temperatureA[index]}` 对比 `{temperatureA[index-1]}`',
        'elif temperatureA': 'A：`{temperatureA[index]}` 对比 `{temperatureA[index-1]}`',
        'flagA = 1': 'A 上升，`flagA = 1`',
        'flagA = 0': 'A 平稳，`flagA = 0`',
        'flagA = -1': 'A 下降，`flagA = -1`',
        'if temperatureB[index] >': 'B：`{temperatureB[index]}` 对比 `{temperatureB[index-1]}`',
        'elif temperatureB': 'B：`{temperatureB[index]}` 对比 `{temperatureB[index-1]}`',
        'flagB = 1': 'B 上升，`flagB = 1`',
        'flagB = 0': 'B 平稳，`flagB = 0`',
        'flagB = -1': 'B 下降，`flagB = -1`',
        'if flagA == flagB': '`flagA = {flagA}`，`flagB = {flagB}` → ' + '{"==相同，连续段延长==" if flagA == flagB else "==不同，这一段结束=="}',
        'cnt += 1': '趋势相同，`cnt` → =={cnt}==',
        'res = max': '用这一段更新答案：`res = max({B.res}, {B.cnt})` = =={res}==',
        26: '`cnt` 重置为 0，从下一天重新数',
        'return max': '遍历完还要用最后一段的 `cnt` 再更新一次：`max({res}, {cnt})` = =={max(res, cnt)}==',
    },
    cards=dict(
        one_liner='逐天算两地趋势，相同就累加，不同就结算并清零',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['两地气温 `temperatureA`、`temperatureB`，相邻两天趋势：升 / 平 / 降',
                 '求两地趋势相同的最大连续天数',
                 '本视频：`A=[21,18,18,18,31]`，`B=[34,32,16,16,17]` → `2`'],
        quote='若趋势相同，则将cnt加上1，否则使用cnt来更新答案，然后将cnt重置为0。另外，在遍历完成后，需要使用当前的cnt再更新一次答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['从下标 1 起，用 `flagA` / `flagB` 记当天趋势（1 / 0 / -1）',
              '相同：`cnt += 1`；不同：先 `res = max(res, cnt)` 再清零',
              '最后一段后面没有“不同”来结算，要在返回时补比一次'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：循环结束后必须 `max(res, cnt)`，否则结尾处的最长段会漏掉',
                 '本例结尾恰好是最长段（天 3、4），这一步最关键',
                 '原文可直接在 Python 3 运行，未做修改',
                 '对比灵神：灵神每步直接更新 `ans`，无需最后补比'],
    ),
)
