% Countdown numbers game solver in Prolog.
% Uses backtracking search to find valid arithmetic expressions.

:- use_module(library(lists)).

% combine(EA, VA, EB, VB, CombinedExpr, CombinedValue) generates a valid operation result.
combine(EA, VA, EB, VB, add(EA, EB), V) :- VA =< VB, V is VA + VB.
combine(EA, VA, EB, VB, sub(EA, EB), V) :- VA > VB, V is VA - VB.
combine(EA, VA, EB, VB, mul(EA, EB), V) :- VA =< VB, V is VA * VB, V > 1.
combine(EA, VA, EB, VB, div(EA, EB), V) :- VB > 1, 0 is VA mod VB, V is VA // VB.

% solve(Pool, Target, Expr) succeeds when an expression evaluating to Target is found.
solve(Pool, Target, Expr) :-
    member(node(Expr, Target), Pool).
solve(Pool, Target, Expr) :-
    select(node(EA, VA), Pool, P1),
    select(node(EB, VB), P1, Rest),
    combine(EA, VA, EB, VB, NewExpr, NewVal),
    solve([node(NewExpr, NewVal) | Rest], Target, Expr).

% fmt(Expr, FormattedString) formats an expression tree into a human-readable string.
fmt(val(V), S) :- !, number_string(V, S).
fmt(Expr, S) :-
    Expr =.. [Op, L, R],
    op_char(Op, C),
    fmt(L, LS),
    fmt(R, RS),
    atomic_list_concat(['(', LS, ' ', C, ' ', RS, ')'], S).

op_char(add, +).
op_char(sub, -).
op_char(mul, *).
op_char(div, /).

% Helper to convert a number to a node.
num_to_node(N, node(val(N), N)).

% main(Target, Numbers) is called by run_all.sh to solve and display the result.
main(Target, Numbers) :-
    run([Target | Numbers]).

% run(Args) is the entry point for the SWI-Prolog interpreter.
run(Args) :-
    Args = [Target | Numbers],
    maplist(num_to_node, Numbers, Pool),
    (   solve(Pool, Target, Expr)
    ->  fmt(Expr, S),
        format('Expression: ~s~n', [S]),
        format('Value: ~d~n', [Target])
    ;   format('No solution could be generated.~n', [])
    ).