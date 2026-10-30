SORT = 'sorted(zip(plantTime, growTime), key=lambda z: -z[1])'


def _cur(S):
    if 'p' in S and 'g' in S and 'days' in S:
        o = sorted(zip(S['plantTime'], S['growTime']), key=lambda z: -z[1])
        return o.index((S['p'], S['g'])) if (S['p'], S['g']) in o else None
    return None


def _txt(S):
    c = _cur(S)
    if c is None or 'days' not in S:
        return '每个种子 `(播种天数 p, 生长天数 g)`：生长久的先种'
    return f'播完这个种子是第 `{S["days"]}` 天，再长 `{S["g"]}` 天 → 开花日 =={S["days"] + S["g"]}=='


CONFIG = dict(
    num=2136, title='全部开花的最早一天', difficulty='Hard', category='贪心算法',
    author='灵茶山艾府', technique='交换论证 · 按生长天数从大到小',
    tags=['灵神题单', '难度分 2033'],
    code='''
class Solution:
    def earliestFullBloom(self, plantTime: List[int], growTime: List[int]) -> int:
        ans = days = 0
        for p, g in sorted(zip(plantTime, growTime), key=lambda z: -z[1]):
            days += p  # 累加播种天数
            ans = max(ans, days + g)  # 再加上生长天数，就是这个种子的开花时间
        return ans
''',
    call='Solution().earliestFullBloom([1,4,3], [2,3,1])',
    expect=9,
    views=[
        dict(type='text', fn=_txt, h=80),
        dict(type='array', var=SORT, cell=130, h=240, label='按 g 从大到小的 (p, g)',
             color=lambda S, i, v: 'yellow' if _cur(S) == i else None,
             dim=lambda S, i, v: _cur(S) is not None and i < _cur(S)),
        dict(type='text', fn=lambda S: '一个人轮流播种：播种不能并行，生长可以并行', h=70),
    ],
    watch=[('days', 'days', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = days = 0': '`days` 是已经花在播种上的总天数，`ans` 是最晚开花日',
        'for p, g': '按生长天数从大到小取下一个种子：播种 `p = {p}` 天，生长 `g = {g}` 天',
        'days += p': '播种这个种子要 `{p}` 天：`days` = {days}（==种完一个再种下一个，不交替==）',
        'ans = max': '它在第 `{days} + {g} = {days + g}` 天开花；`ans = max({B.ans}, {days + g}) = {ans}`',
        'return ans': '最后一朵花开的日子：`{ans}`',
    },
    cards=dict(
        one_liner='播种不交替；生长久的先种，让它早点开始长',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每个种子要先播种 `plantTime` 天，再生长 `growTime` 天才开花',
                 '每天只能为一个种子播种，顺序任意，可拆开',
                 '示例：`plantTime=[1,4,3], growTime=[2,3,1]` → `9`'],
        quote='这意味着按照生长天数从大到小排序后，交换任意两枚种子的播种顺序，不会让最晚开花时间提前。',
        quote_src='—— 灵茶山艾府题解',
        idea=['交替播种不会让总播种时间变短，反而拖慢某些种子，所以种完一个再种下一个',
              '两枚种子比较：设 `g1 ≥ g2`，先 1 后 2 的最晚开花不晚于先 2 后 1',
              '所以按 `g` 从大到小排序，累加 `p` 并取 `days + g` 的最大值'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（排序用到的列表）',
                 '易错点：排序键只看生长天数，与播种天数无关；`g` 相同的顺序随意',
                 '`ans` 取的是==所有种子开花日的最大值==，不是最后一个种子的',
                 '同类交换论证题：1665'],
    ),
)
