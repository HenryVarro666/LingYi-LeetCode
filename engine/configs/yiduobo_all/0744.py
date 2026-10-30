LETTERS = ['b', 'd', 'd', 'g', 'k', 'k', 'p', 't']
TARGET = 'k'


def _color(S, i, v):
    if 'r' not in S:
        return None
    if i < S['l']:
        return 'red'
    if i >= S['r']:
        return 'green'
    return None


def _top(S):
    if 'r' not in S:
        return f"先特判：`target ≥ letters[-1]` 时没有更大的字母"
    l, r = S['l'], S['r']
    if l < r:
        return f'左闭右开 `[{l}, {r})`：答案一定在这里面，还剩 `{r - l}` 个候选'
    return f'`l == r = {l}`：区间收缩成一个点，就是第一个 ==> target== 的位置'


def _while(S, B, ret):
    if S.l < S.r:
        return f'`l = {S.l} < r = {S.r}`：候选区间非空 → 继续二分'
    return f'`l == r = {S.l}`：区间为空，二分结束'


def _if(S, B, ret):
    m, c = S.mid, S.letters[S.mid]
    if c <= S.target:
        return f"`letters[{m}] = '{c}' ≤ '{S.target}'`：它和左边都不够大 → 答案在 `mid` 右侧"
    return f"`letters[{m}] = '{c}' > '{S.target}'`：它可能就是答案 → ==保留 mid==，往左找"


CONFIG = dict(
    num=744, title='寻找比目标字母大的最小字母', difficulty='Easy', category='二分算法',
    author='yiduobo', technique='特判 + 左闭右开二分',
    tags=['灵神核心路线', '灵神题单·二分算法'],
    code='''
class Solution(object):
    def nextGreatestLetter(self, letters, target):

        if target >= letters[-1]:
            return letters[0]

        l = 0
        r = len(letters)

        while l < r:
            mid = (l + r) >> 1
            if letters[mid] <= target:
                l = mid + 1
            else:
                r = mid

        return letters[l]
''',
    call=f'Solution().nextGreatestLetter({LETTERS}, {TARGET!r})',
    expect='p',
    views=[
        dict(type='text', fn=_top, size=27, h=90),
        dict(type='string', var='letters', label=f"letters（target = '{TARGET}'）红 = 排除，绿 = 可能的答案及右边",
             color=_color, pointers={'l': 'red', 'mid': 'yellow', 'r': 'green'}, cell=100, h=300),
    ],
    watch=[('l', 'l', 'red'), ('r', 'r', 'green'), ('mid', 'mid', 'yellow'), 'target'],
    captions={
        'if target >= letters[-1]': lambda S, B, r: (f"`'{S.target}' ≥ letters[-1] = '{S.letters[-1]}'` → 没有更大的字母，按题意返回 `letters[0]`"
                                                     if S.target >= S.letters[-1] else
                                                     f"`'{S.target}' < letters[-1] = '{S.letters[-1]}'`：最后一个字母更大 → ==答案一定存在==，放心二分"),
        'l = 0': '`l = 0`：左端点',
        'r = len': '`r = len(letters) = {r}`：左闭右开，`r` 本身不在候选里',
        'while l < r': _while,
        'mid = (l + r) >> 1': '`mid = ({l} + {r}) >> 1 = {mid}`：右移一位就是除以 2',
        'if letters[mid] <= target': _if,
        'l = mid + 1': '`l = mid + 1 = {l}`：`mid` 已排除',
        'r = mid': '`r = mid = {r}`：`mid` 仍可能是答案，留在 `[l, r)` 的右边界',
        'return letters[l]': "`letters[{l}] = {ret!r}` 就是比 target 大的最小字母",
    },
    cards=dict(
        one_liner='先特判没有答案的情况，再用二分找第一个大于 target 的字母',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['`letters` 非递减有序，至少有两种字母；给定字母 `target`',
                 '返回 letters 中 ==大于 target 的最小字母==，不存在就返回 `letters[0]`',
                 "本视频：`['b','d','d','g','k','k','p','t'], 'k'` → `'p'`"],
        quote='直接一趟扫描判断是最简洁的方法。不过注意到题目保证letters是有序的，那么也可以运用==二分查找==来解决问题，性能方面会相对好一些。',
        quote_src='—— yiduobo 题解原文',
        idea=['先看最后一个字母：`target ≥ letters[-1]` 说明没有更大的 → 返回 `letters[0]`',
              '否则答案一定存在，在 `[0, n)` 里二分',
              '`letters[mid] ≤ target` 就丢掉 mid 及左边，否则 `r = mid` 保留它'],
        summary=['时间 `O(log n)`，空间 `O(1)`；一趟扫描 `O(n)` 也能过',
                 '等于 target 也要往右走：判断用 `<=`',
                 '特判放在最前面，二分结束时 `l` 一定是合法下标',
                 '对比灵神：灵神用开区间 `(-1, n)`，最后再判断 `right < n`'],
    ),
)
