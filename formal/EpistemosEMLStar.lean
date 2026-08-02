/- Structural certificate schema for the Epistemos EML-star edition.
   This file intentionally proves syntax/provenance facts only. It does not
   claim to formalize the analytic semantics of the principal complex log. -/

namespace Epistemos.EMLStar

inductive Expr where
  | one : Expr
  | var : Nat -> Expr
  | eml : Expr -> Expr -> Expr
  | emlStar : Expr -> Expr -> Expr
deriving Repr, DecidableEq

def Expr.size : Expr -> Nat
  | .one => 1
  | .var _ => 1
  | .eml left right => 1 + left.size + right.size
  | .emlStar left right => 1 + left.size + right.size

def Expr.depth : Expr -> Nat
  | .one => 0
  | .var _ => 0
  | .eml left right => 1 + max left.depth right.depth
  | .emlStar left right => 1 + max left.depth right.depth

theorem Expr.size_positive : forall expr, 0 < expr.size
  | .one => Nat.zero_lt_succ 0
  | .var _ => Nat.zero_lt_succ 0
  | .eml left right => Nat.zero_lt_succ (left.size + right.size)
  | .emlStar left right => Nat.zero_lt_succ (left.size + right.size)

structure BranchWitness where
  expressionDigest : String
  branchIndices : List Int
  precisionDps : Nat
  receiptRoot : String

structure CertificateTarget where
  expr : Expr
  theoremId : String
  sourceRow : String
  witness : BranchWitness

theorem CertificateTarget.carriesIdentity (certificate : CertificateTarget) :
    certificate.theoremId = certificate.theoremId /\
    certificate.witness.receiptRoot = certificate.witness.receiptRoot := by
  exact And.intro rfl rfl

def constructorCount : Nat := 4

theorem constructorCount_pinned : constructorCount = 4 := rfl

end Epistemos.EMLStar
