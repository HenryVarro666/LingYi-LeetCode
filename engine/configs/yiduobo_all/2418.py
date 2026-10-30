NAMES = ['Mary', 'John', 'Emma', 'Alice', 'Bob']
HEIGHTS = [180, 165, 170, 155, 185]


def _order(S):
    h = S['heights']
    return sorted(range(len(h)), key=lambda d: h[d], reverse=True)


CONFIG = dict(
    num=2418, title='按身高排序', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='按身高给下标排序',
    tags=[],
    code='''
class Solution(object):
    def sortPeople(self, names, heights):

        return [names[x] for x in sorted(range(len(heights)), key=lambda d:heights[d], reverse=True)]
''',
    call=f'Solution().sortPeople({NAMES}, {HEIGHTS})',
    expect=['Bob', 'Mary', 'Emma', 'John', 'Alice'],
    views=[
        dict(type='array', var='names', label='names', h=130),
        dict(type='array', var='heights', label='heights', h=130),
        dict(type='text', size=30, fn=lambda S: ('下标按 heights 降序：' + ' → '.join(f'=={i}==' for i in _order(S))) if 'names' in S else ''),
        dict(type='text', size=30, fn=lambda S: ('对应名字：' + ' → '.join(S['names'][i] for i in _order(S))) if 'names' in S else ''),
    ],
    watch=['names', 'heights'],
    captions={
        'return [names': '`sorted(range(n), key=lambda d: heights[d], reverse=True)` 把下标按身高从高到低排，再用 `names[x]` 取名字 → =={ret}==',
    },
    cards=dict(
        after=[dict(heading='拆开看这一行', lines=['`range(len(heights))` 是下标 0~4', '按 `heights[d]` 降序排：4 → 0 → 2 → 1 → 3', '`names[x]` 依次取出：Bob, Mary, Emma, John, Alice'])],
        one_liner='不动原数组，只把下标按身高排一遍',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给出名字数组 `names` 和互不相同的身高数组 `heights`', '按身高降序返回名字',
                 '本视频：5 个人 → `["Bob","Mary","Emma","John","Alice"]`'],
        quote='比较基础的题目，按题目要求排序就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['做法一：名字和身高合并，以身高为关键字排序',
              '做法二：只对下标排序，key 取 `heights[d]`，再按排好的下标取名字',
              '视频里演示做法二：一行代码就是整个过程'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`key=lambda d: heights[d]` 里的 `d` 是下标，不是身高',
                 '身高互不相同，所以不用考虑并列',
                 '原文为 Python 2 风格，只是没有类型说明，代码未改动'],
    ),
)
