import System.Environment (getArgs)
import Data.Maybe (listToMaybe, mapMaybe)

-- | Operation type representing addition, subtraction, multiplication, and division.
data Op = Add | Sub | Mul | Div deriving (Show)

-- | Expression tree representing a computation.
data Expr = Val Int | App Op Expr Expr deriving (Show)

-- | Evaluate an expression to its integer result.
eval :: Expr -> Int
eval (Val n) = n
eval (App Add l r) = eval l + eval r
eval (App Sub l r) = eval l - eval r
eval (App Mul l r) = eval l * eval r
eval (App Div l r) = eval l `div` eval r

-- | Format expression as a readable string with parentheses.
formatExpr :: Expr -> String
formatExpr (Val n) = show n
formatExpr (App op l r) = "(" ++ formatExpr l ++ " " ++ sym op ++ " " ++ formatExpr r ++ ")"
  where sym Add = "+"; sym Sub = "-"; sym Mul = "*"; sym Div = "/"

-- | Generate all valid operation results from two (value, expr) pairs.
candidates :: (Int, Expr) -> (Int, Expr) -> [(Int, Expr)]
candidates (x, l) (y, r) = 
  [(x + y, App Add l r), (x * y, App Mul l r)] ++
  [(x - y, App Sub l r) | x > y] ++
  [(y - x, App Sub r l) | y > x] ++
  [(x `div` y, App Div l r) | y /= 0, x `mod` y == 0] ++
  [(y `div` x, App Div r l) | x /= 0, y `mod` x == 0]

-- | Select all pairs of elements from a list, returning them and the remaining elements.
select2 :: [a] -> [(a, a, [a])]
select2 [] = []
select2 (x:xs) = [(x, y, ys) | (y, ys) <- select1 xs] ++ [(y, z, x:ys) | (y, z, ys) <- select2 xs]

-- | Select one element from a list, returning it and the remaining elements.
select1 :: [a] -> [(a, [a])]
select1 [] = []
select1 (x:xs) = (x, xs) : [(y, x:ys) | (y, ys) <- select1 xs]

-- | Recursive solver that tries all pair combinations to reach the target.
solve :: Int -> [(Int, Expr)] -> Maybe Expr
solve target pool 
  | not (null hits) = Just (head hits)
  | otherwise = listToMaybe $ mapMaybe (solve target) 
      [ (v, e) : rest | (a, b, rest) <- select2 pool, (v, e) <- candidates a b ]
  where hits = [e | (v, e) <- pool, v == target]

-- | Main entry point.
main :: IO ()
main = do
  args <- getArgs
  case map read args of
    (target:nums) -> case solve target [(n, Val n) | n <- nums] of
      Just expr -> putStrLn $ "Expression: " ++ formatExpr expr ++ "\nValue: " ++ show (eval expr)
      Nothing   -> putStrLn "No solution could be generated."
    _ -> putStrLn "Usage: countdown <target> <n1> <n2> ..."