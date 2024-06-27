
# 필요한 패키지 로드
library(metafor)
library(magick)

setwd('C:/Users/ilma0/PycharmProjects/pynca/resource/MET_CDM')

# 데이터 프레임 생성
meta_data <- read.csv('meta_test.csv')

# 메타분석 수행
meta_analysis <- rma(m1i = m1, sd1i = sd1, n1i = n1,
                     m2i = m2, sd2i = sd2, n2i = n2,
                     data = meta_data, measure = "SMD", method = "REML")

# # 메타분석 수행
# meta_analysis <- rma(m1i = m1, sd1i = sd1, n1i = n1,
#                      m2i = m2, sd2i = sd2, n2i = n2,
#                      data = data, measure = "SMD", method = "FE")

# 메타분석 결과 출력
summary(meta_analysis)

# 포리스트 플롯 그리기
# forest(meta_analysis, slab=paste(meta_data$hospital))

# 플롯 장치 크기 조정
par(mar=c(4, 4, 2, 2)) # 아래, 왼쪽, 위, 오른쪽 마진 설정

# 그림을 파일로 저장
png("Meta(Efficacy).png", width=2500, height=1500, res=300)

# 포리스트 플롯 그리기
forest(meta_analysis, slab=paste(meta_data$hospital), cex=1.3)

dev.off()

# 이미지 불러오기
img <- image_read("Meta(Efficacy).png")

# 이미지 자르기 (위쪽에서 300 픽셀 잘라내기)
img_cropped <- image_crop(img, geometry_area(width = 2500, height = 1500 - 300, x_off = 0, y_off = 300))

# 자른 이미지 저장
image_write(img_cropped, path = "Meta(Efficacy)_cropped.png", format = "png")
