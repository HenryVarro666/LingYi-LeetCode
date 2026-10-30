def _fmt(v):
    return '-' if v == -1 else str(v)


def _txt(S):
    if 'v' not in S or 'now' not in S:
        return f"当前这一段的目标 `v = {S['v']}`" if 'v' in S else ''
    now = S['now']
    return (f"目标 `v = {S['v']}`；`now` = ==`{now if now is not None else '空'}`==（以 index 结尾的按位与）；"
            f"左端点范围 `[{S['left']}, {S['right']}]`，其中 `g` 最小值 `best` = ==`{_fmt(S['best'])}`==")


CONFIG = dict(
    num=3117, title='划分数组得到最小的值之和', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间划分 DP · 滑动窗口求转移最小值',
    tags=['灵神题单·位运算', '灵神题单·动态规划', '难度分 2735'],
    code='''
class Solution(object):
    def minimumValueSum(self, nums, andValues):

        n = len(nums)
        f = [-1] * (n + 1)
        f[0] = 0
        for v in andValues:
            g = f[:]
            f = [-1] * (n + 1)
            best = -1
            freq = [0] * 17
            now = None
            left = right = 0

            for index, x in enumerate(nums):
                if now is None:
                    now = nums[index]
                    left = right = index
                    best = -1
                else:
                    now &= x

                for t in range(17):
                    if x & (1 << t) == (1 << t):
                        freq[t] += 1

                if now == v:
                    if best == -1:
                        best = g[left]
                    while right < index:
                        tmp = 0
                        remove_pos = []
                        flag = True
                        for t in range(17):
                            if (nums[right] & (1 << t) == (1 << t)):
                                remove_pos.append(t)
                            elif freq[t] == index - right:
                                flag = False
                                break
                        
                        if flag:
                            for p in remove_pos:
                                freq[p] -= 1

                            right += 1
                            if best == -1 or (g[right] != -1 and best > g[right]):
                                best = g[right]
                        else:
                            break

                    if best != -1 and (f[index + 1] == -1 or f[index + 1] > best + x):
                        f[index + 1] = best + x
                    

                elif (now & v) < v:
                    now = None
                    freq = [0] * 17
            
        return f[-1]
''',
    call='Solution().minimumValueSum([1, 4, 3], [0, 3])',
    expect=7,
    skip=['for t in range(17)', 'if x & (1 << t)', 'freq[t] += 1', 'tmp = 0', 'remove_pos = []', 'flag = True', 'if (nums[right]',
          'remove_pos.append', 'elif freq[t]', 'flag = False', 'for p in remove_pos', 'freq[p] -= 1', 'g = f[:]', 'f = [-1] * (n + 1)',
          'freq = [0] * 17', 'left = right = 0', 'best = -1', 'now = None'],
    max_steps=100,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = index，窗口 = 可作段首的左端点范围）', h=150, cell=70,
             pointers={'index': 'blue'}, window=('left', 'right'),
             color=lambda S, k, v: 'blue' if k == S.get('index') else None),
        dict(type='array', var='g', label='g（上一段的 f，-1 = 不可能）', h=130, cell=70, fmt=_fmt),
        dict(type='array', var='f', label='f（这一段的结果）', h=130, cell=70, fmt=_fmt,
             color=lambda S, k, v: 'green' if k == S.get('index', -9) + 1 and v != -1 else None),
        dict(type='text', fn=_txt, size=22, h=70),
    ],
    watch=[('v', 'v', 'orange'), ('index', 'index', 'blue'), ('now', 'now', 'cyan'), ('best', 'best', 'green')],
    captions={
        'n = len': '`f[i]` = 前 `i` 个数分成若干段的最小值之和，`-1` 表示不可能',
        'f[0] = 0': '前 0 个数分成 0 段，和为 0',
        'for v in andValues': '开始划分下一段，这段的按位与必须等于 `v = {v}`',
        'for index, x in enumerate': '考虑 `nums[{index}] = {x}`',
        'if now is None': lambda S, B, r: ('`now` 为空：以 `nums[index]` 作为新窗口的起点' if S.now is None else '`now` 已有值：把 `x` 继续与进去'),
        'left = right = index': '`now = {now}`，窗口左右端点都从 `{index}` 开始',
        'now &= x': '`now` = {B.now} & {x} = =={now}==',
        'if now == v': lambda S, B, r: (f'`now = {S.now}` == `v = {S.v}`：存在合法划分，可以更新 f' if S.now == S.v
                                       else f'`now = {S.now}` ≠ `v = {S.v}`'),
        'if best == -1:': lambda S, B, r: ('还没有 best：取窗口最左端 `g[left]`' if S.best == -1 else '`best` 已有，在它的基础上扩展右端'),
        'best = g[left]': '`best = g[{left}] = {best}`',
        'while right < index': 'right 能右移吗？移走 `nums[right]` 后 `now` 不能变大（用 `freq` 统计每位上 1 的个数判断）',
        'if flag': lambda S, B, r: ('可以移动：`now` 在每个位上的 0 不会被弹掉' if S.flag else '不能移动：`nums[right]` 是某位上唯一的 0，弹出后 `now` 会变大 → 停'),
        'right += 1': '`right` 右移到 `{right}`',
        'if best == -1 or': '新进入范围的 `g[right]` 若更小，就更新 `best`',
        'best = g[right]': '`best = g[{right}] = {best}`',
        'if best != -1 and': lambda S, B, r: (f'`f[{S.index + 1}]` = `best + x` = `{S.best} + {S.x}` = =={S.best + S.x}==' if S.best != -1 and (S.f[S.index + 1] == -1 or S.f[S.index + 1] > S.best + S.x)
                                              else '`best = -1`：左端点范围里的 g 都不可能，f 保持 -1'),
        'f[index + 1] = best + x': '`f[{index + 1}] = {best} + {x}` = =={f[index + 1]}==',
        'elif (now & v) < v': lambda S, B, r: (f'`now & v = {S.now & S.v}` < `v`：有 v 的某位已经丢了，再 AND 也不会等于 v → 清空窗口' if (S.now & S.v) < S.v
                                              else f'`now = {S.now}` > `v`：还有机会降到 v，继续向右'),
        'return f[-1]': lambda S, B, r: f'`f[-1]` = =={r}==',
    },
    cards=dict(
        one_liner='区间划分 DP：转移来自一个窗口，用滑动窗口取最小',
        complexity='时间 `O(n m log U)`，空间 `O(n)`',
        problem=['把 `nums` 分成 `m` 段，第 `i` 段按位与等于 `andValues[i]`',
                 '每段的值是最后一个元素，求值之和最小；不可能则 `-1`',
                 '示例：`nums=[1,4,3,3,2], andValues=[0,3,3,2]` → `12`',
                 '本视频：`nums=[1,4,3,2], andValues=[0,3,2]` → `7`'],
        quote='按位与结果是单调不增的……当now等于andValues[j]时，就可以找出left - 1到right - 1中最小的f值best来更新f[i][j]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j] = min(f[p-1][j-1] + nums[i])`，要求 `nums[p..i]` 按位与等于 `andValues[j]`',
              '朴素枚举起点 `p` 是 `O(n²m)`，太慢',
              '按位与单调不增：合法的 `p` 是一个窗口 `[left, right]`',
              '`now` 记录窗口按位与，`freq[t]` 记录第 t 位有多少个 1，判断 `right` 能否右移'],
        summary=['时间 `O(n m log U)`，空间 `O(n)`（滚动数组）',
                 '`now > v`：别急着清空，后面还可能降到 `v`；`now & v < v` 才彻底失败',
                 '`right` 右移前要查 `freq`：不能弹出某位上唯一的 0',
                 '对比灵神：灵神用 `@cache` 的 `dfs(i,j,and_)` 或单调队列，这里是自己维护窗口'],
    ),
)
