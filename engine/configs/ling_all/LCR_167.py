def _win_text(S):
    if 'right' not in S:
        return '窗口 `[left, right]`：右端点进，重复了就从左边出'
    a, l, r = S['arr'], S['left'], S['right']
    w = a[l:r + 1]
    dup = S['c'] in S['window'] and S['_line'] is not None and len(set(w)) < len(w)
    tag = '==有重复==' if dup else '无重复'
    return f"窗口 `arr[{l}..{r}]` = `\"{w}\"`，长度 `{r - l + 1}`，{tag}"


def _color(S, i, v):
    if 'right' not in S:
        return None
    if i == S['right'] and v == S['c'] and S['c'] in S['window'] and S['left'] <= i:
        w = S['arr'][S['left']:S['right']]
        if S['c'] in w and S['arr'][S['left']:S['right'] + 1].count(S['c']) > 1:
            return 'red'
    return None


CONFIG = dict(
    num='LCR 167', title='招式拆解 I', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='不定长滑动窗口 · 哈希集合', tags=[],
    code='''
class Solution:
    def dismantlingAction(self, arr: str) -> int:
        ans = left = 0
        window = set()  # 维护从下标 left 到下标 right 的字符
        for right, c in enumerate(arr):
            while c in window:  # 加入 c 后，窗口内会有重复元素
                window.remove(arr[left])
                left += 1  # 缩小窗口
            window.add(c)
            ans = max(ans, right - left + 1)  # 更新窗口长度最大值
        return ans
''',
    call='Solution().dismantlingAction("dbascDdad")',
    expect=6,
    views=[
        dict(type='text', fn=_win_text),
        dict(type='string', var='arr', pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'),
             color=_color, cell=90, h=270, label='arr'),
        dict(type='set', var='window', fmt=lambda x: str(x), font=30, h=150, label='window：窗口内的字符'),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('c', 'c', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = left = 0': '`ans` 记录最长长度，`left` 是窗口左端点',
        'window = set()': '`window` 集合：保存窗口 `[left, right]` 内的字符，用来 `O(1)` 判重',
        'for right, c in': lambda S, B, r: ('枚举结束' if 'right' in B and B.right == S.right
                                            else f'枚举右端点 `right = {S.right}`：招式 `"{S.c}"` 准备进入窗口'),
        'while c in window': lambda S, B, r: (f'`"{S.c}"` 已在窗口里：加入后会重复 → ==先从左边缩小窗口=='
                                              if S.c in S.window else f'`"{S.c}"` 不在窗口里：可以直接加入'),
        'window.remove': '移除窗口左端点字符 `"{B.arr[B.left]}"`',
        'left += 1': '缩小窗口：`left` → {left}，窗口变成 `"{arr[left:right]}"`（再看 `"{c}"` 是否还重复）',
        'window.add': '窗口内已无重复 → 加入 `"{c}"`，窗口变成 `"{arr[left:right + 1]}"`',
        'ans = max': '窗口 `"{arr[left:right + 1]}"` 合法，长度 `{right - left + 1}`：`ans = max({B.ans}, {right - left + 1}) = {ans}`',
        'return ans': '最多连续不重复的招式数 `{ans}`',
    },
    cards=dict(
        one_liner='枚举右端点，重复了就收缩左端点：窗口里永远没有重复',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['招式序列 `arr`，求最长的==连续且不重复==的招式段长度',
                 '示例：`"dbascDdad"` → `6`（`"dbascD"` 或 `"bascDd"`）',
                 '注意是子串（连续），不是子序列'],
        quote='`while c in window`：==加入 c 后，窗口内会有重复元素==，所以先缩小窗口，再加入 c。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['用集合 `window` 记录窗口内字符，枚举右端点 `right`',
              '`c` 已在集合中 → 不断移除 `arr[left]`、`left += 1`，直到 `c` 不在窗口里',
              '再把 `c` 加入，此时窗口合法，用长度更新 `ans`'],
        summary=['时间 `O(n)`：`left` 至多增加 `n` 次，二重循环总共至多 `O(n)` 次',
                 '空间 `O(|Σ|)`：字符均为 ASCII，集合至多 128 个元素',
                 '易错：先 `while` 缩窗口、再 `add`；顺序反了集合会误删',
                 '同主站 3 题；视频讲解见「基础算法精讲」滑动窗口'],
    ),
)
