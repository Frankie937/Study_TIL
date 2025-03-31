
(논문 :CONTEXTGNN: BEYOND TWO-TOWER RECOMMENDATION SYSTEMS)

## ContextGNN 논문에 대한 상세 설명

ContextGNN 논문에 대해 깊이, 구체성, 그리고 기술적인 측면에서 상세하게 설명드리겠습니다.

**개요**

이 논문은 추천 시스템에서 기존의 Two-Tower 아키텍처의 한계점을 극복하기 위해 Context-based Graph Neural Networks (ContextGNN)라는 새로운 딥러닝 아키텍처를 제안합니다. Two-Tower 모델은 사용자-아이템 쌍에 대한 상호 작용을 고려하지 않고 사용자 및 아이템을 독립적으로 임베딩하여 추천을 수행합니다. 반면, ContextGNN은 사용자의 로컬 서브그래프 내에 있는 아이템에 대해서는 쌍 기반 표현(Pair-wise Representation)을 사용하고, 탐색적 아이템 추천을 위해서는 Two-Tower 표현을 활용하여 두 가지 접근 방식을 융합합니다.

**문제점 및 해결 방안**

*   **기존 Two-Tower 모델의 문제점:** 사용자-아이템 쌍에 대한 상호 의존성을 고려하지 않아 사용자의 선호도를 정확하게 반영하지 못하고, familiar purchases (반복 구매)와 exploratory purchases (탐색적 구매)를 구별하기 어렵습니다.
*   **Pair-wise 표현의 문제점:** 모든 사용자-아이템 쌍에 대해 표현을 생성하는 것은 연산 비용이 매우 높고 (quadratic complexity), 후보 쌍을 미리 필터링하면 모델의 추천 범위가 제한됩니다.
*   **ContextGNN의 해결 방안:**
    *   사용자의 로컬 서브그래프 내 아이템에 대해서는 Pair-wise 표현을 사용하여 사용자-아이템 간의 세밀한 상호 작용 패턴을 학습합니다.
    *   Two-Tower 표현을 활용하여 탐색적 아이템 및 cold-start 아이템에 대한 추천을 지원합니다.
    *   사용자-특정 융합 점수(user-specific fusion score)를 학습하여 Pair-wise 및 Two-Tower 추천을 적절히 결합합니다.

**핵심 방법론 (ContextGNN 아키텍처)**

ContextGNN은 크게 다음과 같은 세 가지 구성 요소로 이루어져 있습니다.

1.  **Pair-wise Representation (로컬 표현):**

    *   사용자 `v`를 중심으로 k-hop 서브그래프 `G`를 샘플링합니다. (G ← G(−∞,T ]k [v])
    *   사용자 시드 노드(seed node) `v`에 d-차원 INDICATORθ 표현을 추가합니다. (h(0)v ← h(0)v + INDICATORθ)
    *   GNN (Graph Neural Network)을 사용하여 사용자 및 아이템 표현을 학습합니다. 여기서 GNN은 사용자-특정 서브그래프 내에서 메시지 전달(message passing)을 통해 노드 간의 관계를 학습합니다.
        *   구체적으로, GNN의 각 레이어에서 노드 `i`의 임베딩 `h_i^(l)`는 다음과 같이 업데이트됩니다.

        ```
        m_i^(l) = AGGREGATE({h_j^(l-1) | j ∈ N(i)})
        h_i^(l) = UPDATE(h_i^(l-1), m_i^(l))
        ```

        *   여기서 `N(i)`는 노드 `i`의 이웃 노드 집합을 나타내고, `AGGREGATE`는 이웃 노드의 임베딩을 집계하는 함수(예: 평균, 합계)이며, `UPDATE`는 현재 노드의 임베딩과 집계된 이웃 정보를 결합하여 임베딩을 업데이트하는 함수입니다.
    *   GNN의 k번째 레이어에서 사용자 표현 `h(k)v`와 아이템 표현 `{h(k)w : w ∈ Ṽ ∩ R}`을 추출합니다.
    *   사용자 표현과 아이템 표현의 내적을 통해 최종 순위를 계산합니다. (y(pair)(v,w) ← h(k)v · h(k)w)
2.  **Two-Tower Representation (글로벌 표현):**

    *   아이템 측 GNN의 비효율성 문제를 해결하기 위해 얕은(shallow) 아이템 임베딩 행렬 W ∈ R|R|×d을 사용합니다.
    *   사용자 `v`를 중심으로 k-hop 서브그래프 `G`를 샘플링합니다. (G ← G(−∞,T ]k [v])
    *   샘플링된 모든 아이템 `w ∈ Ṽ ∩ R`에 대해 얕은 임베딩을 추가합니다. (h(0)w ← h(0)w + ww)
    *   GNN을 사용하여 사용자 표현 `h(k)v`를 학습합니다.
    *   사용자 표현과 아이템 임베딩의 내적을 통해 최종 순위를 계산합니다. (y(tower)(v,w) ← h(k)v · ww)
3.  **Fusion (융합):**

    *   Pair-wise 표현과 Two-Tower 표현을 융합하기 위해 사용자-특정 융합 점수를 학습합니다.
    *   MLPθ 를 사용하여 GNN의 사용자 임베딩 h(k)v로부터 융합 점수를 예측합니다.
    *   최종 점수는 다음과 같이 계산됩니다.

    ```
    y(v,w) = {
        y(pair)(v,w) + MLPθ(h(k)v)  if w ∈ Ṽ ∪ R,
        y(tower)(v,w)                 otherwise.
    }
    ```

**실험 결과 및 분석**

*   ContextGNN은 RELBENCH 데이터셋에서 기존 모델 대비 평균 20% 향상된 성능을 보였습니다.
*   특히 locality score가 낮은 데이터셋에서 ContextGNN의 성능 향상이 두드러졌습니다. 이는 ContextGNN이 exploratory 아이템 추천에서 Two-Tower 표현의 장점을 효과적으로 활용했기 때문입니다.
*   ContextGNN은 단일 GNN forward pass만 필요로 하므로 기존 Two-Tower GNN 대비 효율성이 높습니다.

**결론**

ContextGNN은 Pair-wise 표현과 Two-Tower 표현을 융합하여 추천 시스템의 성능과 효율성을 동시에 향상시키는 효과적인 아키텍처입니다. 이 모델은 다양한 데이터 특성에 적응하고, familiar items와 exploratory items를 모두 잘 처리할 수 있습니다.

**기술적 세부 사항**

*   **GNN Backbone:** 논문에서는 heterogeneous GraphSAGE 변형을 사용합니다. 이는 다양한 유형의 노드와 엣지를 처리할 수 있도록 설계되었습니다.
*   **학습:** 모델은 end-to-end 방식으로 학습되며, cross-entropy loss를 사용하여 최적화됩니다. sampled softmax formulation을 사용하여 학습 효율성을 높입니다.
*   **추론:** Two-Tower 모델의 top score는 approximate maximum inner product search (MIPS)를 사용하여 계산됩니다.

이 설명이 ContextGNN 논문을 이해하는 데 도움이 되기를 바랍니다.
