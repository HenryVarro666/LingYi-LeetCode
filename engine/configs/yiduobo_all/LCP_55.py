def _fmt_t(S):
    if 'num' not in S or 't' not in S:
        return '每种果实：轮数 = `(数量 − 1) // limit + 1`（向上取整），再乘单轮时间'
    return (f"果实 `{S['type']}`：数量 `{S['num']}`，每轮最多 `{S['limit']}` → 轮数 `({S['num']}−1)//{S['limit']}+1` = =={S['t']}==；"
            f"耗时 `{S['time'][S['type']]}×{S['t']}` = =={S['time'][S['type']] * S['t']}==")


CONFIG = dict(
    num='LCP 55', title='采集果实', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历 · 向上取整',
    tags=[],
    code='''
class Solution(object):
    def getMinimumTime(self, time, fruits, limit):

        res = 0
        for type, num in fruits:
            t = (num - 1) // limit + 1
            res += time[type] * t
        
        return res
''',
    call='Solution().getMinimumTime([2,3,2], [[0,2],[1,4],[2,3]], 3)',
    expect=10,
    views=[
        dict(type='array', var='time', label='time（采集一轮所需时间，按果实种类）', pointers={'type': 'blue'},
             color=lambda S, i, v: 'blue' if 'type' in S and i == S['type'] else None, h=200),
        dict(type='array', var=lambda S: [f'{a}:{b}' for a, b in S['fruits']], label='fruits（种类:数量）', h=200,
             color=lambda S, i, v: 'yellow' if 'type' in S and S['fruits'][i][0] == S['type'] and S['fruits'][i][1] == S.get('num') else None),
        dict(type='text', fn=_fmt_t, size=30, h=150),
    ],
    watch=[('type', 'type', 'blue'), ('num', 'num', 'yellow'), ('t', 't', 'cyan'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计总耗时，从 0 开始',
        'for type, num': lambda S, B, r: ('每种果实都处理完，循环结束' if 'type' in B and B.type == S.type and B.num == S.num
                                      else f'取出一种果实：种类 `{S.type}`，需要采 `{S.num}` 个'),
        't = (num - 1)': '每轮最多采 `{limit}` 个，`{num}` 个要采 `({num}−1)//{limit}+1` = =={t}== 轮（向上取整）',
        'res += time': '每轮 `{time[type]}`，共 `{t}` 轮：`res` += `{time[type]}×{t}` → =={res}==',
        'return res': '所有果实都采完，总时间 `{res}`',
    },
    cards=dict(
        one_liner='每种果实：轮数向上取整，乘单轮时间，累加',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`time[i]` 是采集一轮第 `i` 种果实的时间，一轮最多采 `limit` 个',
                 '`fruits[j] = [种类, 数量]`，求把所有果实采完的最短总时间',
                 '本视频：`time=[2,3,2]`，`limit=3` → `10`'],
        quote='一趟遍历，计算采集每种果实所需的轮次，然后乘以单轮的时间，累加之后就是最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['采 `num` 个、每轮最多 `limit` 个 → 需要 ==向上取整== 的轮数',
              '整数向上取整：`(num - 1) // limit + 1`',
              '各种果实互不影响，把耗时直接相加'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：向上取整别写成 `num // limit`；`num` 刚好整除时 `(num-1)//limit+1` 也正确',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '变量名 `type` 会遮住内置函数，但这里只作循环变量，不影响'],
    ),
)
