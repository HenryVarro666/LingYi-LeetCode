def _ps(S):
    s = [0]
    for x in S['differences']:
        s.append(s[-1] + x)
    return s


def _mm(S):
    s = _ps(S)
    return min(s), max(s)


def _txt(S):
    if 'min_s' not in S:
        return '`a[i] = a[0] + s[i]`：先看前缀和 `s` 的最小、最大值'
    lo, up = S['lower'], S['upper']
    mn = S['min_s']
    if 'max_s' not in S:
        return f'`a[0]` 至少 `lower − min_s = {lo} − ({mn}) = {lo - mn}`'
    mx = S['max_s']
    return f'`a[0]` 取值范围 `[{lo - mn}, {up - mx}]`，个数 = `{up - mx} − ({lo - mn}) + 1` = =={up - mx - (lo - mn) + 1}=='


CONFIG = dict(
    num=2145, title='统计隐藏数组数目', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='前缀和 · 区间交集',
    tags=['灵神题单', '数学算法', '难度分 1614'],
    code='''
class Solution:
    def numberOfArrays(self, differences: List[int], lower: int, upper: int) -> int:
        min_s = min(accumulate(differences, initial=0))  # 前缀和的最小值
        max_s = max(accumulate(differences, initial=0))  # 前缀和的最大值
        return max(upper - lower - max_s + min_s + 1, 0)
''',
    call='Solution().numberOfArrays([3,-4,5,1,-2], -4, 5)',
    expect=4,
    views=[
        dict(type='array', var='differences', label='differences（相邻差 d）', h=200),
        dict(type='array', var=lambda S: _ps(S), label='前缀和 s（s[0] = 0）', h=230,
             color=lambda S, i, v: ('blue' if v == _mm(S)[0] and 'min_s' in S else 'pink' if v == _mm(S)[1] and 'max_s' in S else None)),
        dict(type='text', fn=_txt, size=34, h=120),
    ],
    watch=['lower', 'upper', ('min_s', 'min_s', 'blue'), ('max_s', 'max_s', 'pink')],
    captions={
        'min_s = min': '`a[i] = a[0] + s[i]`，所以只看前缀和 `s`（含 `s[0]=0`）；最小值 `min_s` = =={min_s}==',
        'max_s = max': '前缀和最大值 `max_s` = =={max_s}==',
        'return max': '`a[0]` 的范围是 `[lower − min_s, upper − max_s]`，个数 `{upper} − {lower} − {max_s} + {min_s} + 1` = =={ret}==；为负就取 0',
    },
    cards=dict(
        one_liner='确定了 a[0]，整个隐藏数组就定了：数 a[0] 的取值个数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`differences[i] = hidden[i+1] − hidden[i]`，hidden 所有数都在 `[lower, upper]`',
                 '求满足条件的 hidden 数组有多少个',
                 '示例：`[3,-4,5,1,-2]`，`lower=-4, upper=5` → `4`'],
        quote='这 n+1 个区间的==交集==大小，就是答案。（注意数组 a 的长度是 n+1）',
        quote_src='—— 灵茶山艾府题解',
        idea=['`a[i] = a[0] + s[i]`，`s` 是 d 的前缀和，所以 a[0] 决定一切',
              '`lower ≤ a[0] + s[i] ≤ upper` 对每个 i 都成立 → n+1 个区间求交集',
              '交集左端点 `lower − min s`，右端点 `upper − max s`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '前缀和要包含 `s[0] = 0`，所以 `accumulate` 要加 `initial=0`',
                 '交集可能为空，答案要和 0 取 max',
                 '同类题：3468. 可行数组的数目'],
    ),
)
