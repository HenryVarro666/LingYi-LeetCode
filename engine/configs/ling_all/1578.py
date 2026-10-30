def _top(S):
    if 'ans' not in S:
        return ''
    return f"`ans` = 到目前为止的总耗时 − 已结束各段的最大耗时 = =={S['ans']}=="


def _col(S, i, v):
    if 'i' not in S:
        return None
    c = S['colors']
    a = i
    while a > 0 and c[a - 1] == c[i]:
        a -= 1
    b = i
    while b + 1 < len(c) and c[b + 1] == c[i]:
        b += 1
    if a <= S['i'] <= b and i <= S['i']:
        return 'blue' if i == S['i'] else 'green'
    return None


def _end(S, B, ret):
    if S.i == len(S.colors) - 1:
        return f'`i` 是最后一个气球 → 本段结束'
    if S.colors[S.i] != S.colors[S.i + 1]:
        return f"`colors[{S.i}] = '{S.colors[S.i]}' ≠ colors[{S.i + 1}] = '{S.colors[S.i + 1]}'` → ==本段到此结束=="
    return f"`colors[{S.i}] == colors[{S.i + 1}] = '{S.colors[S.i]}'` → 同一段还没结束"


CONFIG = dict(
    num=1578, title='使绳子变成彩色的最短时间', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环 · 每段保留耗时最大的',
    tags=['灵神题单', '难度分 1574'],
    code='''
class Solution:
    def minCost(self, colors: str, neededTime: List[int]) -> int:
        ans = max_t = 0
        for i, t in enumerate(neededTime):
            ans += t
            if t > max_t:  # 手写 if 比调用 max 快
                max_t = t
            if i == len(colors) - 1 or colors[i] != colors[i + 1]:
                # 遍历到了连续同色段的末尾
                ans -= max_t  # 保留耗时最大的气球
                max_t = 0  # 准备计算下一段的最大耗时
        return ans
''',
    call='Solution().minCost("aabaac", [1,3,2,4,1,5])',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='colors', label='colors（蓝 = 当前，绿 = 当前同色段已扫过的部分）', cell=84,
             pointers={'i': 'pink'}, color=_col),
        dict(type='array', var='neededTime', label='neededTime（删除耗时）', cell=84,
             pointers={'i': 'pink'}, color=_col),
        dict(type='text', fn=lambda S: (f"本段最大耗时 `max_t = {S['max_t']}`" if 'max_t' in S else ''), size=28),
    ],
    watch=[('i', 'i', 'pink'), ('t', 't', 'blue'), ('max_t', 'max_t', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = max_t = 0': '`ans` 累计删除总耗时，`max_t` 记当前同色段里最大的耗时',
        'for i, t': lambda S, B, r: ('气球都看完了，循环结束' if B.get('i') == S.i and 'i' in B
                                     else f'看第 `{S.i}` 个气球：颜色 `{S.colors[S.i]}`，删除耗时 `{S.t}`'),
        'ans += t': '先假设整段都删掉：`ans` += {t} → =={ans}==',
        'if t > max_t': lambda S, B, r: (f'`{S.t} > {S.max_t}` → 它是目前最贵的' if S.t > S.max_t else f'`{S.t} ≤ {S.max_t}` → 最大值不变'),
        'max_t = t': '更新本段最大耗时：`max_t = {max_t}`',
        'if i == len': _end,
        'ans -= max_t': '这一段留下耗时最大的（`{max_t}`）不删，把它从总和里减掉：`ans` → =={ans}==',
        'max_t = 0': '`max_t` 清零，准备下一段',
        'return ans': '每段只留最贵的，其余都删 → 最少耗时 `{ret}`',
    },
    cards=dict(
        one_liner='每个连续同色段只留一个：贪心留耗时最大的',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['绳子上有一排气球，`colors[i]` 是颜色，`neededTime[i]` 是删掉它的耗时',
                 '要删掉一些气球，让==相邻的气球颜色都不同==，求最少总耗时',
                 '示例：`colors = "abaac"`，`neededTime = [1,2,3,4,5]` → `3`'],
        quote='对于 colors 的每个连续同色段，只能保留一个气球。贪心地，保留其中耗时最大的气球。答案为 neededTime 的总和，减去每段的最大耗时。',
        quote_src='—— 灵茶山艾府题解',
        idea=['相邻不同色 ⇒ 每个连续同色段只能剩 1 个气球',
              '要花的时间越少越好，所以留下==耗时最大==的那个',
              '答案 = 总耗时 − 每段最大耗时；遍历时遇到段尾就扣掉 `max_t`',
              '本视频用 `"aabaac"` 演示：四段 `aa`、`b`、`aa`、`c`，只有两个 `aa` 段要删'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '段尾判断：`i == len(colors) - 1` 要放在 `or` 前面，避免越界',
                 '`ans -= max_t` 之后别忘了 `max_t = 0`',
                 '手写 `if` 比较大小，比调用 `max` 更快',
                 '同类：分组循环题 3011、1759、1839'],
    ),
)
