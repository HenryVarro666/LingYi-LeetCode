AST = [8, 3, -5, 4, -8, -2, 6]   # 各元素互不相同，可用 index 反推当前下标


def _idx(S):
    if 'r' not in S or S['_line'] == 16:
        return -1
    return S['asteroids'].index(S['r'])


def _fmt(v):
    return f'{v}→' if v > 0 else f'←{-v}'


def _dim(S, i, v):
    k = _idx(S)
    if k < 0:
        return 'r' in S and S['_line'] == 16 and v not in S['stack']
    if i < k:
        return v not in S['stack']
    return i == k and S['_line'] == 12   # 刚同归于尽：r 已爆炸


def _txt(S):
    st = S.get('stack')
    if st is None:
        return '同向永不相撞 → 结果必然是「若干负数」在左、「若干正数」在右'
    m = sum(1 for v in st if v < 0)
    n = len(st) - m
    return f'栈里现在：`{m}` 个向左 ←（在前）+ `{n}` 个向右 →（在后）'


def _if5(S, B, ret):
    if S.r > 0:
        return f'`r = {S.r}` 是正数：向右飞，左边的碰不到它 → 压栈，等后面的负数来考察'
    return f'`r = {S.r}` 是负数：向左飞 → 要考察左侧最近的、幸存的正数行星'


def _wh(S, B, ret):
    if not S.stack:
        return '栈空：左侧没有幸存的行星可撞 → 退出 while'
    t = S.stack[-1]
    if t < 0:
        return f'栈顶 `{t}` 是负数（也向左飞）→ 不会相撞，退出 while'
    if t < -S.r:
        return f'栈顶 `{t}` < `|r| = {-S.r}`：栈顶更小 → ==栈顶被撞毁==，进入循环体'
    return f'栈顶 `{t}` ≥ `|r| = {-S.r}`：栈顶撞不毁，退出 while'


def _if10(S, B, ret):
    if S.stack and S.stack[-1] > 0:
        return f'栈顶 `{S.stack[-1]}` 是正数，且 ≥ `|r| = {-S.r}` → 要看是同归于尽，还是 r 被撞毁'
    return '栈空，或栈顶是负数 → r 没有对手，==幸存== → 走 `else` 压栈'


def _if11(S, B, ret):
    t = S.stack[-1]
    if t == -S.r:
        return f'栈顶 `{t}` == `|r| = {-S.r}` → 大小相等，==两颗都撞毁=='
    return f'栈顶 `{t}` > `|r| = {-S.r}` → ==r 被撞毁==，栈不用动，直接看下一颗'


CONFIG = dict(
    num=735, title='小行星碰撞', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='栈 · 只看左侧最近的幸存正数',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def asteroidCollision(self, asteroids):
        stack = []
        for r in asteroids:
            if r > 0:
                stack.append(r)
            else:
                while stack and stack[-1] > 0 and stack[-1] < -r:
                    stack.pop()
                if stack and stack[-1] > 0:
                    if stack[-1] == -r:
                        stack.pop()
                else:
                    stack.append(r)

        return stack
''',
    call=f'Solution().asteroidCollision({AST})',
    expect=[-2, 6],
    views=[
        dict(type='array', var='asteroids', label='asteroids（青 = 向右 →，橙 = 向左 ←，灰 = 已撞毁）', cell=100,
             pointers={_idx: 'blue'}, pointer_labels={_idx: 'r'},
             color=lambda S, i, v: 'cyan' if v > 0 else 'orange', dim=_dim),
        dict(type='stack', var='stack', label='stack（幸存的小行星，→ 向右 / ← 向左）', h=180, font=36, fmt=_fmt),
        dict(type='text', fn=_txt, size=28, h=110),
    ],
    watch=[('r', 'r', 'blue'),
           ('栈顶', lambda S: S['stack'][-1] if S.get('stack') and S['_line'] in (8, 9, 10, 11, 12) else None, 'pink'),
           ('stack', 'stack', 'green')],
    captions={
        'stack = []': '栈存==幸存==的小行星。先想清楚：同向不会撞，所以答案必是「负数在左、正数在右」',
        'for r in asteroids': lambda S, B, ret: ('扫描完毕，退出循环' if 'r' in B and B['r'] == S.r
                                                  else f'从左往右扫描，考察 `r = {S.r}`'),
        'if r > 0': _if5,
        6: '正数入栈，记下它的大小，继续往后看：`stack` = {stack}',
        'while stack and stack[-1] > 0': _wh,
        9: '栈顶 `{B.stack[-1]}` 被撞毁，弹出；重复检查新的栈顶，`stack` = {stack}',
        'if stack and stack[-1] > 0': _if10,
        'if stack[-1] == -r': _if11,
        12: '同归于尽：弹出栈顶 `{B.stack[-1]}`，`r` 也不入栈，`stack` = {stack}',
        14: '`r = {r}` 幸存，压入栈：`stack` = {stack}',
        'return stack': '遍历完成，栈就是最终答案 =={ret}==',
    },
    cards=dict(
        one_liner='同向不相撞，反向必相撞：负数只需和左侧最近的幸存正数比',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组的正负表示方向，绝对值表示大小，速度相同；相撞时小的爆炸，一样大同归于尽',
                 '同向永远不会相撞，求碰撞后剩下的行星',
                 '本视频：`[8,3,-5,4,-8,-2,6]` → `[-2,6]`'],
        quote='最终答案必然是m个负数，然后n个正数这种形式，这里的m和n都可以为0。',
        quote_src='—— yiduobo 题解原文',
        idea=['同向永不相撞 → 答案 = 先若干==负数==，后若干==正数==',
              '从左往右扫：正数压栈；负数去考察左侧==最近且幸存==的正数 → 用栈',
              '负数 `r` 对栈顶：栈顶更小 → 弹出继续；相等 → 同归于尽；栈顶更大 → `r` 被撞毁'],
        result='栈里剩 `[-2, 6]`：负数在左、正数在右，正是 m 个负数 + n 个正数 ✓',
        summary=['时间 `O(n)`，空间 `O(n)`：每颗至多入栈、出栈一次',
                 'while 只在栈顶==严格小于== `|r|` 时弹出；相等和更大的情况留到 while 之后分别处理',
                 'while 后要再判一次 `stack and stack[-1] > 0`：栈空或栈顶是负数时，`r` 才能入栈',
                 '原文为 Python 2 风格写法，在 Python 3 下无需修改（只去掉了 def 后的空行）',
                 '对比灵神：灵神用两个独立 if + while-else；yiduobo 把「严格小于」写进 while 条件'],
    ),
)
