FRUITS = [3, 1, 2, 1, 2, 2, 3]
TYPE_COL = {1: 'blue', 2: 'pink', 3: 'purple'}


def _win(S):
    if 'right' not in S:
        return None
    return S['left'], S['right']


def _text(S):
    w = _win(S)
    if w is None:
        return '窗口 `fruits[left..right]` 内至多两种水果'
    l, r = w
    if l > r:
        return ''
    sub = FRUITS[l:r + 1]
    k = len(set(sub))
    tag = '==超过 2 种==' if k > 2 else f'{k} 种'
    return f'窗口 `[{l}, {r}]` = `{sub}`：{tag}，长度 `{r - l + 1}`'


def _cap_in(S, B, ret):
    return f'枚举右端点 `right = {S.right}`：`{S.in_}` 进入窗口 → `cnt[{S.in_}] = {S.cnt[S.in_]}`'


def _cap_while(S, B, ret):
    k = len(S.cnt)
    if k > 2:
        return f'窗口里有 `{k}` 种水果 > 2 → ==不满足要求==，移动左端点'
    return f'`{k}` 种 ≤ 2，窗口合法'


CONFIG = dict(
    num=904, title='水果成篮', difficulty='Medium', category='滑动窗口',
    author='灵茶山艾府', technique='不定长滑动窗口 · 越短越合法',
    tags=['字节30天'],
    code='''
class Solution:
    def totalFruit(self, fruits: List[int]) -> int:
        ans = left = 0
        cnt = defaultdict(int)
        for right, in_ in enumerate(fruits):
            cnt[in_] += 1  # fruits[right] 进入窗口
            while len(cnt) > 2:  # 不满足要求
                out = fruits[left]
                cnt[out] -= 1  # fruits[left] 离开窗口
                if cnt[out] == 0:
                    del cnt[out]
                left += 1
            ans = max(ans, right - left + 1)
        return ans
''',
    call=f'Solution().totalFruit({FRUITS})',
    expect=5,
    skip=['for right, in_ in'],
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='array', var='fruits', label='fruits（颜色 = 水果种类，框 = 窗口）', cell=104,
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'),
             color=lambda S, i, v: TYPE_COL.get(v),
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right']), h=250),
        dict(type='map', var='cnt', label='cnt（窗口内：种类 → 个数；键的个数 = 种类数）',
             fmt=lambda k, v: f'{k}: {v}', font=30, h=130),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('len(cnt)', 'len(cnt)'), 'out', ('ans', 'ans', 'green')],
    captions={
        'ans = left = 0': '`left` 是窗口左端点，`ans` 记录最长的合法窗口',
        'cnt = defaultdict': '`cnt`：窗口内每种水果的个数，`len(cnt)` 就是==种类数==',
        'cnt[in_] += 1': _cap_in,
        'while len(cnt) > 2': _cap_while,
        'out = fruits[left]': '左端点的水果 `out = fruits[{left}] = {out}`',
        'cnt[out] -= 1': '`{out}` 离开窗口 → `cnt[{out}] = {cnt[out]}`',
        'if cnt[out] == 0': lambda S, B, r: (f'`cnt[{S.out}] = 0`：窗口里已经没有 `{S.out}` 了' if S.cnt[S.out] == 0
                                             else f'`{S.out}` 还剩 `{S.cnt[S.out]}` 个，种类数不变'),
        'del cnt[out]': '==必须删掉==键 `{B.out}`：否则 `len(cnt)` 仍会把它算作一种',
        'left += 1': '`left` 右移到 {left}',
        'ans = max': '窗口 `[{left}, {right}]` 合法，长 `{right - left + 1}` → `ans = max({B.ans}, {right - left + 1}) = {ans}`',
        'return ans': '最多可以收集 =={ret}== 个水果',
    },
    cards=dict(
        one_liner='越短越合法：枚举右端点，种类超过 2 就移动左端点',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一排果树，`fruits[i]` 是第 `i` 棵树的水果==种类==；你只有两个篮子，每个只装一种',
                 '从任意一棵树开始向右，每棵树摘一个；遇到装不下的种类就停',
                 '即：求==至多包含两种数字==的最长连续子数组的长度',
                 f'示例：`[1,2,3,2,2]` → `4`；本视频：`{FRUITS}` → `5`'],
        quote='子数组越长，包含的元素越多，越可能不满足题目要求；反之，子数组越短，包含的元素越少，越可能满足题目要求。本题属于==「越短越合法」==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举子数组的右端点 `right`，哈希表 `cnt` 维护窗口内每个元素的出现次数',
              '加入 `fruits[right]` 后若 `len(cnt) > 2`，就右移 `left` 并把次数减一',
              '直到只剩 2 种；此时窗口合法，用 `right - left + 1` 更新答案'],
        result='`ans = 5`：窗口 `[1, 5]` = `[1,2,1,2,2]`',
        summary=['时间 `O(n)`：每个元素最多进、出窗口各一次',
                 '空间 `O(1)`：任意时刻 `cnt` 至多 3 个键',
                 '易错：次数减到 0 必须 `del cnt[out]`，否则 `len(cnt)` 判断不了种类数',
                 '在 `while` 之后更新答案：此时窗口一定合法',
                 '同类：3. 无重复字符的最长子串（也是「越短越合法」求最长）'],
    ),
)
