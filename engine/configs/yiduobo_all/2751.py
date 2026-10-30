CONFIG = dict(
    num=2751, title='机器人碰撞', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='按位置遍历 + 栈 · 向左机器人连撞',
    tags=['栈', '邻项消除', '难度分 2092'],
    code='''
class Solution(object):
    def survivedRobotsHealths(self, positions, healths, directions):

        stack = []
        for index, p in sorted(enumerate(positions), key=lambda d:d[1]):
            if directions[index] == 'R':
                stack.append(index)
            else:
                v = healths[index]
                while stack and healths[stack[-1]] < v:
                    v -= 1
                    healths[stack[-1]] = 0
                    stack.pop()
                
                if stack:
                    if healths[stack[-1]] == v:
                        healths[stack[-1]] = 0
                        stack.pop()
                    else:
                        healths[stack[-1]] -= 1
                    v = 0

                healths[index] = v
        
        res = []
        for v in healths:
            if v > 0:
                res.append(v)
        
        return res
''',
    call="Solution().survivedRobotsHealths([4,1,6,2,3,5], [6,5,3,4,2,3], 'LRRLRL')",
    expect=[4, 3, 3],
    views=[
        dict(type='array', var='positions', label='positions（蓝 = 当前机器人）', h=140,
             color=lambda S, i, v: 'blue' if i == S.get('index') and S.get('_line', 0) < 29 else None),
        dict(type='string', var='directions', label='directions（橙 R / 青 L）', h=140,
             color=lambda S, i, v: 'orange' if v == 'R' else 'cyan'),
        dict(type='array', var='healths', label='healths（0 = 已移除）', pointers={'index': 'blue'}, h=200,
             dim=lambda S, i, v: v == 0),
        dict(type='stack', var='stack', fmt=lambda x: f'R{x}', label='栈（向右的机器人）', h=150),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'pink'), ('stack', 'stack', 'green'), ('res', 'res', 'cyan')],
    captions={
        'stack = []': '栈维护「还在向右走」的机器人下标',
        'for index, p in sorted': lambda S, B, r: ('按位置遍历完了' if B.get('index') == S.index and B.get('p') == S.p else f'按位置从左到右：机器人 `{S.index}`（位置 `{S.p}`，方向 `{S.directions[S.index]}`）'),
        "if directions[index] == 'R'": lambda S, B, r: (f'机器人 `{S.index}` 向右 → 入栈等待' if S.directions[S.index] == 'R' else f'机器人 `{S.index}` 向左 → 会撞上栈里向右的'),
        'stack.append(index)': '`{index}` 入栈：`stack = {stack}`',
        'v = healths[index]': '向左机器人的血量 `v = {v}`：用局部变量 `v` 记它撞完剩多少',
        'while stack and': lambda S, B, r: (f'栈顶 `{S.stack[-1]}` 血量 `{S.healths[S.stack[-1]]}` < `v = {S.v}`：向左的更强 → 成立' if S.stack and S.healths[S.stack[-1]] < S.v
                                           else ('栈空了：没人可撞，不再碰撞' if not S.stack else f'栈顶 `{S.stack[-1]}` 血量 `{S.healths[S.stack[-1]]}` ≥ `v = {S.v}`：向左的不占优 → 结束连撞')),
        'v -= 1': '向左的赢了但掉 1 点：`v` → {v}',
        'if stack:': lambda S, B, r: ('栈里还有向右的：还要和它决胜负' if S.stack else '栈空：向左的毫发无伤继续走，不用处理'),
        'if healths[stack[-1]] == v': lambda S, B, r: (f'`{S.healths[S.stack[-1]]}` = `{S.v}`：血量相同 → ==同归于尽==' if S.healths[S.stack[-1]] == S.v else f'`{S.healths[S.stack[-1]]}` ≠ `{S.v}`：栈顶更强（>），向左的会死'),
        'healths[stack[-1]] -= 1': '栈顶赢了，血量减 1 → `{healths[stack[-1]]}`，留在栈里',
        'healths[stack[-1]] = 0': '栈顶机器人被移除：血量置 0',
        'stack.pop()': '把它从栈里弹出，`stack = {stack}`',
        'v = 0': '向左的机器人已被移除：`v = 0`',
        'healths[index] = v': '把结果写回：机器人 `{index}` 血量 `{v}`',
        'res = []': '扫描完毕，收集还活着的血量',
        'for v in healths': lambda S, B, r: ('收集完了' if B.get('v') == S.v and len(S.res) == sum(1 for h in S.healths if h > 0) else f'看血量 `v = {S.v}`'),
        'if v > 0': lambda S, B, r: (f'`{S.v}` > 0：活着 → 收进答案' if S.v > 0 else '`0`：已移除，跳过'),
        'res.append(v)': '`res = {res}`',
        'return res': '按原编号顺序的幸存者血量：`{res}`',
    },
    cards=dict(
        one_liner='向右入栈，向左就和栈顶比血量，连撞到停',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['机器人在路线上同速相向而行，相撞时血量少的被移除，另一个减 1',
                 '相等则同归于尽；返回幸存者血量，按原编号排',
                 '示例：`positions=[3,5,2,6]`，`healths=[10,10,15,12]`，`directions="RLRL"` → `[14]`'],
        quote='与之前有一题行星碰撞很像，处理方法也是一样，从左向右遍历，使用栈维护当前还在向右移动的机器人。',
        quote_src='—— yiduobo 题解原文',
        idea=['按位置遍历，向右的入栈；向左的和栈顶碰撞，分三种情况',
              '向左血量更高：栈顶置 0 弹出，自己血量减 1，接着撞下一个栈顶',
              '相同：双方清零；向左更低：自己置 0，栈顶血量减 1'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错：向左的赢了每撞一个都要减 1，用 `v` 暂存再写回',
                 '血量相等同归于尽，要把栈顶弹出且 `v = 0`',
                 '最后按原下标顺序收集 `> 0` 的血量'],
    ),
)
