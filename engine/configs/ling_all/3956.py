def _txt(S):
    q, f, s, j = S.get('q'), S.get('f'), S.get('s'), S.get('j')
    if q is None or j is None or not q or S.get('_line') not in (20, 21, 22, 23, 24, 25):
        return '`f[L] − s[L]` 最大的左端点 L 放在队首；`nf[j] = max(不选, f[L] − s[L] + s[j])`'
    L = q[0]
    return f"队首 `L = {L}`：`f[{L}] − s[{L}] + s[{j}] = {f[L]} − {s[L]} + {s[j]}` = =={f[L] - s[L] + s[j]}=="


def _upd(S, B, r):
    j, q, f, s = S.j, S.q, S.f, S.s
    pick = f[q[0]] - s[q[0]] + s[j]
    return f'不选 `nums[{j - 1}]`：`nf[{j - 1}] = {S.nf[j - 1]}`；选一个以它结尾的：`{pick}` → `nf[{j}] =` =={S.nf[j]}=='


def _ncol(S, k, v):
    if S.get('_line') in (21, 22, 23, 24) and k == S.get('j'):
        return 'yellow'
    return None


CONFIG = dict(
    num=3956, title='M 个非重叠子数组最大和 I', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP + 单调队列（滑动窗口最大值）',
    tags=['灵神题单·动态规划', '难度分 2061'],
    code='''
class Solution:
    def maximumSum(self, nums: List[int], m: int, left: int, right: int) -> int:
        n = len(nums)
        s = list(accumulate(nums, initial=0))  # nums 的前缀和
        f = [0] * (n + 1)
        ans = -inf

        for i in range(1, m + 1):
            nf = [-inf] * (n + 1)
            q = deque()

            # 前 i 个子数组至少占用了 i * left 个位置
            for j in range(i * left, n + 1):
                # 1. 入
                k = j - left
                v = f[k] - s[k]
                while q and f[q[-1]] - s[q[-1]] <= v:
                    q.pop()
                q.append(k)

                # 2. 更新
                # 不选 nums[j-1] vs 选一个以 j-1 结尾的子数组
                nf[j] = max(nf[j - 1], f[q[0]] - s[q[0]] + s[j])

                # 3. 出，下一轮循环队首离开窗口
                if q[0] <= j - right:
                    q.popleft()

            f = nf
            ans = max(ans, f[n])

        return ans
''',
    call='Solution().maximumSum([4,1,-5,2], 2, 1, 2)',
    expect=7,
    views=[
        dict(type='array', var='nums', label='nums', h=100, cell=70, index=False),
        dict(type='array', var='s', label='s（前缀和）', h=110, cell=70),
        dict(type='array', var='f', label='f（上一轮：恰好选 i-1 个）', h=110, cell=70),
        dict(type='array', var='nf', label='nf（这一轮：恰好选 i 个）', h=160, cell=70, pointers={'j': 'blue'}, color=_ncol),
        dict(type='queue', var='q', label='q（候选左端点 L，f[L]−s[L] 递减）', h=120),
        dict(type='text', fn=_txt, size=24, h=50),
    ],
    watch=[('i', 'i', 'purple'), ('j', 'j', 'blue'), ('k', 'k', 'cyan'), ('ans', 'ans', 'green')],
    skip=['n = len', 'f = [0] * (n + 1)', 'f = nf', 'ans = -inf', 'nf = [-inf]', 'q = deque()'],
    captions={
        's = list(accumulate': '`s` 是前缀和：子数组 `[L, j-1]` 的和 = `s[j] − s[L]`',
        'for i in range': lambda S, B, r: (f'开始算 ==恰好选 {S.i} 个==子数组的 `nf`；`q` 清空' if S.get('i') != B.get('i') else '轮次都做完了'),
        'for j in range': lambda S, B, r: (f'`j = {S.j}`：考虑前 {S.j} 个数（下标到 {S.j - 1}）' if S.get('j') != B.get('j') or S.get('i') != B.get('i') else '这一轮结束'),
        'k = j - left': '最短子数组长 `left`，新的左端点候选 `L = j − left = {k}`',
        'v = f[k] - s[k]': '把和 `j` 无关的 `s[j]` 提出来：比较 `f[L] − s[L]`，这里 `v = {f[k]} − {s[k]}` = =={v}==',
        'while q and f[q[-1]]': lambda S, B, r: (
            f'队尾 `f[{S.q[-1]}] − s[{S.q[-1]}] = {S.f[S.q[-1]] - S.s[S.q[-1]]} ≤ v = {S.v}`：更早、又不更大 → ==弹出=='
            if S.q and S.f[S.q[-1]] - S.s[S.q[-1]] <= S.v
            else ('队列空了' if not S.q else f'队尾 {S.f[S.q[-1]] - S.s[S.q[-1]]} > v = {S.v}：保留')),
        'q.pop()': '弹出队尾：`q = {list(q)}`',
        'q.append(k)': '`L = {k}` 入队：`q = {list(q)}`',
        'nf[j] = max': _upd,
        'if q[0] <= j - right': lambda S, B, r: (
            f'队首 `L = {S.q[0]} ≤ j − right = {S.j - S.right}`：子数组长度会超过 right → ==出队=='
            if S.q[0] <= S.j - S.right else f'队首 `L = {S.q[0]}` > `j − right = {S.j - S.right}`：还在窗口内'),
        'q.popleft()': '队首离开窗口：`q = {list(q)}`',
        'ans = max': '`f` 换成 `nf`：恰好选 `{i}` 个的最大和 `f[n] = {f[n]}`，`ans` → =={ans}==',
        'return ans': '枚举了恰好选 1…m 个，取最大：=={ret}==',
    },
    cards=dict(
        one_liner='恰好选 i 个子数组，左端点用单调队列取最优',
        complexity='时间 `O(nm)`，空间 `O(n)`',
        problem=['在 `nums` 中选至少 1 个、至多 `m` 个互不重叠的子数组',
                 '每个子数组长度在 `[left, right]` 内，总和最大',
                 '示例：`[4,1,-5,2]`，`m=2`，`left=1`，`right=2` → `7`（`[4,1]` 和 `[2]`）'],
        quote='设 nums 的前缀和数组为 s，子数组 [L,j-1] 的元素和可以表示为 s[j] − s[L]。……这是一个标准的滑动窗口最大值问题。',
        quote_src='—— 灵茶山艾府题解',
        idea=['定义 `f[i][j]`：前 `j` 个数里选==恰好== `i` 个子数组的最大和；「恰好」方便处理「至少一个」',
              '最后一步：不选 `nums[j-1]`，或枚举左端点 `L ∈ [j-right, j-left]`',
              '`s[j] + max(f[L] − s[L])`，窗口随 `j` 右移 → 单调队列，三步：==入、更新、出=='],
        summary=['时间 `O(nm)`：每轮 `i` 里每个下标入队出队各至多一次',
                 '空间 `O(n)`：只保留上一轮 `f` 和这一轮 `nf`',
                 '易错：`j` 从 `i*left` 开始；先入队、再更新、最后出队',
                 '灵神也给了二维 `f[i][j]` 的写法，思路相同；还有 WQS 二分的更快做法（见 3957）'],
    ),
)
