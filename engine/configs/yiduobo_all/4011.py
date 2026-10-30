def _g(name):
    return lambda S: S['_inner'].get(name)


_L, _R, _M, _I, _J = _g('left'), _g('right'), _g('mid'), _g('i'), _g('j')


def _info(S):
    I = S['_inner']
    l, r = I.get('left'), I.get('right')
    if l is None:
        return '偶数 `-b`、奇数 `+a`：和 >= 0 即有效 → 数前缀和的非逆序对'
    if 'mid' not in I:
        return f'`calc({l}, {r})`：数 `s[{l}..{r}]` 里 ==前 <= 后== 的对数'
    return f"`calc({l}, {r})`：左 `[{l}..{I['mid']}]`、右 `[{I['mid'] + 1}..{r}]` 有序后，合并时累加跨半对数"


def _cmp(S, B, ret):
    I = S['_inner']
    i, j, r = I['i'], I['j'], I['right']
    a, b = S['s'][i], S['s'][j]
    if a <= b:
        return (f'`s[{i}] = {a} <= s[{j}] = {b}`：右半 `s[{j}..{r}]` 已有序，共 `{r - j + 1}` 个都 >= {a} '
                f'→ ==这 {r - j + 1} 对都是有效子数组==')
    return f'`s[{i}] = {a} > s[{j}] = {b}`：`{a}` 比 `{b}` 大，和 `{b}` 配不成对 → 先取较小的 `{b}`'


CONFIG = dict(
    num=4011, title='按奇偶比统计子数组 I', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='转成前缀和 + 归并排序数非逆序对',
    tags=[],
    code='''
class Solution(object):
    def countRatioSubarrays(self, nums, a, b):
        
        s = [0]
        for v in nums:
            if v % 2 == 0:
                s.append(s[-1] - b)
            else:
                s.append(s[-1] + a)
        
        def calc(left, right, s):
            if left == right:
                return 0
            
            mid = (left + right) // 2
            tot = calc(left, mid, s) + calc(mid + 1, right, s)
            tmp = []
            
            i, j = left, mid + 1
            while i <= mid and j <= right:
                if s[i] <= s[j]:
                    tot += right - j + 1
                    tmp.append(s[i])
                    i += 1
                else:
                    tmp.append(s[j])
                    j += 1
            
            tmp.extend(s[i: mid + 1])
            tmp.extend(s[j: right + 1])

            for index in range(left, right + 1):
                s[index] = tmp[index - left]
            return tot

        return calc(0, len(s) - 1, s)
''',
    call='Solution().countRatioSubarrays([1, 2, 1], 3, 2)',
    expect=5,
    views=[
        dict(type='text', size=26, h=70, fn=_info),
        dict(type='array', var='s', label='s（前缀和；框 = 当前 calc 区间，蓝 = i，粉 = j）', cell=84, h=190,
             pointers={_I: 'blue', _J: 'pink'}, pointer_labels={_I: 'i', _J: 'j'},
             window=(_L, _R),
             dim=lambda S, k, v: S['_inner'].get('left') is not None and not (S['_inner']['left'] <= k <= S['_inner']['right'])),
        dict(type='array', var=lambda S: S['_inner'].get('tmp', []), label='tmp（合并后的有序结果）', cell=84, h=150),
        dict(type='calls', h=210, hide=('s',)),
    ],
    watch=[('left', _L, 'blue'), ('right', _R, 'pink'), ('mid', _M, 'cyan'), ('tot', lambda S: S['_inner'].get('tot'), 'green')],
    skip=['tmp = []', 'def calc', 'for index in range', 's[index] = tmp', 'return 0'],
    max_steps=75,
    captions={
        's = [0]': '`s` 是前缀和数组，`s[0] = 0`（空前缀）',
        'for v in nums': '取 `v = {v}`',
        'if v % 2 == 0': lambda S, B, ret: (f'`{S.v}` 是==偶数== → 替换成 `-b = {-S.b}`' if S.v % 2 == 0 else f'`{S.v}` 是==奇数== → 替换成 `+a = {S.a}`'),
        's.append(s[-1] - b)': '偶数记 `-b`：`s` 新增 `{s[-1]}`，`s = {s}`',
        's.append(s[-1] + a)': '奇数记 `+a`：`s` 新增 `{s[-1]}`，`s = {s}`',
        'return calc(0': '前缀和 `s = {s}`：数「左边的 <= 右边的」的下标对 = 有效子数组数；用归并排序来数',
        'if left == right': lambda S, B, ret: (f'区间 `[{S.left}, {S.right}]` 只剩一个数，没有对 → 返回 `0`' if S.left == S.right
                                              else f'区间 `[{S.left}, {S.right}]` 有 {S.right - S.left + 1} 个数，继续对半拆'),
        'return 0': '一个数没有对 → 返回 `0`',
        'mid = (left + right) // 2': '从中间拆开：`mid = {mid}`，左半 `[{left}..{mid}]`，右半 `[{mid + 1}..{right}]`',
        'tot = calc(left, mid, s)': '先递归处理左半、右半（各自排好序，并数出各自内部的有效对）',
        'i, j = left, mid + 1': '`i` 扫左半、`j` 扫右半，两边都已经有序；`tmp` 收集合并结果',
        'while i <= mid and j <= right': lambda S, B, ret: (f'`i = {S.i} <= {S.mid}` 且 `j = {S.j} <= {S.right}`：两半都还有数' if S.i <= S.mid and S.j <= S.right
                                                            else '有一半取完了：不再需要比较'),
        'if s[i] <= s[j]': _cmp,
        'tot += right - j + 1': '`tot` += `{right} - {j} + 1 = {right - j + 1}` → `{tot}`',
        'tmp.append(s[i])': '`s[{i}] = {s[i]}` 放进 `tmp` → `{tmp}`',
        'i += 1': '`i` → {i}',
        'tmp.append(s[j])': '`s[{j}] = {s[j]}` 放进 `tmp` → `{tmp}`',
        'j += 1': '`j` → {j}',
        'tmp.extend(s[i: mid + 1])': lambda S, B, ret: (f'左半剩下 `{S.s[S.i:S.mid + 1]}`：比右半的数都大，没有新的对，直接接到 `tmp` → `{S.tmp}`' if S.i <= S.mid
                                                        else '左半没有剩余'),
        'tmp.extend(s[j: right + 1])': lambda S, B, ret: (f'右半剩下 `{S.s[S.j:S.right + 1]}` 接到 `tmp` 后面（它们的对已算过）→ `{S.tmp}`' if S.j <= S.right
                                                          else '右半没有剩余，`tmp` 已是 `{S.tmp}` ，写回 `s` 后区间有序'),
        'return tot': lambda S, B, ret: f'`calc({S.left}, {S.right})` 完成：区间已排好序（写回 `s`），共 `{ret}` 对',
    },
    cards=dict(
        one_liner='偶数 −b、奇数 +a，有效子数组 = 前缀和的非逆序对',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`x` = 子数组偶数个数，`y` = 奇数个数；有效：`y > 0` 且 `x / y <= a / b`',
                 '求 `nums` 中有效子数组的个数',
                 '示例：`nums = [1,2,1,2], a = 3, b = 2` → `7`',
                 '本视频：`nums = [1,2,1], a = 3, b = 2` → `5`，前缀和 `s = [0,3,1,4]`'],
        quote='将其通分后可得bx <= ay时数组有效。……将nums中的所有偶数都替换为-b，所有奇数都替换为a，那么对于一个拥有x个偶数以及y个奇数的子数组，其子数组之和恰好就是ay - bx。',
        quote_src='—— yiduobo 题解原文',
        idea=['`x/y <= a/b` 通分成 `b·x <= a·y`，`y = 0` 时自动不成立，不用单独判',
              '偶数记 `-b`、奇数记 `+a`：子数组和 `a·y − b·x >= 0` 就有效',
              '前缀和 `s`：数有多少下标对 `i < j` 满足 `s[i] <= s[j]` ——归并排序时顺便数'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（`n` 为 `nums` 长度）',
                 '合并时若 `s[i] <= s[j]`：右半 `j..right` 都 >= `s[i]`，一次加 `right - j + 1`',
                 '数的是==非逆序对==（`<=` 含相等），不是普通逆序对',
                 '原文为 Python 2 风格（`class Solution(object)`、整数除法已用 `//`），无需修改即可运行',
                 '同系列 4013（II）数据范围更大，同样用这个做法'],
    ),
)
