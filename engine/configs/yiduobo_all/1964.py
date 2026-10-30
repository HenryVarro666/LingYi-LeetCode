CONFIG = dict(
    num=1964, title='找出到每个位置为止最长的有效障碍赛跑路线', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='贪心 + 二分 · 每位置最长不减子序列', tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1933'],
    code='''
class Solution(object):
    def longestObstacleCourseAtEachPosition(self, obstacles):

        res = [1]
        now = [obstacles[0]]
        for obstacle in obstacles[1:]:
            if obstacle >= now[-1]:
                res.append(len(now) + 1)
                now.append(obstacle)
            else:
                l = 0
                r = len(now) - 1
                while l < r:
                    mid = (l + r) >> 1
                    if now[mid] <= obstacle:
                        l = mid + 1
                    else:
                        r = mid

                res.append(l + 1)
                now[l] = obstacle

        return res
''',
    call='Solution().longestObstacleCourseAtEachPosition([3,1,5,6,4,2])',
    expect=[1, 1, 2, 3, 2, 2],
    views=[
        dict(type='array', var='obstacles', h=170, label='obstacles（黄色 = 当前 obstacle）',
             color=lambda S, i, v: 'yellow' if 'obstacle' in S and v == S['obstacle'] else None),
        dict(type='array', var='now', h=210, label='now：各长度的最小结尾', pointers={'l': 'blue', 'r': 'pink'}),
        dict(type='array', var='res', h=170, label='res：每个位置的答案', color=lambda S, i, v: 'green' if i == len(S['res']) - 1 else None),
    ],
    watch=[('obstacle', 'obstacle', 'yellow'), ('l', 'l', 'blue'), ('r', 'r', 'pink')],
    captions={
        'res = [1]': '`res[i]` 是以第 i 个障碍结尾的最长路线；第 0 个只能是 `1`',
        'now = [': '`now[p]`：长度 `p+1` 的路线里最小的末尾高度，先放 `{now[0]}`',
        'if obstacle >= now[-1]': lambda S, B, r: (f'`{S.obstacle} >= {S.now[-1]}`：不低于末尾，能接在最长路线后面' if S.obstacle >= S.now[-1]
                                                  else f'`{S.obstacle} < {S.now[-1]}`：接不到最长的后面，要二分找位置'),
        'res.append(len(now) + 1)': '最长路线再延长一格：`res` 加入 `{len(now) + 1}`',
        'now.append': '`now` 末尾加入 `{obstacle}`，最长长度变为 {len(now)}',
        'l = 0': '二分区间 `[0, {len(now) - 1}]`：找 `now` 中第一个 `> {obstacle}` 的位置 p',
        'while l < r': lambda S, B, r_: (f'区间 `[{S.l}, {S.r}]` 未收缩完' if S.l < S.r else f'`l = r = {S.l}`：p 找到了'),
        'mid = ': '`mid = ({l} + {r}) >> 1 = {mid}`',
        'if now[mid] <= obstacle': lambda S, B, r: (f'`now[{S.mid}] = {S.now[S.mid]} <= {S.obstacle}`：相等也能接 → p 在右边，`l = mid + 1`' if S.now[S.mid] <= S.obstacle
                                                    else f'`now[{S.mid}] = {S.now[S.mid]} > {S.obstacle}`：p 在 mid 或左边，`r = mid`'),
        'res.append(l + 1)': lambda S, B, r: (f'`l = {S.l}`：比 now 里所有数都小，只能自成开头，长度 =={S.l + 1}==，记入 `res`' if S.l == 0 else f'接在 `now[{S.l - 1}]` 后面，长度 `{S.l} + 1` = =={S.l + 1}==，记入 `res`'),
        'now[l] = obstacle': '`now[{l}]` 改成更小的 `{obstacle}`：长度不变，后面的障碍更容易接上',
        'return res': '每个位置的最长路线：`{res}`',
    },
    cards=dict(
        one_liner='对每个位置，二分找它在最长不减序列里的落点',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给定障碍高度 `obstacles`，对每个位置 `i`，求必须包含 `i` 的最长不减路线长度',
                 '路线按原顺序选，后一个不能比前一个矮',
                 '示例：`[3,1,5,6,4,2]` → `[1,1,2,3,2,2]`'],
        quote='找到其中最小的那个，设其在当前最长上升子序列中的位置为p，那么x就可以加在第p - 1个数的后面，因此此时应该使用p + 1来更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['维护 `now`：每个长度对应的最小末尾，有序可二分',
              '能放最后就放；否则找第一个比它大的位置 p，答案 `p + 1`',
              '同时用它替换 `now[p]`：更小的末尾对后面更有利'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '不减允许相等，二分找第一个严格大于的位置',
                 '`now` 不是真实路线，只记录各长度的最小末尾',
                 '原文是 Python 3 可运行写法，无需修改',
                 '本题与 300 题的区别：这里要记录每个位置的长度，而不只是最终长度'],
    ),
)
