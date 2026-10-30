NUMS = [1, 2, 2, 1, 3]


def _phase(S):
    ln = S.get('_line', 0)
    if 'ans' in S and 'q' in S and ln >= 34:
        return '第二步：每个查询 O(1)：哈希相等 ⇒ 都是偶数次，`l` 在 `[l1[r], l2[r])` ⇒ 恰好 k 种'
    if 'lefts' in S:
        return f'滑窗：对每个右端点 `i`，求最小的 `l` 使得窗口内不同元素 ==< {S["k"]}== 种（当前 k = {S["k"]}）'
    return '第一步：每种值映射成随机数，前缀异或 `s[i]`；偶数次出现的值异或后抵消'


def _sv(S):
    s = S.get('s')
    if s is None:
        return None
    return [f'{v & 0xFFFF:04x}' for v in s]


def _scolor(S, i, v):
    if 'ans' in S and 'r' in S and S.get('_line', 0) >= 34:
        if i == S['l']:
            return 'blue'
        if i == S['r'] + 1:
            return 'pink'
    return None


def _win_r(S):
    if 'r' in S and S.get('_line', 0) >= 34:
        return S['r']
    return S.get('i', -1)


def _ncolor(S, i, v):
    if 'r' in S and S.get('_line', 0) >= 34 and S['l'] <= i <= S['r']:
        return 'cyan'
    return None


def _cmp(S, B, r):
    l, rr = S.l, S.r
    same = S.s[rr + 1] == S.s[l]
    lo, hi = S.l1[rr], S.l2[rr]
    if not same:
        why = f'`s[{rr + 1}] ≠ s[{l}]` → 有的数出现奇数次'
    elif l1_ok(S):
        why = f'异或相等（都出现偶数次），且 `{lo} ≤ {l} < {hi}` → 恰好 {S.k} 种'
    else:
        why = f'异或相等，但 `l = {l}` 不在 `[{lo}, {hi})` → 不是恰好 {S.k} 种'
    return f'查询 `[{l}, {rr}]`：{why} → =={S.ans[S.i]}=='


def l1_ok(S):
    return S.l1[S.r] <= S.l < S.l2[S.r]


CONFIG = dict(
    num=4042, title='有效 K 个不同元素子数组 II', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='异或哈希 + 两次滑窗 + 强制在线',
    code='''
class Solution:
    def validSubarrays(self, nums: list[int], k: int, l0: int, r0: int, q: int) -> list[bool]:
        n = len(nums)
        s = [0] * (n + 1)
        # 把 nums[i] 映射成随机数
        # 不要在 [0, 2**L) 内随机，见 https://codeforces.com/blog/entry/153335
        mp = defaultdict(lambda: randrange(10 ** 18))
        for i, x in enumerate(nums):
            s[i + 1] = s[i] ^ mp[x]

        def calc_left(k: int) -> list[int]:
            lefts = [0] * n
            cnt = defaultdict(int)
            l = 0
            for i, x in enumerate(nums):
                cnt[x] += 1
                while len(cnt) >= k:
                    v = nums[l]
                    if cnt[v] > 1:
                        cnt[v] -= 1
                    else:
                        del cnt[v]  # 保证 len(cnt) 是窗口内的不同元素个数
                    l += 1
                lefts[i] = l
            return lefts

        l1 = calc_left(k + 1)
        l2 = calc_left(k)

        ans = [False] * q
        l, r = l0, r0
        for i in range(q):
            if i > 0:
                g = l + r if ans[i - 1] else r - l
                l = (l ^ g) % n
                r = (r ^ g) % n
                if l > r:
                    l, r = r, l
            ans[i] = s[r + 1] == s[l] and l1[r] <= l < l2[r]
        return ans
''',
    setup='import random\nfrom random import randrange\nrandom.seed(0)',
    call=f'Solution().validSubarrays({NUMS}, 2, 1, 2, 3)',
    expect=[False, True, True],
    skip=['n = len(nums)', 's = [0] * (n + 1)', 'mp = defaultdict', 'for i, x in enumerate', 'lefts = [0]', 'cnt = defaultdict',
          'l = 0', 'v = nums[l]', 'for i in range(q)', 'ans = [False]', 'l, r = l0, r0', 'cnt[v] -= 1', 'del cnt[v]', 'if cnt[v] > 1', 'cnt[x] += 1', 'if i > 0', 'return lefts', 'r = (r ^ g)', 'if l > r'],
    views=[
        dict(type='text', fn=_phase, size=22, h=70),
        dict(type='array', var='nums', label='nums（粉 = l，蓝 = r；框 = 当前窗口）', h=200, cell=84,
             pointers={'l': 'pink', 'r': 'blue'}, window=(lambda S: S.get('l', 0), _win_r), color=_ncolor),
        dict(type='array', var=_sv, label='s：前缀异或哈希（只显示低 16 位）', h=170, cell=100, color=_scolor, min_slots=7),
        dict(type='text', fn=lambda S: ('`l1` = ==' + str(S['l1']) + '==　（`l1[r]`：窗口种类 < k+1 的最小左端）') if 'l1' in S else '`l1`（种类 < k+1 的最小左端）：还没算', size=24, h=62),
        dict(type='text', fn=lambda S: ('`l2` = ==' + str(S['l2']) + '==　（`l2[r]`：窗口种类 < k 的最小左端）') if 'l2' in S else '`l2`（种类 < k 的最小左端）：还没算', size=24, h=62),
    ],
    watch=['k', 'i', 'l', 'r', ('ans', 'ans', 'green')],
    max_steps=80,
    captions={
        's[i + 1] = s[i] ^ mp[x]': '`x={x}` 的随机数异或进前缀：出现==偶数次==就抵消，`s[i+1]` 是前 {i+1} 个数的哈希',
        'while len(cnt) >= k': lambda S, B, r: (f'右端 `i={S.i}`（`{S.x}`），窗口 `{len(S.cnt)}` 种 ≥ {S.k} → `l` 右移，把种类降到 {S.k - 1} 以下' if len(S.cnt) >= S.k
                                                else f'右端 `i={S.i}`（`{S.x}`），窗口 `{len(S.cnt)}` 种 < {S.k}：此时 `l = {S.l}` 是最小的合法左端'),
        'l += 1': '移出 `{v}`（窗口里它{"没有了" if v not in cnt else "还剩 " + str(cnt[v]) + " 个"}）→ 窗口 `{len(cnt)}` 种，`l` → {l}',
        'lefts[i] = l': '`lefts[{i}] = {l}`：以 {i} 结尾、==种类 < {k}== 的子数组，左端至少是 {l}',
        'l1 = calc_left': '`l1[r]`：左端 `< l1[r]` 时种类 ≥ k+1',
        'l2 = calc_left': '`l2[r]`：左端 `≥ l2[r]` 时种类 < k；所以 ==恰好 k 种 ⇔ l1[r] ≤ l < l2[r]==',
        'g = l + r': lambda S, B, r: f'强制在线：上一个答案 `{S.ans[S.i - 1]}` → `g = {S.g}`（真取 l+r，假取 r−l）',
        'l = (l ^ g)': '`l = (l ^ g) % n` = {l}，`r = (r ^ g) % n` = {(r ^ g) % n}（先 l 后 r，用的是同一个 g）',
        'l, r = r, l': '`l > r` → 交换，得到 `[l, r] = [{l}, {r}]`',
        'ans[i] = s[r + 1]': _cmp,
        'return ans': '全部查询答案：`{ans}`',
    },
    cards=dict(
        one_liner='异或哈希判偶数次，两次滑窗判恰好 k 种，查询 O(1)',
        complexity='时间 `O(n+q)`，空间 `O(n)`',
        problem=['子数组有效：==恰好 k 种不同的数，且每种都出现偶数次==',
                 '`q` 个查询强制在线：下一个 `(l, r)` 由上一个答案算出，不能离线',
                 '本视频：`nums=[1,2,2,1,3], k=2, (l0,r0)=(1,2), q=3` → `[False, True, True]`'],
        quote='本强制在线（不允许使用离线算法）。做法同 4033. 有效 K 个不同元素子数组 I 的方法一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每种值映射成随机数，前缀异或：`s[r+1] == s[l]` ⇔ 区间内每个数出现偶数次（极大概率）',
              '`calc_left(k)` 滑窗：每个 `r` 求最小的 `l`，使 `[l, r]` 种类 `< k`',
              '`l1 = calc_left(k+1)`、`l2 = calc_left(k)`：恰好 k 种 ⇔ `l1[r] ≤ l < l2[r]`'],
        summary=['预处理 `O(n)`，每个查询 `O(1)`，所以强制在线也不怕',
                 '随机数用 `randrange(10**18)`，别在 `[0, 2^L)` 内随机（原文链接说明）',
                 '滑窗里 `cnt` 计数为 0 要 `del`，这样 `len(cnt)` 才是种类数',
                 '本视频固定了随机种子，哈希只显示低 16 位',
                 '前置：4033（离线版），异或哈希'],
    ),
)
