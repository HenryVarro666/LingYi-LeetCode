def _win(S):
    if 'r' in S and 'l' in S and S['l'] <= S['r']:
        return f"窗口 `arr[{S['l']}..{S['r']}]`，和 `s = {S['s']}`，目标 `{S['target']}`"
    return '滑动窗口：右端点 `r` 往右走，和超了就收缩左端点 `l`'


CONFIG = dict(
    num=1477, title='找两个和为目标值且不重叠的子数组', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='滑动窗口 + 前后缀分解（枚举右，维护左）',
    tags=['灵神题单·动态规划', '难度分 1851'],
    code='''
class Solution:
    def minSumOfLengths(self, arr: List[int], target: int) -> int:
        n = len(arr)
        ans = inf
        # pre_min[i] 表示右端点 < i 的和为 target 的最短子数组长度（不存在则为 inf）
        pre_min = [inf] * (n + 1)
        min_len = inf
        s = l = 0

        for r, x in enumerate(arr):
            s += x
            while s > target:
                s -= arr[l]
                l += 1
            if s == target:
                # 枚举第二个子数组的右端点为 r，用滑动窗口算出此时第二个子数组的左端点为 l
                # 那么第一个子数组的右端点必须 < l
                ans = min(ans, pre_min[l] + r - l + 1)
                min_len = min(min_len, r - l + 1)  # 维护遍历过的和为 target 的子数组的最短长度
            pre_min[r + 1] = min_len  # 保存此时此刻的 min_len

        return -1 if ans == inf else ans
''',
    call='Solution().minSumOfLengths([3,1,1,4,1,2,1], 3)',
    expect=3,
    views=[
        dict(type='array', var='arr', label='arr（蓝框 = 当前窗口 [l, r]）', h=190, cell=76,
             pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r')),
        dict(type='array', var='pre_min', label='pre_min[i]：右端点 < i 的最短合法子数组（inf = 无）', h=190, cell=70,
             color=lambda S, i, v: 'yellow' if S.get('_line') in (18,) and i == S.get('l') else None),
        dict(type='text', fn=_win, size=26, h=80),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), 's', ('min_len', 'min_len', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'pre_min = [inf]': '`pre_min[i]`：只看 `arr[0..i-1]`，和为 target 的最短子数组长度；一开始全是 `inf`',
        'for r, x in enumerate(arr)': lambda S, B, ret: ('所有右端点都枚举完了，循环结束' if B.get('r') == S.r else f'枚举第二个子数组的==右端点== `r = {S.r}`，加入 `{S.x}`'),
        's += x': '窗口和 `s` += `{x}` → =={s}==',
        'while s > target': '`s = {s}` {"> target，太大，需要收缩左端点" if s > target else "<= target，不用收缩"}（`target = {target}`）',
        's -= arr[l]': '丢掉左端点 `arr[{B.l}] = {arr[B.l]}`：`s` → {s}',
        'l += 1': '`l` → {l}',
        'if s == target': '`s = {s}`，`target = {target}`：{"恰好相等，窗口 [l, r] 是一个合法子数组" if s == target else "不相等，这个右端点没有合法子数组"}',
        'ans = min': '另一个子数组必须在 `l` 之前：`pre_min[{l}] = {pre_min[l]}`，这个窗口长 `{r - l + 1}` → `ans` = =={ans}==',
        'min_len = min': '把这个窗口也纳入“遍历过的最短长度”：`min_len` = =={min_len}==',
        'pre_min[r + 1] = min_len': '`pre_min[{r+1}] = {min_len}`：之后右端点 `> {r}` 的子数组，都可以用它',
        'return -1 if': '`ans` {"仍是 inf，找不到" if ans == inf else "= " + str(ans)} → ==返回 {ret}==',
    },
    cards=dict(
        one_liner='枚举第二个子数组的右端点，第一个子数组的最短长度边走边存',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组 `arr` 全是正数，在其中找两个==不重叠==的子数组，和都等于 `target`',
                 '返回两个子数组长度和的最小值，找不到返回 `-1`',
                 '示例：`[3,1,1,4,1,2,1], target = 3` → `3`（`[3]` + `[1,2]`）'],
        quote='用滑动窗口枚举第二个子数组 [l, r]，我们需要知道右端点 < l 的最短子数组的长度 preMin[l]。……preMin[l] 可以在滑动窗口的同时维护。',
        quote_src='—— 灵茶山艾府题解（方法二：枚举右维护左）',
        idea=['数组全是正数 → 滑动窗口能 `O(n)` 找出所有和恰为 `target` 的窗口',
              '窗口右端点 `r` 往右走，同时存下“`r+1` 之前”的最短长度 `pre_min[r+1]`',
              '窗口 `[l, r]` 命中时：`pre_min[l]` + 窗口长度，就是以它为第二段的最优答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`pre_min[l]` 取的是右端点 `< l` 的，保证不重叠',
                 '易错：`pre_min[r+1] = min_len` 要在命中判断之后写，每个 `r` 都要写',
                 '灵神方法一是倒着滑一遍预处理 `suf_min`，再正着滑一遍（前后缀分解），本视频演示的是方法二',
                 '思考题：有负数时滑窗失效，要改用前缀和 + 哈希表'],
    ),
)
