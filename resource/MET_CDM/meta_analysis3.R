# 필요한 패키지 로드
library(metafor)

# 데이터 준비 (예시 데이터프레임)
data <- data.frame(
  study = c("SNUH", "SNUBH"),
  ai = c(273, 233),
  bi = c(434, 480),
  ci = c(252, 197),
  di = c(438, 505)
)

#  a𝑖 : 사건이 발생한 실험군의 환자 수
# 𝑏𝑖 : 사건이 발생하지 않은 실험군의 환자 수
# 𝑐𝑖 : 사건이 발생한 대조군의 환자 수
# 𝑑𝑖 : 사건이 발생하지 않은 대조군의 환자 수

# 로그 오즈비와 그 표준 오류 계산
data <- escalc(measure = "OR", ai = ai, bi = bi, ci = ci, di = di, data = data)

# 메타분석 수행
meta_analysis <- rma(yi = yi, vi = vi, data = data, method = "REML")

# 메타분석 결과 출력
summary(meta_analysis)

# 포리스트 플롯 그리기
forest(meta_analysis, slab = data$study)