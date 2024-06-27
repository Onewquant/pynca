# 필요한 패키지 로드
install.packages("magick")

library(magick)
library(metafor)

setwd('C:/Users/ilma0/PycharmProjects/pynca/resource/MET_CDM')

# 데이터 준비 (예시 데이터프레임)
data <- data.frame(
  study = c("SNUH", "SNUBH"),
  ai = c(100, 9),
  bi = c(716, 836),
  ci = c(114, 12),
  di = c(702, 833)
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

# 플롯 장치 크기 조정
par(mar=c(4, 4, 2, 2)) # 아래, 왼쪽, 위, 오른쪽 마진 설정

# 그림을 파일로 저장
png("Meta(AE).png", width=2500, height=1500, res=300)

# 포리스트 플롯 그리기
forest(meta_analysis, slab = data$study, cex=1.3)

dev.off()


# 이미지 불러오기
img <- image_read("Meta(AE).png")

# 이미지 자르기 (위쪽에서 300 픽셀 잘라내기)
img_cropped <- image_crop(img, geometry_area(width = 2500, height = 1500 - 300, x_off = 0, y_off = 300))

# 자른 이미지 저장
image_write(img_cropped, path = "Meta(AE)_cropped.png", format = "png")