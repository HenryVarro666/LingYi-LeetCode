CONFIG = dict(
    num=3964, title='照亮道路的最少灯泡数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='差分数组 + 贪心装灯',
    tags=['灵神题单·常用数据结构', '灵神题单·贪心与思维', '难度分 1572'],
    code='''
class Solution:
    def minLights(self, lights: list[int]) -> int:
        n = len(lights)
        diff = [0] * (n + 1)
        for i, v in enumerate(lights):
            if v > 0:
                # 照亮 [max(i-v, 0), min(i+v, n-1)]
                diff[max(i - v, 0)] += 1
                diff[min(i + v + 1, n)] -= 1

        ans = sum_d = 0
        for i in range(n):
            sum_d += diff[i]
            if sum_d == 0:
                # 在 i+1 装一个灯泡，照亮 [i, i+2]
                ans += 1
                sum_d += 1  # diff[i] += 1 直接更新到 sum_d 中
                diff[min(i + 3, n)] -= 1
        return ans
''',
    call='Solution().minLights([0,0,0,0,0,1,0,0])',
    expect=3,
    views=[
        dict(type='array', var='lights', pointers={'i': 'blue'}, h=170, label='lights（原有灯泡的照射半径）'),
        dict(type='array', var='diff', pointers={'i': 'blue'}, h=170, label='diff（差分数组）'),
        dict(type='text', fn=lambda S: (f"位置 `{S['i']}`：照到它的灯泡数 `sum_d` = =={S['sum_d']}==，已加灯 `ans` = {S['ans']}" if 'sum_d' in S and 'ans' in S and S.get('_line', 0) >= 12 else '')),
    ],
    watch=['i', ('v', 'v', 'cyan'), ('sum_d', 'sum_d', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'diff = [0]': '差分数组，多开一位放 `min(i+v+1, n)`',
        'if v > 0': lambda S, B, r: f'`lights[{S.i}] = {S.v}`：' + ('有灯泡，要照亮一段' if S.v > 0 else '没灯泡，跳过'),
        'diff[max(i - v, 0)] += 1': '灯泡照亮 `[{max(i-v,0)}, {min(i+v,n-1)}]`：左端点处 `+1` → `diff[{max(i-v,0)}] = {diff[max(i-v,0)]}`',
        'diff[min(i + v + 1, n)] -= 1': '右端点后一位 `−1`，区间加一就做完了 → `diff[{min(i+v+1,n)}] = {diff[min(i+v+1,n)]}`',
        'ans = sum_d = 0': '`sum_d` 是 `diff` 的前缀和 = 当前位置被几个灯泡照亮；`ans` 是新装的灯数',
        'sum_d += diff[i]': '前缀和：位置 `{i}` 被 =={sum_d}== 个灯泡照亮',
        'if sum_d == 0': lambda S, B, r: f'位置 `{S.i}` 被照亮 {S.sum_d} 次：' + ('==没人照到==，必须装新灯' if S.sum_d == 0 else '已经可见，不用管'),
        'ans += 1': '位置 `{i}` 没照到：贪心地装在 `{min(i+1,n-1)}`（`i+1`，到头则 `n-1`），能照 `[{i}, {min(i+2,n-1)}]`，向右覆盖最多 → `ans = {ans}`',
        'sum_d += 1': '新灯照亮当前位置：直接 `sum_d += 1`，代替 `diff[i] += 1` → {sum_d}',
        'diff[min(i + 3, n)] -= 1': '新灯到 `{min(i+2,n-1)}` 为止：在 `{min(i+3,n)}` 处 `−1` → `diff[{min(i+3,n)}] = {diff[min(i+3,n)]}`',
        'return ans': '全部位置都可见，最少加 `{ans}` 个灯泡',
    },
    cards=dict(
        one_liner='差分数组边扫边查，发现黑的位置就在它右边一格装灯',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`lights[i] = v > 0`：位置 `i` 的灯泡照亮 `[i−v, i+v]`；`0` 表示没灯',
                 '可额外装灯，每个只照亮自己和左右各一格',
                 '求让所有位置都可见的最少额外灯数；示例 `[0,0,0,2,0]` → `1`；本视频 `[0,0,0,0,0,1,0,0]` → `3`'],
        quote='如果遍历到位置 i 时，发现位置 i 没被照亮，那么贪心地，在 i+1 处安装灯泡，照亮 [i,i+2]，更新差分数组。',
        quote_src='—— 灵茶山艾府题解',
        idea=['原有灯泡是区间加一：用差分数组，前缀和就是每个位置被照亮的次数',
              '从左往右，第一个照不到的位置 `i`，左边没有需求了，灯装在 `i+1` 覆盖最靠右',
              '新灯直接把 `sum_d += 1`，并在 `i+3` 处记 `−1`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`diff` 开 `n + 1`，右端点要 `min(i+v+1, n)`，新灯是 `min(i+3, n)`',
                 '`i = n−1` 时灯装在 `n−1` 同样照亮 `n−1`，不影响结果',
                 '同类题：差分数组 §2.1；区间贪心 §2.5'],
    ),
)
