def _top(S):
    ln = S.get('_line') or 0
    if ln < 24:
        return f'阈值 `threshold = {S.get("threshold", "?")}`：`k` 大的暴力改，`k` 小的按 `(k, left % k)` 分组'
    if ln < 31:
        return '预处理 `1..max_v` 的逆元（线性递推），后面“除以 v”要用'
    if ln < 56:
        return f'分组 `{S.get("key")}`：下标 `{S.get("r", "?")}, +k, …` 是一条链，在链上做乘法差分'
    return '最后一趟异或所有元素'


CONFIG = dict(
    num=3655, title='区间乘法查询后的异或 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='按 (k, l%k) 分组 · 乘法差分',
    tags=['常用数据结构', '难度分 2454'],
    code='''
class Solution(object):
    def xorAfterQueries(self, nums, queries):
        
        f = {}
        n = len(nums)
        mod = 10 ** 9 + 7

        max_v = 0
        q_dict = {}
        max_r = {}
        threshold = int(n ** 0.5)
        for left, right, k, v in queries:
            if k >= threshold:
                for index in range(left, right + 1, k):
                    nums[index] *= v
                    nums[index] %= mod
            else:
                key = (k, left % k)
                if key not in q_dict:
                    q_dict[key] = []
                    max_r[key] = 0
                right = (right - left % k) // k
                left //= k
                max_r[key] = max(max_r[key], right)
                q_dict[key].append((left, right, v))
                max_v = max(max_v, v)

        fac = [1, 1]
        inv = [None, 1]
        for v in range(2, max_v + 1):
            fac.append(fac[-1] * v % mod)
            inv.append(-(mod // v) * inv[mod % v] % mod)

        now_key = None
        for key in q_dict:
            k, r = key
            f = [1] * (max_r[key] + 1)
            for left, right, v in q_dict[key]:
                f[left] *= v
                f[left] %= mod
                if right + 1 <= max_r[key]:
                    f[right + 1] *= inv[v]
                    f[right + 1] %= mod

            now = r
            v = 1
            for index in range(max_r[key] + 1):
                v *= f[index]
                v %= mod
                nums[now] *= v
                nums[now] %= mod
                now += k

        res = 0
        for v in nums:
            res ^= v
        return res
''',
    call='Solution().xorAfterQueries([1,2,3,4,5,6], [[1,4,1,3],[2,5,3,2],[0,2,1,2],[0,2,1,5],[3,5,2,4],[1,3,1,7]])',
    expect=1069,
    views=[
        dict(type='text', fn=_top, size=23, h=80),
        dict(type='array', var='nums', pointers={'now': 'pink'}, label='nums（模 10^9+7）', cell=100, h=190),
        dict(type='array', var='f', color=lambda S, i, v: 'blue' if 47 <= (S.get('_line') or 0) < 54 and i == S.get('index') else None, label='f（乘法差分：初值 1，起点乘 v，终点后一格乘逆元）', cell=100, h=190),
        dict(type='map', var='q_dict', fmt=lambda k, v: f'{k} → {v}', h=150),
    ],
    watch=[('threshold', 'threshold', 'orange'), ('key', 'key', 'yellow'), ('now', 'now', 'pink'), ('v', 'v', 'green')],
    skip=['f = {}', 'mod = 10 **', 'now_key = None', 'max_v = 0', 'q_dict = {}', 'max_r = {}', 'fac = [1, 1]',
          'fac.append', 'max_r[key] = max(', 'q_dict[key] = []', 'max_r[key] = 0', 'now += k', 'for left, right, k, v in queries',
          'for v in range(2', 'inv.append', 'for key in q_dict', 'max_v = max(max_v, v)', 'if key not in q_dict',
          'nums[index] *= v', 'f[left] *= v', 'f[right + 1] *= inv[v]', 'v *= f[index]', 'nums[now] *= v', 'for v in nums', 'for index in range(max_r', 'left //= k', 'right = (right - left', 'for index in range(left'],
    max_steps=90,
    captions={
        'n = len(nums)': '`n = {n}`',
        'threshold = int': '阈值 `threshold = int(√{n}) = {threshold}`：步长 `k ≥ threshold` 时每个询问最多改 `n/k` 个下标，直接暴力',
        'if k >= threshold': lambda S, B, r: (f'询问 `[{S.left},{S.right},{S.k},{S.v}]`：`k = {S.k} ≥ {S.threshold}` → 暴力' if S.k >= S.threshold else f'询问 `[{S.left},{S.right},{S.k},{S.v}]`：`k = {S.k} < {S.threshold}` → 分组做乘法差分'),
        'nums[index] %= mod': '暴力：`nums[{index}]` 乘 `{v}` 再取模 → =={nums[index]}==',
        'key = (k, left % k)': '修改的下标模 `k` 都等于 `left % k`：用 `(k, left % k)` = `{key}` 当分组 key，同组下标连成一条链',
        'q_dict[key].append': '记入分组 `{key}`：链上起点 `left//k = {left}`，终点 `(right − left%k)//k = {right}`，乘数 `{v}`',
        'inv = [None, 1]': '预处理逆元表 `inv[1..{max_v}]`（线性递推）：后面“除以 v”要乘 `inv[v]`',
        'k, r = key': '处理分组 `{key}`：步长 `k = {k}`，链从下标 `{r}` 开始',
        'f = [1] *': '`f` 长度 `max_r + 1 = {max_r[key]+1}`，全是 ==1==（乘法单位元，相当于差分数组）',
        'f[left] %= mod': '链上起点 `{left}` 处乘 `{v}`：`f[{left}]` → =={f[left]}==',
        'if right + 1 <= max_r': lambda S, B, r: (f'终点后一格 `{S.right+1}` 还在链内 → 需要撤销' if S.right + 1 <= S.max_r[S.key] else f'终点后一格 `{S.right+1}` 已越过链尾 → 不用撤销'),
        'f[right + 1] %= mod': '终点后一格乘 `{v}` 的逆元 `inv[{v}]`（相当于“除以 {v}”）：`f[{right+1}] = {f[right+1]}`',
        'now = r': '`now` 是链上当前位置对应的真实下标，从 `{r}` 开始',
        'v = 1': '`v` 记录 `f` 的前缀积，从 1 开始',
        'v %= mod': '前缀积 `v = {v}`：链上第 `{index}` 个位置要乘的总倍数',
        'nums[now] %= mod': '`nums[{now}]` 乘 `v` → =={nums[now]}==，`now += k` 走到链上下一个下标',
        'res = 0': '所有询问处理完，开始异或',
        'res ^= v': '`res ^= {v}` → {res}',
        'return res': '异或结果 `{res}`',
    },
    cards=dict(
        one_liner='相同 (k, 下标模 k) 的修改连成一条链，链上做乘法差分',
        complexity='时间约 `O(n√n + q)`，空间 `O(n + q)`',
        problem=['`queries[i] = [l, r, k, v]`：对 `l, l+k, … ≤ r` 的下标都乘 `v`，模 `10^9+7`',
                 '处理完所有询问，求 `nums` 所有元素的==异或==',
                 '本视频：`n=6`，6 个询问，阈值 `int(√6) = 2`'],
        quote='对于k > 1的情况，则可以将所有数组下标按照对k取模的结果分组。……用(k, l % k)作为key建立若干个上面所说的乘积数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['`k = 1` 时是区间乘：像差分数组一样，`f[l] *= v`，`f[r+1]` 乘 `v` 的逆元，前缀积就是倍数',
              '`k > 1`：下标按模 `k` 分组，组内就是 `k = 1` 的情形，起点 `l//k`、终点 `(r − l%k)//k`',
              '`k ≥ √n` 时分组数比要改的下标还多，直接暴力；逆元用线性递推表一次算好'],
        summary=['时间约 `O(n√n + q + max_v)`，空间 `O(n + q)`',
                 '易错点：链上终点是 `(right − left % k) // k`，终点后一格才乘逆元；取模别漏',
                 '“除以 v”不能用整除，要乘模意义下的逆元 `inv[v]`',
                 '对比灵神：灵神用 `isqrt(q)` 当阈值、`pow(v, -1, MOD)` 求逆元；yiduobo 阈值取 `√n`、预处理逆元表',
                 '原文本来就是整数运算（除法已写成 `//`），代码未修改'],
    ),
)
