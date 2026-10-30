TRACK = '''
class Tracked(str):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k, ch in enumerate(str.__iter__(self)):
            self.k = k
            yield ch
        self.k = None
'''

# 代码行号（第 1 行是 class Solution）：7 pop / 9 += 1 / 11 append，执行完这三行才算 s[i] 处理完毕
DONE_LINES = (7, 9, 11)


def _cur(S):
    s = S.get('s')
    i = getattr(s, 'k', None)
    return i if isinstance(i, int) and i >= 0 else None


def _upto(S):
    s = S.get('s')
    i = getattr(s, 'k', -1)
    if i == -1:
        return 0
    if i is None:
        return len(s)
    return i + 1 if S['_line'] in DONE_LINES else i


def _alive(s, K, upto):
    """模拟算法，返回仍留在栈里的字符下标（只用于画图）"""
    st = []
    for i in range(upto):
        c = s[i]
        if st and st[-1][0] == c:
            if len(st[-1][1]) == K - 1:
                st.pop()
            else:
                st[-1][1].append(i)
        else:
            st.append((c, [i]))
    return {j for _, idxs in st for j in idxs}


def _dim(S, i, v):
    s = S.get('s')
    if s is None or 'k' not in S:
        return False
    u = _upto(S)
    return i < u and i not in _alive(str(s), S['k'], u)


def _txt(S):
    st = S.get('stack')
    if st is None:
        return f"遇到连续 `{S['k']}` 个相同字符就删掉，删完两边会拼到一起"
    cur = ''.join(c * n for c, n in st)
    return f"栈里剩下的字符（拼起来）：`{cur}`" if cur else '栈里剩下的字符：（空）'


def _for(S, B, ret):
    if getattr(S.s, 'k', None) is None:
        return '扫描结束，栈里剩下的就是答案'
    return f'扫描到第 `{S.s.k}` 个字符 `char = "{S.char}"`'


def _if1(S, B, ret):
    if not S.stack:
        return f'栈是空的，没有可以延续的连续段 → 走 `else`，==新开一段=='
    t = S.stack[-1][0]
    if t == S.char:
        return f'栈顶字符 `"{t}"` == `char` → 它们属于同一段，要看这一段有多长'
    return f'栈顶字符 `"{t}"` ≠ `char = "{S.char}"` → 连续段断了，走 `else`'


def _if2(S, B, ret):
    t, c = S.stack[-1]
    if c == S.k - 1:
        return f'`"{t}"` 在栈中已出现 `{c}` 次 = `k - 1` → 加上当前这个就是 ==k 个==，要删'
    return f'`"{t}"` 在栈中才出现 `{c}` 次 < `k - 1 = {S.k - 1}` → 还没凑够，次数加一就行'


CONFIG = dict(
    num=1209, title='删除字符串中的所有相邻重复项 II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='栈 · 存字符和出现次数',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1542'],
    code='''
class Solution(object):
    def removeDuplicates(self, s, k):
        stack = []
        for char in s:
            if stack and stack[-1][0] == char:
                if stack[-1][1] == k - 1:
                    stack.pop()
                else:
                    stack[-1][1] += 1
            else:
                stack.append([char, 1])

        return ''.join([x[0] * x[1] for x in stack])
''',
    setup=TRACK,
    call='Solution().removeDuplicates(Tracked("aabbbacdddc"), 3)',
    expect='cc',
    views=[
        dict(type='string', var=lambda S: str(S['s']), label='s（灰色 = 已被删掉的字符）', h=260, cell=80,
             pointers={_cur: 'blue'}, pointer_labels={_cur: 'char'}, dim=_dim),
        dict(type='stack', var='stack', label='stack（每项 = 字符×出现次数）', h=190, font=36,
             fmt=lambda p: f'{p[0]}×{p[1]}'),
        dict(type='text', fn=_txt, size=30, h=130),
    ],
    watch=[('char', 'char', 'blue'), ('k', 'k', 'yellow'), ('栈顶', 'stack[-1] if stack else None', 'purple'),
           ('栈深', 'len(stack)', 'green')],
    captions={
        'stack = []': '用栈存==每个剩下的字符和它连续出现的次数==，后面用到的总是最靠后的那一段',
        'for char in s': _for,
        'if stack and stack[-1][0] == char': _if1,
        'if stack[-1][1] == k - 1': _if2,
        'stack.pop()': '凑够 `k` 个 `"{B.stack[-1][0]}"`（栈里 `{B.stack[-1][1]}` 个 + 当前 1 个）→ 整段弹出，露出更早的字符',
        'stack[-1][1] += 1': '出现次数加一：`"{stack[-1][0]}"` 在栈中共 `{stack[-1][1]}` 次',
        'stack.append([char, 1])': '`"{char}"` 作为新的一段入栈，出现次数置为 `1`',
        'return': '每段按 `字符 × 次数` 展开再拼接，别忘了乘次数；返回 =={ret}==',
    },
    cards=dict(
        one_liner='用栈存「字符 + 出现次数」，凑够 k 个就整段弹出',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['在 `s` 中找 `k` 个相邻且相同的字符删掉，两边拼起来；重复直到删不动',
                 '示例：`s = "deeedbbcccbdaa"`，`k = 3` → `"aa"`',
                 '本视频用 `"aabbbacdddc"`，`k = 3`：先删 `bbb`，两个 `a` 碰到一起，再配上后面的 `a` 又凑够 3 个'],
        quote='每次我们使用的都是最靠后的字符，因此一个自然的想法就是使用栈来储存每个剩下的字符以及出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['删掉一段后要往回看更早的字符 → 得把它们==连同出现次数==存起来',
              '每次用的都是最靠后的 → 后进先出 → 栈',
              '一趟扫描三种情况：相同且已有 `k - 1` 个 → 弹出；相同不够 → 次数加一；不同 → 入栈，次数 1'],
        result='`ddd` 删掉后，前后的 `c` 靠到一起，栈里只剩 `c×2` → `"cc"` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：拼答案时别忘了乘出现次数：`x[0] * x[1]`',
                 '次数 `== k - 1` 时再来一个才满 `k` 个，所以这时==弹出==，而不是加一',
                 '原文为 Python 2 风格写法，在 Python 3 下无需修改（只去掉了 def 后的空行）',
                 '对比灵神：灵神放哨兵省掉判空；这里用 `stack and ...` 判空，空栈时直接入栈'],
    ),
)
