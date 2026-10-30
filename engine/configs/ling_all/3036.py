def _ci(S):
    """当前这对相邻元素 (x, y) 在 nums 中的下标 i（本例中每对都互不相同）"""
    if 'x' not in S or S.get('_line', 0) < 15:
        return None
    n = S['nums']
    for i in range(len(n) - 1):
        if n[i] == S['x'] and n[i + 1] == S['y']:
            return i
    return None


def _b(S):
    n = S['nums']
    return [(n[i + 1] > n[i]) - (n[i + 1] < n[i]) for i in range(len(n) - 1)]


def _bcolor(S, k, v):
    i, cnt, ln = _ci(S), S.get('cnt', 0), S.get('_line', 0)
    if i is None or not cnt:
        return None
    if ln <= 19:
        return 'green' if i - cnt <= k <= i - 1 else None
    return 'green' if i - cnt + 1 <= k <= i else None


def _top(S):
    if 'x' in S and _ci(S) is not None:
        x, y = S['x'], S['y']
        r = '>' if y > x else '<' if y < x else '=='
        return f"`nums[{_ci(S)}] = {x}`，`nums[{_ci(S)+1}] = {y}` → `y {r} x` → `b[{_ci(S)}] = {S['v']}`" if 'v' in S else ''
    return 'b = 相邻元素的大小关系（1 升、0 平、-1 降），问题变成「b 里有多少个 pattern」'


CONFIG = dict(
    num=3036, title='匹配模式数组的子数组数目 II', difficulty='Hard', category='字符串',
    author='灵茶山艾府', technique='转成 1/0/-1 序列后 KMP 匹配',
    tags=['灵神题单', '字符串', '难度分 1895'],
    code='''
class Solution:
    def countMatchingSubarrays(self, nums: List[int], pattern: List[int]) -> int:
        m = len(pattern)
        pi = [0] * m
        cnt = 0
        for i in range(1, m):
            v = pattern[i]
            while cnt and pattern[cnt] != v:
                cnt = pi[cnt - 1]
            if pattern[cnt] == v:
                cnt += 1
            pi[i] = cnt

        ans = cnt = 0
        for x, y in pairwise(nums):
            v = (y > x) - (y < x)
            while cnt and pattern[cnt] != v:
                cnt = pi[cnt - 1]
            if pattern[cnt] == v:
                cnt += 1
            if cnt == m:
                ans += 1
                cnt = pi[cnt - 1]
        return ans
''',
    call='Solution().countMatchingSubarrays([1,4,4,1,3,5,5,3], [1,0,-1])',
    expect=2,
    views=[
        dict(type='text', size=26, h=50, fn=_top),
        dict(type='array', var='nums', label='nums', cell=76, h=190, pointers={_ci: 'pink'}, pointer_labels={_ci: 'x'},
             color=lambda S, k, v: 'blue' if _ci(S) is not None and k == _ci(S) + 1 else None),
        dict(type='array', var=_b, label='b：相邻元素关系（绿 = 当前匹配上的部分）', cell=76, h=190, color=_bcolor),
        dict(type='array', var='pattern', label='pattern（蓝箭头 = cnt 已匹配长度）', cell=76, h=200,
             pointers={'cnt': 'blue', 'i if _line < 14 else None': 'pink'}, pointer_labels={'i if _line < 14 else None': 'i'}),
        dict(type='array', var='pi', label='pi[i]：pattern[:i+1] 的最长相等前后缀', cell=76, h=130),
    ],
    watch=[('cnt', 'cnt', 'blue'), ('v', 'v', 'pink'), ('pi', 'pi'), ('ans', 'ans', 'green')],
    captions={
        'm = len(pattern)': '`m = len(pattern) = {m}`',
        5: '`cnt` 是当前已匹配的长度，也是下一个要比较的下标',
        'pi = [0] * m': '`pi[i]`：pattern 前 i+1 个数里，最长的「前缀 = 后缀」长度',
        'v = pattern[i]': '`v = pattern[{i}] = {v}`',
        'while cnt and pattern[cnt] != v': lambda S, B, r: (
            f"`pattern[{S.cnt}] = {S.pattern[S.cnt]}` ≠ `v = {S.v}`：失配，`cnt` 退到 `pi[{S.cnt-1}] = {S.pi[S.cnt-1]}`" if S.cnt and S.pattern[S.cnt] != S.v
            else ('`cnt = 0`，没得退了' if not S.cnt else f'`pattern[{S.cnt}] = {S.v}` 已匹配，不用回退')),
        18: '失配后不从头来，用 `pi` 回退：`cnt` → {cnt}',
        23: '已匹配满的这段，它的最长相等前后缀还能当下一次匹配的开头（允许重叠）：`cnt` → {cnt}',
        9: '失配后不从头来，用 `pi` 回退：`cnt` → {cnt}',
        'if pattern[cnt] == v': lambda S, B, r: (
            f"`pattern[{S.cnt}] = {S.pattern[S.cnt]}` == `v = {S.v}` → 匹配长度 +1" if S.pattern[S.cnt] == S.v
            else f"`pattern[{S.cnt}] = {S.pattern[S.cnt]}` ≠ `v = {S.v}` → 这一位没匹配上"),
        'cnt += 1': '`cnt` → {cnt}',
        'pi[i] = cnt': '`pi[{i}] = {cnt}`',
        'ans = cnt = 0': '开始在 `b` 上匹配：`ans` 记匹配次数，`cnt` 重新从 0 数起',
        'for x, y in pairwise(nums)': '取相邻两个数 `x = {x}`，`y = {y}`',
        'v = (y > x) - (y < x)': '`y > x` 得 1，`y < x` 得 -1，相等得 0：`v = {v}`，不用真的建出数组 b',
        'if cnt == m': lambda S, B, r: (
            f"`cnt = {S.cnt} == m = {S.m}` → ==完整匹配一次==" if S.cnt == S.m else f"`cnt = {S.cnt} < m = {S.m}`，还没匹配完"),
        'ans += 1': '匹配成功：`ans` → {ans}',
        'return ans': '一共有 `{ans}` 个子数组匹配 pattern',
    },
    cards=dict(
        one_liner='相邻元素比大小转成 1/0/-1，就是标准的字符串匹配',
        complexity='时间 `O(n)`，空间 `O(m)`',
        problem=['`pattern` 只含 `1`、`0`、`-1`，长为 `m`；统计 `nums` 里长为 `m+1` 的子数组，其相邻元素的升/平/降恰好依次对应 `pattern`',
                 '示例：`nums = [1,4,4,1,3,5,5,3]`，`pattern = [1,0,-1]` → `2`',
                 '匹配的子数组是 `[1,4,4,1]` 和 `[3,5,5,3]`'],
        quote='把 nums 的相邻元素，根据题目规定的大小关系，转换成 1, 0, -1，得到一个长为 n-1 的数组 b。问题相当于问 b 中有多少个连续子数组等于 pattern。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`b[i]` = `nums[i]` 与 `nums[i+1]` 的大小关系；子数组匹配 ⇔ `b` 的一段等于 `pattern`',
              '这是字符串匹配，只不过「字符」是数字；`n` 到 `10^6`，用 KMP 做到 `O(n)`',
              '代码不建 `b`，边遍历 `pairwise(nums)` 边算 `v`，匹配满了 `cnt = pi[cnt - 1]` 继续找下一个'],
        summary=['时间 `O(n)`，空间 `O(m)`',
                 '易错：匹配成功后要 `cnt = pi[cnt - 1]`（允许重叠匹配），不能清零',
                 '`pattern` 的长度是 `m`，对应 `m+1` 个数，所以 `b` 的长度是 `n-1`',
                 '另一种写法：把 pattern、2、b 拼起来求 Z 函数，`z[i] = m` 就是一次匹配'],
    ),
)
