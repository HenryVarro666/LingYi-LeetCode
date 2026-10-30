def _grp(S):
    x = S.get('x')
    if x is None or 'cnt' not in S:
        return '先数各个数的次数；只从「x/2 不在表里」的最小数出发，沿 x、2x、4x… 成对消除'
    c = S['cnt']
    if x in c and 'cnt_x' in S and S.get('_line') is not None:
        return f'当前链：`{x}` ×{c.get(x, 0)}  与  `{2 * x}` ×{c.get(2 * x, 0)}'
    return f'当前枚举 `x = {x}`'


CONFIG = dict(
    num=2007, title='从双倍数组中还原原数组', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表 · 消消乐（免排序）',
    tags=['哈希表', '计数'],
    code='''
class Solution:
    def findOriginalArray(self, changed: List[int]) -> List[int]:
        cnt = Counter(changed)
        # 单独处理 0
        cnt0 = cnt.pop(0, 0)
        if cnt0 % 2:
            return []
        ans = [0] * (cnt0 // 2)

        for x in cnt:
            # 如果 x/2 在 cnt 中，则跳过
            if x % 2 == 0 and x // 2 in cnt:
                continue
            # 把 x, 2x, 4x, 8x, ... 全部配对
            while x in cnt:
                # 每次循环，把 cnt_x 个 x 和 cnt_x 个 2x 配对
                cnt_x = cnt[x]
                # 无法配对，至少要有 cnt_x 个 2x
                if cnt_x > cnt[x * 2]:
                    return []
                ans.extend([x] * cnt_x)
                if cnt_x < cnt[x * 2]:
                    # 还剩下一些 2x
                    cnt[x * 2] -= cnt_x
                    x *= 2
                else:
                    x *= 4
        return ans
''',
    call='Solution().findOriginalArray([3,2,1,16,2,6,4,1,8,2])',
    expect=[3, 1, 1, 2, 8],
    views=[
        dict(type='array', var='changed', label='changed（蓝 = 当前 x，粉 = 2x）', cell=84, h=150,
             color=lambda S, i, v: ('blue' if v == S.get('x') else 'pink' if v == 2 * S['x'] else None) if S.get('x') else None),
        dict(type='map', var='cnt', label='cnt（x → 还没配对的个数）', fmt=lambda k, v: f'{k} → {v}', h=190, font=30),
        dict(type='array', var='ans', label='ans（原数组）', cell=84, h=130, index=False),
        dict(type='text', h=70, size=28, fn=_grp),
    ],
    watch=[('x', 'x', 'blue'), 'cnt_x', ('ans', 'ans', 'green')],
    captions={
        'cnt = Counter(changed)': '`cnt` 统计每个数的出现次数，不需要排序',
        'cnt0 = cnt.pop(0, 0)': '==0 单独处理==：0 乘 2 还是 0，只能自己和自己配对。`cnt0 = {cnt0}`',
        'if cnt0 % 2': '0 的个数 `{cnt0}` 是偶数，才能两两配对',
        'ans = [0] * (cnt0 // 2)': '`{cnt0}` 个 0 配成 `{cnt0 // 2}` 对，答案里放 `{cnt0 // 2}` 个 0',
        'for x in cnt': '枚举 `cnt` 里的数：`x = {x}`',
        'if x % 2 == 0 and x // 2 in cnt': lambda S, B, ret: (
            f'`{S.x}` 的一半 `{S.x // 2}` 在表里 → ==它不是链头==，等链头来处理它' if S.x % 2 == 0 and S.x // 2 in S.cnt
            else f'`{S.x}` 的一半不在表里 → `{S.x}` 是这条链的最小数，==一定属于原数组=='),
        'continue': '跳过，不是链头',
        'while x in cnt': lambda S, B, ret: (f'`x = {S.x}` 还在 `cnt` 中，继续配对' if S.x in S.cnt else f'`{S.x}` 不在 `cnt` 中，这条链结束'),
        'cnt_x = cnt[x]': '`{x}` 还剩 `{cnt_x}` 个，要找 `{cnt_x}` 个 `{x * 2}` 来配',
        'if cnt_x > cnt[x * 2]': lambda S, B, ret: (
            f'`{S.cnt_x}` 个 x 比 `{S.cnt[S.x * 2]}` 个 2x 还多 → ==配不齐==，返回空' if S.cnt_x > S.cnt[S.x * 2]
            else f'`{S.cnt_x} ≤ {S.cnt[S.x * 2]}`：2x 够用'),
        'return []': '无法配对，返回 `[]`',
        'ans.extend([x] * cnt_x)': '这 `{cnt_x}` 个 `{x}` 是原数组元素，加入答案：`ans = {ans}`',
        'if cnt_x < cnt[x * 2]': lambda S, B, ret: (
            f'`{S.cnt_x} < {S.cnt[S.x * 2]}`：2x 配完还剩一些，剩下的要当下一轮的 x' if S.cnt_x < S.cnt[S.x * 2]
            else f'`{S.cnt_x} = {S.cnt[S.x * 2]}`：2x 刚好配完'),
        'cnt[x * 2] -= cnt_x': '2x 被用掉 `{cnt_x}` 个，还剩 `cnt[{x * 2}] = {cnt[x * 2]}`',
        'x *= 2': '下一轮从剩下的 `{x}` 开始',
        'x *= 4': '`x` 和 `2x` 都配完了，直接跳到 `4x` = `{x}`',
        'return ans': '全部配对成功，返回 `{ans}`',
    },
    cards=dict(
        one_liner='把 x、2x、4x… 分成一条条链，从链头成对消除，不用排序',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`changed` 是把 `original` 每个数乘 2 加进去再打乱得到的',
                 '判断 `changed` 是不是双倍数组，是就还原 `original`，否则返回 `[]`',
                 '示例：`[1,3,4,2,6,8]` → `[1,3,4]`',
                 '本视频：`[3,2,1,16,2,6,4,1,8,2]` → `[3,1,1,2,8]`'],
        quote='只要 x/2 不在数组中，我们就可以从 x 开始。从 x 开始，通过不断地乘二，找到这一组内的其它数字。实现以上两点，完全不需要排序！',
        quote_src='—— 灵茶山艾府题解 · 方法三「消消乐」',
        idea=['链头 = 一个 `x/2` 不在表里的数，它不可能是别人的两倍 → ==必在原数组==',
              '每轮用 `cnt[x]` 个 x 去消 `cnt[x]` 个 2x；2x 多出来的部分接着当 x',
              '`0` 的两倍还是自己，要单独处理：个数必须是偶数'],
        summary=['时间 `O(n)`：每个不同的数至多被配对一次；排序写法是 `O(n log n)`',
                 '易错：`0` 必须单独处理，否则 `x*2` 还是自己',
                 '易错：2x 有剩余时要把 `cnt[2x]` 减掉再让 `x *= 2`',
                 '另两种写法：排序 + 哈希表 / 排序 + 队列，都是从小到大贪心配对'],
    ),
)
