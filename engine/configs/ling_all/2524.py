def _wl(S):
    i = S.get('i')
    if i is None:
        return None
    return max(0, i - S['k'] + 1)


def _stk(S):
    m = S.get('st_map')
    if m is None:
        return ''
    return f"窗口分数 `score = {S.get('score', 0)}`：每个数 x 贡献它的栈顶（栈顶 = x^出现次数）"


CONFIG = dict(
    num=2524, title='子数组的最大频率分数', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='定长窗口 · 每个数一个乘积栈',
    tags=['滑动窗口与双指针', '常用数据结构'],
    code='''
class Solution:
    def maxFrequencyScore(self, nums: List[int], k: int) -> int:
        MOD = 10 ** 9 + 7
        ans = score = 0
        st_map = {}
        for i, x in enumerate(nums):
            if x not in st_map:
                score += x
                st_map[x] = [x]
            else:
                last = st_map[x][-1]
                cur = last * x % MOD
                score += cur - last
                st_map[x].append(cur)
            if i >= k - 1:
                ans = max(ans, score % MOD)
                x = nums[i - k + 1]
                st = st_map[x]
                score -= st.pop()
                if st: score += st[-1]
                else: del st_map[x]
        return ans
''',
    call='Solution().maxFrequencyScore([2,3,2,2,3,2], 4)',
    expect=13,
    views=[
        dict(type='array', var='nums', label='nums（框 = 长为 k 的窗口）', pointers={'i': 'blue'}, window=(_wl, 'i'), h=190, cell=96),
        dict(type='map', var='st_map', label='st_map：x → 乘积栈（栈顶 = x^次数）', fmt=lambda k, v: f"{k}: {v}", h=170, font=30),
        dict(type='text', h=90, size=30, fn=_stk),
    ],
    watch=[('i', 'i', 'blue'), 'x', ('score', 'score', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'if x not in st_map': '`{x}` 在窗口里有吗？{"没有，开一个新栈" if B.x not in B.st_map else "有，栈顶乘上它"}',
        'score += x': '第一次出现：`x^1 = {x}` 直接加进分数 → `score = {score}`',
        'st_map[x] = [x]': '为 `{x}` 建栈，栈里放 `{x}`（栈顶 = `{x}^1`）',
        'last = st_map': '`last` = 栈顶 = `{x}` 的当前幂 = {last}',
        'cur = last': '再多一个 `{x}`：新幂 `cur = last * x % MOD = {cur}`',
        'score += cur - last': '分数变化只有这一项：`+ (cur - last) = {cur - last}` → `score = {score}`，==O(1) 更新，不用快速幂==',
        'st_map[x].append': '新幂入栈，之后滑出一个 `{x}` 时直接弹栈就能回到旧幂',
        'if i >= k - 1': '`i = {i}`：窗口{"还没填满 k 个" if i < k - 1 else "已满 k 个，可以统计答案了"}',
        'ans = max': '窗口分数 `{score}`，`ans = max({B.ans}, {score % MOD}) = {ans}`',
        'x = nums[i - k + 1]': '最左边的 `{x}` 要滑出窗口',
        'st = st_map[x]': '取出 `{x}` 的栈 `{st}`',
        'score -= st.pop()': '弹出栈顶 `{x}` 的当前幂，`score -= ` 它 → `{score}`',
        'if st: score': '栈里还剩旧幂 `{st[-1]}`：把它补回分数 → `score = {score}`',
        'else: del': '栈空了：窗口里没有 `{x}` 了，删掉这个栈',
        'return ans': '最大分数 `{ans}`',
    },
    cards=dict(
        one_liner='每个数一个栈，栈顶记录当前幂，滑入滑出都是 O(1)',
        complexity='时间 `O(n)`，空间 `O(k)`',
        problem=['长为 `k` 的子数组：出现 `c` 次的数 `x` 贡献 `x^c`，分数是所有不同数的贡献之和（对 `10^9+7` 取模）',
                 '求所有长为 `k` 的子数组中分数最大的值（取模前比较）',
                 '本视频：`[2,3,2,2,3,2]`，`k=4`'],
        quote='对每个 x=nums[i] 创建一个栈，每遇到一个 x 就把 x 与栈顶的乘积入栈，滑出窗口时同理。这样就可以 O(1) 地计算分数的变化量了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['定长窗口：每步进一个、出一个',
              '`x` 的幂只在“多一个 / 少一个 x”时变，乘一次或除一次',
              '用栈存历史幂：进窗口入栈，出窗口弹栈，==免去快速幂和逆元=='],
        summary=['时间 `O(n)`，空间 `O(k)`',
                 '先更新答案，再把左端点滑出窗口',
                 '栈弹空要 `del`，否则 `x not in st_map` 判断会出错',
                 '`score` 保持取模前的累加值，比较前才 `% MOD`（原写法）'],
    ),
)
