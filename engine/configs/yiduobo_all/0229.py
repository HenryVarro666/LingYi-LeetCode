def _cand(S):
    if 'cnt1' not in S:
        return '两个候选 + 两个计数器：最多只有 ==2 个数== 能超过 n/3'
    x, y = S.get('x'), S.get('y')
    if 'res' in S:
        return f'验证完毕：`x={x}` 出现 {S["cnt1"]} 次，`y={y}` 出现 {S["cnt2"]} 次（需要 > {len(S["nums"])//3}）'
    return f'候选 `x={x}`（计数 {S["cnt1"]}） ｜ 候选 `y={y}`（计数 {S["cnt2"]}）'


def _color(S, i, v):
    if 'cnt1' not in S:
        return None
    if v == S.get('x') and S.get('x') is not None:
        return 'blue'
    if v == S.get('y') and S.get('y') is not None:
        return 'pink'
    return None


CONFIG = dict(
    num=229, title='求众数II', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='双候选摩尔投票',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def majorityElement(self, nums):

        cnt1 = cnt2 = 0
        x = y = None
        for num in nums:
            if x == num:
                cnt1 += 1
            elif y == num:
                cnt2 += 1
            elif cnt1 == 0:
                x = num
                cnt1 = 1
            elif cnt2 == 0:
                y = num
                cnt2 = 1
            else:
                cnt1 -= 1
                cnt2 -= 1

        cnt1 = cnt2 = 0
        for num in nums:
            if num == x:
                cnt1 += 1
            elif num == y:
                cnt2 += 1

        res = []
        if cnt1 > len(nums) // 3:
            res.append(x)
        if cnt2 > len(nums) // 3:
            res.append(y)

        return res
''',
    call='Solution().majorityElement([1,2,1,3,1,2,2,4])',
    expect=[1, 2],
    views=[
        dict(type='text', fn=_cand, h=70),
        dict(type='array', var='nums', color=_color, h=260, label='nums（蓝 = 候选 x，粉 = 候选 y）'),
    ],
    watch=[('num', 'num'), ('x', 'x', 'blue'), ('cnt1', 'cnt1', 'blue'), ('y', 'y', 'pink'), ('cnt2', 'cnt2', 'pink')],
    captions={
        'cnt1 = cnt2 = 0': lambda S, B, r: '两个候选的计数器清零' if 'res' not in S and S.get('_line') is not None and 'x' not in S else '第二趟：重新计数，检验候选真的超过三分之一',
        'x = y = None': '还没有候选：`x`、`y` 都是 None',
        'for num in nums': lambda S, B, r: (f'看下一个数 `num = {S["num"]}`' if S.get('_line') is not None and not (B.get('num') == S['num'] and S['_line'] in (6, 22) and B.get('_line') == S['_line']) else '遍历结束'),
        'if x == num': '`x == num`（{x} vs {num}）→ {"成立，给 x 投一票" if x == num else "不成立，看 y"}',
        'elif y == num': '`y == num`（{y} vs {num}）→ {"成立，给 y 投一票" if y == num else "不成立，看有没有空位"}',
        'elif cnt1 == 0': '`cnt1 == {cnt1}` → {"x 位空着，新数来当 x" if cnt1 == 0 else "x 位有人，看 y 位"}',
        'elif cnt2 == 0': '`cnt2 == {cnt2}` → {"y 位空着，新数来当 y" if cnt2 == 0 else "两个位都有人，只能抵消"}',
        'x = num': '`x = {x}`：空位被新数顶替',
        'y = num': '`y = {y}`：空位被新数顶替',
        'cnt1 = 1': '`cnt1 = 1`：新候选从 1 票开始',
        'cnt2 = 1': '`cnt2 = 1`：新候选从 1 票开始',
        'cnt1 -= 1': '`num` 和两个候选都不同 → ==三票互相抵消==：`cnt1` → {cnt1}',
        'cnt2 -= 1': '同时 `cnt2` → {cnt2}',
        'if num == x': '`num == x`（{num} vs {x}）→ {"成立，x 的真实次数 +1" if num == x else "不成立，看 y"}',
        'elif num == y': '`num == y`（{num} vs {y}）→ {"成立，y 的真实次数 +1" if num == y else "都不是，跳过"}',
        'cnt1 += 1': '`cnt1` → {cnt1}',
        'cnt2 += 1': '`cnt2` → {cnt2}',
        'if cnt1 > len': '`cnt1 = {cnt1}` 与 `len(nums)//3 = {len(nums)//3}` 比较：{"超过，x 入选" if cnt1 > len(nums)//3 else "不够，x 淘汰"}',
        'if cnt2 > len': '`cnt2 = {cnt2}` 与 `len(nums)//3 = {len(nums)//3}` 比较：{"超过，y 入选" if cnt2 > len(nums)//3 else "不够，y 淘汰"}',
        'res.append(x)': '`x = {x}` 加入答案：`res = {res}`',
        'res.append(y)': '`y = {y}` 加入答案：`res = {res}`',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='对两个候选投票，三票互相抵消，最后再验证',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定整数数组 `nums`，找出所有出现次数 ==超过 n/3== 的元素',
                 '这样的数最多只有 2 个',
                 '示例：`[1,2,1,3,1,2,2,4]` → `[1, 2]`'],
        quote='如果新来的数与这两个数都不相同，那么这两个候选者的计数器分别减一，相当于这三票抵消。',
        quote_src='—— yiduobo 题解原文',
        idea=['是第 169 题的升级版：169 题一个候选，这里维护两个候选',
              '新数等于某个候选就加票；都不等且有空位就顶替；否则 ==三票抵消==',
              '投票只保证「可能的」候选，所以必须再扫一趟验证次数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：==第二趟验证不能省==，投票剩下的候选不一定真的超过 n/3',
                 '判断顺序：先比较两个候选，再看空位，最后才抵消',
                 '原文为 Python 2 写法，`len(nums) / 3` 已改为 `len(nums) // 3`'],
    ),
)
