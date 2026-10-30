A = [1, 1, 2, 2, 2, 3, 4, 4]


def _stack(S):
    """用题解里的栈规则从 a 的前缀模拟出『栈』：栈大小为偶数随意放，奇数则不能和栈顶相同"""
    a = S.get('a')
    if a is None or 'odd' not in S:
        return None
    ln = S.get('_line', 0)
    done = S['i'] if ln in (6, 14, 16, 18, 19, 20, 21) else S.get('start', 0)
    st = []
    for x in a[:done]:
        if len(st) % 2 == 0 or st[-1] != x:
            st.append(x)
    if ln >= 20 and len(st) % 2 == 1:
        st.pop()
    return st


def _info(S):
    if 'odd' not in S:
        return ''
    n = len(S['a'])
    ans = S['ans']
    par = '==奇数==（还差一个才能凑成一对）' if S['odd'] else '偶数（成对，下一个可以随便放）'
    return f'栈大小是{par}。已删除 `ans = {ans}` 个'


CONFIG = dict(
    num=2216, title='美化数组的最少删除数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='栈 · 邻项消除，压缩成奇偶性 + 连续段（Go 原文转写）',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1510'],
    code='''
class Solution:
    def minDeletion(self, a: List[int]) -> int:
        ans = 0
        odd = False  # 栈大小的奇偶性
        i, n = 0, len(a)
        while i < n:
            start = i
            # 注意这里的 i 和外层循环的 i 是同一个变量，因此时间复杂度为 O(n)
            while i < n and a[i] == a[start]:
                i += 1
            l = i - start  # 连续相同元素个数
            if not odd:  # 只能放一个元素
                ans += l - 1
                odd = True
            elif l == 1:
                odd = False
            else:  # 放两个元素，奇偶性不变
                ans += l - 2
        if odd:  # 栈大小必须为偶数
            ans += 1
        return ans
''',
    call=f'Solution().minDeletion({A})',
    expect=4,
    views=[
        dict(type='array', var='a', label='a（青框 = 当前这一段连续相同的元素，蓝 = i，粉 = start）', cell=92, h=215,
             pointers={'i': 'blue', 'start': 'pink'}, window=('start', 'i - 1'),
             color=lambda S, k, v: 'blue' if k == S.get('i') else None),
        dict(type='stack', var=_stack, label='对应的栈（题解说实际不需要它，只记奇偶性）', h=120, font=34),
        dict(type='text', fn=_info, size=28, h=90),
    ],
    watch=[('i', 'i', 'blue'), ('start', 'start', 'pink'), ('l', 'l'), ('odd', 'odd', 'orange'), ('ans', 'ans', 'green')],
    captions={
        3: '`ans` 统计要删除的元素个数',
        4: '用一个变量 `odd` 代替栈：只记==栈大小的奇偶性==。现在栈是空的，大小为偶数',
        'i, n = 0, len(a)': '`n = {n}`，`i` 从 0 开始，一段一段地处理',
        'while i < n:': lambda S, B, r: (f'`i = {S.i} < n = {S.n}`：还有没处理的元素，取下一段' if S.i < S.n else f'`i = {S.i} = n`：所有段都处理完了'),
        'start = i': '新的一段从 `start = {start}` 开始，值是 `a[{start}] = {a[start]}`',
        'while i < n and a[i] == a[start]': lambda S, B, r: (f'`a[{S.i}] = {S.a[S.i]}` 和这一段的值 `{S.a[S.start]}` ==相同== → 属于这一段' if S.i < S.n and S.a[S.i] == S.a[S.start]
                                                         else (f'`i = n`，数组结束，这一段到此为止' if S.i >= S.n
                                                               else f'`a[{S.i}] = {S.a[S.i]}` ≠ `{S.a[S.start]}` → 这一段到此为止')),
        'i += 1': '这一段再多一个，`i` 右移到 {i}（外层循环共用 `i`，所以总共只扫一遍）',
        'l = i - start': '这一段共 `l = {i} - {start}` = =={l}== 个连续相同的元素',
        'if not odd': lambda S, B, r: ('栈大小是==偶数==（`odd = False`）：这一段只能放一个，其余 `l - 1` 个都要删' if not S.odd
                                       else '栈大小是奇数（`odd = True`）→ 看 `elif`'),
        'ans += l - 1': '偶数大小：放 1 个，删 `l - 1 = {l - 1}` 个 → `ans = {ans}`',
        14: '栈里多了 1 个，大小变成==奇数== → `odd = True`',
        'elif l == 1': lambda S, B, r: ('栈大小是奇数，这一段只有 1 个，和栈顶不同，可以放 → ==凑成一对==' if S.l == 1
                                        else f'`l = {S.l} > 1`：这一段不止一个 → 看 `else`'),
        16: '放进去后栈大小变成==偶数== → `odd = False`，没有删除',
        'ans += l - 2': '奇数大小：先放 1 个凑成一对，再放 1 个，共 2 个，删 `l - 2 = {l - 2}` 个 → `ans = {ans}`（奇偶性不变，仍是奇数）',
        'if odd': lambda S, B, r: ('遍历结束，栈大小是==奇数==，不满足“长度为偶数” → 要多删 1 个' if S.odd else '遍历结束，栈大小是偶数，已经是美丽数组'),
        'ans += 1': '删掉栈顶那个落单的元素：`ans = {ans}`',
        'return ans': '最少删除 =={ret}== 个',
    },
    max_steps=80,
    cards=dict(
        one_liner='相邻去重 = 栈；再压缩成“奇偶性 + 连续段长度”',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组长度要是偶数，且每对 `(a[2k], a[2k+1])` 的两个数不能相等',
                 '可以随意删元素（右边的元素左移），求最少删除个数',
                 f'示例：`{A}` → `4`（留下 `[1,2,2,3]`）'],
        quote='如果栈大小为偶数，可以随意加入元素；如果栈大小为奇数，那么加入的元素不能和栈顶相同。……实际上不需要栈，用一个变量表示栈的奇偶性即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['套路：从前往后 + 看相邻元素 + 有消除 = ==栈==。栈大小是偶数随便放，奇数不能和栈顶相同',
              '栈不用真建：只要 `odd`（栈大小奇偶性）和一段连续相同元素的个数 `l`',
              '偶数：只能放 1 个；奇数 + `l == 1`：放 1 个凑对；奇数 + `l > 1`：放 2 个，其余删'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`for i, n := 0, len(a); i < n;` 对应 `while i < n`）',
                 '时间 `O(n)`，空间 `O(1)`：内外层循环共用 `i`，每个元素只扫一次',
                 '易错：遍历结束后栈大小若是奇数，要==再删 1 个==',
                 '变形：条件改成 `nums[i] == nums[i+1]` 见 CF1660C'],
    ),
)
