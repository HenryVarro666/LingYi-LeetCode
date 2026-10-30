def _loop(msg_next, msg_end):
    box = [0]

    def f(S, B, ret):
        n = len(S['nums'])
        k = box[0] % (n + 1)
        box[0] += 1
        if k == n:
            return msg_end
        return msg_next % S['num']
    return f


def _txt(S):
    if 'last_dict' not in S:
        return '先数一遍：`num_dict[x]` = 数 `x` 还剩几个没安置'
    if 'num' not in S:
        return '`last_dict[x]` = 现有「以 x 结尾」的子序列条数'
    ends = {k: v for k, v in S['last_dict'].items() if v > 0}
    return f'现有子序列的结尾：{ends if ends else "还没有"}　　当前处理 ==`{S["num"]}`=='


CONFIG = dict(
    num=659, title='分割数组为连续子序列', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='贪心 + 两个哈希表',
    tags=['贪心与思维'],
    code='''
class Solution(object):
    def isPossible(self, nums):

        num_dict = {}
        for num in nums:
            num_dict[num] = num_dict.get(num, 0) + 1

        last_dict = {}
        for num in nums:
            if num_dict[num] == 0:
                continue

            if last_dict.get(num - 1, 0) > 0:
                last_dict[num - 1] -= 1
                last_dict[num] = last_dict.get(num, 0) + 1
                num_dict[num] -= 1
            elif num_dict.get(num + 1, 0) > 0 and num_dict.get(num + 2, 0) > 0:
                last_dict[num + 2] = last_dict.get(num + 2, 0) + 1
                num_dict[num] -= 1
                num_dict[num + 1] -= 1
                num_dict[num + 2] -= 1
            else:
                return False

        return True
''',
    call='Solution().isPossible([1,2,3,3,4,4,5,5])',
    expect=True,
    views=[
        dict(type='array', var='nums', label='nums（已排好序，黄 = 当前数的位置）', cell=76, h=150,
             color=lambda S, i, v: 'yellow' if S.get('num') == v and S['_line'] >= 9 else None),
        dict(type='map', var='num_dict', label='num_dict：每个数还剩几个没安置', fmt=lambda k, v: f'{k}: {v}', h=150),
        dict(type='map', var='last_dict', label='last_dict：以 x 结尾的合法子序列条数', fmt=lambda k, v: f'{k}: {v}', h=150),
        dict(type='text', h=90, size=26, fn=_txt),
    ],
    watch=[('num', 'num', 'blue')],
    captions={
        5: _loop('先统计：看到数 `%d`', '统计完了，每个数出现几次都记下了'),
        9: _loop('处理下一个数 `num = %d`', '所有数都处理完了，没有返回 False'),
        'num_dict = {}': '`num_dict[x]`：数 `x` 还有几个没被安置（先统计出现次数）',
        'num_dict[num] = num_dict.get': '数 `{num}` 出现次数：`num_dict[{num}] = {num_dict[num]}`',
        'last_dict = {}': '`last_dict[x]`：已经凑好、以 `x` 结尾的子序列有几条',
        'if num_dict[num] == 0': '`{num}` 还剩 `{num_dict[num]}` 个 → {"==已被前面用完，跳过==" if num_dict[num] == 0 else "还要安置它"}',
        'continue': '用完了，直接看下一个数',
        'if last_dict.get(num - 1, 0) > 0': '有以 `{num - 1}` 结尾的子序列吗？现有 `{last_dict.get(num - 1, 0)}` 条 → {"==有，把它接上去（最优）==" if last_dict.get(num - 1, 0) > 0 else "没有，只能自己另起一条"}',
        'last_dict[num - 1] -= 1': '一条以 `{num - 1}` 结尾的子序列被取走：`last_dict[{num - 1}]` → {last_dict[num - 1]}',
        'last_dict[num] = last_dict.get(num, 0) + 1': '它接上 `{num}` 后，变成以 `{num}` 结尾：`last_dict[{num}]` = {last_dict[num]}',
        'num_dict[num] -= 1': '`{num}` 用掉一个，还剩 `{num_dict[num]}`',
        'elif num_dict.get': '没有可接的 → 另起新序列，需要后面还有 `{num + 1}` 和 `{num + 2}`：{"==都有，凑出 " + str(num) + "," + str(num + 1) + "," + str(num + 2) + "==" if (num_dict.get(num + 1, 0) > 0 and num_dict.get(num + 2, 0) > 0) else "凑不齐"}',
        'last_dict[num + 2] =': '新序列 `{num},{num + 1},{num + 2}` 长度刚好 3，以 `{num + 2}` 结尾：`last_dict[{num + 2}]` = {last_dict[num + 2]}',
        'num_dict[num + 1] -= 1': '`{num + 1}` 也用掉一个，还剩 `{num_dict[num + 1]}`',
        'num_dict[num + 2] -= 1': '`{num + 2}` 也用掉一个，还剩 `{num_dict[num + 2]}`',
        'return False': '`{num}` 既接不上，也凑不出新的长度 3 序列 → ==无处安置，返回 False==',
        'return True': '所有数都安置好了 → ==返回 True==',
    },
    cards=dict(
        one_liner='能接就接：x 优先接在以 x-1 结尾的序列后面',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['有序整数数组 `nums`，能否分成若干条子序列',
                 '每条子序列由 ==连续整数== 组成，且长度 `>= 3`',
                 '示例：`[1,2,3,3,4,4,5,5]` → `True`（`1,2,3,4,5` 与 `3,4,5`）'],
        quote='对于一个数x而言，若现在已经有了以x - 1为结尾的连续子序列，那么我们应该将x加入其中。',
        quote_src='—— yiduobo 题解',
        idea=['能接就接：另起新序列只有凑到长度 3 才合法，而接在旧序列后面总是安全',
              '`num_dict` 记每个数还剩几个，`last_dict` 记以 `x` 结尾的序列条数',
              '接不上就用 `x, x+1, x+2` 另起一条；凑不出就返回 `False`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：必须先判断「能否接在以 `x-1` 结尾的序列后」，再考虑另起',
                 '易错点：跳过已被前面用完的数（`num_dict[num] == 0`）',
                 '另起新序列时，三个数的剩余次数都要减一',
                 '原文代码已是 Python 3 写法，无需修改。简报无题面，题意按 LeetCode 659 原题'],
    ),
)
