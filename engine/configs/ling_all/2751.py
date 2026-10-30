CONFIG = dict(
    num=2751, title='机器人碰撞', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='按位置排序 + 栈模拟碰撞',
    tags=['栈', '邻项消除', '难度分 2092'],
    code='''
class Solution:
    def survivedRobotsHealths(self, positions: List[int], healths: List[int], directions: str) -> List[int]:
        # 创建一个下标数组，对下标数组排序，这样不会打乱输入顺序
        idx = sorted(range(len(positions)), key=lambda i: positions[i])

        st = []
        for i in idx:
            if directions[i] == 'R':  # 机器人 i 向右
                st.append(i)
                continue
            while st:  # 栈顶机器人向右
                j = st[-1]
                if healths[j] > healths[i]:  # 栈顶机器人的健康度大
                    healths[i] = 0  # 移除机器人 i
                    healths[j] -= 1
                    break
                if healths[j] == healths[i]:  # 健康度一样大，都移除
                    healths[i] = 0
                    healths[j] = 0
                    st.pop()
                    break
                # 机器人 i 的健康度大
                healths[i] -= 1
                healths[j] = 0  # 移除机器人 j
                st.pop()

        # 返回幸存机器人的健康度
        return [h for h in healths if h > 0]
''',
    call="Solution().survivedRobotsHealths([4,1,6,2,3,5], [6,5,3,4,2,3], 'LRRLRL')",
    expect=[4, 3, 3],
    views=[
        dict(type='array', var='positions', label='positions（蓝 = 当前 i）', h=140,
             color=lambda S, i, v: 'blue' if i == S.get('i') else None),
        dict(type='string', var='directions', label='directions（橙 R / 青 L）', h=140,
             color=lambda S, i, v: 'orange' if v == 'R' else 'cyan'),
        dict(type='array', var='healths', label='healths（0 = 已移除）', pointers={'i': 'blue', 'j': 'pink'}, h=215,
             dim=lambda S, i, v: v == 0),
        dict(type='stack', var='st', fmt=lambda x: f'R{x}', label='栈（向右的机器人）', h=150),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('idx', 'idx', 'cyan'), ('st', 'st', 'green')],
    captions={
        'idx = sorted': '按位置排序下标：`idx = {idx}`，不动输入顺序，最后好按编号输出',
        'st = []': '栈里放「还没碰撞的向右机器人」，向左的机器人只会撞到它们',
        'for i in idx': lambda S, B, r: ('机器人都处理完了' if B.get('i') == S.i else f'从左到右处理机器人 `{S.i}`，位置 `{S.positions[S.i]}`，方向 `{S.directions[S.i]}`'),
        "if directions[i] == 'R'": lambda S, B, r: (f'机器人 `{S.i}` 向右 → 先入栈，等着被后面向左的撞' if S.directions[S.i] == 'R'
                                                    else f'机器人 `{S.i}` 向左 → 会和栈顶向右的机器人相撞'),
        'st.append(i)': '向右的 `{i}` 入栈：`st = {st}`',
        'while st': lambda S, B, r: (f'栈非空：向左的 `{S.i}`（健康度 {S.healths[S.i]}）还要继续碰撞' if S.st else '栈空了：左边没有向右的机器人，它不再碰撞'),
        'j = st[-1]': '栈顶 `j = {j}`，健康度 `{healths[j]}`',
        'if healths[j] > healths[i]': lambda S, B, r: (f'`{S.healths[S.j]}` > `{S.healths[S.i]}`：栈顶更健康，==机器人 i 被移除=='
                                                      if S.healths[S.j] > S.healths[S.i] else f'`{S.healths[S.j]}` ≤ `{S.healths[S.i]}`：栈顶不更健康 → 不成立'),
        'healths[i] = 0  # 移除': '机器人 `{i}` 健康度归 0',
        'healths[j] -= 1': '胜者栈顶 `{j}` 健康度减 1 → `{healths[j]}`，它继续留在栈里',
        'if healths[j] == healths[i]': lambda S, B, r: (f'`{S.healths[S.j]}` = `{S.healths[S.i]}`：一样大 → ==同归于尽==' if S.healths[S.j] == S.healths[S.i]
                                                        else f'`{S.healths[S.j]}` ≠ `{S.healths[S.i]}`：不一样大 → 不成立，说明 i 更健康'),
        'healths[i] -= 1': '机器人 `{i}` 更健康：赢了但掉 1 点 → `{healths[i]}`（原来 ≥ 2，所以仍大于 0）',
        'healths[j] = 0  # 移除机器人 j': '栈顶机器人 `{j}` 被移除（归 0）',
        'continue': '向右的机器人先留在栈里，看下一个',
        'break': '这个机器人的碰撞结束，处理下一个',
        'st.pop()': '栈顶 `{B.st[-1]}` 已被移除，弹出；回到 `while` 继续和新的栈顶比',
        'return [h': '把剩下 `h > 0` 的按原编号顺序返回：`{ret}`',
    },
    cards=dict(
        one_liner='排好序后，向左的机器人只会撞栈顶向右的',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['机器人在路线上同速相向而行，相撞时健康度低的被移除，另一个减 1',
                 '相等则同归于尽；返回幸存者的健康度，按原编号排列',
                 '示例：`positions=[3,5,2,6]`，`healths=[10,10,15,12]`，`directions="RLRL"` → `[14]`'],
        quote='遍历到一个向左的机器人时，我们需要找到左边最近的未移除的机器人。这可以用一个栈维护。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先对下标按位置排序，不打乱输入顺序',
              '向右的直接入栈；向左的和栈顶比健康度，三种结果：栈顶赢、同归于尽、自己赢继续撞',
              '直接在 `healths` 上改：移除就置 0，最后返回正数'],
        summary=['时间 `O(n log n)`（排序），栈部分总共 `O(n)`',
                 '易错：自己赢了要 `healths[i] -= 1` 并继续和下一个栈顶比',
                 '比大小的两个健康度都是正整数，减 1 后仍大于 0',
                 '先做简单版：735 行星碰撞'],
    ),
)
