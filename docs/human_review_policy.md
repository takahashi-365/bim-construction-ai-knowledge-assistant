# Human Review Policy

## 1. このドキュメントの目的

このドキュメントは、PoC 3：BIM / Construction AI Knowledge Assistant における Human Review 方針を定義するための設計資料である。

PoC 3では、PoC 1・PoC 2の成果物を検索対象ナレッジとして整理し、質問に対して関連documentを検索し、根拠付き回答を生成する。

ただし、このPoCの目的は、AIが最終判断を行うことではない。

PoC 3の回答は、BIM担当者、設計者、施工担当者、AI/DX導入担当者、関係者が確認・協議するための参考情報として扱う。

このドキュメントでは、以下を定義する。

```text
Human Reviewの基本方針
AIが最終判断しない領域
HumanReviewRequired=True / False の意味
Revitモデル自動修正との関係
AI/DX自動化との関係
DeepDiveRequiredとの関係
回答生成時の注意書き
pytestで確認する観点
```

---

## 2. Human Reviewの基本方針

PoC 3では、以下を基本方針とする。

* AIは最終判断を行わない
* 回答は協議用の参考情報として扱う
* 設計判断、施工判断、法規判断、安全判断、契約判断は人間レビュー必須とする
* Revitモデルの自動修正は行わない
* 自動化候補であっても、人間確認が必要な範囲を明確にする
* 検索結果に参照元を示す
* 判断根拠としてRuleId、UseCaseId、SourceFileを示す
* HumanReviewRequired=True の場合は、回答内で人間レビューが必要であることを明示する
* DeepDiveRequired=True の場合は、追加確認が必要であることを明示する

PoC 3は、判断を代行するAIではなく、判断に必要な情報を整理するRAG-style Knowledge Assistantとして扱う。

---

## 3. Human Reviewが必要な理由

BIM・建設業務では、AIが検索・分類・要約・候補提示を行える場合でも、最終的な判断には専門知識、責任範囲、関係者合意が必要になる。

特に以下のような判断は、AIだけで確定してはいけない。

```text
設計意図に関わる判断
施工方法に関わる判断
法規適合に関わる判断
安全性に関わる判断
契約条件に関わる判断
コストや工程に関わる判断
顧客合意が必要な判断
RevitモデルやBIMデータを実際に変更する判断
```

PoC 3では、AIがこれらの判断を代替するのではなく、関連情報を検索し、協議のための材料を提示する。

---

## 4. AIが最終判断しない領域

PoC 3では、以下の領域についてAIが最終判断しない。

```text
設計判断
施工判断
法規判断
安全判断
契約判断
コスト判断
工程判断
品質保証上の判断
顧客合意が必要な判断
BIMモデルの正式修正判断
社内外への正式提出判断
```

例えば、品質チェックでDoor Name Missingが検出された場合でも、AIが自動的に正しいDoor Nameを決めることはしない。

また、ある業務ユースケースが自動化候補に分類された場合でも、AIが完全自動化を承認することはしない。

AIは、以下のような補助に限定する。

```text
関連情報を検索する
品質問題の意味を説明する
Fix Guideを提示する
ユースケース分類を説明する
RecommendedApproachを提示する
Human Reviewが必要な理由を整理する
Deep Diveが必要な論点を整理する
```

---

## 5. HumanReviewRequiredの定義

HumanReviewRequiredは、そのdocumentや回答に対して、人間による確認が必要かどうかを示すmetadataである。

値は以下の2つとする。

```text
True
False
```

JSONL上ではbooleanとして以下を使用する。

```text
true
false
```

CSV上では、必要に応じて以下を使用してもよい。

```text
True
False
```

Python処理時にbooleanへ変換する。

---

## 6. HumanReviewRequired=True の意味

HumanReviewRequired=True は、該当する情報や回答を、AIだけで確定してはいけないことを示す。

Trueの場合、回答には必ず人間レビューが必要であることを含める。

HumanReviewRequired=True になる代表例は以下である。

```text
設計判断が含まれる
施工判断が含まれる
法規判断が含まれる
安全判断が含まれる
契約判断が含まれる
コスト判断が含まれる
工程判断が含まれる
顧客合意が必要である
BIMモデルの正式修正が関係する
Revitモデルの自動修正が不適切である
入力情報だけでは判断できない
業務ルールやプロジェクトルールの確認が必要である
```

回答では、以下の趣旨を含める。

```text
この回答は協議用の参考情報です。
設計判断、施工判断、法規判断、安全判断、契約判断は人間レビューが必要です。
AIは最終判断を行いません。
```

---

## 7. HumanReviewRequired=False の意味

HumanReviewRequired=False は、そのdocument単体では強い人間レビュー要否が設定されていないことを示す。

ただし、Falseであっても、AIが最終判断してよいという意味ではない。

Falseにできる例は以下である。

```text
単純な情報参照
PoC全体の概要説明
検索対象ナレッジの説明
明確なルールに基づく分類表示
協議前の参考情報整理
README的な説明
```

HumanReviewRequired=False の場合でも、以下の考え方は維持する。

```text
AIは最終判断を行わない
実案件適用時は関係者確認が必要
設計判断・施工判断・法規判断・安全判断・契約判断は人間レビューが必要
```

つまり、Falseは「人間確認が一切不要」という意味ではない。

---

## 8. Revitモデル自動修正との関係

PoC 3では、Revitモデルの自動修正は行わない。

品質チェックやFix Guideで修正候補が示された場合でも、AIがRevitモデルを直接変更することはしない。

Revitモデル修正に関する方針は以下である。

```text
AIは修正候補を提示してよい
AIは確認ポイントを提示してよい
AIはFix Guideを参照して説明してよい
AIはRevitモデルを自動修正しない
AIは修正内容を確定しない
最終的な修正判断はBIM担当者または関係者が行う
```

例えば、Door Name Missingが検出された場合、PoC 3は以下を説明できる。

```text
どのRuleIdに該当するか
Nameが不足していることがAI Readinessにどう影響するか
Fix Guide上の確認方針
Human Reviewが必要な理由
```

しかし、PoC 3は以下を行わない。

```text
正しいDoor Nameを自動決定する
Revitモデルへ自動入力する
修正済みとして自動承認する
人間確認なしでモデル更新する
```

---

## 9. AI/DX自動化との関係

PoC 2では、BIM・建設業務ユースケースに対して、RAG、BI、自動化、ルールベースチェック、人間レビュー、深掘り対象などの分類を行った。

PoC 3では、これらの分類を検索対象ナレッジとして扱う。

ただし、ある業務が自動化候補に分類されていても、それは完全自動化を意味しない。

PoC 3における自動化方針は以下である。

```text
AutomationSuitable=True は、自動化支援の候補であることを示す
Automation Support は、人間作業の補助を意味する
HumanReviewRequired=True の場合、最終判断は人間が行う
設計判断・施工判断・法規判断・安全判断・契約判断を含む業務は完全自動化しない
DeepDiveRequired=True の場合、追加確認なしに自動化方針を決めない
```

回答では、以下のように表現する。

```text
この業務は一部自動化支援の候補として扱えます。
ただし、設計判断、施工判断、法規判断、安全判断、契約判断を含む場合は、人間レビューが必要です。
AIは最終判断を行いません。
```

---

## 10. RAG-style検索との関係

PoC 3では、PoC 1・PoC 2の成果物をRAG-style Knowledge Documentsとして整理し、質問に応じて関連documentを検索する。

RAG-style検索は、回答の根拠候補を探すための仕組みである。

RAG-style検索によって関連documentが見つかった場合でも、それだけで最終判断が確定するわけではない。

RAG-style検索の位置づけは以下である。

```text
関連するRuleIdを探す
関連するFix Guideを探す
関連するUseCaseIdを探す
関連するPolicyを探す
参照元付きで回答案を作る
協議材料を整理する
```

RAG-style検索で行わないことは以下である。

```text
設計判断を確定する
施工判断を確定する
法規判断を確定する
安全判断を確定する
契約判断を確定する
自動承認する
自動修正する
```

---

## 11. DeepDiveRequiredとの関係

DeepDiveRequiredは、追加確認や詳細調査が必要かどうかを示すmetadataである。

DeepDiveRequired=True の場合、Human Reviewとあわせて、追加確認が必要であることを回答に明示する。

DeepDiveRequired=True になる代表例は以下である。

```text
入力情報が不足している
業務範囲が広すぎる
判断条件が曖昧である
成果物の使われ方が不明確である
関係者確認が必要である
AI/DX適用方針を決めるには追加ヒアリングが必要である
```

回答では、以下の趣旨を含める。

```text
この内容は追加確認が必要です。
入力情報、判断条件、関係者確認、業務範囲などを確認したうえで、AI/DX活用方針を協議する必要があります。
```

DeepDiveRequired=True の場合、すぐにRAG、BI、自動化などへ確定分類するのではなく、追加確認を前提とする。

---

## 12. Human Reviewが必要な質問タイプ

PoC 3では、以下のような質問に対してHuman Review方針を強く反映する。

```text
この指摘はRevitモデルを自動修正してよいですか？
この業務はAIで自動化してよいですか？
このRuleIdの違反は重大ですか？
この品質問題は設計ミスですか？
この結果をそのまま顧客に提出してよいですか？
このユースケースは完全自動化できますか？
DeepDiveRequired の業務では何を追加確認すべきですか？
HumanReviewRequired=True になる理由は何ですか？
```

これらの質問に対しては、回答内に以下を含める。

```text
検索結果に基づく参考情報であること
AIが最終判断しないこと
人間レビューが必要であること
追加確認が必要な場合はその内容
参照元情報
```

---

## 13. Human Review注意書きの基本文

PoC 3の回答では、必要に応じて以下の注意書きを使用する。

```text
この回答は協議用の参考情報です。
設計判断、施工判断、法規判断、安全判断、契約判断は人間レビューが必要です。
AIは最終判断を行いません。
```

Markdown回答では、Cautionとして以下のように記載する。

```markdown
### Caution

この回答は協議用の参考情報です。設計判断、施工判断、法規判断、安全判断、契約判断は人間レビューが必要です。AIは最終判断を行いません。
```

---

## 14. 質問タイプ別のHuman Review文言

### 14.1 Revitモデル修正に関する質問

```text
このPoCでは、Revitモデルの自動修正は行いません。
修正の要否や内容は、BIM担当者がモデル、集計表、プロジェクトルールを確認したうえで判断する必要があります。
```

### 14.2 AI/DX自動化に関する質問

```text
自動化候補であっても、設計判断、施工判断、法規判断、安全判断、契約判断を含む場合は、人間レビューを前提とします。
AIは最終判断を行いません。
```

### 14.3 Deep Diveに関する質問

```text
この内容は追加確認が必要です。
入力情報、判断条件、関係者確認、業務範囲を確認したうえで、AI/DX活用方針を協議する必要があります。
```

### 14.4 参照元が不足している場合

```text
検索結果だけでは十分な根拠が不足しています。
追加の資料確認または人間レビューが必要です。
```

### 14.5 PoC全体の説明に関する質問

```text
この回答はPoC全体の関係を説明するための参考情報です。
実案件への適用判断や導入判断は、人間レビューと関係者協議が必要です。
```

---

## 15. HumanReviewRequiredと回答生成の関係

回答生成時には、検索結果に含まれるdocumentのHumanReviewRequiredを確認する。

基本ルールは以下である。

```text
検索結果にHumanReviewRequired=Trueが1件でも含まれる場合、回答にHuman Review注意書きを含める
HumanReviewRequired=Trueのdocumentを主根拠にする場合、Answer本文でも人間レビューが必要であることを説明する
HumanReviewRequired=Falseのみの場合でも、重要判断に関わる質問であればCautionを含める
Policy系documentが検索された場合、Cautionに方針を反映する
```

回答生成では、HumanReviewRequiredを単なる表示項目ではなく、回答内容を制御する重要なmetadataとして扱う。

---

## 16. HumanReviewRequiredとmetadataの関係

RAG-style document JSONLでは、HumanReviewRequiredはmetadata内に保持する。

例。

```json
{
  "document_id": "P1-RULE-D001",
  "source_poc": "PoC1",
  "source_type": "RuleMaster",
  "title": "Door Name Missing Rule",
  "content": "このRuleは、DoorカテゴリのName項目が未入力または不明確な状態を検出するための品質チェックである。",
  "metadata": {
    "category": "Door",
    "rule_id": "D-001",
    "use_case_id": "",
    "severity": "High",
    "human_review_required": true,
    "deep_dive_required": false,
    "source_file": "poc1_knowledge_samples.csv"
  },
  "keywords": ["door", "name", "missing", "quality", "human review"]
}
```

この値は、以下の出力に反映する。

```text
output/retrieval_results_v001.csv
output/sample_answers_v001.md
```

---

## 17. 出力ファイルでのHuman Review表示

### 17.1 retrieval_results_v001.csv

検索結果CSVでは、以下の列にHuman Review情報を表示する。

```text
HumanReviewRequired
DeepDiveRequired
```

例。

```text
QuestionId,Question,Rank,DocumentId,SourcePoC,SourceType,Title,HumanReviewRequired,DeepDiveRequired,SourceFile
Q001,このRuleIdの違反は何を意味しますか？,1,P1-RULE-D001,PoC1,RuleMaster,Door Name Missing Rule,True,False,poc1_knowledge_samples.csv
```

### 17.2 sample_answers_v001.md

回答Markdownでは、以下の項目を含める。

```markdown
### HumanReviewRequired

True

### DeepDiveRequired

False

### Caution

この回答は協議用の参考情報です。設計判断、施工判断、法規判断、安全判断、契約判断は人間レビューが必要です。AIは最終判断を行いません。
```

---

## 18. Human Review方針で避ける表現

PoC 3では、以下の表現を避ける。

```text
AIが最終判断します
AIが自動で承認します
AIが設計判断します
AIが施工判断します
AIが法規判断します
AIが安全判断します
AIが契約判断します
Revitモデルを自動修正します
人間確認は不要です
確認なしで実行できます
この判断は確定です
必ず正しいです
```

これらの表現は、回答、docs、sample data、output、READMEのいずれにも含めない。

pytestでも禁止表現として検出対象にする。

---

## 19. 推奨する表現

PoC 3では、以下の表現を推奨する。

```text
協議用の参考情報です
確認が必要です
人間レビューが必要です
追加確認が必要です
可能性があります
検索結果に基づくと
参照元では以下のように整理されています
このPoCでは自動修正は行いません
最終判断は関係者が行う必要があります
AIは最終判断を行いません
```

これらの表現により、PoC 3が最終判断AIではなく、根拠付きの確認・協議支援ツールであることを明確にする。

---

## 20. Human Review方針とPoC 1の関係

PoC 1では、BIMデータ品質、AI Readiness、Fix Guide、HumanReviewRequiredを扱った。

PoC 3では、PoC 1由来の情報を検索対象ナレッジとして扱い、以下を回答できるようにする。

```text
RuleIdの意味
品質問題の内容
AI Readinessへの影響
Fix Guideの確認方針
HumanReviewRequired=Trueの理由
Revitモデルを自動修正しない理由
```

PoC 1由来の品質チェック結果は、AIが自動修正するためのものではない。

BIM担当者が品質問題を確認し、必要に応じて修正や関係者確認を行うための材料として扱う。

---

## 21. Human Review方針とPoC 2の関係

PoC 2では、BIM・建設業務ユースケースを、RAG、BI、自動化、ルールベースチェック、人間レビュー、深掘り対象などに分類した。

PoC 3では、PoC 2由来の情報を検索対象ナレッジとして扱い、以下を回答できるようにする。

```text
このユースケースはRAGに向いているか
この業務はAIで自動化してよいか
RecommendedApproachは何を意味するか
HumanReviewRequired=Trueになる理由
DeepDiveRequired=Trueの場合の追加確認事項
```

PoC 2由来の自動化候補は、完全自動化を意味しない。

HumanReviewRequired=True の場合は、AIが候補提示や整理を行い、最終判断は関係者が行う。

---

## 22. Human Review方針とPoC 3の関係

PoC 3は、PoC 1・PoC 2の成果物を検索し、根拠付きで説明するRAG-style Knowledge Assistantである。

PoC 3では、Human Review方針を以下に反映する。

```text
RAG-style document JSONL
metadata
retrieval_results_v001.csv
sample_answers_v001.md
answer_policy.md
README.md
pytest
```

特に、以下を一貫させる。

```text
AIは最終判断しない
回答は協議用の参考情報である
参照元を明示する
HumanReviewRequired=Trueの場合は注意書きを入れる
DeepDiveRequired=Trueの場合は追加確認を促す
Revitモデルの自動修正は行わない
```

---

## 23. pytestで確認する観点

Human Review方針は、pytestでも最低限確認する。

確認項目は以下である。

```text
rag_documents_v001.jsonl に human_review_required が含まれること
rag_documents_v001.jsonl に deep_dive_required が含まれること
retrieval_results_v001.csv に HumanReviewRequired が含まれること
retrieval_results_v001.csv に DeepDiveRequired が含まれること
sample_answers_v001.md に HumanReviewRequired が含まれること
sample_answers_v001.md に Caution が含まれること
sample_answers_v001.md に Human Review注意書きが含まれること
禁止表現が含まれていないこと
```

禁止表現の例。

```text
AIが最終判断します
自動で承認します
Revitモデルを自動修正します
人間確認は不要です
```

---

## 24. 将来的な拡張時の注意

将来的に、Azure AI Search、Azure OpenAI API、OpenAI API、LangChain、LlamaIndex、FAISS、Chroma、Embedding検索などへ拡張する場合でも、Human Review方針は維持する。

実装が高度になっても、以下は変えない。

```text
AIは最終判断しない
回答には参照元を含める
Human Reviewが必要な判断を明示する
Deep Diveが必要な場合は追加確認を促す
Revitモデルの自動修正を前提にしない
実案件データや顧客データを無断で使わない
```

本格的なRAG構成へ拡張した場合でも、PoC 3の責任範囲は「判断支援」であり、「最終判断」ではない。

---

## 25. まとめ

PoC 3におけるHuman Review方針は、以下である。

```text
AIは最終判断を行わない
回答は協議用の参考情報として扱う
設計判断・施工判断・法規判断・安全判断・契約判断は人間レビュー必須
Revitモデルの自動修正は行わない
自動化候補であっても、最終判断は人間が行う
DeepDiveRequired=Trueの場合は追加確認を促す
参照元を明示する
```

HumanReviewRequired=True は、人間レビューが必要であることを示す。

HumanReviewRequired=False は、AIが最終判断してよいという意味ではない。

PoC 3は、PoC 1・PoC 2の成果物を検索し、根拠付きで説明することで、BIM担当者やAI/DX導入担当者の確認・協議を支援する。

このHuman Review Policyにより、PoC 3は以下を実現する。

```text
BIMデータ品質の確認を支援する
AI Readinessの説明を支援する
Fix Guideの確認を支援する
BIM・建設業務ユースケースのAI/DX分類を説明する
自動化支援と人間判断の境界を明確にする
AIが最終判断しない設計を保つ
```
