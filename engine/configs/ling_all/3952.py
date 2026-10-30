def _seg(S):
    if 'i' not in S:
        return '每个 `0111…1` 是一段：段内恰有一个数不能选，贪心地不选最小的'
    return f"累计 `ans = {S['ans']}`；当前段最小值 `mn = {S['mn']}`"


CONFIG = dict(
    num=3952, title='下标覆盖处的最大总和', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='贪心 · 分组循环（0111..1 分段）',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1763'],
    code='''
class Solution:
    def maxTotal(self, nums: list[int], s: str) -> int:
        n = len(s)
        ans = mn = 0
        for i, x in enumerate(nums):
            if s[i] == '1':
                ans += x
                mn = min(mn, x)  # 维护这一段的最小值
                if i == n - 1 or s[i + 1] == '0':  # 遍历到了段的末尾
                    ans -= mn  # 段的最小值不选
            elif i < n - 1 and s[i + 1] == '1':  # 0111..11 段的开头
                ans += x
                mn = x
        return ans
''',
    call="Solution().maxTotal([9,3,5,2,7,4,6], '0110101')",
    expect=27,
    views=[
        dict(type='array', var='nums', label='nums', h=200, cell=86, pointers={'i': 'blue'},
             color=lambda S, i, v: ('blue' if i == S['i'] else None) if 'i' in S else None),
        dict(type='string', var='s', label='s（标记）', h=190, cell=86, pointers={'i': 'blue'},
             color=lambda S, i, v: ('green' if v == '1' else None)),
        dict(type='text', fn=_seg, size=26, h=80),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'cyan'), ('mn', 'mn', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = mn = 0': '`ans` 累计答案；`mn` 是当前段的最小值，初值 0（`s[0]=1` 时第一段可全选）',
        "if s[i] == '1'": lambda S, B, r: (f'`s[{S.i}] = 1`：这个位置有标记，属于当前段' if S.s[S.i] == '1'
                                          else f'`s[{S.i}] = 0`：没有标记，看它是不是新一段的开头'),
        'ans += x': '`nums[{i}] = {x}` 先算进来：`ans` → {ans}',
        'mn = min(mn, x)': '维护本段最小值：`mn = min({B.mn}, {x}) = {mn}`',
        'if i == n - 1': lambda S, B, r: ('到了段的末尾（右边是 0 或已到头）' if S.i == len(S.s) - 1 or S.s[S.i + 1] == '0'
                                         else '右边还是 1，这一段还没结束'),
        'ans -= mn': '段内恰有一个数不能选，贪心去掉最小的：`ans −= {mn}` → =={ans}==',
        'elif i < n - 1': lambda S, B, r: (f'`s[{S.i}] = 0` 且右边是 1：这是 `0111..1` 段的开头' if S.i < len(S.s) - 1 and S.s[S.i + 1] == '1'
                                          else f'`s[{S.i}] = 0` 且右边不是 1：这个 0 单独存在，什么也不做'),
        'mn = x': '新一段的最小值先设为开头的 `{x}`',
        'return ans': '答案 `{ans}`',
    },
    cards=dict(
        one_liner='每段 0111…1 恰有一个数选不到，不选最小的',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s[i]=1` 表示下标 `i` 有标记，每个标记至多向左移 1 次',
                 '被标记覆盖的下标，对应 `nums` 之和最大是多少',
                 '示例：`nums=[9,2,6,1], s="0101"` → `15`'],
        quote='每个 0111…11 可以视作一段。每一段恰好有一个 nums[i] 不能选，其余全选，所以贪心地，不选最小的 nums[i]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['标记只能左移一格：`0111` 变成 `1101`，覆盖的是除了某一个位置外的全部',
              '分组循环：段内累加，到段末减去最小值',
              '`s[0]=1` 时第一段可全选，最小值取 0（`nums` 非负）'],
        after=[dict(heading='其他写法', lines=['写法二倒序遍历：遇到 `s[i]=0` 就结算并重置 `mn`',
                                              '方法二：状态机 DP，`f0`/`f1` 表示有没有标记从右边移进来'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：段的开头是 `0`，它的 `nums` 也要算进去',
                 '`mn` 在段开头用 `mn = x` 重置，开头的 `1` 段靠初值 0 处理',
                 '延伸：标记可移动多次 → 3781 题'],
    ),
)
