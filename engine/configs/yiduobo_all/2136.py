SORT = 'sorted(zip(plantTime, growTime), key=lambda d:d[1], reverse=True)'


def _cur(S):
    if 'p' in S and 'g' in S and 'now' in S:
        o = sorted(zip(S['plantTime'], S['growTime']), key=lambda d: d[1], reverse=True)
        return o.index((S['p'], S['g'])) if (S['p'], S['g']) in o else None
    return None


def _txt(S):
    c = _cur(S)
    if c is None or 'now' not in S:
        return '花开得慢（g 大）的先种：让慢花尽早开始长'
    return f'当前种到第 `{S["now"]}` 天，这朵再长 `{S["g"]}` 天 → 第 =={S["now"] + S["g"]}== 天开花'


CONFIG = dict(
    num=2136, title='全部开花的最早一天', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='慢花先种 · 一趟扫描',
    tags=['灵神题单', '贪心与思维', '难度分 2033'],
    code='''
class Solution(object):
    def earliestFullBloom(self, plantTime, growTime):

        res = 0
        now = 0
        for p, g in sorted(zip(plantTime, growTime), key=lambda d:d[1], reverse=True):
            now += p
            res = max(res, now + g)
        
        return res
''',
    call='Solution().earliestFullBloom([1,4,3], [2,3,1])',
    expect=9,
    views=[
        dict(type='text', fn=_txt, h=80),
        dict(type='array', var=SORT, cell=130, h=240, label='先种谁：按 g 从大到小的 (p, g)',
             color=lambda S, i, v: 'yellow' if _cur(S) == i else None,
             dim=lambda S, i, v: _cur(S) is not None and i < _cur(S)),
        dict(type='text', fn=lambda S: '`now` = 播种进行到第几天，`res` = 目前最晚的开花日', h=70),
    ],
    watch=[('now', 'now', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res`：目前为止最晚的开花时间',
        'now = 0': '`now`：播种累计用了多少天，从第 0 天开始',
        'for p, g': '下一朵花：播种 `p = {p}` 天，生长 `g = {g}` 天（生长慢的排前面）',
        'now += p': '播种这朵花，播种完成在第 `{now}` 天（==不穿插，一朵种完再种下一朵==）',
        'res = max': '播完后再长 `{g}` 天，开花在第 `{now + g}` 天；`res = max({B.res}, {now + g}) = {res}`',
        'return res': '所有花开完的最早一天：`{res}`',
    },
    cards=dict(
        one_liner='先证明播种不穿插，再让开得慢的花先种',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每朵花先播种 `plantTime` 天，再生长 `growTime` 天开花',
                 '每天只能种一颗，可以拆开，顺序随意',
                 '示例：`plantTime=[1,4,3], growTime=[2,3,1]` → `9`'],
        quote='首先可以明确的是，播种的行为必然不会穿插进行，证明也很简单。对于两个种子i和j，播种的总时间固定为plantTime[i] + plantTime[j]。',
        quote_src='—— yiduobo 题解原文',
        idea=['穿插播种会让先完成的那朵更晚，另一朵不变，显然不优',
              '直觉：哪朵花开得慢就先种；反证：若最晚开花的是第 k 朵，往前挪只会挤下更慢的花',
              '所以按 `g` 从大到小排序，`now` 累加播种天数，`res` 取最大开花日'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错点：`now` 只累加播种天数，生长天数只用来算开花日，不占用播种时间',
                 '原文已是 Python 3 可运行写法，未做修改',
                 '对比灵神：灵神用「相邻交换」论证，yiduobo 用「最晚的那朵往前挪」的反证法'],
    ),
)
