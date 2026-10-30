CONFIG = dict(
    num=927, title='三等分', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='统计 1 的个数 · 分段比对',
    tags=[],
    code='''
class Solution(object):
    def threeEqualParts(self, arr):

        s = sum(arr)
        if s % 3 != 0:
            return [-1, -1]
        s //= 3
        if s == 0:
            return [0, 2]

        l1 = 0
        while arr[l1] != 1:
            l1 += 1
        now = 1
        r1 = l1
        while now < s:
            r1 += 1
            now += arr[r1]
        
        l2 = r1 + 1
        while arr[l2] != 1:
            l2 += 1
        now = 1
        r2 = l2
        while now < s:
            r2 += 1
            now += arr[r2]
        
        l3 = r2 + 1
        while arr[l3] != 1:
            l3 += 1
        r3 = len(arr) - 1
        while arr[r3] == 0:
            r3 -= 1
        
        if r1 - l1 != r2 - l2 or r1 - l1 != r3 - l3:
            return [-1, -1]
        
        suffix_zero = len(arr) - r3 - 1
        if l3 - 1 - (r2 + 1) + 1 < suffix_zero:
            return [-1, -1]
        if l2 - 1 - (r1 + 1) + 1 < suffix_zero:
            return [-1, -1]

        return [r1 + suffix_zero, r2 + suffix_zero + 1]
''',
    call='Solution().threeEqualParts([1,0,0,1,0,0,1,0])',
    expect=[1, 5],
    views=[
        dict(type='text', fn=lambda S: (f"每段 `{S['s']}` 个 1" if 's' in S and 'l1' in S else (f"1 的总数 `{S['s']}`" if 's' in S else ''))),
        dict(type='array', var='arr', h=300, cell=70,
             pointers={'l1': 'blue', 'r1': 'cyan', 'l2': 'pink', 'r2': 'purple', 'l3': 'orange', 'r3': 'green'},
             color=lambda S, i, v: ('yellow' if v == 1 else None)),
    ],
    watch=['s', 'l1', 'r1', 'l2', 'r2', 'l3', 'r3', 'suffix_zero'],
    captions={
        's = sum(arr)': '统计 1 的总数：三段 1 的个数必须相同 → `s = {s}`',
        's % 3 != 0': '`{s} % 3 = {s % 3}`：{"不能被 3 整除 → 无解" if s % 3 else "能被 3 整除，继续"}',
        's //= 3': '每一段应含 `{s}` 个 1',
        's == 0': '`s = {s}`：{"全是 0，任意切分都行" if s == 0 else "有 1，需要按 1 的位置来分段"}',
        'l1 = 0': '`l1` 从头找第一个 1',
        'while arr[l1] != 1': '`arr[{l1}] = {arr[l1]}`：{"还不是 1，l1 右移（前导 0 不影响数值）" if arr[l1] != 1 else "找到第一个 1"}',
        'now = 1': '`now` 记录本段已数到的 1 的个数，起点已含 1 个',
        'r1 = l1': '`r1` 从 `l1` 出发，数到第 `{s}` 个 1',
        'while now < s': '`now = {now}`，需要 `{s}` 个：{"还不够，继续扩" if now < s else "够了，本段结束"}',
        'r1 += 1': '`r1` → {r1}',
        'r2 += 1': '`r2` → {r2}',
        'now += arr': '数到的 1 增加：`now = {now}`',
        'l2 = r1 + 1': '第 2 段从 `r1` 之后找起，`l2 = {l2}`',
        'while arr[l2] != 1': '`arr[{l2}] = {arr[l2]}`：{"是 0，跳过（这些 0 可作前导 0）" if arr[l2] != 1 else "找到第 2 段的第一个 1"}',
        'l3 = r2 + 1': '第 3 段从 `r2` 之后找起，`l3 = {l3}`',
        'while arr[l3] != 1': '`arr[{l3}] = {arr[l3]}`：{"是 0，跳过" if arr[l3] != 1 else "找到第 3 段的第一个 1"}',
        'r3 = len(arr) - 1': '第 3 段的 1 到末尾为止，`r3` 从末尾往前找最后一个 1',
        'while arr[r3] == 0': '`arr[{r3}] = {arr[r3]}`：{"末尾的 0 必须留给第三段（后缀 0）" if arr[r3] == 0 else "找到最后一个 1"}',
        'r3 -= 1': '`r3` → {r3}',
        'if r1 - l1 != r2 - l2': '三段长度：`{r1 - l1 + 1}`、`{r2 - l2 + 1}`、`{r3 - l3 + 1}`：{"不一致 → 无解" if (r1 - l1 != r2 - l2 or r1 - l1 != r3 - l3) else "一致（含内部 0 的排布也相同）"}',
        'suffix_zero =': '第三段后面有 `{suffix_zero}` 个后缀 0，前两段也必须各带同样多的后缀 0',
        'l3 - 1 - (r2 + 1) + 1 < suffix_zero': '第 2、3 段之间有 `{l3 - r2 - 1}` 个 0，要拿 `{suffix_zero}` 个：{"不够 → 无解" if l3 - r2 - 1 < suffix_zero else "够"}',
        'l2 - 1 - (r1 + 1) + 1 < suffix_zero': '第 1、2 段之间有 `{l2 - r1 - 1}` 个 0，要拿 `{suffix_zero}` 个：{"不够 → 无解" if l2 - r1 - 1 < suffix_zero else "够"}',
        'return [r1 + suffix_zero': '第一段终点 `i = r1 + 后缀0 = {r1 + suffix_zero}`，第二段起点 `j = r2 + 后缀0 + 1 = {r2 + suffix_zero + 1}`',
    },
    cards=dict(
        one_liner='三段二进制值相等 → 每段 1 的个数相同、排布也相同',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['0/1 数组 `arr`，把它分成三个非空部分，每部分表示的二进制值相等（允许前导 0）',
                 '返回分割点 `[i, j]`：`arr[0..i]`、`arr[i+1..j-1]`、`arr[j..]`；无解返回 `[-1, -1]`',
                 '本视频：`[1,0,0,1,0,0,1,0]` → `[1, 5]`'],
        quote='若可以分出来，那么这三个连续子数组中1的数量必然是相等的，且排布也必须是一样的。',
        quote_src='—— yiduobo 题解原文',
        idea=['先数 1 的总数 `s`：不是 3 的倍数无解；全 0 随便切',
              '按每段 `s/3` 个 1 找出三段 `[l..r]`，比较三段长度是否一致',
              '最后一段后面的 0 是后缀 0：前两段也要各拿同样多，所以中间的 0 要够分'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '前导 0 不改变数值，但最后一段后缀 0 会放大数值，前两段必须配同样数量',
                 '原文为 Python 2 写法，整数除法 `s /= 3` 已改为 `s //= 3`',
                 '易错：全 0 要单独返回 `[0, 2]`'],
    ),
)
