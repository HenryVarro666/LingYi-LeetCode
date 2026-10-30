def _grp(S, a, b):
    s1, s2 = S.get('s1'), S.get('s2')
    if not s1:
        return ''
    p, q = sorted([s1[a], s1[b]]), sorted([s2[a], s2[b]])
    return f'下标 {a}、{b} 一组：`{"".join(p)}` vs `{"".join(q)}` → ' + ('==相同==' if p == q else '==不同==')


CONFIG = dict(
    num=2839, title='判断通过操作能否让字符串相等 I', difficulty='Easy', category='字符串',
    author='yiduobo', technique='下标 0/2、1/3 分组比 min 和 max',
    code='''
class Solution(object):
    def canBeEqual(self, s1, s2):

        if min(s1[0], s1[2]) != min(s2[0], s2[2]):
            return False
        if max(s1[0], s1[2]) != max(s2[0], s2[2]):
            return False
        if min(s1[1], s1[3]) != min(s2[1], s2[3]):
            return False
        if max(s1[1], s1[3]) != max(s2[1], s2[3]):
            return False
        return True
''',
    call='[Solution().canBeEqual("abcd", "cdab"), Solution().canBeEqual("abcd", "dacb")]',
    expect=[True, False],
    views=[
        dict(type='string', var='s1', label='s1', h=150,
             color=lambda S, i, v: 'blue' if i % 2 == 0 else 'pink'),
        dict(type='string', var='s2', label='s2', h=150,
             color=lambda S, i, v: 'blue' if i % 2 == 0 else 'pink'),
        dict(type='text', fn=lambda S: _grp(S, 0, 2), h=70),
        dict(type='text', fn=lambda S: _grp(S, 1, 3), h=70),
    ],
    watch=['s1', 's2'],
    captions={
        'min(s1[0], s1[2]) !=': '下标 0、2 的较小字符：`{min(s1[0], s1[2])}` vs `{min(s2[0], s2[2])}`，'
                                 '{"不同 → 换不成" if min(s1[0], s1[2]) != min(s2[0], s2[2]) else "相同，继续"}',
        'max(s1[0], s1[2]) !=': '下标 0、2 的较大字符：`{max(s1[0], s1[2])}` vs `{max(s2[0], s2[2])}`，'
                                 '{"不同 → 换不成" if max(s1[0], s1[2]) != max(s2[0], s2[2]) else "相同，说明这一组字符一样"}',
        'min(s1[1], s1[3]) !=': '下标 1、3 的较小字符：`{min(s1[1], s1[3])}` vs `{min(s2[1], s2[3])}`，'
                                 '{"不同 → 换不成" if min(s1[1], s1[3]) != min(s2[1], s2[3]) else "相同，继续"}',
        'max(s1[1], s1[3]) !=': '下标 1、3 的较大字符：`{max(s1[1], s1[3])}` vs `{max(s2[1], s2[3])}`，'
                                 '{"不同 → 换不成" if max(s1[1], s1[3]) != max(s2[1], s2[3]) else "相同，这一组也一样"}',
        'return False': '有一组对不上，不管怎么交换都无法相等 → `False`',
        'return True': '两组都一致，可以通过交换变成相等 → `True`',
    },
    cards=dict(
        one_liner='下标 0、2 一组，1、3 一组，组内可互换',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['长度为 4 的两个字符串，可交换同一字符串里下标差为 2 的字符，问能否相等',
                 '示例：`"abcd"` 和 `"cdab"` → `true`；`"abcd"` 和 `"dacb"` → `false`',
                 '本视频连着演示这两个示例'],
        quote='字符串长度为4，且可交换的下标之差为2，那么就意味着两个字符串中的下标0、2可以互相交换，下标1、3可以互相交换。',
        quote_src='—— yiduobo 题解原文',
        idea=['每组只有两个字符，排好序就是（较小，较大）',
              '两串在同一组里的 min 和 max 都相等，这一组就一样',
              '四次比较全过才返回 `True`'],
        summary=['时间、空间都是 `O(1)`',
                 '易错点：下标 0、2 不能和 1、3 混起来比较',
                 '原文为 Python 2 风格，只删去了空行；代码逐字保留',
                 '对比灵神：灵神用 Counter 通用地比较奇偶两组，这里利用长度只有 4 直接比 min/max'],
    ),
)
