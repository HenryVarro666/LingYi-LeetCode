def _text(S):
    if 'mx' not in S:
        return '倒着遍历：`mx` 维护右侧（后缀）最大值，初始 `-1` 对应最后一个元素'
    if 'i' not in S:
        return f'`mx = {S["mx"]}`：最后一个元素右边没有数，所以初始是 `-1`'
    i, x, mx = S['i'], S.get('x'), S['mx']
    return f'下标 `{i}`：右侧最大 = ==`mx`==，替换后再把 `{x}` 并入 `mx`'


CONFIG = dict(
    num=1299, title='将每个元素替换为右侧最大元素', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='倒序遍历维护后缀最大值',
    code='''
class Solution:
    def replaceElements(self, arr: List[int]) -> List[int]:
        mx = -1
        for i in range(len(arr) - 1, -1, -1):
            x = arr[i]
            arr[i] = mx
            mx = max(mx, x)  # 维护后缀最大值
        return arr
''',
    call='Solution().replaceElements([17, 18, 5, 4, 6, 1])',
    expect=[18, 6, 6, 6, 1, -1],
    views=[
        dict(type='text', fn=_text, h=90),
        dict(type='array', var='arr', pointers={'i': 'blue'}, h=300, label='arr',
             dim=lambda S, i, v: 'i' in S and i > S['i'] and False,
             color=lambda S, i, v: 'green' if ('i' in S and i > S['i']) or ('i' in S and i == S['i'] and S['_line'] in (6, 7)) or S['_line'] == 8 else None),
    ],
    watch=['i', 'x', ('mx', 'mx', 'orange')],
    captions={
        'mx = -1': '`mx = -1`：最后一个元素右边没有数，要替换成 `-1`；这样初始化就==不用特判==最后一个',
        'for i in range': lambda S, B, r: ('`i` 已走过 0，全部替换完成' if ('i' in B and B.i == S.i and S.i == 0) else f'倒着走，下标 `i = {S.i}`：`mx` 恰好是 `arr[{S.i}+1:]` 的最大值'),
        'x = arr[i]': '先把原值 `{x}` 存到 `x`，马上要被覆盖',
        'arr[i] = mx': '替换：`arr[{i}] = mx = {mx}`（右侧最大值）',
        'mx = max': '再把 `{x}` 并入：`mx = max({B.mx}, {x}) = {mx}`；==必须在替换之后==，否则会包含自己',
        'return arr': '原地修改完成，返回 `{arr}`',
    },
    cards=dict(
        one_liner='倒着走：先替换，再把原值并入后缀最大值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 `arr[i]` 换成它右边的最大值，最后一个元素换成 `-1`',
                 '示例：`[17,18,5,4,6,1]` → `[18,6,6,6,1,-1]`',
                 '`[400]` → `[-1]`'],
        quote='倒着遍历 arr，这样可以 O(1) 维护最大值 mx。注意后两步不能反过来，因为要替换的最大值不能包含 arr[i]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['倒序遍历，`mx` 始终是已走过部分（即右侧）的最大值',
              '每步三件事：存 `x = arr[i]`、写 `arr[i] = mx`、更新 `mx = max(mx, x)`',
              '初始化 `mx = -1`，最后一个元素自然变成 `-1`'],
        summary=['时间 `O(n)`，空间 `O(1)`（原地修改）',
                 '易错：先更新 `mx` 再赋值，会把自己算进右侧最大',
                 '后缀最大值的经典技巧，接雨水等题也会用到'],
    ),
)
