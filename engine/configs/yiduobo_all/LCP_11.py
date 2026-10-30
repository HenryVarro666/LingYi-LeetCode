SC = [5, 3, 5, 5, 8, 3]
PAL = ['blue', 'pink', 'green', 'purple']


def _color(S, i, v):
    return PAL[sorted(set(S['scores'])).index(v) % 4]


def _groups(S):
    sc = S['scores']
    parts = []
    for v in sorted(set(sc)):
        m = sc.count(v)
        parts.append(f'能力值 `{v}`：{m} 份')
    return '　'.join(parts)


def _exp(S):
    sc = S['scores']
    k = len(set(sc))
    return f'每组期望都是 1，{k} 组相加 = =={k}==（组数 = `len(set(scores))`）'


CONFIG = dict(
    num='LCP 11', title='期望个数统计', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='期望线性性 · 每组期望为 1',
    tags=['灵神题单·数学算法'],
    code='''
class Solution(object):
    def expectNumber(self, scores):

        return len(set(scores))
''',
    setup='',
    call=f'Solution().expectNumber({SC})',
    expect=3,
    views=[
        dict(type='array', var='scores', color=_color, label='scores：同色 = 能力值相同的简历', h=240),
        dict(type='text', fn=_groups, size=26, h=100),
        dict(type='text', fn=_exp, size=28, h=100),
    ],
    watch=[('不同能力值个数', 'len(set(scores))', 'green')],
    captions={
        'return len(set(scores))': '`set(scores)` 去重后有 `{len(set(scores))}` 种能力值 → 期望个数 =={ret}==',
    },
    cards=dict(
        one_liner='相同能力值的一组，期望恰好有 1 个落在原位',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['有 `n` 份简历，各有一个能力值 `scores[i]`；按能力值排序后，相同能力值的简历顺序随机打乱',
                 '求排序后「位置与原来一致」的简历个数的期望',
                 f'本视频：`{SC}` → `3`'],
        quote='由于只有相同的能力值将打乱简历的顺序，那么就可以将简历按相同能力值分开，各算各的，最后再把期望加起来。',
        quote_src='—— yiduobo 题解原文',
        idea=['只有能力值相同的简历才会互相打乱，所以按能力值分组，每组单独算',
              '一组 `n` 份：相当于随机排列，每个数落在自己位置的概率是 `1/n`',
              '期望可以拆开加：`n` 个 `1/n` 之和 = ==1==，与组大小无关 → 答案 = 组数'],
        after=[dict(heading='按组算一遍', lines=['能力值 `5` 有 3 份：随机排列，每份在原位的概率 `1/3`，3 份合计 `3 × 1/3` = ==1==',
                                              '能力值 `3` 有 2 份：每份概率 `1/2`，合计 `2 × 1/2` = ==1==',
                                              '能力值 `8` 只有 1 份：位置不会变，概率 1，合计 ==1==',
                                              '三组相加 = 3，正好是不同能力值的个数'])],
        summary=['时间 `O(n)`，空间 `O(n)`（集合去重）',
                 '期望的线性性：不用管各位置事件是否独立',
                 '不要真的去枚举排列：数据规模很大，结论只与不同能力值个数有关',
                 '原文本来就是 Python 3 可运行写法，代码未改动'],
    ),
)
