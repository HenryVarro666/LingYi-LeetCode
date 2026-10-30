TESTS = [[1, 2, 1], [1, 3, 2, 1]]


def _just(S, j):
    return S.get('_line') == 6 and 'i' in S and j in (S['i'], S['i'] + S['n'])


CONFIG = dict(
    num=1929, title='数组串联', difficulty='Easy', category='普通数组',
    author='灵茶山艾府', technique='手动复制：ans[i] = ans[i+n] = x',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        n = len(nums)
        ans = [0] * (n * 2)
        for i, x in enumerate(nums):
            ans[i] = ans[i + n] = x
        return ans
''',
    call='[' + ', '.join(f'Solution().getConcatenation({t})' for t in TESTS) + ']',
    expect=[t * 2 for t in TESTS],
    views=[
        dict(type='text', fn=lambda S: (f"`ans[{S['i']}] = ans[{S['i']} + {S['n']}] = {S['x']}`：同一个 x ==一次写两格=="
                                        if S.get('_line') == 6 else
                                        '`ans` 的前半段 = nums，后半段 = nums（下标整体 +n）'), h=60),
        dict(type='array', var='nums', label='nums（蓝 = 当前 i）', h=200,
             pointers={'i': 'blue'},
             color=lambda S, i, v: 'blue' if i == S.get('i') else None),
        dict(type='array', var='ans', label='ans（长 2n；绿 = 这一步写入的两格，灰 = 还没填）', h=240,
             pointers={'i': 'blue', 'i + n': 'pink'}, pointer_labels={'i + n': 'i+n'},
             color=lambda S, j, v: 'green' if _just(S, j) else None,
             dim=lambda S, j, v: v == 0),
    ],
    watch=['n', ('i', 'i', 'blue'), 'x', ('i + n', 'i + n', 'pink')],
    captions={
        'n = len': '`n = len(nums) = {n}`',
        'ans = [0]': '先开好长为 `2n = {2 * n}` 的数组，全填 0',
        'for i, x': lambda S, B, r: (f'枚举 `i = {S.i}`，`x = nums[{S.i}] = {S.x}`' if S.get('i') != B.get('i') or 'i' not in B
                                     else '`nums` 枚举完，ans 已填满'),
        'ans[i] = ans[i + n]': '`x = {x}` 同时写到前半段 `ans[{i}]` 和后半段 `ans[{i + n}]`：==后半段下标 = i + n==',
        'return ans': lambda S, B, r: f'返回 =={r}==',
    },
    cards=dict(
        one_liner='后半段就是前半段平移 n：ans[i] = ans[i + n] = nums[i]',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计入）',
        problem=['给长为 `n` 的数组 `nums`，返回长为 `2n` 的数组 `ans`',
                 '要求 `ans[i] == nums[i]` 且 `ans[i + n] == nums[i]`，即两个 nums ==串联==',
                 '示例：`[1,2,1]` → `[1,2,1,1,2,1]`；`[1,3,2,1]` → `[1,3,2,1,1,3,2,1]`'],
        quote='创建一个长为 2n 的数组 ans，==手动把元素一个一个地填入 ans==。',
        quote_src='—— 灵茶山艾府题解（写法二）',
        idea=['ans 的前 n 格放 nums，后 n 格也放 nums',
              '`nums[i]` 在 ans 里出现两次：下标 `i` 和 ==下标 `i + n`==',
              '所以遍历一次 nums，每个 x 用连等式写两格'],
        summary=['时间 `O(n)`，空间 `O(1)`（返回值不计入）',
                 '写法一（库函数）：`return nums * 2`，或 `nums + nums`',
                 '易错：后半段下标是 `i + n` 而不是 `i + 1`；数组长度要开 `2n`',
                 '`a = b = x` 是 Python 连续赋值，两个位置拿到同一个值'],
    ),
)
