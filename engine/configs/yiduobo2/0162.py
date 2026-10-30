NUMS = [1, 2, 1, 3, 5, 6, 4]


def _live(S):
    return isinstance(S.get('l'), int) and isinstance(S.get('r'), int)


def _color(S, i, v):
    if not _live(S):
        return None
    if S.get('_line') == 12 and i == S['l']:
        return 'green'
    m = S.get('mid')
    if isinstance(m, int) and S.get('_line') in (6, 7, 8, 10):
        if i == m:
            return 'orange'
        if i == m + 1:
            return 'cyan'
    return None


def _dim(S, i, v):
    return _live(S) and not (S['l'] <= i <= S['r'])


def _text(S):
    if not _live(S):
        return ''
    l, r = S['l'], S['r']
    if S.get('_line') == 12:
        return f"`l == r = {l}`：范围缩成一个点，它就是峰值"
    return f"答案一定在闭区间 `[l, r] = [{l}, {r}]` 里"


def _cap_while(S, B, ret):
    l, r = B.l, B.r
    if l < r:
        return f'`l = {l} < r = {r}`：范围里不止一个数 → 继续二分'
    return f'`l == r = {l}`：逐步缩小范围直到 l 等于 r → 结束'


def _cap_if(S, B, ret):
    m = S.mid
    a, b = S.nums[m], S.nums[m + 1]
    if a > b:
        return f'`nums[{m}] = {a} > nums[{m + 1}] = {b}`：==nums[mid] 较大== → 答案在 `l` 到 `mid` 之间'
    return f'`nums[{m}] = {a} < nums[{m + 1}] = {b}`：==nums[mid+1] 较大== → 答案在 `mid+1` 到 `r` 之间'


CONFIG = dict(
    num=162, title='寻找峰值', difficulty='Medium', category='二分查找',
    author='yiduobo', technique='闭区间二分 · l 与 r 相遇即峰值',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution(object):
    def findPeakElement(self, nums):
        l = 0
        r = len(nums) - 1
        while l < r:
            mid = (l + r) // 2
            if nums[mid] > nums[mid + 1]:
                r = mid
            else:
                l = mid + 1

        return l
''',
    call=f'Solution().findPeakElement({NUMS})',
    expect=5,
    views=[
        dict(type='text', fn=_text, h=64),
        dict(type='bars', var='nums', label='nums（框 = [l, r]，橙 = mid，青 = mid+1）', h=420,
             pointers={'l': 'blue', 'r': 'pink', 'mid': 'orange'},
             window=('l', 'r'), color=_color, dim=_dim, vmax=7),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'orange')],
    captions={
        'l = 0': '要求 `O(log n)` → 自然想到==二分==：`l = 0`',
        'r = len(nums) - 1': '`r = {r}`，答案在闭区间 `[l, r]` 中',
        'while l < r': _cap_while,
        'mid = (l + r) // 2': '`mid = ({B.l} + {B.r}) // 2 = {mid}`',
        'if nums[mid] > nums[mid + 1]': _cap_if,
        'r = mid': '`r = mid = {r}`（mid 自己也可能是峰）',
        'l = mid + 1': '`l = mid + 1 = {l}`（mid 比右邻居小，不可能是峰）',
        'return l': '`l == r`，返回 =={ret}==（`nums[{ret}] = {nums[ret]}`，比两边都大）',
    },
    cards=dict(
        one_liner='比较 nums[mid] 与 nums[mid+1]，往大的那一边缩',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['峰值：==严格大于左右相邻值==的元素，返回任意一个峰值的下标',
                 '假设 `nums[-1] = nums[n] = -∞`，相邻元素互不相等，要求 `O(log n)`',
                 '示例：`[1,2,1,3,5,6,4]` → `1` 或 `5`（本视频二分到 `5`）'],
        quote='又因为题目保证了nums[i] != nums[i +1]，于是我们可以在每轮二分时==比较nums[mid]与nums[mid + 1]==：若nums[mid]较大，那么答案位于l到mid之间……若nums[mid + 1]较大，那么答案位于mid + 1到r之间。',
        quote_src='—— yiduobo 题解原文',
        idea=['`O(log n)` 的要求 → 二分；相邻不等 → `nums[mid]` 与 `nums[mid+1]` ==必有大小==',
              '往较大的一侧走一定能"爬"到峰：`r = mid` 或 `l = mid + 1`',
              '逐步缩小范围直到 `l == r`，返回 `l`'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '`while l < r` 保证 `mid < r`，所以 `mid + 1` 不越界',
                 '`r = mid` 而不是 `mid - 1`：`nums[mid]` 较大时 mid 本身可能就是峰',
                 '对比灵神：灵神用开区间 `(-1, n-1)` 返回 `right`，思路相同',
                 '原文为 Python 2 写法，`(l + r) / 2` 已改为整除 `//`；删去了文档字符串'],
    ),
)
