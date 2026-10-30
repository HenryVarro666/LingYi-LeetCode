
_st = {}


def _reset_z(S, B, ret):
    _st['z'] = None
    return '`z[i]`：后缀 `s[i:]` 与 `s` 的最长公共前缀长度，`z[0]` 不用算（先全填 0）'


def _for_z(S, B, ret):
    key = (S.i, len(S.s))
    done = _st.get('z') == key
    _st['z'] = key
    return f'`z[1..{S.n - 1}]` 都算完了，循环结束' if done else f'求 `z[{S.i}]`：后缀 `s[{S.i}:]` 和 `s` 的 LCP'


def _for_i(S, B, ret):
    key = S.i
    done = _st.get('i') == key
    _st['i'] = key
    return '第二段起点 `i` 都枚举完了' if done else f'枚举第二段起点 `i = {S.i}`（第一段 `nums[0:{S.i}]` 非空，第三段也要非空）'


def _for_j(S, B, ret):
    key = (S.i, S.j)
    done = _st.get('j') == key
    _st['j'] = key
    return '第三段起点 `j` 都枚举完了' if done else f'枚举第三段起点 `j = {S.j}`：第二段 `nums[{S.i}:{S.j}]`，第三段 `nums[{S.j}:]`'


def _top(S):
    ln = S['_line']
    if ln <= 15:
        who = 'calc_z 正在求 Z 数组'
        return f'{who}：`z[i]` = 后缀 `s[i:]` 与 `s` 的最长公共前缀（LCP）'
    if 'j' in S and ln >= 24 and 'z' in S and 'z0' in S:
        i, j, n = S['i'], S['j'], S['n']
        return f"三段：蓝 `nums[0:{i}]` | 黄 `nums[{i}:{j}]` | 粉 `nums[{j}:{n}]`"
    return '第一段 `nums[0:i]`，第二段 `nums[i:j]`，第三段 `nums[j:]`；枚举 i、j'


def _color(S, idx, v):
    if S['_line'] <= 15 or 'j' not in S or 'z' not in S or 'z0' not in S or S['_line'] < 23:
        return None
    i, j = S['i'], S['j']
    return 'blue' if idx < i else ('yellow' if idx < j else 'pink')


def _cond(S, B, ret):
    i, j, z0, z = S.i, S.j, S.z0, S.z
    a1 = i <= j - i
    a2 = z0[i] >= i
    b = z[j - i] >= j - i
    p1 = f'①第一段是第二段前缀：`i <= j-i` ({i} <= {j - i}) {"成立" if a1 else "不成立"}'
    if a1:
        p1 += f'，`z0[{i}] >= {i}` ({z0[i]} >= {i}) {"成立" if a2 else "不成立"}'
    p2 = f'②第二段是第三段前缀：`z[{j - i}] >= {j - i}` ({z[j - i]} >= {j - i}) {"成立" if b else "不成立"}'
    res = '==至少一个成立 → 美丽分割==' if (a1 and a2) or b else '都不成立 → 不是美丽分割'
    return p1 + '；' + p2 + ' → ' + res


CONFIG = dict(
    num=3388, title='统计数组中的美丽分割', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='Z 数组（扩展 KMP）',
    tags=['灵神题单', '字符串', '难度分 2365'],
    code='''
class Solution:
    def calc_z(self, s: List[int]) -> List[int]:
        n = len(s)
        z = [0] * n
        box_l = box_r = 0  # z-box 左右边界
        for i in range(1, n):
            if i <= box_r:
                # 手动 min，加快速度
                x = z[i - box_l]
                y = box_r - i + 1
                z[i] = x if x < y else y
            while i + z[i] < n and s[z[i]] == s[i + z[i]]:
                box_l, box_r = i, i + z[i]
                z[i] += 1
        return z

    def beautifulSplits(self, nums: List[int]) -> int:
        z0 = self.calc_z(nums)
        n = len(nums)
        ans = 0
        for i in range(1, n - 1):
            z = self.calc_z(nums[i:])
            for j in range(i + 1, n):
                if i <= j - i and z0[i] >= i or z[j - i] >= j - i:
                    ans += 1
        return ans
''',
    call='Solution().beautifulSplits([1,1,2,1])',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=24, h=70),
        dict(type='array', var=lambda S: S['s'] if S['_line'] <= 15 else S['nums'], label='s / nums（calc_z 里是 s，之后是 nums）',
             pointers={'i': 'blue'}, window=('box_l', 'box_r'), color=_color, h=200),
        dict(type='array', var='z', label='z（本次 calc_z 算出的 Z 数组）', pointers={'i': 'blue'}, h=190,
             color=lambda S, k, v: 'green' if S.get('i') == k and S['_line'] <= 15 else None),
        dict(type='array', var='z0', label='z0（nums 的 Z 数组，z0[i] = lcp[0][i]）', pointers={'i': 'blue'}, h=190),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('box_l', 'box_l', 'cyan'), ('box_r', 'box_r', 'cyan'), ('ans', 'ans', 'green')],
    max_steps=90,
    skip=['n = len(s)', 'n = len(nums)'],
    captions={
        'n = len(s)': '`s` 的长度 `n = {n}`',
        'z = [0] * n': _reset_z,
        'box_l = box_r': '`[box_l, box_r]` 是向右扩得最远的 z-box：`s[box_l..box_r]` 等于 `s` 的前缀',
        'range(1, n):': _for_z,
        'if i <= box_r': lambda S, B, ret: (f'`i = {S.i} <= box_r = {S.box_r}`：落在 z-box 内 → ==先借用 z[i - box_l]==' if S.i <= S.box_r
                                              else f'`i = {S.i} > box_r = {S.box_r}`：z-box 外面，没有现成信息，从 0 开始比'),
        'x = z[i - box_l]': '`x = z[{i} - {box_l}] = {x}`：镜像位置已经算过的 LCP',
        'y = box_r - i + 1': '`y = {box_r} - {i} + 1 = {y}`：z-box 里还剩的长度，借用不能超过它',
        'z[i] = x if': '取较小的：`z[{i}] = min({x}, {y})` = =={z[i]}==',
        'while i + z[i] < n': lambda S, B, ret: (f"比 `s[{S.z[S.i]}] = {S.s[S.z[S.i]]}` 和 `s[{S.i + S.z[S.i]}] = {S.s[S.i + S.z[S.i]]}` → ==相等==，继续扩"
                                                 if S.i + S.z[S.i] < S.n and S.s[S.z[S.i]] == S.s[S.i + S.z[S.i]]
                                                 else (f'`i + z[i] = {S.i + S.z[S.i]}` 到末尾了，停止' if S.i + S.z[S.i] >= S.n
                                                       else f"比 `s[{S.z[S.i]}] = {S.s[S.z[S.i]]}` 和 `s[{S.i + S.z[S.i]}] = {S.s[S.i + S.z[S.i]]}` → ==不等==，停止，`z[{S.i}] = {S.z[S.i]}`")),
        'box_l, box_r = i': '扩到了更靠右的位置，更新 z-box：`[{box_l}, {box_r}]`',
        'z[i] += 1': '`z[{i}]` → =={z[i]}==',
        'return z': 'Z 数组算完：`{z}`',
        'z0 = self.calc_z': '调用 `calc_z(nums)` → 得到 `z0`：`z0[i]` 就是方法一里的 `lcp[0][i]`，用来判断「第一段是第二段的前缀」',
        'n = len(nums)': '`n = {n}`',
        'ans = 0': lambda S, B, ret: (_st.clear(), '`ans` 统计美丽分割数')[1],
        'range(1, n - 1)': _for_i,
        'z = self.calc_z(nums[i:])': '再算后缀 `nums[{i}:]` 的 Z 数组 `z`：`z[j - i]` 就是 `lcp[i][j]`，用来判断「第二段是第三段的前缀」',
        'range(i + 1, n)': _for_j,
        'if i <= j - i and': _cond,
        'ans += 1': '美丽分割 +1：`ans` = =={ans}==',
        'return ans': '所有 `(i, j)` 枚举完，共 =={ret}== 个美丽分割',
    },
    cards=dict(
        one_liner='枚举两个切点，「前缀」判断全部交给 Z 数组',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['把 `nums` 切成三段非空子数组 `nums1, nums2, nums3`',
                 '`nums1` 是 `nums2` 的前缀，或 `nums2` 是 `nums3` 的前缀 → 美丽分割',
                 '示例：`[1,1,2,1]` → `2`；本视频就用示例 1'],
        quote='对于第一、二段，可以计算 nums 的 z 数组，其中 z[i] 就是方法一中的 lcp[0][i]。对于第二、三段，可以计算 nums[i:] 的 z 数组，其中 z[j-i] 就是方法一中的 lcp[i][j]。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['设第二段从 `i` 开始、第三段从 `j` 开始',
              '第一段是第二段前缀：`i <= j-i` 且 `z0[i] >= i`',
              '第二段是第三段前缀：`z[j-i] >= j-i`（长度自然够，不用再判 `j-i <= n-j`）'],
        result='`[1,1,2,1]` 一共 2 个美丽分割 ✓',
        summary=['时间 `O(n^2)`，空间 `O(n)`；方法一用 `lcp[i][j]` 二维表，空间 `O(n^2)`，思路相同',
                 '本视频演示方法二（Z 数组）：对每个 `i` 重新算一次 `nums[i:]` 的 Z',
                 '易错：`and` 比 `or` 优先，条件是「(长度够且 z0 够) 或 z 够」',
                 '同类题：2430 对字母串可执行的最大删除数、1977 划分数字的方案数'],
    ),
)
