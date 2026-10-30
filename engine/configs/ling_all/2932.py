CONFIG = dict(
    num=2932, title='找出强数对的最大异或值 I', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='排序 + 逐位试填（哈希表）', tags=[],
    code='''
class Solution:
    def maximumStrongPairXor(self, nums: List[int]) -> int:
        nums.sort()
        ans = mask = 0
        high_bit = nums[-1].bit_length() - 1
        for i in range(high_bit, -1, -1):  # 从最高位开始枚举
            mask |= 1 << i
            new_ans = ans | (1 << i)  # 这个比特位可以是 1 吗？
            d = {}
            for y in nums:
                mask_y = y & mask  # 低于 i 的比特位置为 0
                if new_ans ^ mask_y in d and d[new_ans ^ mask_y] * 2 >= y:
                    ans = new_ans  # 这个比特位可以是 1
                    break
                d[mask_y] = y
        return ans
''',
    call='Solution().maximumStrongPairXor([1,2,3,4,5])',
    expect=7,
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue'}, label='nums（已排序）',
             color=lambda S, k, v: 'yellow' if 'y' in S and S['y'] == v and S.get('_line', 0) >= 9 else None, h=200),
        dict(type='map', var='d', fmt=lambda k, v: f'{k:03b} → {v}', label='d：高位 → 最大的 nums[i]', h=250),
        dict(type='text', size=38, h=100, fn=lambda S: (
            f"`ans = {S['ans']:03b}`，`mask = {S['mask']:03b}`" + (f"，试填 `new_ans = {S['new_ans']:03b}`" if 'new_ans' in S else '')
            if 'mask' in S else '')),
    ],
    watch=['i', 'y', ('mask', 'mask', 'cyan'), ('new_ans', 'new_ans', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'nums.sort()': '答案与顺序无关，先排序：这样后面扫到的 `x` 一定不大于 `y`',
        'high_bit =': '最大数 `{nums[-1]}` 的最高位是第 `{high_bit}` 位，从这位开始逐位决定答案',
        'mask |= 1 << i': '只看高于等于第 `{i}` 位的比特：`mask = {mask:03b}`',
        'new_ans = ': '试探：答案的第 `{i}` 位能是 1 吗？`new_ans = {new_ans:03b}`',
        'd = {}': '清空哈希表，准备记录 `y` 的高位',
        'mask_y = ': '`y = {y}` 只保留高位：`mask_y = {mask_y:03b}`',
        'if new_ans ^ mask_y in d': lambda S, B, r: (
            f'需要找 `x` 使 `x 的高位 = new_ans ^ mask_y = {S.new_ans ^ S.mask_y:03b}`，且强数对 `2x >= y`：'
            + (f'找到 `x = {S.d[S.new_ans ^ S.mask_y]}`，`{S.d[S.new_ans ^ S.mask_y]*2} >= {S.y}` → 成立'
               if (S.new_ans ^ S.mask_y) in S.d and S.d[S.new_ans ^ S.mask_y] * 2 >= S.y
               else ('哈希表里有，但 `2x < y` 不是强数对' if (S.new_ans ^ S.mask_y) in S.d else '哈希表里还没有'))),
        'ans = new_ans': '这一位可以是 1：`ans = {ans:03b}`，==不用再看后面的 y==，直接 break',
        'd[mask_y] = y': '记录 `d[{mask_y:03b}] = {y}`：排好序，后来的 `y` 更大，==保留最大的 x 最容易满足 2x >= y==',
        'return ans': '每一位都试过了 → 最大异或值 `{ret}`',
    },
    skip=['d = {}'],
    max_steps=80,
    cards=dict(
        one_liner='排序后从高位往低位试：这一位能填 1 就填',
        complexity='时间 `O(n log n + n log U)`，空间 `O(n)`',
        problem=['强数对：`|x − y| <= min(x, y)`，可选同一个数两次',
                 '在所有强数对里求最大的 `x XOR y`',
                 '示例：`[1,2,3,4,5]` → `7`（`3 XOR 4`）'],
        quote='把 hashset 改成 hashmap，一边遍历数组，一边记录每个 key 对应的最大的 nums[i]。由于数组已经排好序，只要 2x≥y，就说明这个比特位可以是 1。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['排序后设 `x <= y`，强数对条件化简为 `2x >= y`',
              '逐位试填：这一位填 1，需要某个 `x` 的高位等于 `new_ans ^ y 的高位`',
              '哈希表存高位对应的最大 `x`，一边扫一边查'],
        summary=['时间 `O(n log n + n log U)`，空间 `O(n)`',
                 '题解还给了方法一：0-1 trie + 滑动窗口，这里演示的是方法二',
                 '易错：`new_ans ^ mask_y in d` 之后还要检查 `2x >= y`',
                 '同类题：2935（本题加强版，数据更大）'],
    ),
)
