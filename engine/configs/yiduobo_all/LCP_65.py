def _num(S):
    return S['_inner'].get('num')


def _txt(S):
    if 'left' not in S:
        return '二分「整体不适宜度」的上界 `mid`：能构造出所有前缀和落在 `[0, mid]` 的方案吗？'
    n = _num(S)
    base = f'二分区间 `[{S["left"]}, {S["right"]}]`'
    if 'mid' in S:
        base += f'，试 `mid = {S["mid"]}`'
    if n is not None and 'op' in S['_inner'] and 'g' in S['_inner']:
        base += f'；`num = {n}`'
    return base


CONFIG = dict(
    num='LCP 65', title='舒适的湿度', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='二分答案 + 前缀和范围可达性 DP',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def unSuitability(self, operate):

        n = len(operate)

        ma = max(operate)

        def check(v):
            g = [True] * (v + 1)
            for op in operate:
                f = [False] * (v + 1)
                for num in range(mid + 1):
                    if g[num]:
                        if num + op <= mid:
                            f[num + op] = True
                        if num >= op:
                            f[num - op] = True
                
                g = f[:]
            
            for num in range(mid + 1):
                if f[num]:
                    return True
            
            return False

        left = 1
        right = ma + ma
        while left < right:
            mid = (left + right) >> 1
            if check(mid):
                right = mid
            else:
                left = mid + 1
        
        return left
''',
    call='Solution().unSuitability([2, 2, 1])',
    expect=2,
    skip=['for num in range', 'if g[num]', 'ma = max', 'n = len'],
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var='operate', label='operate（每个数可正可负）', cell=64, h=120,
             color=lambda S, i, v: 'blue' if 'op' in S['_inner'] and i == S['operate'].index(S['_inner']['op']) else None),
        dict(type='array', var=lambda S: S['_inner'].get('g'), label='g[num]：上一步，前缀和能停在 num 吗（绿 = 能）', cell=56, h=150,
             pointers={_num: 'pink'}, pointer_labels={_num: 'num'},
             color=lambda S, i, v: 'green' if v is True else None, dim=lambda S, i, v: v is False),
        dict(type='array', var=lambda S: S['_inner'].get('f'), label='f[num]：加入 op 之后能停在哪（绿 = 能）', cell=56, h=150,
             color=lambda S, i, v: 'green' if v is True else None, dim=lambda S, i, v: v is False),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'),
           ('op', lambda S: S['_inner'].get('op'), 'cyan')],
    captions={
        'right = ma + ma': '上界 `right = 2 × max = {right}`：前缀和为正就放负数、为负就放正数，前缀和绝对值不超过 `max`，极差不超过 `2max`',
        'left = 1': '下界 `left = 1`，答案一定在 `[{left}, {right}]`',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`，区间还没缩成一点，继续二分' if S.left < S.right
                                               else f'`left = right = {S.left}`：区间缩成一点，就是答案'),
        'mid = (left': '`mid = ({left} + {right}) >> 1 = {mid}`：试试能不能把极差压到 `{mid}` 以内',
        'for op in': '`for op in operate`：逐个处理指令，每个数可以选正或负（当前 `op = {op}`）',
        'g = [True]': '枚举数组最前面补的一项 `−x`：等价于==起点在 `0..mid` 任意位置==，所以 `g` 全为 True',
        'f = [False]': '放入 `op = {op}`（可正可负）：`f` 记录放完它之后，前缀和还能停在哪些位置',
        'if num + op <= mid': lambda S, B, r: (f'`num = {S.num}`，取正：`{S.num} + {S.op} = {S.num + S.op}` ≤ `mid = {S.mid}` → 没出界，可以停在这里'
                                               if S.num + S.op <= S.mid else f'`num = {S.num}`，取正：`{S.num} + {S.op} = {S.num + S.op}` > `mid = {S.mid}` → 超出上界，这条路不行'),
        'f[num + op] = True': '`f[{num + op}] = True`：前缀和可以停在 {num + op}',
        'if num >= op': lambda S, B, r: (f'`num = {S.num}`，取负：`{S.num} − {S.op} = {S.num - S.op}` ≥ 0 → 没掉出下界，可以停在这里'
                                         if S.num >= S.op else f'`num = {S.num}`，取负：`{S.num} < {S.op}` 会掉到 0 以下 → 这条路不行'),
        'f[num - op] = True': '`f[{num - op}] = True`：前缀和可以停在 {num - op}',
        'g = f[:]': '这一个数放完：`g` 更新为 `f`，下一个数从这些位置出发',
        'if f[num]': lambda S, B, r: (f'`f[{S.num}]` 为真：最后停得下来，说明 ==能构造== → 返回 True' if S.f[S.num]
                                      else f'`f[{S.num}]` 为假，看下一个位置'),
        'return True': '`mid = {mid}` 可行：答案 ≤ `mid`，==右边界收到 mid==',
        'return False': '`mid = {mid}` 不可行：答案 > `mid`',
        'right = mid': '可行 → `right = {right}`（往小的方向找）',
        'left = mid + 1': '不可行 → `left = {left}`（答案更大）',
        'return left': '`left = right = {left}`：最小的整体不适宜度',
    },
    max_steps=58,
    cards=dict(
        one_liner='二分答案：能否让所有前缀和落进长为 mid 的区间',
        complexity='时间 `O(n·U·log U)`，空间 `O(U)`',
        problem=['每条指令可以取正或负，所有连续段之和的绝对值取最大，叫「整体不适宜度」',
                 '求最小的整体不适宜度',
                 '示例：`[5,3,7]` → `8`；本视频：`[2,2,1]` → `2`'],
        quote='这个最小值越大，数组就越好构造，那么在这里可以二分答案，然后将问题转化成判断当前能否构造出一个数组使得各子数组之和绝对值中的最大值小于这个二分的mid。',
        quote_src='—— yiduobo 题解原文',
        idea=['子数组和的最大绝对值 = ==最大前缀和 − 最小前缀和==',
              '前缀和要落在长为 `mid` 的区间里：把起点放在 `0..mid` 任意位置，区间就固定为 `[0, mid]`',
              '`g[num]` 表示能否停在 `num`：每个数 `num+op` 或 `num-op`，不出界就可达'],
        summary=['时间 `O(n·U·log U)`，`U = max(operate)`，上界取 `2U`',
                 '`check` 里循环用的是外层的 `mid`（和参数 `v` 同值），原文如此',
                 '判定只看最后一行 `f` 是否有任何位置可达',
                 '对比灵神：他直接 DP 记录「极差」的最小值，不用二分'],
    ),
)
