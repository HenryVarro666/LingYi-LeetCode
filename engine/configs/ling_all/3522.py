INS = ["jump", "add", "add", "jump", "add", "jump"]
VAL = [2, 1, 3, 1, -2, -3]
CONFIG = dict(
    num=3522, title='执行指令后的得分', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='模拟 · vis 数组判重',
    tags=[],
    code='''
class Solution:
    def calculateScore(self, instructions: List[str], values: List[int]) -> int:
        n = len(instructions)
        vis = [False] * n
        ans = i = 0
        while 0 <= i < n and not vis[i]:
            vis[i] = True
            if instructions[i][0] == 'a':
                ans += values[i]
                i += 1
            else:
                i += values[i]
        return ans
''',
    call='Solution().calculateScore(%r, %r)' % (INS, VAL),
    expect=1,
    views=[
        dict(type='array', var='instructions', pointers={'i': 'blue'}, h=200, label='instructions',
             color=lambda S, i, v: 'green' if 'vis' in S and S['vis'][i] else None, cell=110),
        dict(type='array', var='values', pointers={'i': 'blue'}, h=200, label='values', cell=110),
        dict(type='array', var='vis', h=200, label='vis（访问过 = True）', cell=110,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='text', size=30, fn=lambda S: f"当前 `i = {S['i']}`，得分 `ans` = =={S['ans']}==" if 'i' in S and 'ans' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), ('ans', 'ans', 'green'), 'n'],
    captions={
        'vis = [False]': '`vis[i]` 记录下标 `i` 是否执行过，初始全是 ==False==',
        'ans = i = 0': '从下标 0 开始，得分 `ans = 0`',
        'while 0 <= i < n': lambda S, B, r: (f'`i = {S.i}`：{"越界了，结束" if not (0 <= S.i < S.n) else ("已经访问过，不再执行 → 结束" if S.vis[S.i] else "在范围内且没访问过 → 继续")}'),
        'vis[i] = True': '首次访问 `i = {i}`，标记 `vis[{i}] = True`：以后再来就会终止',
        "instructions[i][0] == 'a'": '`instructions[{i}]` = `{instructions[i]}`，首字母{"是 a → add，加分" if instructions[i][0] == "a" else "不是 a → jump，跳转"}',
        'ans += values[i]': 'add：把 `values[{i}]` 加到得分，`ans` = =={ans}==',
        'i += 1': 'add 之后移到下一条指令，`i` → {i}',
        'i += values[i]': 'jump：不改得分，`i` 加上 `values` 里的偏移，跳到 =={i}==',
        'return ans': '过程结束，得分 =={ret}==',
    },
    cards=dict(
        one_liner='照题意模拟，用 vis 数组发现重复访问就停',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`add`：把 `values[i]` 加到得分，走到 `i+1`',
                 '`jump`：跳到 `i + values[i]`，得分不变',
                 '越界或走到执行过的指令就停止，返回得分',
                 '本视频：`[jump,add,add,jump,add,jump]`，`[2,1,3,1,-2,-3]` → `1`'],
        quote='如何知道当前位置是否访问过？创建一个布尔数组 vis。首次访问 i 时，标记 vis[i]=true。',
        quote_src='—— 灵茶山艾府题解',
        idea=['按题意一步步模拟，循环条件同时检查「不越界」和「没访问过」',
              '每个下标至多被执行一次，所以总共最多 `n` 步',
              '灵神写 `instructions[i][0] == \'a\'` 只看首字母区分 add / jump'],
        after=[dict(heading='写法二', lines=['把执行过的 `instructions[i]` 置为 `None`，代替 `vis` 数组',
                                              '空间降到 `O(1)`，但会修改入参，工程里不推荐'])],
        summary=['时间 `O(n)`，空间 `O(n)`（vis 数组）',
                 '易错：`0 <= i < n` 要写在 `vis[i]` 前面，否则越界下标会报错',
                 '重复访问的指令==不会再执行==，所以先判重再标记',
                 '写法二用置空代替 vis，空间 `O(1)` 但会改入参'],
    ),
)
