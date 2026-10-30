CONFIG = dict(
    num=3224, title='使差值相等的最少数组改动次数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='区间同值修改 · 差分数组',
    tags=['灵神题单', '常用数据结构', '难度分 1996'],
    code='''
class Solution(object):
    def minChanges(self, nums, k):
        
        f = [0] * (k + 1)
        left, right = 0, len(nums) - 1
        while left < right:
            v = max(nums[left], nums[right], k - nums[left], k - nums[right])
            diff = abs(nums[left] - nums[right])
            f[0] += 1
            f[diff] -= 1
            if diff < k:
                f[diff + 1] += 1
            if v < k:
                f[v + 1] += 1
            
            left += 1
            right -= 1

        now = 0
        res = None
        for d in range(0, k + 1):
            now += f[d]
            if res is None or res > now:
                res = now
            
        return res
''',
    call='Solution().minChanges([1,0,1,2,4,3], 4)',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = left，粉 = right）',
             pointers={'left': 'blue', 'right': 'pink'}, h=210),
        dict(type='text', fn=lambda S: ('' if 'v' not in S else f"这一对 `nums[{S['left']}]={S['nums'][S['left']]}`，`nums[{S['right']}]={S['nums'][S['right']]}`" + (f"：最大可达差值 `v={S['v']}`" if 7 <= S.get('_line', 0) <= 15 else '') + (f"，原差值 `diff={S['diff']}`" if 8 <= S.get('_line', 0) <= 15 else '')), h=60),
        dict(type='array', var='f', label='f（差分数组）', h=170, cell=90,
             pointers={'d': 'orange'}),
    ],
    watch=['left', 'right', 'v', 'diff', 'now', ('res', 'res', 'green')],
    captions={
        'f = [0]': '`f` 是差分数组：之后对 `cnt[x]`（改成 x 的最少操作数）做区间加',
        'left, right': '双指针从两端往中间，配对 `nums[left]` 和 `nums[right]`',
        'while left < right': lambda S, B, r: ('还有数对没处理，继续' if S.left < S.right else '`left >= right`：所有数对都处理完了'),
        'v = max': '改一个数最多能让差值覆盖 `0..v`：`v` 为 =={v}==',
        'diff = abs': '不动的话差值就是 `diff` 为 =={diff}==',
        'f[0] += 1': '`cnt[0..v]` 先都按「改一次」算：`f[0]` 加 1',
        'f[diff] -= 1': '`cnt[diff]` 要置 0，把区间在 `diff` 处切开：`f[{diff}]` 减 1',
        'f[diff + 1] += 1': '`diff` 之后接着算「改一次」：`f[{diff+1}]` 加 1',
        'f[v + 1] += 1': '`v` 之后要改两次，再多加 1：`f[{v+1}]` 加 1',
        'now += f[d]': '前缀和：`now` = 把差值全改成 `{d}` 的最少操作数 为 =={now}==',
        'res > now': lambda S, B, r: ((f'`now = {S.now}` 比目前最小的 `{B.res}` 还小 → 更新' if B.res is not None else f'`res` 还是 None，没有答案 → 直接记 `{S.now}`') if (B.res is None or B.res > S.now) else f'`now = {S.now}` 不比 `{B.res}` 小，保留'),
        'return res': '最少操作次数 = =={ret}==',
    },
    cards=dict(
        one_liner='cnt[x] 是改成差值 x 的代价：区间同值修改，差分求解',
        complexity='时间 `O(n+k)`，空间 `O(k)`',
        problem=['`n` 为偶数，每次把任一元素改成 `0..k` 内任意整数',
                 '让所有 `|nums[i] - nums[n-1-i]|` 都等于同一个 `X`，求最少操作次数',
                 '示例：`nums=[1,0,1,2,4,3], k=4` → `2`'],
        quote='令cnt[x]表示将数对的差值修改成x时所需的最少操作次数，那么对于nums[i]以及nums[n - i - 1]这一组数对，就应该将cnt[0]到cnt[v]这一段都加上1，将cnt[v + 1]到cnt[k]这一段都加上2。',
        quote_src='—— yiduobo 题解原文',
        idea=['一对数：不改 0 次，改一个数能覆盖 `0..v`，改两个数能覆盖 `0..k`',
              '所以 `cnt[0..v]` 加 1，`cnt[v+1..k]` 加 2，`cnt[diff]` 置 0',
              '离线区间修改、最后单点求值 → 差分数组，前缀和取最小'],
        summary=['时间 `O(n+k)`，空间 `O(k)`',
                 '`diff+1` 和 `v+1` 可能等于 `k+1`，所以要加 `if diff < k`、`if v < k` 防越界',
                 '`res = None` 表示还没有答案，第一个 `now` 直接成为最小值',
                 '原文为 Python 2 风格，本题代码无需改动'],
    ),
)
