install.packages("metafor")

# 필요한 패키지 로드
library(metafor)

setwd('C:/Users/ilma0/PycharmProjects/pynca/resource/MET_CDM')

# 데이터 로드
a_data <- read.csv('SNUH.csv')
b_data <- read.csv('SNUBH.csv')

a_data <- a_data[c("pt_type", "HbA1C_delta")]
a_data$hospital = 'SNUH'
  
b_data <- b_data[c("pt_type", "HbA1C_delta")]
b_data$hospital = 'SNUBH'

data <- rbind(a_data, b_data)[c('hospital','pt_type', 'HbA1C_delta')]
# data <- rbind(a_data, b_data)
# data <- data[,order(data$hospital, data$pt_type)]

# data <- read.csv('meta_test.csv')

# 각 그룹 및 병원별 평균 및 표준편차 계산
stats_summary <- aggregate(HbA1C_delta ~ pt_type + hospital, data, 
                           function(x) c(mean = mean(x), sd = sd(x), n = length(x)))

# 메타 분석을 위한 데이터 준비
effect_sizes <- c()
variances <- c()
for (i in 1:nrow(stats_summary)) {
  row <- stats_summary[i, ]
  mean_val <- row$HbA1C_delta[1]
  sd_val <- row$HbA1C_delta[2]
  n_val <- row$HbA1C_delta[3]
  
  effect_sizes <- c(effect_sizes, mean_val)
  variances <- c(variances, (sd_val^2) / n_val)
}

# 데이터 프레임 생성
meta_data <- data.frame(
  effect_size = effect_sizes,
  variance = variances,
  hospital = rep(stats_summary$hospital, each = 1),
  pt_type = rep(stats_summary$pt_type, each = 1)
  
)

meta_data <-meta_data[order(meta_data$pt_type), ]

# 메타 분석 수행
res <- rma(yi = effect_size, vi = variance, data = meta_data, method = "REML")

# 결과 출력
summary(res)

# 포리스트 플롯 그리기
forest(res, slab=paste(meta_data$pt_type, meta_data$hospital), sep=", ")