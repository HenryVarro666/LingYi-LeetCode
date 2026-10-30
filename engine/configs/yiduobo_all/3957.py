def _N(x):
    if isinstance(x, int) and abs(x) >= 10 ** 6:
        e = len(str(abs(x))) - 1
        return f"{'-' if x < 0 else ''}{abs(x) / 10 ** e:.1f}×10^{e}"
    return str(x)


def _lst(S, k):
    v = S.get('_inner', {}).get(k)
    return v if isinstance(v, list) else None


def _q(S):
    I = S.get('_inner', {})
    q, h, t = I.get('q'), I.get('head'), I.get('tail')
    if q is None:
        return None
    return q[h:t]


def _txt(S):
    I = S.get('_inner', {})
    if 'lamb' in I:
        bf = I.get('best_f')
        return (f"惩罚 `lamb = {_N(I['lamb'])}`：每选一个子数组，得分先减 lamb；"
                f"目前最优 `best_f` = =={_N(bf) if bf is not None else '—'}==，个数 `best_cnt` = =={I.get('best_cnt', 0)}==")
    if 'mid' in S and 'left' in S:
        return f"二分惩罚：`left = {_N(S['left'])}`，`right = {_N(S['right'])}`；目标：选的个数 `cnt ≤ m = {S['m']}`"
    return '先看无约束时选几个、与 m 比较；个数太多就加惩罚 `lamb` 来压低'


def _txt2(S):
    c = S.get('cnt')
    if not isinstance(c, int):
        return ''
    ok = '≤' if c <= S['m'] else '>'
    return f"上一次 `calc` 的结果：个数 `cnt = {c}` {ok} `m = {S['m']}`，{'够了' if c <= S['m'] else '选多了'}"


CONFIG = dict(
    num=3957, title='M 个非重叠子数组最大和 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='wqs 二分 + 单调队列优化 DP',
    tags=['动态规划', '难度分 2611'],
    code='''
class Solution(object):
    def maximumSum(self, nums, m, l, r):

        n = len(nums)
        s = [0]
        for v in nums:
            s.append(s[-1] + v)
        def calc(lamb):
            f = [None] * (n + 1)
            f[0] = 0
            cnt = [0] * (n + 1)
            q = []
            head, tail = 0, 0
            best_f = None
            best_cnt = 0
            for index in range(1, n + 1):
                if head < tail and index - q[head] > r:
                    head += 1
                if index >= l and f[index - l] is not None:
                    while tail > head and f[index - l] - s[index - l] > f[q[-1]] - s[q[-1]]:
                        q.pop()
                        tail -= 1
                    q.append(index - l)
                    tail += 1

                f[index] = f[index - 1]
                cnt[index] = cnt[index - 1]

                if head < tail:
                    score = f[q[head]] + s[index] - s[q[head]] - lamb
                    if f[index] is None or f[index] < score:
                        f[index] = score
                        cnt[index] = cnt[q[head]] + 1
                    if best_cnt == 0 or best_f < score:
                        best_f = score
                        best_cnt = cnt[q[head]] + 1
            return best_f, best_cnt

        res, cnt = calc(0)
        if cnt <= m:
            return res
        left = 1
        right = 10 ** 18
        while left < right:
            mid = (left + right) // 2
            res, cnt = calc(mid)
            if cnt > m:
                left = mid + 1
            else:
                right = mid
        res, cnt = calc(left)
        return res + m * left
''',
    call='Solution().maximumSum([2, -1, 3, -1, 2], 2, 1, 2)',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums（l = 1，r = 2）', h=300, cell=100),
        dict(type='text', fn=_txt, size=28, h=110),
        dict(type='text', fn=_txt2, size=26, h=60),
    ],
    skip=['n = len', 's = [0]', 's.append', 'for v in nums', 'def calc', 'f = [None]', 'f[0] = 0', 'cnt = [0]', 'q = []',
          'head, tail', 'best_f = None', 'best_cnt = 0', 'for index in range', 'if head < tail and index', 'head += 1',
          'if index >= l', 'while tail > head', 'q.pop()', 'tail -= 1', 'q.append', 'tail += 1', 'f[index] = f[index - 1]',
          'cnt[index] = cnt[index - 1]', 'if head < tail:', 'if f[index] is None', 'f[index] = score',
          'cnt[index] = cnt[q', 'if best_cnt == 0', 'score = ', 'best_cnt = cnt', 'return best_f',
          'left = 1', 'right = 10', 'while left < right'],
    max_steps=39,
    watch=['m', ('lamb', 'lamb', 'yellow'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'cyan'), 'cnt'],
    captions={
        'best_f = score': lambda S, B, r: f"右端点 `{S.index}` 接一个子数组，得分 {_N(S.score)}，比之前的 `best_f` 更好 → 记下：`best_f` = =={_N(S.score)}==，选了 `{S.cnt[S.q[S.head]] + 1}` 个",
        'res, cnt = calc(0)': '先不加惩罚（`lamb = 0`）算无约束最优：`best_f` 和需要的子数组个数 `cnt`',
        'if cnt <= m': '`cnt = {cnt}`，`m = {m}`：{"个数没超，best_f 就是答案" if cnt <= m else "选多了 → 上 wqs 二分，找让个数刚好落到 m 的惩罚"}',
        'mid = (left + right)': lambda S, B, r: f"惩罚值二分：`left = {_N(S.left)}`，`right = {_N(S.right)}`，试 `mid = {_N((S.left + S.right) // 2)}`",
        'res, cnt = calc(mid)': '带惩罚 `lamb = mid` 再算一遍 → 每个子数组都要扣 `mid`，选得越少',
        'if cnt > m': '`cnt = {cnt}`，`m = {m}`：{"仍然选多了，惩罚还不够 → left = mid + 1" if cnt > m else "个数够少了（≤ m）→ 惩罚可能还能再小一点，right = mid"}',
        'left = mid + 1': lambda S, B, r: f'惩罚加大：`left = {_N(S.left)}`',
        'right = mid': lambda S, B, r: f'`right = {_N(S.right)}`：记录「个数 ≤ m」的最小惩罚（惩罚越小，个数越多）',
        'res, cnt = calc(left)': '二分结束，`left = {left}` 是让个数 ≤ m 的最小惩罚，最后算一遍',
        'return res + m * left': '`res + m·left` = {res} + {m}×{left} = =={ret}==：把 m 个惩罚加回去',
    },
    cards=dict(
        one_liner='原函数是凸的：加惩罚 lamb 压个数，二分 lamb 让个数落到 m',
        complexity='时间 `O(n log C)`，空间 `O(n)`',
        problem=['选至少 1 个、至多 `m` 个互不重叠、长度在 `[l, r]` 的子数组，求元素和最大值',
                 '`n` 最大 `10^5`，`O(mn)` 的 DP 会超时',
                 '本视频：`nums=[2,-1,3,-1,2]`，`m=2`，`l=1`，`r=2` → `5`'],
        quote='对于这类有约束的最优化问题，如果能证明原函数的凸性，就可以使用wqs二分来求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['无约束 DP 用单调队列 `O(n)`：`f[p] + s[index] − s[p] − lamb`，`lamb` 是惩罚项',
              '先用 `lamb = 0` 算一次；个数 `cnt ≤ m` 就直接是答案',
              '否则二分最小的 `lamb`，使个数 `≤ m`；答案 `res + m·lamb`'],
        summary=['时间 `O(n log C)`，`C = 10^18` 约 60 次二分，视频只展示开头与结尾几轮',
                 '`f[index - l]` 可能是 `None`，要判断；`cnt` 随 `f` 一起转移',
                 '二分上界取 `10^18`，找「个数 ≤ m 的最小 lamb」，最后再算一遍 `calc(left)`',
                 '原文已是 Python 3 兼容写法，未改动代码；对比灵神：灵神把个数取反放进元组一起比较，yiduobo 单独用 `cnt` 数组'],
    ),
)
