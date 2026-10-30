def _cur(S):
    return S['a'] if 'a' in S else S.get('nums')


def _fview(S):
    if 'a' in S:
        return S['f']
    return S.get('pre')


def _expl(S):
    if 'x' not in S or 'y' not in S or 'z' not in S or 'i' not in S or 'f' in S and 'a' in S:
        return '先算 `pre`（以 i 结尾）和 `suf`（以 i 开头）的最长交替长度，再枚举删除 `nums[i]`'
    sg = {1: '大于', -1: '小于', 0: '等于'}
    return (f"删 `nums[{S['i']}]`：`x`=(i-2,i-1) {sg[S['x']]}，`y`=(i-1,i+1) {sg[S['y']]}，`z`=(i+1,i+2) {sg[S['z']]}"
            f"　交替要求 `x == -y` 且 `z == -y`")


CONFIG = dict(
    num=3830, title='移除至多一个元素后的最长交替子数组', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='前后缀分解',
    tags=['动态规划', '难度分 2162'],
    code='''
class Solution:
    def calc(self, a: List[int]) -> List[int]:
        f = [0] * len(a)  # f[i] 表示以 i 结尾的最长交替子数组的长度
        for i, x in enumerate(a):
            if i == 0 or a[i - 1] == x:
                f[i] = 1
            elif i > 1 and a[i - 2] != a[i - 1] and (a[i - 2] < a[i - 1]) == (a[i - 1] > x):
                f[i] = f[i - 1] + 1
            else:
                f[i] = 2
        return f

    def longestAlternating(self, nums: List[int]) -> int:
        n = len(nums)
        pre = self.calc(nums)  # pre[i] 表示以 i 结尾的最长交替子数组的长度
        suf = self.calc(nums[::-1])[::-1]  # suf[i] 表示以 i 开头的最长交替子数组的长度

        # 不删除元素时的最长交替子数组的长度
        ans = max(pre)

        # 枚举删除 nums[i]
        for i in range(1, n - 1):
            if nums[i - 1] == nums[i + 1]:  # 无法拼接
                continue

            # 计算 (i-2,i-1), (i-1,i+1), (i+1,i+2) 的大小关系
            x = (nums[i - 2] > nums[i - 1]) - (nums[i - 2] < nums[i - 1]) if i > 1 else 0
            y = (nums[i - 1] > nums[i + 1]) - (nums[i - 1] < nums[i + 1])
            z = (nums[i + 1] > nums[i + 2]) - (nums[i + 1] < nums[i + 2]) if i < n - 2 else 0

            if x == -y and x == z:  # 左右两边可以拼接
                ans = max(ans, pre[i - 1] + suf[i + 1])
            else:
                if x == -y:
                    ans = max(ans, pre[i - 1] + 1)  # 只拼接 nums[i+1]
                if z == -y:
                    ans = max(ans, suf[i + 1] + 1)  # 只拼接 nums[i-1]

        return ans
''',
    call='Solution().longestAlternating([1,3,2,2,4])',
    expect=4,
    views=[
        dict(type='array', var=_cur, label='数组', h=170, pointers={'i': 'blue'},
             color=lambda S, k, v: 'orange' if 'a' not in S and S.get('i') == k and 'x' in S else (
                 'pink' if 'a' not in S and 'x' in S and k in (S['i'] - 1, S['i'] + 1) else None)),
        dict(type='array', var=_fview, label='f / pre', h=150, color=lambda S, k, v: 'green' if 'a' in S and k == S.get('i') else None),
        dict(type='array', var='suf', label='suf', h=150),
        dict(type='text', fn=_expl, size=24, h=90),
    ],
    watch=[('i', 'i', 'blue'), 'x', 'y', 'z', ('ans', 'ans', 'green')],
    max_steps=90,
    skip=['n = len(nums)', 'x = (', 'y = ('],
    captions={
        'f = [0]': '`f[i]`：以 `i` 结尾的最长交替子数组长度，先全填 0',
        'f[i] = 1': '第一个数，或与前一个相等：只能自己单独一段 → `f[{i}] = 1`',
        'f[i] = f[i - 1] + 1': '`a[i-2] < a[i-1] > a[i]`（或反过来）成立：能接在 `{i-1}` 结尾的交替段后面 → `f[{i}] = f[{i-1}] + 1 = {f[i]}`',
        'f[i] = 2': '与前一个不等但接不上上一段：从 `i-1` 重新起一段 → `f[{i}] = 2`',
        'pre = self.calc': '先算 `pre`：对 `nums` 调用 `calc`，得到以每个 i 结尾的最长交替长度',
        'suf = self.calc': '再算 `suf`：把数组反转，算完再反转回来，就是以每个 i 开头的最长交替长度',
        'ans = max(pre)': '先考虑不删元素：`max(pre)` = =={ans}==',
        'if nums[i - 1] == nums[i + 1]': lambda S, B, ret: (f"删掉 `nums[{S['i']}]` 后左右两个数都是 {S['nums'][S['i']-1]}，相等无法拼接，跳过" if S['nums'][S['i']-1] == S['nums'][S['i']+1] else f"删掉 `nums[{S['i']}]` 后左右是 `{S['nums'][S['i']-1]}` 和 `{S['nums'][S['i']+1]}`，不相等，有可能拼起来"),
        'z = (': '算三个大小关系（1 大于，-1 小于，越界记 0）：`x`=(i-2,i-1) → {x}，`y`=(i-1,i+1) → {y}，`z`=(i+1,i+2) → {z}',
        'if x == -y and x == z': lambda S, B, ret: (f"`x={S['x']}`、`z={S['z']}` 都与 `y={S['y']}` 相反：两侧能拼成 ==一整段==" if S['x'] == -S['y'] and S['x'] == S['z'] else f"`x={S['x']}, y={S['y']}, z={S['z']}`：两侧不能同时接上，只看单侧"),
        'ans = max(ans, pre[i - 1] + suf[i + 1])': '两侧拼接：`{pre[i-1]} + {suf[i+1]} = {pre[i-1] + suf[i+1]}`，`ans` → =={ans}==',
        'if x == -y:': '只有左边能和 `nums[{i+1}]` 接上？`x == -y` → {x == -y}',
        'ans = max(ans, pre[i - 1] + 1)': '只拼接 `nums[i+1]`：`pre[{i-1}] + 1 = {pre[i-1] + 1}`，`ans` → =={ans}==',
        'if z == -y:': '只有右边能和 `nums[{i-1}]` 接上？`z == -y` → {z == -y}',
        'ans = max(ans, suf[i + 1] + 1)': '只拼接 `nums[i-1]`：`suf[{i+1}] + 1 = {suf[i+1] + 1}`，`ans` → =={ans}==',
    },
    cards=dict(
        one_liner='删 a[i]：左边以 i-1 结尾的一段 + 右边以 i+1 开头的一段',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['交替子数组：相邻元素 ==严格大于、严格小于交替==，长度 1 也算',
                 '可以从 `nums` 里最多删掉一个元素，再选一个交替子数组，求最长长度',
                 '示例：`[1,3,2,2,4]` → 删掉一个 `2` 后得到 `[1,3,2,4]`，答案 `4`'],
        quote='假设删除的是 a[i]，我们需要知道什么？以 i-1 结尾的最长交替子数组的长度，记作 pre[i-1]。以 i+1 开头的最长交替子数组的长度，记作 suf[i+1]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先递推算出 `pre`、`suf`：接得上就 +1，接不上从 2 或 1 重新开始',
              '枚举删除 `nums[i]`：用 `x, y, z` 三个大小关系判断两侧能否拼接',
              '都能拼：`pre[i-1] + suf[i+1]`；只有一侧能接：那一侧长度 + 1'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：`i-2`、`i+2` 越界时 `x`、`z` 取 0，且 `nums[i-1] == nums[i+1]` 必须先跳过',
                 '只一侧能拼时，答案是那一侧长度加 1（删掉后新接上的那个数）',
                 '题解还给了分组循环 O(1) 空间写法和状态机 DP 写法'],
    ),
)
