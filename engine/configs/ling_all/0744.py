LETTERS = ['a', 'c', 'c', 'e', 'f', 'h', 'j', 'm']
TARGET = 'e'


def _color(S, i, v):
    if 'right' not in S:
        return None
    if i <= S['left']:
        return 'red'
    if i >= S['right']:
        return 'blue'
    return None


def _top(S):
    if 'right' not in S:
        return f"找 ==> '{TARGET}'== 的第一个字母：红 = `≤ target`，蓝 = `> target`"
    l, r = S['left'], S['right']
    if l + 1 < r:
        return f'开区间 `({l}, {r})`：里面 `{r - l - 1}` 个字母还==没染色=='
    return f'开区间为空：`right = {r}` 就是第一个蓝色（`> target`）的位置'


def _while(S, B, ret):
    l, r = S.left, S.right
    if l + 1 < r:
        return f'开区间 `({l}, {r})` 不为空 → 继续二分'
    return f'`left + 1 == right = {r}`：开区间为空，==每个字母都染好色了=='


def _if(S, B, ret):
    m, c = S.mid, S.letters[S.mid]
    if c > S.target:
        return f"`letters[{m}] = '{c}' > '{S.target}'`：成立 → `{m}` 及右边都 ==> target==，染蓝"
    return f"`letters[{m}] = '{c}' ≤ '{S.target}'`：不成立 → `{m}` 及左边都 ==≤ target==，染红"


CONFIG = dict(
    num=744, title='寻找比目标字母大的最小字母', difficulty='Easy', category='二分算法',
    author='灵茶山艾府', technique='开区间二分 · 红蓝染色',
    tags=['灵神核心路线', '灵神题单·二分算法'],
    code='''
class Solution:
    def nextGreatestLetter(self, letters: List[str], target: str) -> str:
        n = len(letters)
        left, right = -1, n
        while left + 1 < right:
            mid = (left + right) // 2
            if letters[mid] > target:
                right = mid
            else:
                left = mid
        return letters[right] if right < n else letters[0]
''',
    call=f'Solution().nextGreatestLetter({LETTERS}, {TARGET!r})',
    expect='f',
    views=[
        dict(type='text', fn=_top, size=27, h=90),
        dict(type='string', var='letters', label=f"letters（target = '{TARGET}'）红 = ≤ target，蓝 = > target",
             color=_color, pointers={'left': 'red', 'mid': 'yellow', 'right': 'blue'}, h=300),
    ],
    watch=[('left', 'left', 'red'), ('right', 'right', 'blue'), ('mid', 'mid', 'yellow'), 'n', 'target'],
    captions={
        'n = len': '`n = {n}` 个字母，已按非递减排序',
        'left, right = -1, n': '开区间 `(-1, {n})`：`left` 左边视为红，`right` 右边视为蓝，==区间外的不用再看==',
        'while left + 1 < right': _while,
        'mid = (left': '取中点：`mid = ({left} + {right}) // 2 = {mid}`',
        'if letters[mid] > target': _if,
        'right = mid': '`right` → {right}：`right` 及右边==恒为蓝==',
        'left = mid': '`left` → {left}：`left` 及左边==恒为红==',
        'return letters[right]': lambda S, B, r: (f"`right = {S.right} < n`：存在比 target 大的字母 → 返回 =={r!r}=="
                                                  if S.right < S.n else f'`right == n`：没有更大的 → 按题意返回 `letters[0]`'),
    },
    cards=dict(
        one_liner='二分找第一个 > target 的位置；找不到就返回 letters[0]',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['`letters` 非递减有序，至少有两种字母；给定字母 `target`',
                 '返回 letters 中 ==大于 target 的最小字母==，不存在就返回 `letters[0]`',
                 "示例：`['c','f','j'], 'c'` → `'f'`；`['x','x','y','y'], 'z'` → `'x'`"],
        quote='推荐写开区间二分，简单好记。',
        quote_src='—— 灵茶山艾府题解',
        idea=['红蓝染色：`≤ target` 染红，`> target` 染蓝；有序 → 红在左、蓝在右',
              '开区间 `(left, right)` 是未染色部分，每次看 `mid` 就能把一半染色',
              '结束时 `right` 是第一个蓝色；`right == n` 说明全红 → 返回 `letters[0]`'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '求的是 ==严格大于==：判断用 `>`，等于 target 的要染红',
                 '别忘了不存在的情况：`right == n` 时返回 `letters[0]`',
                 '库函数写法：`i = bisect_right(letters, target)`，同样判断 `i < len(letters)`'],
    ),
)
