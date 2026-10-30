NAMES = ['Mary', 'John', 'Emma', 'Alice', 'Bob']
HEIGHTS = [180, 165, 170, 155, 185]


def _pairs(S):
    return sorted(zip(S['heights'], S['names']), reverse=True)


CONFIG = dict(
    num=2418, title='按身高排序', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='zip 后排序',
    tags=[],
    code='''
class Solution:
    def sortPeople(self, names: List[str], heights: List[int]) -> List[str]:
        return [name for _, name in sorted(zip(heights, names), reverse=True)]
''',
    call=f'Solution().sortPeople({NAMES}, {HEIGHTS})',
    expect=['Bob', 'Mary', 'Emma', 'John', 'Alice'],
    views=[
        dict(type='array', var='names', label='names', h=130),
        dict(type='array', var='heights', label='heights', h=130),
        dict(type='text', size=30, fn=lambda S: ('`zip(heights, names)` 配对：' + '  '.join(f'({h},{n})' for h, n in zip(S['heights'], S['names'])))
             if 'names' in S else ''),
        dict(type='text', size=30, fn=lambda S: ('按身高降序：' + '  '.join(f'==({h},{n})==' for h, n in _pairs(S)))
             if 'names' in S else ''),
    ],
    watch=['names', 'heights'],
    captions={
        'return [name': '先 `zip(heights, names)` 把身高和名字绑成一对，再 `sorted(..., reverse=True)` 按身高从高到低排；最后只取名字 → =={ret}==',
    },
    cards=dict(
        after=[dict(heading='拆开看这一行', lines=['`zip(heights, names)`：(180,Mary) (165,John) (170,Emma) (155,Alice) (185,Bob)', '降序排序：185 → 180 → 170 → 165 → 155', '推导式 `for _, name in ...` 丢掉身高，只留名字'])],
        one_liner='身高和名字绑成一对，一起排序',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`names[i]` 和 `heights[i]` 是第 `i` 个人的名字和身高', '按身高 ==降序== 返回名字数组，身高互不相同',
                 '本视频：5 个人 → `["Bob","Mary","Emma","John","Alice"]`'],
        quote='Python 可以直接 `zip` 后排序。',
        quote_src='—— 灵茶山艾府题解',
        idea=['通用做法是对下标数组排序，不打乱输入、又保持名字和身高对应',
              'Python 里 `zip` 一下，元组默认先比身高，身高互不相同所以不会比到名字',
              '排完用推导式丢掉身高，只留名字'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`zip(heights, names)` 身高必须放在前面，排序才以身高为关键字',
                 '要降序别忘了 `reverse=True`',
                 '通用写法（C++/Java）：对下标数组按 `heights` 排序'],
    ),
)
