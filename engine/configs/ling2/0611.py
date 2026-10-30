def _live(S):
    return all(x in S for x in ('i', 'j', 'k', 'c')) and S['i'] < S['j'] < S['k']


def _color(S, idx, v):
    if 'k' not in S:
        return None
    if idx == S['k']:
        return 'orange'
    if S.get('_line') == 16 and _live(S) and S['i'] <= idx < S['j']:
        return 'green'  # nums[i..j-1] 都能和 nums[j] 配对
    if S.get('_line') in (7, 8) and S['nums'][0] + S['nums'][1] > S['c'] and idx <= S['k']:
        return 'green'  # 优化一：前 k+1 个数任选三个都合法
    if S.get('_line') == 10 and idx in (S['k'] - 2, S['k'] - 1):
        return 'red'
    return None


def _formula(S):
    if not _live(S):
        if 'k' in S:
            return f"最长边 `c = nums[{S['k']}] = {S['nums'][S['k']]}`：在它左边找 `a + b > c` 的 (a, b)"
        return '规定 `a ≤ b ≤ c`，只需检查 ==a + b > c=='
    a, b, c = S['nums'][S['i']], S['nums'][S['j']], S['c']
    rel = '>' if a + b > c else '≤'
    return f"`a + b = {a} + {b} = {a + b}` {rel} `c = {c}`" + (' → ==合法==' if a + b > c else ' → 不合法')


def _opt1(S, B, ret):
    a, b, c = S.nums[0], S.nums[1], S.c
    if a + b > c:
        return f'优化一：最小的两边 `{a} + {b} = {a + b} > c = {c}` → ==前 k+1 个数任选三个都能组成三角形=='
    return f'优化一：最小的两边 `{a} + {b} = {a + b} ≤ c = {c}`，不满足'


def _opt2(S, B, ret):
    k = S.k
    a, b, c = S.nums[k - 2], S.nums[k - 1], S.c
    if a + b <= c:
        return f'优化二：最大的两边 `{a} + {b} = {a + b} ≤ c = {c}` → ==不可能有 a + b > c==，跳过双指针'
    return f'优化二：最大的两边 `{a} + {b} = {a + b} > c = {c}`，可能有解 → 执行双指针'


def _cmp(S, B, ret):
    a, b, c = S.nums[S.i], S.nums[S.j], S.c
    if a + b > c:
        return f'`nums[{S.i}] + nums[{S.j}] = {a} + {b} = {a + b} > {c}` → 成立'
    return f'`nums[{S.i}] + nums[{S.j}] = {a} + {b} = {a + b} ≤ {c}` → 不成立'


CONFIG = dict(
    num=611, title='有效三角形的个数', difficulty='Medium', category='双指针',
    author='灵茶山艾府', technique='枚举最长边 + 相向双指针',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def triangleNumber(self, nums: List[int]) -> int:
        nums.sort()
        ans = 0
        for k in range(len(nums) - 1, 1, -1):
            c = nums[k]
            if nums[0] + nums[1] > c:  # 优化一
                ans += (k + 1) * k * (k - 1) // 6
                break
            if nums[k - 2] + nums[k - 1] <= c:  # 优化二
                continue
            i = 0  # a=nums[i]
            j = k - 1  # b=nums[j]
            while i < j:
                if nums[i] + nums[j] > c:
                    ans += j - i
                    j -= 1
                else:
                    i += 1
        return ans
''',
    call='Solution().triangleNumber([4, 2, 9, 3, 7, 2])',
    expect=5,
    skip=['c = nums[k]'],
    views=[
        dict(type='text', h=70, size=28, fn=_formula),
        dict(type='array', var='nums', h=360, cell=120, label='nums（排序后；橙 = 最长边 c，灰 = 已枚举过的 c）',
             pointers={'i if i < j else None': 'blue', 'j if i < j else None': 'pink', 'k': 'orange'},
             pointer_labels={'i if i < j else None': 'i', 'j if i < j else None': 'j', 'k': 'k'},
             color=_color, dim=lambda S, idx, v: 'k' in S and idx > S['k']),
    ],
    watch=[('k', 'k', 'orange'), ('c', 'nums[k]', 'orange'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'nums.sort()': '先排序：规定 ==a ≤ b ≤ c==，三元组就不会重复统计，也能用双指针',
        'ans = 0': '只需检查 `a + b > c`：另外两个不等式在 `a ≤ b ≤ c` 时必然成立',
        'for k in range': '==倒序==枚举最长边 `c = nums[{k}] = {nums[k]}`',
        'if nums[0] + nums[1] > c': _opt1,
        'ans += (k + 1)': '直接加上 `C({k + 1}, 3) = {k + 1}·{k}·{k - 1} / 6 = {(k + 1) * k * (k - 1) // 6}` → `ans = {ans}`',
        'break': '更小的 c 的方案也都在这 `C(k+1, 3)` 里 → ==退出外层循环==（这就是倒序枚举的原因）',
        'if nums[k - 2] + nums[k - 1] <= c': _opt2,
        'continue': '`c = {c}` 没有合法的 (a, b)，看下一个 c',
        'i = 0': '`a = nums[i]`：左指针从最小的数开始',
        'j = k - 1': '`b = nums[j]`：右指针从 c 左边的数开始',
        'while i < j': lambda S, B, r: ('`i < j`，继续找' if S.i < S.j else f'`i = {S.i}`，`j = {S.j}` 相遇：`c = {S.c}` 统计完'),
        'if nums[i] + nums[j] > c': _cmp,
        'ans += j - i': '数组有序：`nums[{i}..{j - 1}]` 和 `nums[{j}]` 相加都 > c → 一次加 `j − i = {j - i}`，`ans = {ans}`',
        'j -= 1': '`b = nums[{j + 1}]` 的方案全部统计完 → `j` 左移到 {j}',
        'i += 1': '`nums[{i - 1}]` 和后面任何 b 相加都 ≤ c，==没用了== → `i` 右移到 {i}',
        'return ans': '一共 `{ret}` 个有效三角形',
    },
    cards=dict(
        one_liner='排序后枚举最长边 c，相向双指针找 a + b > c',
        complexity='时间 `O(n²)`，空间 `O(1)`（忽略排序栈开销）',
        problem=['给定非负整数数组 `nums`，返回能组成三角形三条边的三元组个数',
                 '同一组下标只算一次：`(2,3,4)` 和 `(4,3,2)` 算同一个',
                 '示例：`[2,2,3,4]` → `3`；本视频：`[4,2,9,3,7,2]` → `5`'],
        quote='如果 nums[i]+nums[j] > c，由于数组是有序的，nums[j] 与下标 i′ 在 [i,j−1] 中的任何 nums[i′] 相加，都是 >c 的，因此直接找到了 j−i 个合法方案。',
        quote_src='—— 灵茶山艾府题解「方法一：枚举最长边 + 相向双指针」',
        idea=['规定 `a ≤ b ≤ c`：只需满足 ==a + b > c==，另两个不等式自动成立',
              '外层枚举 `c = nums[k]`，内层 `i = 0, j = k − 1` 相向而行',
              '`> c` 就把 `j − i` 个一起算上再左移 j；`≤ c` 说明 `nums[i]` 太小，右移 i'],
        summary=['时间 `O(n²)`：每个 c 双指针 `O(n)`；空间 `O(1)`',
                 '优化一：`nums[0] + nums[1] > c` 时直接加 `C(k+1, 3)` 并 break，所以要==倒序枚举 k==',
                 '优化二：`nums[k−2] + nums[k−1] ≤ c` 时跳过这个 c',
                 '易错：`ans += j − i` 而不是 `+1`；0 不能当边，`a + b > c` 会自动排除它',
                 '题解另有：枚举最短边 + 同向双指针、值域 FFT 卷积'],
    ),
)
