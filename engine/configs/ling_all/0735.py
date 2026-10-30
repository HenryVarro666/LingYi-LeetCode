AST = [3, 5, -6, 4, -1, 2, -2]   # 各元素互不相同，可用 index 反推当前下标


def _idx(S):
    if 'x' not in S or S['_line'] == 16:
        return -1
    return S['asteroids'].index(S['x'])


def _fmt(v):
    return f'{v}→' if v > 0 else f'←{-v}'


def _dim(S, i, v):
    k = _idx(S)
    if k < 0:
        return i >= 0 and 'x' in S and S['_line'] == 16 and v not in S['st']
    if i < k:
        return v not in S['st']
    return i == k and S['_line'] == 13   # 刚执行 break：x 已爆炸


def _txt(S):
    if 'x' not in S:
        return '正数向右 →，负数向左 ←；只有「向右在左、向左在右」才会相撞'
    x = S['x']
    if S['_line'] == 16:
        return '栈里剩下的就是答案：左边若干向左的，右边若干向右的'
    if x > 0:
        return f'`x = {x}` 向右 →：左边没有谁能撞到它，直接入栈'
    return f'`x = {x}` 向左 ←：只会撞上栈顶==向右==的小行星，撞到爆炸或没得撞为止'


def _if5(S, B, ret):
    if S.x > 0:
        return f'`x = {S.x} > 0`：==向右== → 它只可能被后面向左的撞上，先入栈等着'
    return f'`x = {S.x}`：==向左== → 要去撞左边最近的、向右的小行星'


def _wh(S, B, ret):
    if S.st and S.st[-1] > 0:
        return f'栈顶 `{S.st[-1]}` 向右，`x = {S.x}` 向左 → ==相撞=='
    if not S.st:
        return '栈空了，左边没有小行星可撞 → 循环正常结束（没有 break）'
    return f'栈顶 `{S.st[-1]}` 也向左，背道而驰永不相撞 → 循环正常结束（没有 break）'


def _if10(S, B, ret):
    if S.top <= -S.x:
        return f'栈顶 `{S.top}` ≤ `|x| = {-S.x}`：栈顶更小（或一样大）→ ==栈顶爆炸=='
    return f'栈顶 `{S.top}` > `|x| = {-S.x}`：栈顶更大 → 栈顶不会爆炸'


def _if12(S, B, ret):
    if S.top > -S.x:
        return f'栈顶 `{S.top}` > `|x| = {-S.x}` → x 被撞碎，==x 爆炸=='
    if S.top == -S.x:
        return f'栈顶 `{S.top}` == `|x| = {-S.x}` → 大小相同，==同归于尽==（栈顶刚才已弹出）'
    return f'栈顶 `{S.top}` < `|x| = {-S.x}` → x 毫发无伤，回到 while 继续撞下一个栈顶'


CONFIG = dict(
    num=735, title='小行星碰撞', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='栈 · 邻项消除',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        st = []
        for x in asteroids:
            if x > 0:  # x 向右
                st.append(x)
                continue
            while st and st[-1] > 0:  # 栈顶小行星向右
                top = st[-1]
                if top <= -x:  # 栈顶小行星爆炸
                    st.pop()
                if top >= -x:  # x 爆炸
                    break
            else:  # while 没有 break，说明 x 没有爆炸
                st.append(x)
        return st
''',
    call=f'Solution().asteroidCollision({AST})',
    expect=[-6, 4],
    views=[
        dict(type='array', var='asteroids', label='asteroids（青 = 向右 →，橙 = 向左 ←，灰 = 已爆炸）', cell=100,
             pointers={_idx: 'blue'}, pointer_labels={_idx: 'x'},
             color=lambda S, i, v: 'cyan' if v > 0 else 'orange', dim=_dim),
        dict(type='stack', var='st', label='st（还活着的小行星，→ 向右 / ← 向左）', h=180, font=36, fmt=_fmt),
        dict(type='text', fn=_txt, size=28, h=110),
    ],
    watch=[('x', 'x', 'blue'), ('top', lambda S: S['top'] if S['_line'] in (10, 11, 12, 13) else None, 'pink'), ('st', 'st', 'green')],
    skip=['continue'],
    captions={
        'st = []': '栈里存==还活着==的小行星，从左往右一颗颗处理',
        'for x in asteroids': lambda S, B, ret: ('全部处理完毕，退出循环' if 'x' in B and B['x'] == S.x
                                                 else f'取下一颗小行星 `x = {S.x}`'),
        'if x > 0': _if5,
        6: '向右的小行星直接入栈：`st` = {st}',
        'while st and st[-1] > 0': _wh,
        'top = st[-1]': '先记下栈顶 `top = {top}`：下面 `pop` 之后还要拿它和 `x` 比大小',
        'if top <= -x': _if10,
        'st.pop()': '栈顶小行星 `{top}` 爆炸，弹出；栈剩 `{st}`',
        'if top >= -x': _if12,
        'break': '`x = {x}` 已经爆炸 → ==break== 跳出 while，且==不会==执行 else，x 不入栈',
        15: 'while 正常结束、没有 break → ==x 活了下来==，入栈：`st` = {st}',
        'return st': '栈里剩下的就是碰撞后的结果 =={ret}==',
    },
    cards=dict(
        one_liner='向左的 x 不断撞掉栈顶更小的向右者；撞不动或被撞碎才停',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['正数向右飞、负数向左飞，绝对值是大小；相撞时小的爆炸，一样大同归于尽，同向永不相撞',
                 '示例：`[3,5,-6,2,-1,4]` → `[-6,2,4]`',
                 '本视频用 `[3,5,-6,4,-1,2,-2]` → `[-6,4]`，三种碰撞结果都会出现'],
        quote='遍历到一颗向左的小行星时，我们需要找到左边最近的未爆炸的小行星。这可以用一个栈维护。',
        quote_src='—— 灵茶山艾府题解',
        idea=['向右的小行星 ==直接入栈==，它只会被后面向左的撞上',
              '向左的 `x`：栈顶向右且 `≤ |x|` → 栈顶爆炸弹出；栈顶 `≥ |x|` → `x` 爆炸',
              '内层 `while` 里 ==break 表示 x 爆炸==；没 break（栈空或栈顶向左）才把 `x` 入栈'],
        result='碰撞后只剩 `[-6, 4]`：`-6` 向左飞出，`4` 向右飞走，再也撞不到 ✓',
        after=[dict(heading='为什么二重循环仍是 O(n)', lines=[
            '每颗小行星至多入栈一次、出栈一次',
            '内层 `while` 的总次数 ≤ 总出栈次数 + n（每个 x 最后一轮不出栈）',
            '所以总时间是 `O(n)`，不是 `O(n²)`'])],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`top == |x|` 时==两颗都爆炸==：先 `pop`，再因 `top >= -x` 而 `break`',
                 '两个判断是==两个独立的 if==，不是 elif：相等时两个都要成立',
                 'while-else：只有没 break 才执行 else；栈空时也要把 x 入栈',
                 '结果必然是「若干向左的 + 若干向右的」'],
    ),
)
