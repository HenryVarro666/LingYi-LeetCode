CONFIG = dict(
    num=556, title='下一个更大元素 III', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='下一个排列',
    tags=[],
    code='''
class Solution(object):
    def nextGreaterElement(self, n):

        nums = []
        tmp = n
        while tmp:
            nums.append(tmp % 10)
            tmp //= 10
        nums.reverse()

        pos = 0
        for index in range(len(nums) - 1, 0, -1):
            if nums[index] > nums[index - 1]:
                pos = index
                break
        if pos == 0:
            for index in range(len(nums) // 2):
                tmp = nums[index]
                nums[index] = nums[len(nums) - index - 1]
                nums[len(nums) - index - 1] = tmp
        else:
            pos -= 1
            sawp_pos = None
            sawp_num = None
            for index in range(len(nums) - 1, pos, -1):
                if nums[index] > nums[pos]:
                    if sawp_num is None or sawp_num > nums[index]:
                        sawp_num = nums[index]
                        sawp_pos = index

            tmp = nums[pos]
            nums[pos] = nums[sawp_pos]
            nums[sawp_pos] = tmp

            for index in range((len(nums) - pos - 1) // 2):
                tmp = nums[pos + index + 1]
                nums[pos + index + 1] = nums[len(nums) - index - 1]
                nums[len(nums) - index - 1] = tmp

        res = 0
        for index in range(len(nums)):
            res = res * 10 + nums[index]
        if res > 2147483647 or res <= n:
            return -1
        return res
''',
    call='Solution().nextGreaterElement(12443)',
    expect=13244,
    views=[
        dict(type='array', var='nums', h=190, pointers={'pos': 'pink', 'index': 'blue', 'sawp_pos': 'green'},
             color=lambda S, i, v: 'pink' if ('sawp_pos' in S and i == S.get('pos')) else None),
        dict(type='text', size=30,
             fn=lambda S: ('数位排列：`' + ''.join(map(str, S['nums'])) + '`，pos = ' + str(S.get('pos', '')) + '（交换位置），index = ' + str(S.get('index', ''))) if 'nums' in S else ''),
    ],
    watch=[('n', 'n', 'text'), ('pos', 'pos', 'pink'), ('index', 'index', 'blue'), ('sawp_pos', 'sawp_pos', 'green'), ('res', 'res', 'orange')],
    captions={
        'nums.append': '取个位 `{tmp % 10}` 放进 `nums`：此时 `nums = {nums}`',
        'tmp //= 10': '去掉个位：`tmp = {tmp}`',
        'nums.reverse': '数位是倒着取的，翻转后 `nums = {nums}` 就是 n 的各位数字，当成一个排列',
        'if nums[index] > nums[index - 1]': '从右往左找第一处「上升」：`nums[{index}] = {nums[index]}` 与 `nums[{index-1}] = {nums[index-1]}`，前者更大吗？→ {nums[index] > nums[index - 1]}',
        14: '找到了：右边这段已经是降序（最大排列），要动的是前一位。`pos = {pos}`',
        'if pos == 0': '`pos = {pos}`：若一直没找到上升，整体是降序，已是最大排列，只能翻转（最终会返回 -1）。是吗？→ {pos == 0}',
        'pos -= 1': '真正要换的位置是上升处的前一位：`pos = {pos}`，值 `{nums[pos]}`',
        'if nums[index] > nums[pos]': '右半段里找比 `nums[pos] = {nums[pos]}` 大的数：`nums[{index}] = {nums[index]}` 是吗？→ {nums[index] > nums[pos]}',
        'if sawp_num is None': '要选 ==比它大的里面最小的==，这样增幅最小：现在最小候选 `{sawp_num}`，`nums[{index}] = {nums[index]}` 更小或还没候选吗？→ {sawp_num is None or sawp_num > nums[index]}',
        28: '更新候选：`sawp_num = {sawp_num}`，目前最小的更大数就是它',
        29: '记下它的位置：`sawp_pos = {sawp_pos}`，稍后用它和 `nums[pos]` 交换',
        'nums[pos] = nums[sawp_pos]': '把 `nums[pos]` 换成刚好比它大的数：`nums = {nums}`',
        'nums[sawp_pos] = tmp': '另一个位置放原来的小数：交换完成，`nums = {nums}`',
        'for index in range((len(nums) - pos - 1)': '换完后，pos 右边仍是降序；翻转成升序才是最小的，所以接下来翻转 pos 右侧',
        'nums[len(nums) - index - 1] = tmp': '一对数交换完成：`nums = {nums}`',
        'res = res * 10': '把数位拼回整数：`res = {res}`',
        'if res > 2147483647': '题目限制 32 位整数：`res = {res}`，超出范围或不比 n 大吗？→ {res > 2147483647 or res <= n}',
        'return res': '`res` 比 `n = {n}` 大，且在 int 范围内 → 返回 =={ret}==',
    },
    skip=['tmp = nums[index]', 'tmp = nums[pos + index + 1]', 'tmp //= 10', 'tmp = n', 'nums = []', 'res = 0', 'sawp_num = None', 'sawp_pos = None'],
    max_steps=110,
    cards=dict(
        one_liner='数位重排 = 求「下一个排列」，再检查范围',
        complexity='时间 `O(log n)`（数位个数），空间 `O(log n)`',
        problem=['给正整数 `n`，找到只用 `n` 的各位数字、==比 n 大的最小整数==',
                 '不存在，或结果超出 32 位整数，返回 `-1`',
                 '示例：`12443` → `13244`'],
        quote='如果将n的每一位分离出来，看成一个排列的话，题目实际上就是求下一个排列是什么。最后还需要判断其是否大于n，且是否在int范围之内。',
        quote_src='—— yiduobo 题解',
        idea=['先把 n 的每一位拆进 `nums`，当成一个排列',
              '从右往左找第一处 `nums[i] > nums[i-1]`，`i-1` 就是要增大的位置 `pos`',
              '右边找「比它大的最小数」换过来，再把右边翻转成升序，增幅最小',
              '最后拼回整数，超过 `2147483647` 或不大于 n 就返回 -1'],
        summary=['时间 `O(log n)`，空间 `O(log n)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（`tmp //= 10`、`len(nums) // 2`、`(len(nums)-pos-1) // 2`）',
                 '易错点：换完后右半段要翻转成升序，才是最小的更大排列',
                 '易错点：别忘了 32 位整数范围检查，以及全降序时返回 -1',
                 '同类题：31 下一个排列'],
    ),
)
