-- Countdown numbers game solver in Haskell.
-- Uses a tree-based recursive search to find valid arithmetic expressions.

import System.Environment (getArgs)

-- | Expression tree representing a computation.
data Expr
    = Val Int
    | Add Expr Expr
    | Sub Expr Expr
    | Mul Expr Expr
    | Div Expr Expr
    deriving (Show)

-- | Evaluate an expression to its integer result.
eval :: Expr -> Int
eval (Val n)    = n
eval (Add l r)  = eval l + eval r
eval (Sub l r)  = eval l - eval r
eval (Mul l r)  = eval l * eval r
eval (Div l r)  = eval l `div` eval r

-- | Format expression as a readable string.
formatExpr :: Expr -> String
formatExpr = go True
  where
    go :: Bool -> Expr -> String
    go _ (Val n) = show n
    go outer (Add l r) = wrap outer (go False l ++ " + " ++ go False r)
    go outer (Sub l r) = wrap outer (go False l ++ " - " ++ go False r)
    go outer (Mul l r) = wrap outer (go False l ++ " * " ++ go False r)
    go outer (Div l r) = wrap outer (go False l ++ " / " ++ go False r)
    wrap False s = "(" ++ s ++ ")"
    wrap _   s   = s

-- | Remove element at a given index from a list.
removeAt :: [a] -> Int -> [a]
removeAt xs i = take i xs ++ drop (i + 1) xs

-- | Generate all valid operation results from two (value, expr) pairs.
candidates :: (Int, Expr) -> (Int, Expr) -> [(Int, Expr)]
candidates (v1, e1) (v2, e2) =
    [ (v1 + v2, Add e1 e2)
    , (v1 * v2, Mul e1 e2)
    ]
    ++ [ (v1 - v2, Sub e1 e2) | v1 > v2 ]
    ++ [ (v2 - v1, Sub e2 e1) | v2 > v1 ]
    ++ [ (v1 `div` v2, Div e1 e2) | v2 /= 0, v1 `mod` v2 == 0 ]
    ++ [ (v2 `div` v1, Div e2 e1) | v1 /= 0, v2 `mod` v1 == 0 ]

-- | Recursive solver that tries all pair combinations to reach the target.
solve :: Int -> [(Int, Expr)] -> Maybe Expr
solve target pool =
    -- Check if any value directly matches target
    case [ e | (v, e) <- pool, v == target ] of
        (e:_) -> Just e
        [] ->
            if length pool < 2
                then Nothing
                else findInPairs target pool

-- | Try all pairs in pool, combine them, and recurse.
findInPairs :: Int -> [(Int, Expr)] -> Maybe Expr
findInPairs target pool = firstJust $ do
    i <- [0 .. length pool - 1]
    j <- [i + 1 .. length pool - 1]
    let (v1, e1) = pool !! i
        (v2, e2) = pool !! j
        rest = removeAt (removeAt pool i) $ if j > i then j - 1 else j
    (v, e) <- candidates (v1, e1) (v2, e2)
    return $ solve target ((v, e) : rest)
  where
    firstJust [] = Nothing
    firstJust (Nothing:xs) = firstJust xs
    firstJust (Just x:_) = Just x

-- | Entry point: create initial pool and search.
findSolution :: Int -> [Int] -> Maybe Expr
findSolution target nums = solve target [(n, Val n) | n <- nums]

-- | Main entry point.
main :: IO ()
main = do
    args <- getArgs
    case args of
        [] -> putStrLn "Usage: countdown <target> <n1> <n2> ... <nk>"
        (t:ns) ->
            let target = read t :: Int
                nums   = map read ns :: [Int]
            in case findSolution target nums of
                Just expr -> do
                    putStrLn $ "Expression: " ++ formatExpr expr
                    putStrLn $ "Value: " ++ show (eval expr)
                Nothing ->
                    putStrLn "No solution could be generated."