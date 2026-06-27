# Answer Policy

## 1. このドキュメントの目的

このドキュメントは、PoC 3：BIM / Construction AI Knowledge Assistant における回答方針を定義するための設計資料である。

PoC 3では、PoC 1・PoC 2の成果物をRAG-style Knowledge Documentsとして整理し、質問に対して関連documentを検索し、根拠付き回答を生成する。

このとき、回答はAIが自由に推測して作るものではない。

検索されたdocument、metadata、source_file、RuleId、UseCaseId、HumanReviewRequired、DeepDiveRequiredなどをもとに、確認・協議のための回答案として生成する。

このドキュメントでは、以下を定義する。

```text
回答の基本方針
回答に含める項目
参照元の示し方
Human Reviewが必要な場合の扱い
Deep Diveが必要な場合の扱い
回答で避ける表現
回答テンプレート
pytestで確認する観点
```

---

## 2. 回答の基本方針

PoC 3の回答では、以下の方針を守る。

* 回答は検索結果に基づく
* 回答には参照元を含める
* 回答は協議用の参考情報として扱う
* AIが最終判断する表現は使わない
* 設計判断、施工判断、法規判断、安全判断、契約判断は人間レビューが必要であることを明記する
* HumanReviewRequired=True の場合は注意書きを入れる
* DeepDiveRequired=True の場合は追加確認が必要であることを示す
* 検索結果にない内容を断定しない
* 実案件データ、顧客データ、社内サービス詳細は使わない
* 本格RAGであると誇張しない
* RAG-style Knowledge Assistantとして説明する

PoC 3の回答は、最終判断ではなく、BIM担当者、設計者、施工担当者、AI/DX導入担当者、関係者が確認・協議するための材料である。

---

## 3. 回答が参照する情報

回答生成では、以下の情報を使用する。

```text
input/sample_questions_v001.csv
output/retrieval_results_v001.csv
output/rag_documents_v001.jsonl
output/rag_index_v001.json
```

主に使用する情報は以下である。

```text
Question
DocumentId
SourcePoC
SourceType
Title
Content
RuleId
UseCaseId
RecommendedApproach
HumanReviewRequired
DeepDiveRequired
SourceFile
Keywords
```

回答では、検索されたdocumentのcontentを主な根拠として使用し、metadataを補足情報として表示する。

---

## 4. 回答に必ず含める項目

PoC 3の回答Markdownでは、原則として以下の項目を含める。

```text
Question
Answer
Reasoning Summary
Referenced Sources
RuleId
UseCaseId
RecommendedApproach
HumanReviewRequired
DeepDiveRequired
Caution
```

各項目の意味は以下。

| 項目                  | 説明                             |
| ------------------- | ------------------------------ |
| Question            | 入力された質問                        |
| Answer              | 検索結果に基づく回答案                    |
| Reasoning Summary   | どの情報をもとに回答したかの要約               |
| Referenced Sources  | 参照したdocument、source_file、title |
| RuleId              | PoC 1由来のRuleId                 |
| UseCaseId           | PoC 2由来のUseCaseId              |
| RecommendedApproach | PoC 2由来の推奨アプローチ                |
| HumanReviewRequired | 人間レビュー要否                       |
| DeepDiveRequired    | 追加確認要否                         |
| Caution             | 注意書き                           |

値がない項目は、空欄ではなく以下のように表現してよい。

```text
該当なし
Not applicable
```

MVPでは、日本語で読みやすい回答を優先する。

---

## 5. 回答の基本テンプレート

回答Markdownの基本テンプレートは以下である。

```markdown
## Question: {Question}

### Answer

{検索結果に基づく回答案}

### Reasoning Summary

{どのdocumentを根拠にしたか、なぜその回答になるかの短い説明}

### Referenced Sources

- DocumentId: {DocumentId}
- SourcePoC: {SourcePoC}
- SourceType: {SourceType}
- Title: {Title}
- SourceFile: {SourceFile}

### RuleId

{RuleId または 該当なし}

### UseCaseId

{UseCaseId または 該当なし}

### RecommendedApproach

{RecommendedApproach または 該当なし}

### HumanReviewRequired

{True / False}

### DeepDiveRequired

{True / False}

### Caution

この回答は協議用の参考情報です。設計判断、施工判断、法規判断、安全判断、契約判断は人間レビューが必要です。AIは最終判断を行いません。
```

---

## 6. Answerの書き方

Answerでは、検索結果に基づいて質問に直接答える。

ただし、断定しすぎない。

良い表現。

```text
このRuleIdは、DoorカテゴリのName項目が不足している可能性を示す品質チェックです。
AI Context生成や検索対象ナレッジ化において、対象要素を識別しにくくなる可能性があります。
そのため、BIM担当者がRevitモデルまたは集計表を確認する必要があります。
```

避ける表現。

```text
このRuleIdの違反は必ず重大な設計ミスです。
AIが自動で修正します。
人間確認は不要です。
```

Answerでは、以下のような表現を使う。

```text
可能性があります
確認が必要です
参考情報として扱います
協議材料として利用できます
人間レビューが必要です
追加確認が必要です
```

---

## 7. Reasoning Summaryの書き方

Reasoning Summaryでは、回答の根拠を短く説明する。

目的は、回答がどの情報に基づいているかを利用者が確認できるようにすることである。

良い例。

```text
検索結果では、PoC 1由来のRuleMaster documentが参照されています。
このdocumentでは、Door Name MissingがAI Context生成時の要素識別に影響する可能性があると説明されています。
また、HumanReviewRequired=Trueであるため、AIによる自動修正ではなく、BIM担当者による確認が必要です。
```

避ける例。

```text
AIがそう判断しました。
検索結果から自動的に正しい答えが決まりました。
```

Reasoning Summaryは、AIの内部推論を説明するものではない。

参照したdocument、metadata、検索結果に基づく要約として記述する。

---

## 8. Referenced Sourcesの書き方

Referenced Sourcesでは、回答の参照元を明示する。

最低限、以下を表示する。

```text
DocumentId
SourcePoC
SourceType
Title
SourceFile
```

例。

```text
- DocumentId: P1-RULE-D001
- SourcePoC: PoC1
- SourceType: RuleMaster
- Title: Door Name Missing Rule
- SourceFile: poc1_knowledge_samples.csv
```

複数のdocumentを参照した場合は、Rank順に表示する。

例。

```text
1. DocumentId: P2-USECASE-UC001
   SourcePoC: PoC2
   SourceType: UseCaseMapping
   Title: BIM Issue Report Review Use Case
   SourceFile: poc2_knowledge_samples.csv

2. DocumentId: P3-POLICY-HUMAN001
   SourcePoC: PoC3
   SourceType: HumanReviewPolicy
   Title: AI does not make final decisions
   SourceFile: human_review_policy.md
```

Referenced Sourcesを表示することで、回答がどの情報に基づくかを確認できるようにする。

---

## 9. RuleIdの扱い

RuleIdは、PoC 1由来の品質チェックルールを示す。

RuleIdがある場合は、回答内で明示する。

例。

```text
RuleId: D-001
```

RuleIdが複数ある場合は、カンマ区切りまたは箇条書きで表示する。

例。

```text
RuleId:
- D-001
- R-101
```

RuleIdがない場合は、以下のように表示する。

```text
RuleId: 該当なし
```

RuleIdを表示することで、品質チェック結果やFix Guideと回答を結びつけやすくする。

---

## 10. UseCaseIdの扱い

UseCaseIdは、PoC 2由来の業務ユースケースを示す。

UseCaseIdがある場合は、回答内で明示する。

例。

```text
UseCaseId: UC-001
```

UseCaseIdが複数ある場合は、箇条書きで表示する。

例。

```text
UseCaseId:
- UC-001
- UC-003
```

UseCaseIdがない場合は、以下のように表示する。

```text
UseCaseId: 該当なし
```

UseCaseIdを表示することで、PoC 2のユースケース分類や協議用レポートと回答を結びつけやすくする。

---

## 11. RecommendedApproachの扱い

RecommendedApproachは、PoC 2で分類したAI/DX活用方針を示す。

例。

```text
RAG Support
BI / Dashboard
Automation Support
Rule-based Check
Human Review
Deep Dive Required
RAG Support + Human Review
Automation Support + Human Review
BI + Human Review
```

RecommendedApproachがある場合は、回答内で以下のように説明する。

```text
このユースケースは、RecommendedApproachとして「RAG Support + Human Review」に分類されています。
過去のルール、Fix Guide、関連資料を参照しながら対応方針を整理する用途に向いています。
ただし、設計判断や施工判断を含む場合は、人間レビューが必要です。
```

RecommendedApproachがない場合は、以下のように表示する。

```text
RecommendedApproach: 該当なし
```

---

## 12. HumanReviewRequiredの扱い

HumanReviewRequiredは、PoC 3の回答において特に重要な項目である。

HumanReviewRequired=True の場合、回答には必ず注意書きを入れる。

基本の注意書きは以下。

```text
この回答は協議用の参考情報です。
設計判断、施工判断、法規判断、安全判断、契約判断は人間レビューが必要です。
AIは最終判断を行いません。
```

HumanReviewRequired=True になる例。

```text
設計判断が含まれる
施工判断が含まれる
法規判断が含まれる
安全判断が含まれる
契約判断が含まれる
顧客合意が必要である
Revitモデルの自動修正が不適切である
```

HumanReviewRequired=False の場合でも、AIが最終判断してよいという意味ではない。

Falseは、そのdocument単体では強い人間レビュー要否が設定されていないことを示すだけである。

PoC 3全体では、重要な判断は人間レビューを前提とする。

---

## 13. DeepDiveRequiredの扱い

DeepDiveRequiredは、追加確認や詳細調査が必要かを示す項目である。

DeepDiveRequired=True の場合、回答には追加確認が必要であることを明記する。

基本の注意書きは以下。

```text
この内容は追加確認が必要です。
入力情報、判断条件、関係者確認、業務範囲などを確認したうえで、AI/DX活用方針を協議する必要があります。
```

DeepDiveRequired=True になる例。

```text
入力情報が不足している
業務内容が広すぎる
判断条件が曖昧である
関係者確認が必要である
AI/DX適用方針を決めるには追加ヒアリングが必要である
```

DeepDiveRequired=True の場合は、AnswerまたはCautionに追加確認事項を入れる。

---

## 14. Cautionの書き方

Cautionには、回答を利用する際の注意書きを記載する。

基本文は以下。

```text
この回答は協議用の参考情報です。設計判断、施工判断、法規判断、安全判断、契約判断は人間レビューが必要です。AIは最終判断を行いません。
```

質問内容に応じて、以下を追加する。

### 14.1 Revitモデル修正に関する質問の場合

```text
このPoCでは、Revitモデルの自動修正は行いません。修正の要否や内容は、BIM担当者がモデル、集計表、プロジェクトルールを確認したうえで判断する必要があります。
```

### 14.2 AI/DX自動化に関する質問の場合

```text
自動化候補であっても、設計判断、施工判断、法規判断、安全判断、契約判断を含む場合は、人間レビューを前提とします。
```

### 14.3 Deep Diveが必要な場合

```text
この内容は追加確認が必要です。入力情報、判断条件、関係者確認、業務範囲を確認したうえで、AI/DX活用方針を協議する必要があります。
```

### 14.4 参照元が不足している場合

```text
検索結果だけでは十分な根拠が不足しています。追加の資料確認または人間レビューが必要です。
```

---

## 15. 質問タイプ別の回答方針

PoC 3では、質問タイプごとに回答方針を変える。

| 質問タイプ             | 優先する情報                             | 回答方針                       |
| ----------------- | ---------------------------------- | -------------------------- |
| RuleIdに関する質問      | RuleMaster / FixGuide              | Ruleの意味、影響、確認方針を説明する       |
| 品質チェックに関する質問      | RuleMaster / QualityCheckResult    | 品質問題とAI Readinessへの影響を説明する |
| Fix Guideに関する質問   | FixGuide                           | 確認・修正方針を説明する               |
| Revit自動修正に関する質問   | FixGuide / HumanReviewPolicy       | 自動修正しない方針を明記する             |
| AI/DXユースケースに関する質問 | UseCaseMapping                     | RecommendedApproachを説明する   |
| RAG適性に関する質問       | UseCaseMapping / WorkflowSummary   | RAG-style検索に向く理由を説明する      |
| 自動化可否に関する質問       | UseCaseMapping / HumanReviewPolicy | 自動化支援と人間レビューの境界を説明する       |
| Deep Diveに関する質問   | UseCaseMapping / Policy            | 追加確認事項を説明する                |
| PoC全体に関する質問       | WorkflowSummary                    | PoC 1・PoC 2・PoC 3の関係を説明する  |
| 制約事項に関する質問        | Limitations                        | MVPでできること・できないことを説明する      |

---

## 16. 検索結果がある場合の回答方針

検索結果がある場合は、上位のdocumentを主な根拠として回答する。

ただし、検索結果が複数ある場合は、以下のように扱う。

* Rank 1を主根拠にする
* Rank 2以降は補足根拠として使う
* Policy系documentが含まれる場合はCautionに反映する
* HumanReviewRequired=Trueが含まれる場合は注意書きを入れる
* DeepDiveRequired=Trueが含まれる場合は追加確認事項を入れる

回答では、検索結果が複数ある場合でも、根拠を無理に増やしすぎない。

MVPでは、上位1〜3件程度を参照元として表示する。

---

## 17. 検索結果が不足している場合の回答方針

検索結果が不足している場合は、無理に断定しない。

回答例。

```text
検索結果だけでは、この質問に対する十分な根拠は見つかりませんでした。
追加のナレッジ、Rule Master、Use Case Mapping、またはPolicy documentを確認する必要があります。
この回答は暫定的な参考情報であり、最終判断には人間レビューが必要です。
```

避ける表現。

```text
根拠はありませんが、おそらく正しいです。
検索結果がなくてもAIが判断できます。
```

検索結果が不足している場合も、Referenced Sourcesには以下のように記載してよい。

```text
Referenced Sources:
該当する検索結果なし
```

---

## 18. 回答で禁止する表現

PoC 3の回答では、以下の表現を禁止する。

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

これらの表現は、pytestでも検出対象にする。

---

## 19. 推奨する表現

PoC 3の回答では、以下の表現を推奨する。

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
```

これらの表現により、PoC 3が最終判断AIではなく、根拠付きの確認・協議支援ツールであることを明確にする。

---

## 20. 回答例：RuleIdに関する質問

### Question

```text
このRuleIdの違反は何を意味しますか？
```

### Answer例

```markdown
## Question: このRuleIdの違反は何を意味しますか？

### Answer

このRuleIdは、BIMデータ内の特定項目に不足または不整合がある可能性を示す品質チェックです。

例えば、DoorカテゴリのName項目が不足している場合、対象要素をAI Contextや検索対象ナレッジとして扱う際に、識別しにくくなる可能性があります。

そのため、BIM担当者がRevitモデル、集計表、プロジェクトの命名ルールを確認し、必要に応じて修正方針を協議する必要があります。

### Reasoning Summary

検索結果では、PoC 1由来のRuleMaster documentが参照されています。
このdocumentでは、RuleIdに対応する品質問題と、AI Readinessへの影響が説明されています。
HumanReviewRequired=Trueの場合は、AIによる自動修正ではなく、人間レビューが必要です。

### Referenced Sources

- DocumentId: P1-RULE-D001
- SourcePoC: PoC1
- SourceType: RuleMaster
- Title: Door Name Missing Rule
- SourceFile: poc1_knowledge_samples.csv

### RuleId

D-001

### UseCaseId

該当なし

### RecommendedApproach

該当なし

### HumanReviewRequired

True

### DeepDiveRequired

False

### Caution

この回答は協議用の参考情報です。設計判断、施工判断、法規判断、安全判断、契約判断は人間レビューが必要です。AIは最終判断を行いません。
```

---

## 21. 回答例：AI自動化に関する質問

### Question

```text
この業務はAIで自動化してよいですか？
```

### Answer例

```markdown
## Question: この業務はAIで自動化してよいですか？

### Answer

検索結果に基づくと、この業務は一部の情報整理や候補抽出については自動化支援の対象になり得ます。

ただし、設計判断、施工判断、法規判断、安全判断、契約判断を含む場合は、AIが最終判断するのではなく、人間レビューを前提とする必要があります。

RecommendedApproachが「Automation Support + Human Review」の場合、AIは作業補助や候補提示を行い、最終判断は関係者が行う位置づけとします。

### Reasoning Summary

検索結果では、PoC 2由来のUseCaseMapping documentが参照されています。
このdocumentでは、該当ユースケースが自動化支援の候補である一方、HumanReviewRequired=Trueとして扱われています。
そのため、完全自動化ではなく、人間レビューを含む自動化支援として回答します。

### Referenced Sources

- DocumentId: P2-USECASE-UC001
- SourcePoC: PoC2
- SourceType: UseCaseMapping
- Title: BIM Issue Report Review Use Case
- SourceFile: poc2_knowledge_samples.csv

### RuleId

該当なし

### UseCaseId

UC-001

### RecommendedApproach

Automation Support + Human Review

### HumanReviewRequired

True

### DeepDiveRequired

False

### Caution

この回答は協議用の参考情報です。自動化候補であっても、設計判断、施工判断、法規判断、安全判断、契約判断を含む場合は人間レビューが必要です。AIは最終判断を行いません。
```

---

## 22. 回答例：Deep Diveに関する質問

### Question

```text
DeepDiveRequired の業務では何を追加確認すべきですか？
```

### Answer例

```markdown
## Question: DeepDiveRequired の業務では何を追加確認すべきですか？

### Answer

DeepDiveRequired=True の業務では、AI/DX活用方針を決める前に、入力情報、判断条件、業務範囲、関係者確認、成果物の使われ方を追加確認する必要があります。

特に、業務内容が広すぎる場合や、どこまで自動化してよいかが不明確な場合は、すぐにRAG、BI、自動化などへ分類するのではなく、追加ヒアリングや業務分解を行う必要があります。

### Reasoning Summary

検索結果では、PoC 2由来のUseCaseMapping documentが参照されています。
このdocumentでは、DeepDiveRequired=Trueとして扱われており、業務条件が曖昧なままAI/DX方針を決めるべきではないことが示されています。

### Referenced Sources

- DocumentId: P2-USECASE-UC003
- SourcePoC: PoC2
- SourceType: UseCaseMapping
- Title: Deep Dive Required Use Case
- SourceFile: poc2_knowledge_samples.csv

### RuleId

該当なし

### UseCaseId

UC-003

### RecommendedApproach

Deep Dive Required

### HumanReviewRequired

True

### DeepDiveRequired

True

### Caution

この内容は追加確認が必要です。入力情報、判断条件、関係者確認、業務範囲などを確認したうえで、AI/DX活用方針を協議する必要があります。AIは最終判断を行いません。
```

---

## 23. 回答例：PoC全体に関する質問

### Question

```text
PoC 1とPoC 2はどうつながりますか？
```

### Answer例

```markdown
## Question: PoC 1とPoC 2はどうつながりますか？

### Answer

PoC 1は、BIMデータがAI活用に適しているかを評価するPoCです。

PoC 2は、BIM・建設業務がどのAI/DX活用に適しているかを分類するPoCです。

PoC 3では、PoC 1のBIMデータ品質・AI Readiness評価と、PoC 2の業務ユースケース分類を検索対象ナレッジとして扱い、質問に対して根拠付きで説明することを目的とします。

整理すると、PoC 1は「データ品質」、PoC 2は「業務ユースケース」、PoC 3は「検索・説明」の役割を持ちます。

### Reasoning Summary

検索結果では、PoC 3由来のWorkflowSummary documentが参照されています。
このdocumentでは、PoC 1・PoC 2・PoC 3の関係が、データ品質評価、業務ユースケース分類、ナレッジ検索・根拠付き回答の流れとして整理されています。

### Referenced Sources

- DocumentId: P3-SUMMARY-WORKFLOW001
- SourcePoC: PoC3
- SourceType: WorkflowSummary
- Title: PoC 1 to PoC 3 Workflow Summary
- SourceFile: bim_to_ai_workflow_blueprint.md

### RuleId

該当なし

### UseCaseId

該当なし

### RecommendedApproach

該当なし

### HumanReviewRequired

False

### DeepDiveRequired

False

### Caution

この回答はPoC全体の関係を説明するための参考情報です。実案件への適用判断や導入判断は、人間レビューと関係者協議が必要です。
```

---

## 24. 回答品質の確認観点

生成された回答は、以下の観点で確認する。

```text
質問に直接答えているか
検索結果に基づいているか
Referenced Sourcesが含まれているか
RuleIdまたはUseCaseIdが必要に応じて表示されているか
HumanReviewRequiredが表示されているか
DeepDiveRequiredが表示されているか
Cautionが含まれているか
AIが最終判断する表現が含まれていないか
Revitモデルの自動修正を前提にしていないか
本格RAGとして誇張していないか
実案件データ、顧客データ、社内サービス詳細を含んでいないか
```

---

## 25. pytestで確認する観点

PoC 3では、回答方針が守られていることをpytestで確認する。

確認する内容は以下。

```text
sample_answers_v001.md が存在すること
各Questionに対するAnswerが存在すること
Referenced Sourcesが含まれていること
HumanReviewRequiredが含まれていること
DeepDiveRequiredが含まれていること
Cautionが含まれていること
禁止表現が含まれていないこと
AIが最終判断する表現が含まれていないこと
Revitモデルを自動修正する表現が含まれていないこと
人間確認不要という表現が含まれていないこと
```

禁止表現の例。

```text
AIが最終判断します
自動で承認します
Revitモデルを自動修正します
人間確認は不要です
```

---

## 26. 将来的な拡張時の注意

将来的にLLMやAzure AI Search、OpenAI API、Azure OpenAI API、LangChain、LlamaIndex、FAISS、Chromaなどを使う場合でも、このAnswer Policyは維持する。

本格的なRAG構成に拡張しても、以下は変えない。

```text
回答には参照元を含める
AIは最終判断しない
Human Reviewが必要な判断を明示する
Deep Diveが必要な場合は追加確認を促す
実案件データや顧客データを無断で使わない
Revitモデルの自動修正を前提にしない
```

実装が高度になっても、回答の責任範囲は変えない。

---

## 27. まとめ

PoC 3の回答は、検索結果に基づく根拠付き回答である。

回答の目的は、AIが最終判断を行うことではなく、BIM担当者やAI/DX導入担当者が確認・協議するための参考情報を提示することである。

回答には以下を含める。

```text
Question
Answer
Reasoning Summary
Referenced Sources
RuleId
UseCaseId
RecommendedApproach
HumanReviewRequired
DeepDiveRequired
Caution
```

PoC 3では、以下を必ず守る。

```text
検索結果に基づいて回答する
参照元を明示する
AIが最終判断しない
Human Reviewが必要な判断を明示する
Deep Diveが必要な場合は追加確認を促す
実案件データ、顧客データ、社内サービス詳細を含めない
本格RAGであると誇張しない
```

このAnswer Policyにより、PoC 3は以下を実現する。

```text
PoC 1・PoC 2の成果物を根拠として再利用する
質問に対して関連documentを検索する
回答に参照元を含める
Human Review方針を回答に反映する
Deep Dive方針を回答に反映する
AIが最終判断しない設計を保つ
```
