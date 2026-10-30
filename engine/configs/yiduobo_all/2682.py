def _col(S, i, v):
    return 'green' if v else None


CONFIG = dict(
    num=2682, title='找出转圈游戏输家', difficulty='Easy', category='模拟',
    author='yiduobo', technique='暴力模拟 · 手动回绕',
    tags=[],
    code='''
class Solution(object):
    def circularGameLosers(self, n, k):

        res = []
        vis = [False] * (n + 1)
        now = 1
        vis[1] = True
        step = k
        while True:
            now += step
            if now > n:
                now -= n
            if vis[now]:
                break
            vis[now] = True

            step += k
            if step >= n:
                step -= n
        
        for index in range(1, n + 1):
            if not vis[index]:
                res.append(index)
        
        return res
''',
    call='Solution().circularGameLosers(7, 3)',
    expect=[2, 6, 7],
    views=[
        dict(type='array', var='vis', pointers={'now': 'blue'}, color=_col, h=260, label='vis（下标 1~n 就是朋友编号，绿 = 接过球；0 号不用）'),
        dict(type='array', var='res', h=130, label='输家 res'),
    ],
    watch=[('now', 'now', 'blue'), ('step', 'step', 'pink')],
    captions={
        'vis = [False]': '`vis` 多开一格，下标 1 到 `n` 直接对应朋友编号',
        'now = 1': '第 1 个朋友先接球，立刻标记',
        'while True': '开始传球',
        'now += step': '球传出 `{step}` 步：`now` = {now}',
        'if now > n': lambda S, B, r: (f'`now = {S.now} > n = {S.n}`：越过了末尾，要绕回圈的开头' if S.now > S.n else f'`now = {S.now} ≤ n`：没出圈，不用回绕'),
        'now -= n': '绕回去：`now` 减去 `n` → =={now}==',
        'if vis[now]': lambda S, B, r: (f'第 {S.now} 个朋友已经接过球 → 第 2 次接球，游戏结束' if S.vis[S.now]
                                         else f'第 {S.now} 个朋友还没接过球 → 继续'),
        'vis[now] = True': '第 `{now}` 个朋友接到球，标记',
        'step += k': '下一次多传 `k` 步：`step` = {step}',
        'if step >= n': lambda S, B, r: (f'`step = {S.step} ≥ n = {S.n}`：步数转一圈等于没走，减去 `n`' if S.step >= S.n
                                          else f'`step = {S.step} < n`：不用处理'),
        'step -= n': '`step` 减去一圈：=={step}==',
        'for index in range': lambda S, B, r: ('游戏结束，从 1 到 n 逐个找没接过球的人' if 'index' not in B else f'下一个：第 {S.index} 个朋友'),
        'break': '球传回了接过的人，跳出循环',
        'if not vis[index]': lambda S, B, r: (f'第 {S.index} 个朋友没接过球 → 输家' if not S.vis[S.index]
                                               else f'第 {S.index} 个朋友接过球 → 不是输家'),
        'res.append': '加入输家：`res` = {res}',
        'return res': '输家按编号升序：=={res}==',
    },
    cards=dict(
        one_liner='数据很小，直接暴力模拟传球，手动处理绕圈',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 个朋友围成圈，第 1 个人接球，第 `i` 次传球走 `i*k` 步',
                 '某人第 2 次接到球时游戏结束，没接过球的人是输家',
                 '示例：`n=5, k=2` → `[4,5]`；本视频用 `n=7, k=3`'],
        quote='约瑟夫问题的某种变种，应该存在数学方法或者动态规划方法进行求解，不过本题的数据规模很小，因此在这里直接使用暴力法求解就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['编号 1 到 `n`，所以 `vis` 开 `n + 1` 格，不做下标换算',
              '`now` 超过 `n` 就减 `n`；`step` 超过 `n` 也减 `n`，不让数字越滚越大',
              '遇到已标记的人就 `break`，再扫一遍 `vis` 收集输家'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：`now` 回绕用 `now -= n`（不是取模到 0），所以编号范围是 1 到 `n`',
                 '`step` 每次回绕一圈不改变落点，所以可以先减掉',
                 '对比灵神：灵神下标从 0 + 取模，yiduobo 编号从 1 + 手动减 `n`'],
    ),
)
