class Solution:
    def checkTree(self, root: Optional[TreeNode]) -> bool:
        return True if root.val == root.left.val + root.right.val else False
    


##	•	== 本身就返回 True / False
##	•	没必要再包一层 True if ... else False



# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def checkTree(self, root: Optional[TreeNode]) -> bool:
        return root.val == root.left.val + root.right.val
        

## 现在把题目扩展一下：设二叉树上有 n 个节点（n≥3），且每个节点都有 0 或 2 个儿子。要求判断除了叶子节点，是否每个节点的值都等于其左右儿子的节点值之和。
class Solution:
    def checkTree(self, root: Optional[TreeNode]) -> bool:
        if root.left is None and root.right is None:  # 递归边界：判断 root 是否为叶子节点
            return True
        return root.val == root.left.val + root.right.val and self.checkTree(root.left) and self.checkTree(root.right)