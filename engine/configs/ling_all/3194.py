def _sums(S):
    n = len(S['nums'])
    return [S['nums'][i] + S['nums'][n - 1 - i] for i in range(n // 2)]


def _txt(S):
    if S['nums'] != sorted(S['nums']):
        return '先排序，再让最小的和最大的配对'
    sums = _sums(S)
    n = len(S['nums'])
    parts = [f"`{S['nums'][i]}+{S['nums'][n - 1 - i]}={s}`" for i, s in enumerate(sums)]
    return '配对和：' + '  '.join(parts) + f'；最小的和 =={min(sums)}==，除以 2 得 =={min(sums) / 2}=='


def _color(S, i, v):
    n = len(S['nums'])
    if S['nums'] != sorted(S['nums']):
        return None
    sums = _sums(S)
    k = min(i, n - 1 - i)
    return 'green' if sums[k] == min(sums) else 'blue'


CONFIG = dict(
    num=3194, title='最小元素和最大元素的最小平均值', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='排序 + 首尾配对',
    tags=[],
    code='''
class Solution:
    def minimumAverage(self, nums: List[int]) -> float:
        nums.sort()
        return min(nums[i] + nums[-1 - i] for i in range(len(nums) // 2)) / 2
''',
    call='Solution().minimumAverage([7,8,3,4,15,13,4,1])',
    expect=5.5,
    views=[
        dict(type='array', var='nums', h=260, label='nums（排序后首尾配对）', color=_color),
        dict(type='text', fn=_txt, size=28, h=200),
    ],
    watch=[('n', 'len(nums)', 'blue')],
    captions={
        'nums.sort()': '先排序：每一轮要取的最小、最大，就是当前 ==最左和最右== 的两个数 → `{nums}`',
        'return min': lambda S, B, r: '`nums[i] + nums[-1-i]` 枚举 `i < n/2` 的每一对，最小和是 `%s`；最后才除以 2，返回 ==%s==' % (min(_sums(S)), r),
    },
    cards=dict(
        one_liner='排序后首尾配对，先比和、最后只除一次 2',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['每轮删掉当前最小和最大的数，把平均值放进 `averages`',
                 '返回 `averages` 里最小的那个',
                 '示例：`[7,8,3,4,15,13,4,1]` → `5.5`'],
        quote='最后除以 2，这样可以避免在循环中做浮点运算，只在最后返回时做一次浮点运算。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先 `sort`，第 `i` 轮取到的就是 `nums[i]` 和 `nums[-1-i]`',
              '平均值最小 ⇔ 两数之和最小，所以直接比较和',
              '一行生成器求最小和，返回前除以 `2`'],
        after=[dict(heading='为什么先比和、后除 2', lines=['平均值 = 和 / 2，除以同一个 `2` 不改变大小顺序', '所以比较 `nums[i] + nums[-1-i]` 就够了', '整数加法比浮点运算干净，只在返回时除一次', '这也是灵神写法里 `/ 2` 放在 `min(...)` 外面的原因'])],
        summary=['时间 `O(n log n)`（排序），空间 `O(1)`',
                 '`n` 为偶数，`range(n // 2)` 刚好配完每一对',
                 '`nums[-1 - i]` 是倒数第 `i+1` 个，别写成 `nums[-i]`',
                 '`/ 2` 在 Python 3 得到浮点数，所以返回 `5.5`'],
    ),
)
