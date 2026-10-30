def _merged_color(S, i, v):
    if S.get('_line') in (21, 23) and 'index' in S and i == S['index']:
        return 'blue'
    return None


def _txt(S):
    if 'index' in S and 'a' in S:
        return f"`a` = 与开头同奇偶结尾的最大得分 =={S['a']}==；`b` = 另一种奇偶结尾 =={S['b']}=="
    if 'merged_nums' in S and 'left' in S and S['left'] >= len(S['nums']):
        return f"合并完成：`merged_nums = {S['merged_nums']}`，奇偶交替出现"
    if 'now' in S:
        return f"当前这一段同奇偶的数加起来 `now = {S['now']}`"
    return '同奇偶的连续一段 ==要么全要要么全不要==，先合并成一个数'


CONFIG = dict(
    num=2786, title='访问数组中的位置使分数最大', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='合并同奇偶段 + 两状态 DP',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1733'],
    code='''
class Solution(object):
    def maxScore(self, nums, x):

        merged_nums = []
        left = 0
        while left < len(nums):
            now = nums[left]
            right = left + 1
            while right < len(nums) and (nums[left] + nums[right]) % 2 == 0:
                now += nums[right]
                right += 1
            
            merged_nums.append(now)
            left = right
        
        if len(merged_nums) == 1:
            return merged_nums[0]
        
        a, b = merged_nums[0], merged_nums[0] + merged_nums[1] - x
        for index in range(2, len(merged_nums)):
            v = merged_nums[index]
            if index % 2 == 0:
                a, b = max(a + v, b + v - x), b
            else:
                a, b = a, max(a + v - x, b + v)

        return max(a, b)
''',
    call='Solution().maxScore([2,4,3,5,6,1,4], 5)',
    expect=16,
    views=[
        dict(type='array', var='nums', label='nums', h=170, cell=84,
             pointers={'left': 'blue', 'right': 'pink'},
             window=('left', 'right - 1'),
             color=lambda S, i, v: ('cyan' if v % 2 == 0 else 'orange') if 'left' in S and S['left'] <= i < S.get('right', S['left'] + 1) and S.get('_line', 0) < 14 else None),
        dict(type='array', var='merged_nums', label='merged_nums（奇偶交替）', h=170, cell=96,
             color=lambda S, i, v: 'blue' if S.get('_line', 0) >= 20 and S.get('index') == i else None),
        dict(type='text', fn=_txt, size=26, h=90),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('now', 'now', 'yellow'), ('a', 'a', 'cyan'), ('b', 'b', 'orange'), ('x', 'x', 'red')],
    captions={
        'merged_nums = []': '先把数组里==连续同奇偶==的一段合并成一个数',
        'now = nums[left]': '新的一段从 `left = {left}` 开始，`now = {now}`',
        'while right < len(nums) and': lambda S, B, r: (f'`nums[{S.left}] + nums[{S.right}]` = `{S.nums[S.left]} + {S.nums[S.right]}` 是偶数：同奇偶 → ==并入这一段==' if S.right < len(S.nums) and (S.nums[S.left] + S.nums[S.right]) % 2 == 0
                                                         else '这一段到头了（越界或奇偶变了）'),
        'now += nums[right]': '同奇偶，全是正数，一起要：`now` → {now}',
        'right += 1': '`right` → {right}',
        'merged_nums.append': '这一段合成一个数：`merged_nums = {merged_nums}`',
        'left = right': '下一段从 `{right}` 开始',
        'if len(merged_nums) == 1': '只剩 1 段 → 全部同奇偶，没有扣分，直接返回总和' if False else '只有一段说明全同奇偶，不会扣分；否则要 DP',
        'a, b = merged_nums[0]': ('`a` = 只选第一段 `{a}`；`b` = 必须选第一段再跳到第二段（奇偶不同扣 `x`）：'
                                  '`{merged_nums[0]} + {merged_nums[1]} − {x} = {b}`'),
        'for index in range': lambda S, B, r: ('合并后的数组扫完了' if B.get('index') == S.get('index') and 'index' in B else f'`index = {S.index}`：偶数下标与首段同奇偶，更新 `a`；奇数更新 `b`'),
        'v = merged_nums[index]': '当前这一段的和 `v = {v}`',
        'if index % 2 == 0': '`index = {index}` 是{"偶" if index % 2 == 0 else "奇"}数：{"与首段同奇偶，更新 a" if index % 2 == 0 else "与首段不同奇偶，更新 b"}',
        'a, b = max(a + v, b + v - x), b': ('`a = max({B.a} + {v}, {B.b} + {v} − {x}) = =={a}==`：接同奇偶不扣分，从另一种奇偶过来扣 `x`；`b` 不变'),
        'a, b = a, max': ('`b = max({B.a} + {v} − {x}, {B.b} + {v}) = =={b}==`：从 a 过来扣 `x`，接 b 不扣；`a` 不变'),
        'return max(a, b)': '两种结尾取大：`max({a}, {b}) = {max(a, b)}`',
    },
    cards=dict(
        one_liner='正数下同奇偶的一段要么全要，先合并，再做奇偶交替的 DP',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['从下标 0 出发只能往右跳，得分 `nums[i]`',
                 '相邻两次访问的奇偶性不同要扣 `x`',
                 '示例：`[2,4,3,5,6,1,4], x=5` → `16`'],
        quote='对于数组中所有同奇偶的子数组，这些子数组要么全要，要么全都不要。',
        quote_src='—— yiduobo 题解原文',
        idea=['全是正数：选了同奇偶段里的一个，再多选其他几个不会扣分，只会加分',
              '合并后奇偶交替；`a`/`b` 分别表示以与首段同奇偶 / 不同奇偶结尾的最大得分',
              '偶数下标更新 `a`，奇数下标更新 `b`，换奇偶扣 `x`'],
        summary=['时间 `O(n)`，空间 `O(n)`（`merged_nums`）',
                 '`b` 的初值必须选首段：`merged_nums[0] + merged_nums[1] − x`',
                 '只有一段时直接返回总和',
                 '原文为 Python 2 写法，无需改动即可在 Python 3 运行',
                 '对比灵神：灵神倒着递推两个状态，不合并；这里先压缩成交替数组'],
    ),
)
