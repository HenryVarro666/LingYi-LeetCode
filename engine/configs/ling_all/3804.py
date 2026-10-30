def _sub(S):
    nums = S['nums']
    if 'i' not in S:
        return None
    return nums, S['i']


CONFIG = dict(
    num=3804, title='中心子数组的数量', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举子数组 + 哈希集合',
    tags=[],
    code='''
class Solution:
    def centeredSubarrays(self, nums: List[int]) -> int:
        ans = 0
        for i in range(len(nums)):
            st = set()
            s = 0
            for x in nums[i:]:
                st.add(x)
                s += x
                if s in st:
                    ans += 1
        return ans
''',
    call='Solution().centeredSubarrays([-1, 1, 0])',
    expect=5,
    views=[
        dict(type='array', var='nums', h=230, cell=90,
             pointers={'i': 'blue'},
             label='nums（i = 当前左端点）'),
        dict(type='set', var='st', h=170, fmt=lambda x: str(x), label='st：子数组里的元素'),
        dict(type='text', size=32, fn=lambda S: (f"子数组和 `s = {S['s']}`，`{S['s']} in st` → =={'是' if S['s'] in S['st'] else '否'}==" if 's' in S and S.get('st') and S['_line'] in (9, 10, 11) else '')),
    ],
    watch=['i', 'x', ('s', 's', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'st = set()': '换一个左端点 `i = {i}`：集合清空，子数组和从 0 开始',
        'st.add': '右端点右移：把 `{x}` 加入集合，子数组 `nums[{i}..]` 的元素有 `{sorted(st)}`',
        6: '子数组和 `s` 清零，重新累加',
        's += x': '子数组和更新：`s` = =={s}==',
        'if s in st': lambda S, B, r: (f'`{S.s}` 在 `{sorted(S.st)}` 里 → 和等于某个元素，是中心子数组' if S.s in S.st
                                       else f'`{S.s}` 不在 `{sorted(S.st)}` 里 → 不是中心子数组'),
        'ans += 1': '又找到一个中心子数组：`ans` = =={ans}==',
    },
    cards=dict(
        one_liner='枚举左端点，右端点边扩边维护「元素集合」和「子数组和」',
        complexity='时间 `O(n²)`，空间 `O(n)`',
        problem=['子数组的和 ==等于== 其中至少一个元素 → 中心子数组',
                 '求中心子数组的个数，`n ≤ 500`',
                 '示例：`[-1,1,0]` → `5`'],
        quote='写个二重循环，枚举子数组的左端点和右端点。在枚举右端点的同时，用一个哈希集合记录子数组中的元素，用一个变量 s 维护子数组和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['外层枚举左端点 `i`，内层枚举右端点，所以每个子数组只处理一次',
              '右端点右移一格，集合和子数组和都是 ==O(1) 增量更新==',
              '判断 `s in st` 就知道和是否等于某个元素'],
        summary=['时间 `O(n²)`，空间 `O(n)`',
                 '易错：换左端点时 `st` 和 `s` 都要重置',
                 '单元素子数组一定满足（和就是它自己），所以答案至少是 `n`',
                 '`nums[i:]` 会复制切片，对 n ≤ 500 没问题'],
    ),
)
