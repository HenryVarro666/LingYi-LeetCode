def _bad_color(S, i, v):
    return 'red' if v >= 7 else None


CONFIG = dict(
    num=278, title='第一个错误的版本', difficulty='Easy', category='二分算法',
    author='yiduobo', technique='二分答案 · 找左边界',
    tags=['灵神题单'],
    setup='''
FIRST_BAD = 7
VERSIONS = list(range(1, 11))
def isBadVersion(v):
    return v >= FIRST_BAD
''',
    code='''
class Solution(object):
    def firstBadVersion(self, n):

        left = 1
        right = n

        while left < right:
            mid = (left + right) // 2
            if isBadVersion(mid):
                right = mid
            else:
                left = mid + 1

        return left
''',
    call='Solution().firstBadVersion(10)',
    expect=7,
    views=[
        dict(type='text', size=26, h=60,
             fn=lambda S: (f"答案区间 [`{S['left']}`, `{S['right']}`]，共 {S['right']-S['left']+1} 个版本" if 'right' in S else '版本 1..10，红色 = 错误版本（从 7 开始）')),
        dict(type='array', var=lambda S: list(range(1, 11)), label='版本号（红 = 错误版本）', cell=84, h=300,
             pointers={'left-1': 'blue', 'right-1': 'pink', 'mid-1': 'yellow'},
             window=('left-1', 'right-1'), index=False,
             pointer_labels={'left-1': 'left', 'right-1': 'right', 'mid-1': 'mid'},
             color=_bad_color,
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= v <= S['right'])),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow')],
    captions={
        'left = 1': '版本从 1 开始，`left = 1`',
        'right = n': '`right = n = {right}`：答案一定在 [1, n] 之内',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`：区间里还有多个候选 → 继续二分' if S.left < S.right
                                                else f'`left = right = {S.left}`：区间只剩一个版本 → 它就是答案'),
        'mid = ': '取中点 `mid = ({left} + {right}) // 2 = =={mid}==`',
        'if isBadVersion': lambda S, B, r: (f'`isBadVersion({S.mid})` 为 ==真==：mid 本身可能就是第一个错误版本，答案在 [left, mid]' if S.mid >= 7
                                            else f'`isBadVersion({S.mid})` 为 ==假==：mid 及左边都是好版本，答案在 [mid+1, right]'),
        'right = mid': '`right = mid = {right}`：==保留 mid==（它可能就是答案）',
        'left = mid + 1': '`left = mid + 1 = {left}`：mid 是好版本，直接排除',
        'return left': '`left = {left}` 就是第一个错误版本',
    },
    cards=dict(
        one_liner='mid 是错的，答案在左半含 mid；否则在右半',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['版本 `1..n`，从某个版本开始之后全是错误版本',
                 '用 `isBadVersion(v)` 判断，找出第一个错误版本，调用次数尽量少',
                 '本视频：`n = 10`，第一个错误版本是 `7`'],
        quote='若当前的mid是错误的版本，那么答案就位于left到mid之间，否则答案位于mid + 1到right之间。',
        quote_src='—— yiduobo 题解原文',
        idea=['对 `1..n` 二分：错误版本是单调的（好好好错错错）',
              'mid 是错的 → ==right = mid==（mid 仍是候选）',
              'mid 是好的 → ==left = mid + 1==，区间每次至少缩小一半'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '`right = mid` 与 `left = mid + 1` 配套，才不会死循环',
                 '若写成 `left = mid`，当 `left + 1 == right` 时 mid 不变会死循环',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
