% Countdown numbers game solver in Prolog.
% Uses backtracking search to find valid arithmetic expressions.

:- use_module(library(lists)).

% === Expression Evaluation ===

% evaluate(Expr, Value) succeeds when Expr evaluates to Value.
evaluate(val(V), V).
evaluate(add(L, R), V) :-
    evaluate(L, VL),
    evaluate(R, VR),
    V is VL + VR.
evaluate(sub(L, R), V) :-
    evaluate(L, VL),
    evaluate(R, VR),
    VL > VR,
    V is VL - VR.
evaluate(mul(L, R), V) :-
    evaluate(L, VL),
    evaluate(R, VR),
    V is VL * VR.
evaluate(div(L, R), V) :-
    evaluate(L, VL),
    evaluate(R, VR),
    VR =\= 0,
    VL mod VR =:= 0,
    V is VL // VR.

% === Expression Formatting ===

format_expr(val(V), Expr) :-
    number_string(V, Expr).
format_expr(add(L, R), Expr) :-
    format_expr(L, LS),
    format_expr(R, RS),
    string_concat("(", LS, T1),
    string_concat(T1, " + ", T2),
    string_concat(T2, RS, T3),
    string_concat(T3, ")", Expr).
format_expr(sub(L, R), Expr) :-
    format_expr(L, LS),
    format_expr(R, RS),
    string_concat("(", LS, T1),
    string_concat(T1, " - ", T2),
    string_concat(T2, RS, T3),
    string_concat(T3, ")", Expr).
format_expr(mul(L, R), Expr) :-
    format_expr(L, LS),
    format_expr(R, RS),
    string_concat("(", LS, T1),
    string_concat(T1, " * ", T2),
    string_concat(T2, RS, T3),
    string_concat(T3, ")", Expr).
format_expr(div(L, R), Expr) :-
    format_expr(L, LS),
    format_expr(R, RS),
    string_concat("(", LS, T1),
    string_concat(T1, " / ", T2),
    string_concat(T2, RS, T3),
    string_concat(T3, ")", Expr).

% === Core Solver ===

% valid_state(Pool, Target, Expr) finds an expression evaluating to Target.
% Pool is a list of node(Expr, Value) terms.
valid_state(Pool, Target, Expr) :-
    member(node(Candidate, Value), Pool),
    Value =:= Target,
    Expr = Candidate.
valid_state(Pool, Target, Expr) :-
    length(Pool, Len),
    Len >= 2,
    select(node(EA, VA), Pool, Pool1),
    select(node(EB, VB), Pool1, Rest),
    combine(VA, VB, EA, EB, CombinedExpr, CombinedValue),
    valid_state([node(CombinedExpr, CombinedValue) | Rest], Target, Expr).

% combine(VA, VB, EA, EB, ResultExpr, ResultValue) generates a valid operation result.
combine(VA, VB, EA, EB, add(EA, EB), V) :-
    VA =< VB, % Symmetry breaking
    V is VA + VB,
    V > 0.
combine(VA, VB, EA, EB, sub(EA, EB), V) :-
    VA > VB,
    V is VA - VB.
combine(VA, VB, EA, EB, mul(EA, EB), V) :-
    VA =< VB, % Symmetry breaking
    V is VA * VB,
    V > 0.
combine(VA, VB, EA, EB, div(EA, EB), V) :-
    VB =\= 0,
    VA mod VB =:= 0,
    V is VA // VB,
    V > 0.

% === Main Predicate ===

% Convert a list of numbers to a list of node/2 terms.
numbers_to_vals([], []).
numbers_to_vals([N|Ns], [node(val(N), N)|Vt]) :-
    numbers_to_vals(Ns, Vt).

% Strips the outermost parentheses from the expression string if present.
strip_outer(ExprStr, Stripped) :-
    sub_string(ExprStr, 0, 1, _, "("),
    sub_string(ExprStr, _, 1, 0, ")"),
    !,
    string_length(ExprStr, Len),
    InnerLen is Len - 2,
    sub_string(ExprStr, 1, InnerLen, _, Stripped).
strip_outer(ExprStr, ExprStr).

% main(Target, Numbers) solves and prints the result.
main(Target, Numbers) :-
    numbers_to_vals(Numbers, Pool),
    (   valid_state(Pool, Target, Expr)
    ->  format_expr(Expr, ExprStr),
        strip_outer(ExprStr, FinalExprStr),  % Removes outermost parentheses for output consistency.
        evaluate(Expr, Value),
        format('Expression: ~s~n', [FinalExprStr]),
        format('Value: ~d~n', [Value])
    ;   format('No solution could be generated.~n', [])
    ).

% === Entry Point for swipl -g ===
% Usage: swipl -s countdown.pl -g "run([765,1,3,7,10,25,50])" -g "halt."
run(Args) :-
    Args = [Target | Numbers],
    main(Target, Numbers).