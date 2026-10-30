def _cmp(S):
    if 'p' not in S:
        return ''
    s1, s2, p, n = S['sensor1'], S['sensor2'], S['p'], len(S['sensor1'])
    if p >= n:
        return '两数组完全相同，无法判断'
    return (f"若 ==传感器 1 坏==：要求 `sensor1[{p}:{n-1}] = {s1[p:n-1]}` 等于 `sensor2[{p+1}:] = {s2[p+1:]}`；"
            f"若 ==传感器 2 坏==：要求 `sensor2[{p}:{n-1}] = {s2[p:n-1]}` 等于 `sensor1[{p+1}:] = {s1[p+1:]}`")


CONFIG = dict(
    num=1826, title='有缺陷的传感器', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='找首个差异 + 切片比较',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution(object):
    def badSensor(self, sensor1, sensor2):

        n = len(sensor1)
        p = 0
        while p < n and sensor1[p] == sensor2[p]:
            p += 1
        
        if p == n:
            return -1
        
        flag1 = False
        if sensor2[p] != sensor1[-1] and sensor1[p : n - 1] == sensor2[p + 1:]:
            flag1 = True
        
        flag2 = False
        if sensor1[p] != sensor2[-1] and sensor2[p : n - 1] == sensor1[p + 1:]:
            flag2 = True
        
        if flag1:
            if flag2:
                return -1
            else:
                return 1
        elif flag2:
            return 2
        else:
            return -1
''',
    call='Solution().badSensor([2,3,4,5], [2,1,3,4])',
    expect=1,
    views=[
        dict(type='array', var='sensor1', pointers={'p': 'blue'}, label='sensor1', h=230,
             color=lambda S, i, v: 'pink' if 'p' in S and i == S['p'] else None),
        dict(type='array', var='sensor2', pointers={'p': 'blue'}, label='sensor2', h=230,
             color=lambda S, i, v: 'pink' if 'p' in S and i == S['p'] else None),
        dict(type='text', fn=_cmp, size=26, h=150),
    ],
    watch=[('p', 'p', 'blue'), 'n', ('flag1', 'flag1', 'green'), ('flag2', 'flag2', 'orange')],
    captions={
        'p = 0': '`p` 从 0 开始，找两个数组==第一次不相等==的下标',
        'while p < n': lambda S, B, r: (f'`sensor1[{S.p}] = {S.sensor1[S.p]}` 与 `sensor2[{S.p}] = {S.sensor2[S.p]}` 相等 → 继续往后找'
                                         if S.p < S.n and S.sensor1[S.p] == S.sensor2[S.p]
                                         else (f'`sensor1[{S.p}] = {S.sensor1[S.p]}` ≠ `sensor2[{S.p}] = {S.sensor2[S.p]}`：==首个差异在 p = {S.p}==' if S.p < S.n else '一直相等，走到了末尾')),
        'p += 1': '这一位相同，肯定不是坏掉的位置，`p` → {p}',
        'if p == n': lambda S, B, r: ('`p == n`：两数组完全一样 → 无法判断哪个坏，返回 -1' if S.p == S.n
                                      else f'`p = {S.p} < n`：有差异，但还不知道是==哪个传感器==坏，要分别验证'),
        'if sensor2[p] != sensor1[-1]': lambda S, B, r: ('假设传感器 1 坏：它丢一个数、后面左移，则 `sensor1[p:n-1]` 应等于 `sensor2[p+1:]`，末位还要 ≠ `sensor2[p]`'
                                                         + f'：`{S.sensor2[S.p] != S.sensor1[-1]}` 且 `{S.sensor1[S.p:S.n-1] == S.sensor2[S.p+1:]}` → '
                                                         + ('==成立==' if S.sensor2[S.p] != S.sensor1[-1] and S.sensor1[S.p:S.n-1] == S.sensor2[S.p+1:] else '不成立')),
        'flag1 = True': '传感器 1 满足条件：`flag1 = True`',
        'if sensor1[p] != sensor2[-1]': lambda S, B, r: ('对称地假设传感器 2 坏：`sensor2[p:n-1]` 应等于 `sensor1[p+1:]`，末位 ≠ `sensor1[p]`'
                                                         + f'：`{S.sensor1[S.p] != S.sensor2[-1]}` 且 `{S.sensor2[S.p:S.n-1] == S.sensor1[S.p+1:]}` → '
                                                         + ('==成立==' if S.sensor1[S.p] != S.sensor2[-1] and S.sensor2[S.p:S.n-1] == S.sensor1[S.p+1:] else '不成立')),
        'flag2 = True': '传感器 2 满足条件：`flag2 = True`',
        'if flag1': '`flag1 = {flag1}`，`flag2 = {flag2}`：只有恰好一个成立才能确定',
        'elif flag2': '`flag1` 不成立，看 `flag2 = {flag2}`',
        'return 1': '只有传感器 1 满足 → 返回 ==1==',
        'return 2': '只有传感器 2 满足 → 返回 ==2==',
        'return -1': '两个都满足或都不满足 → 无法确定，返回 -1',
    },
    cards=dict(
        one_liner='先找首个差异，再对两个传感器分别验证“丢一个数”',
        complexity='时间 `O(n)`，空间 `O(n)`（切片）',
        problem=['两个传感器各采集 `n` 个数据，==至多一个==坏了：坏的那个从某处丢掉一个数据，后面整体左移，末尾补一个随机数',
                 '返回坏的传感器编号 `1` 或 `2`；无法确定或没有坏就返回 `-1`',
                 '示例：`[2,3,4,5]` 与 `[2,1,3,4]` → `1`'],
        quote='首先一趟遍历，找出两个数组中第一次数值不相等的下标p。……暂时还无法确定是哪个传感器出问题，因此需要分别进行校验。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据坏的位置一定在首个差异 `p`：之前都一样，没法坏',
              '若传感器 1 坏：`sensor1[p:n-1]` 必须等于 `sensor2[p+1:]`',
              '再要求被补的末位 `sensor1[-1]` 不等于 `sensor2[p]`，否则无法区分；两个传感器对称检查'],
        summary=['时间 `O(n)`，空间 `O(n)`（切片拷贝）',
                 '两个标志都成立或都不成立 → `-1`',
                 '易错：忘记检查末尾补的数与 `sensor2[p]` 是否不同',
                 '原文为 Python 2 风格，本题无需改动，可直接在 Python 3 运行'],
    ),
)
