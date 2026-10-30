CONFIG = dict(
    num=3653, title='区间乘法查询后的异或 I', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='按步长分组 · 乘法差分数组', tags=[],
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
    call='Solution().xorAfterQueries([2,3,1,5,4], [[1,4,2,3],[0,2,1,2]])',
    expect=31,
    max_steps=90,
    views=[
        dict(type='array', var='nums', label='nums（黄 = 刚被乘过）', h=190,
             pointers={'index': 'pink', 'now': 'blue'},
             color=lambda S, i, v: 'yellow' if S.get('_line') in (11, 12, 13) and S.get('index') == i else None),
        dict(type='array', var=lambda S: S['f'] if isinstance(S.get('f'), list) else [], label='f（当前分组的乘法差分数组）', h=190,
             pointers={'left': 'cyan', 'right + 1': 'orange'}),
        dict(type='map', var='q_dict', label='q_dict：(k, l % k) → [(起点, 终点, v)]', h=170,
             fmt=lambda k, v: str(v)),
    ],
    watch=['threshold', 'key', 'v', 'res'],
    captions={
        'threshold = ': '`threshold = int(√n) = {threshold}`：步长 ≥ 它的查询直接暴力改，更小的才分组',
        'for left, right, k, v in queries': '取出一个查询：`[{left}, {right}, {k}, {v}]`',
        'if k >= threshold': lambda S, B, r: (f'步长 `k = {S.k} ≥ {S.threshold}`：要改的下标不多 → ==暴力==' if S.k >= S.threshold
                                              else f'步长 `k = {S.k} < {S.threshold}`：下标太多 → 按 `k` 分组做差分'),
        'for index in range(left, right + 1, k)': lambda S, B, r: ('这个查询的暴力部分改完了' if S.index == B.get('index') else f'暴力：`index = {S.index}`，从 `{S.left}` 每隔 `{S.k}` 走'),
        'for left, right, v in q_dict[key]': '这一组的记录：取下一条（取完就结束）',
        'if right + 1 <= max_r[key]': lambda S, B, r: (f'终点后一格 `{S.right+1}` 还在数组里 → 要把 `v` 除掉' if S.right + 1 <= S.max_r[S.key] else f'终点后一格 `{S.right+1}` 已超出这组，不用再除'),
        'for key in q_dict': '轮到下一个分组（分完就结束）：`key = {key}`',
        'k, r = key': '拆开分组键：步长 `k = {k}`，起始余数 `r = {r}`',
        'nums[index] *= v': '`nums[{index}]` × `{v}` = {nums[index]}',
        'nums[index] %= mod': '取模后 `nums[{index}] = {nums[index]}`',
        'key = (k, left % k)': '下标 `l, l+k, …` 模 `k` 都相同，分组键 `key = (k, l % k) = {key}`',
        'right = (right - left % k) // k': '这组里的第 j 个位置对应原下标 `l%k + j×k`：终点 `right` = {right}',
        'left //= k': '起点换成组内位置：`left` = {left}',
        'q_dict[key].append': '记录 `(起点 {left}, 终点 {right}, ×{v})` 到分组 `{key}`',
        'for v in range(2, max_v + 1)': '预处理逆元：用 `inv[v]` 代替「除以 v」',
        'fac.append': '`fac[{v}] = {fac[v]}`',
        'inv.append': '`inv[{v}] = {inv[v]}`：模 `10^9+7` 下的乘法逆元',
        'f = [1] * ': '为这组建差分数组 `f`，长度 {len(f)}，初值全 1',
        'f[left] *= v': '区间起点 `f[{left}]` × `{v}`：从这里起整体乘 `{v}`',
        'f[right + 1] *= inv[v]': '区间终点后一格 × `inv[{v}]`：把 `{v}` 再「除」掉',
        'v *= f[index]': '前缀积 `v` 累乘 `f[{index}]` = {v}：这个位置的总倍率',
        'nums[now] *= v': '`nums[{now}]` × 倍率 `{v}`',
        'nums[now] %= mod': '`nums[{now}]` = {nums[now]}',
        'now += k': '组内下一个位置对应原下标 `now` = {now}',
        'res ^= v': '`res ^= {v}` → {res}',
        'return res': '全部异或结果 =={ret}==',
    },
    cards=dict(
        one_liner='步长为 1 用乘法差分，步长 k 就按下标模 k 分组再差分',
        complexity='本题数据小，直接模拟也行；差分思路为第 II 题准备',
        problem=['每个查询 `[l, r, k, v]`：从 `l` 起每隔 `k` 个，把 `nums[idx]` 乘以 `v` 取模 `10^9+7`',
                 '全部查询后，返回所有元素的异或',
                 '本视频：`[2,3,1,5,4]`，查询 `[1,4,2,3]`、`[0,2,1,2]` → `31`'],
        quote='对于这类问题，可以仿照静态区间加法常用的差分数组，设计一个使用乘除法的数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['步长 `k` 大：要改的下标少，直接循环乘',
              '步长 `k` 小：按 `(k, l % k)` 分组，组内就是连续区间，用差分：起点乘 `v`，终点后乘 `inv[v]`',
              '差分数组求前缀积就得到每个位置的总倍率，最后异或所有元素'],
        summary=['暴力部分 `O(n/k)`，分组部分按组做前缀积',
                 '易错点：除法要用逆元，因为结果取模 `10^9+7`',
                 '组内位置：起点 `l // k`，终点 `(r - l % k) // k`',
                 '原文已使用 `//`，无需改动 Python 3；`f = {}` 与 `fac` 为原文遗留，未影响结果'],
    ),
)
