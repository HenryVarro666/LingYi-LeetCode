CONFIG = dict(
    num=2697, title='字典序最小回文串', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='相向双指针 · 改大的为小的',
    tags=['灵神题单', '难度分 1304'],
    code='''
class Solution(object):
    def makeSmallestPalindrome(self, s):

        left = 0
        right = len(s) - 1
        res = list(s)
        while left < right:
            if res[left] < res[right]:
                res[right] = res[left]
            else:
                res[left] = res[right]
            
            left += 1
            right -= 1
        
        return ''.join(res)
''',
    call="Solution().makeSmallestPalindrome('cabzxb')",
    expect='babbab',
    views=[
        dict(type='text', fn=lambda S: (f"这一对：`{S['res'][S['left']]}` 和 `{S['res'][S['right']]}`" + ('，已相等，不用改' if S['res'][S['left']] == S['res'][S['right']] else '，不等，改大的为小的')) if 'right' in S and 'res' in S and S['left'] < S['right'] else '', size=30),
        dict(type='string', var='res', pointers={'left': 'blue', 'right': 'pink'}, h=300,
             color=lambda S, i, v: ('blue' if i == S['left'] else 'pink' if i == S['right'] else None) if 'right' in S else None,
             dim=lambda S, i, v: 'right' in S and S['left'] <= S['right'] and not (i == S['left'] or i == S['right']) and (i < S['left'] or i > S['right'])),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink')],
    captions={
        'left = 0': '`left = 0`：左指针从头出发',
        'right = len': '`right = len(s) - 1` = {right}：左右指针从两端出发',
        'res = list': '字符串不能原地改，先拷成列表 `res`',
        'while left < right': lambda S, B, r: (f"`left = {S.left} < right = {S.right}`：还有没配对的两端 → 继续" if S.left < S.right else f"`left = {S.left} >= right = {S.right}`：每一对都处理完了"),
        'if res[left] < res[right]': lambda S, B, r: f"比较 `{S.res[S.left]}` 与 `{S.res[S.right]}` → " + ('左边更小' if S.res[S.left] < S.res[S.right] else '左边不更小（右边更小或相等）'),
        'res[right] = res[left]': '左边小：把右边改成 `{res[left]}`，只改 1 个字符、字典序又最小',
        'res[left] = res[right]': '右边更小或相等：把左边改成 `{res[right]}`（相等时等于没改）',
        'left += 1': '`left` → {left}',
        'right -= 1': '`right` → {right}',
        'return': "回文构造完成：返回 `{''.join(res)}`",
    },
    cards=dict(
        one_liner='不等的一对，把大的字符改成小的',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给小写字符串 `s`，每步可替换一个字符，用最少次数变成回文串',
                 '最少次数的方案不止一种时，取字典序最小的',
                 '示例：`"seven"` → `"neven"`','本视频用 `"cabzxb"` → `"babbab"`'],
        quote='为了使得修改的总次数最小，每次就只能修改其中的一个字符。又因为要使得最终的字符串字典序最小，因此只能将字典序较大的那个修改成字典序较小的那个。',
        quote_src='—— yiduobo 题解原文',
        idea=['从两侧向中心遍历，每一对必须相等',
              '不等时只改一个字符，次数最少',
              '改大的为小的，字典序最小'],
        summary=['时间 `O(n)`，空间 `O(n)`（字符串不可变，要拷成列表）',
                 '`while left < right`：奇数长度的中间字符不用管',
                 '相等的一对走 else 分支，赋值等于没改',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
