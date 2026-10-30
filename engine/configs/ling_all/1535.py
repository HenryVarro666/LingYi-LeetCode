CONFIG = dict(
    num=1535, title='找出数组游戏的赢家', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='遍历打擂台',
    code='''
class Solution:
    def getWinner(self, arr: List[int], k: int) -> int:
        mx = arr[0]
        win = -1  # 对于 arr[0] 来说，需要连续 k+1 个回合都是最大值
        for x in arr:
            if x > mx:  # 新的最大值
                mx = x
                win = 0
            win += 1  # 获胜回合 +1
            if win == k:
                break
        return mx
''',
    call='Solution().getWinner([2,1,3,5,4,6,7], 2)',
    expect=5,
    views=[
        dict(type='text', fn=lambda S: f"擂主 `mx = {S['mx']}`，已连续获胜 ==`{S['win']}`== / {S['k']} 回合" if 'win' in S else ''),
        dict(type='array', var='arr', pointers={'x': 'blue'} if False else {}, h=300,
             color=lambda S, i, v: ('green' if v == S.get('mx') else None) if 'mx' in S else None,
             label='arr（绿色 = 当前擂主）'),
    ],
    watch=['k', ('mx', 'mx', 'green'), ('win', 'win', 'yellow'), 'x'],
    captions={
        'mx = arr[0]': '擂主先设为 `arr[0] = {mx}`：游戏本质是从左到右遍历，打擂台求最大值',
        'win = -1': '`arr[0]` 没有和别人比过，所以要连赢 `k+1` 回合才算数，故 `win` 从 `-1` 开始',
        'for x in arr': '取下一个挑战者 `x = {x}`',
        'if x > mx': lambda S, B, r: (f'`{S.x} > {S.mx}`：挑战者更大 → 成立，新擂主上台' if S.x > S.mx
                                       else f'`{S.x}` 就是 `arr[0]` 自己，不大于 mx → 不成立' if S.x == S.mx
                                       else f'`{S.x} < {S.mx}`：挑战者更小 → 不成立，它被移到末尾，擂主守擂'),
        'mx = x': '擂主换人：`mx = {mx}`',
        'win = 0': '新擂主刚上台，连胜清零：`win = 0`',
        'win += 1': '擂主又赢一回合（新擂主算赢下刚才那局）：`win = {win}`',
        'if win == k': lambda S, B, r: (f'`win = {S.win} == k = {S.k}`：连胜够了 → ==成立==，游戏结束' if S.win == S.k
                                         else f'`win = {S.win}`，还没到 `k = {S.k}` → 继续'),
        'break': '连胜 `k` 回合，赢家就是 `mx = {mx}`，退出循环',
        'return mx': '返回擂主 `{mx}`（若遍历完都没人连胜 k 局，最大值 mx 一定是赢家）',
    },
    cards=dict(
        one_liner='游戏就是从左到右打擂台，找首个连胜 k 回合的擂主',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组前两个数比大小，大的留在 `0` 位，小的移到末尾',
                 '某个数连赢 `k` 回合就是赢家，求这个数',
                 '示例：`arr=[2,1,3,5,4,6,7], k=2` → `5`'],
        quote='考察游戏执行的流程，本质上是在从左到右遍历 arr，求数组最大值（打擂台）。我们要找首个连续 k 回合都是最大值的数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['小的数被移到末尾，重新遇到它们之前，每个元素都先被访问一遍',
              '所以不必真的搬动数组：遍历 `arr`，维护擂主 `mx` 和连胜数 `win`',
              '遍历完还没人连胜 `k` 次，最大值就是赢家：比它小的都排在它后面'],
        summary=['时间 `O(n)`，空间 `O(1)`，不需要真的模拟队列',
                 '易错点：`arr[0]` 要连赢 `k+1` 回合才算（它没有先赢过一局），所以 `win` 初始为 `-1`',
                 '换成新最大值时 `win = 0`，随后 `win += 1` 算它赢下的这一局',
                 '`k` 很大也没关系：遍历结束返回最大值即可'],
    ),
)
