CONFIG = dict(
    num=1550, title='存在连续三个奇数的数组', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='枚举右端点看三连',
    code='''
class Solution:
    def threeConsecutiveOdds(self, arr: List[int]) -> bool:
        for i in range(2, len(arr)):
            if arr[i - 2] % 2 and arr[i - 1] % 2 and arr[i] % 2:
                return True
        return False
''',
    call='Solution().threeConsecutiveOdds([1,2,34,3,4,5,7,23,12])',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: (f"看 `arr[{S['i']-2}..{S['i']}]` = {S['arr'][S['i']-2:S['i']+1]}：奇偶 "
                                         + ' '.join('奇' if v % 2 else '偶' for v in S['arr'][S['i']-2:S['i']+1])) if 'i' in S else ''),
        dict(type='array', var='arr', h=300, window=('i-2', 'i'),
             color=lambda S, i, v: 'green' if v % 2 else None, label='arr（绿色 = 奇数，框 = 当前三个数）'),
    ],
    watch=[('i', 'i', 'blue')],
    captions={
        'for i in range': '枚举三连的右端点 `i = {i}`，看 `arr[i-2], arr[i-1], arr[i]`',
        'if arr[i - 2]': lambda S, B, r: (f'`{S.arr[S.i-2]}`、`{S.arr[S.i-1]}`、`{S.arr[S.i]}` 都是奇数 → ==成立==，找到三连奇' if all(v % 2 for v in S.arr[S.i-2:S.i+1])
                                           else f'`{S.arr[S.i-2]}`、`{S.arr[S.i-1]}`、`{S.arr[S.i]}` 里有偶数 → 不成立，继续右移'),
        'return True': '找到三连奇，直接返回 `True`',
        'return False': '枚举完都没有三连奇，返回 `False`',
    },
    cards=dict(
        one_liner='枚举右端点 i，看 arr[i-2..i] 是不是三个奇数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['判断数组里是否存在连续三个元素都是奇数',
                 '示例：`[2,6,4,1]` → `false`',
                 '本视频：`[1,2,34,3,4,5,7,23,12]` → `true`（`5,7,23`）'],
        quote='枚举 i=2,3,…,n-1，如果 arr[i-2],arr[i-1],arr[i] 都是奇数，返回 true。如果遍历结束也没有找到三连奇，返回 false。',
        quote_src='—— 灵茶山艾府题解',
        idea=['三个连续元素的窗口，右端点从 `2` 到 `n-1`',
              '`x % 2` 为 `1` 就是奇数，三个都为真才返回',
              '一旦找到立刻 `return True`，不用看后面'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：`i` 从 `2` 开始，否则 `arr[i-2]` 会越界或绕到末尾',
                 '写法二用 `any(...)` 生成器，逻辑完全一样',
                 '思考题：改成连续 `k` 个奇数，可维护连续奇数个数'],
    ),
)
