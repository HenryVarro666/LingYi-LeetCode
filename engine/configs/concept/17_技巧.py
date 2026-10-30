def _moore_state(nums, upto):
    """模拟擂台赛处理 nums[0..upto]，返回 (当前这一段的起点, 擂主)；hp 归零则整段都已抵消"""
    ans = hp = 0
    seg = 0
    for k in range(upto + 1):
        if hp == 0:
            ans, hp, seg = nums[k], 1, k
        else:
            hp += 1 if nums[k] == ans else -1
    return (upto + 1 if hp == 0 else seg), ans


def _color(S, k, v):
    if 'hp' in S and 'i' in S:
        upto = S['i'] - (1 if S.get('_line') == 9 else 0)     # for 这一行：nums[i] 还没上擂台
        if k > upto or upto < 0:
            return None
        seg, champ = _moore_state(S['nums'], upto)
        if k < seg:
            return (64, 70, 80)                                # 已经同归于尽的段
        return 'green' if v == champ else 'red'
    return None


def _formula(S):
    if 'hp' in S:
        if 'i' not in S:
            return '摩尔投票：不同的数 ==两两同归于尽==，绝对众数一定活到最后'
        return f"擂主 `ans = {S['ans']}`，生命值 `hp = {S['hp']}`"
    if 'x' in S:
        x, a = S['x'], S['ans']
        if S.get('_line') == 4:
            return f"`{a ^ x:03b}` ^ `{x:03b}` = `{a:03b}`（二进制）　→　`ans = {a}`"
        return f"当前 `ans = {a:03b}`₂，下一个数 `x = {x:03b}`₂"
    return '异或：`a ^ a = 0`，`a ^ 0 = a`，==成对出现的数会互相抵消=='


CONFIG = dict(
    num=None, title='技巧 · 通用思想与模板', author='概念讲解', category='技巧',
    technique='通用思想与模板', kind='concept', difficulty='',
    code='''
def single_number(nums):             # 136. 异或：成对的数抵消
    ans = 0                          # 0 ^ x = x
    for x in nums:
        ans ^= x                     # x ^ x = 0
    return ans

def majority_element(nums):          # 169. 摩尔投票（擂台赛）
    ans = hp = 0                     # 擂主、生命值
    for i, x in enumerate(nums):
        if hp == 0:                  # 擂台空了：x 成为新擂主
            ans, hp = x, 1
        else:                        # 同门加血，否则同归于尽
            hp += 1 if x == ans else -1
    return ans
''',
    call='''
a = single_number([4, 1, 2, 1, 2])
b = majority_element([2, 2, 1, 1, 1, 2, 2, 3, 2])
(a, b)
''',
    expect=(4, 2),
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='array', var='nums', label='nums', pointers={'i': 'blue'}, color=_color, h=200),
        dict(type='text', fn=lambda S: ('`a ^ b ^ a = b`：顺序无所谓（交换律 + 结合律）' if 'x' in S and 'hp' not in S else
                                        ('灰 = 已同归于尽的段，绿 = 擂主同门，红 = 挑战者' if 'hp' in S else '')), size=26, h=60),
    ],
    watch=[('x', 'x'), ('ans', 'ans', 'green'), ('hp', 'hp', 'pink'), ('i', 'i', 'blue')],
    captions={
        'ans = 0  ': '模板① 异或：`ans` 从 0 开始，因为 `0 ^ x = x`',
        'for x in nums': lambda S, B, ret: (f'下一个数 `x = {S.x}`' if B.get('x') != S.x or B.get('ans') != S.ans
                                            or 'x' not in B else '所有数都异或完了'),
        'ans ^= x': lambda S, B, ret: (f'`ans = {B.ans} ^ {S.x} = {S.ans}`'
                                       + ('：`1` 第二次出现，==抵消了==' if S.x == 1 and B.ans & 1 else
                                          ('：`2` 第二次出现，==抵消了==' if S.x == 2 and B.ans & 2 else ''))),
        'return ans': lambda S, B, ret: (f'成对的数全部抵消，剩下 `{ret}`' if 'hp' not in S
                                         else f'最后站在擂台上的 `{ret}` 就是绝对众数'),
        'ans = hp = 0': '模板② 摩尔投票：`ans` 是擂主，`hp` 是它的生命值',
        'for i, x in': lambda S, B, ret: (f'挑战者 `nums[{S.i}] = {S.x}` 登场' if B.get('i') != S.i else '所有人都上过擂台了'),
        'if hp == 0': lambda S, B, ret: ('擂台空着（`hp = 0`）' if S.hp == 0 else f'擂主 `{S.ans}` 还有 `{S.hp}` 点血 → 比武'),
        'ans, hp = x, 1': '`{x}` 成为新擂主，生命值 1',
        'hp += 1 if': lambda S, B, ret: (f'`{S.x}` 和擂主同门 → 加血，`hp = {S.hp}`' if S.x == S.ans
                                         else (f'`{S.x}` 不同门 → 和擂主 `{S.ans}` 拼掉一条命，`hp = {S.hp}`'
                                               + ('——==擂台空了==' if S.hp == 0 else ''))),
    },
    cards=dict(
        one_liner='抓住题目的特殊性质，用 `O(1)` 空间完成看似要哈希表的事',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem_heading='什么时候用？',
        problem=['要求 `O(n)` 时间 + `O(1)` 额外空间，常规做法都不满足',
                 '成对出现 → 异或；某个数出现超过一半 → 摩尔投票',
                 '只有 0 / 1 / 2 三种值 → 三指针（荷兰国旗）',
                 '值域是 `[1, n]` → 把值当下标：建图找环、原地交换'],
        before=[dict(heading='核心概念：利用题目的特殊性质', lines=[
            '异或：`a ^ a = 0`，`a ^ 0 = a`，满足交换律和结合律',
            '摩尔投票：不同的数两两同归于尽，绝对众数一定活到最后',
            '三指针：维护 0 段和 1 段的右边界，一次遍历分成三段',
            '下一个排列：从右找第一个下降点 → 交换 → 反转后缀']),
        ],
        idea_heading='两位作者怎么说',
        quote='如果比武后，擂主生命值降为 0（同归于尽），那么下一个挑战者成为新的擂主，生命值为 1。最后在擂台上的那人，==便是武林盟主（绝对众数）==。',
        quote_src='—— 灵茶山艾府 · 169. 多数元素',
        idea=['136 两人一致：`x ^ x = 0`、`x ^ 0 = x`，==成对的数互相抵消==',
              'yiduobo 287：把 `x → nums[x]` 看成有向边，就变成了 ==142 环形链表==',
              '75：灵神「狸猫换太子」`O(1)` 插入；yiduobo 维护红、白两段的右边界'],
        summary_heading='本类 Hot100 题目 & 学习顺序',
        summary=['`136` 只出现一次的数字：全部异或',
                 '`169` 多数元素：摩尔投票（擂台赛）',
                 '`75` 颜色分类：三指针 / 「狸猫换太子」',
                 '`31` 下一个排列：找下降点 → 交换 → 反转后缀',
                 '`287` 寻找重复数：`i → nums[i]` 建图，快慢指针找环入口',
                 '易错：摩尔投票要保证存在多数元素；31 的后缀是反转而不是排序'],
    ),
)
