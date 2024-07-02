import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

# 데이터 파일 로드
resource_dir = '/resource/MET_CDM'

# 이미지 파일 로드
img1_path = f'{resource_dir}/Meta(AE).png'
img2_path = f'{resource_dir}/Meta(Efficacy).png'
img1 = Image.open(img1_path)
img2 = Image.open(img2_path)



# 이미지의 상단 여백을 제거하는 함수
def crop_top(image, crop_height):
    width, height = image.size
    return image.crop((0, crop_height, width, height))

# 상단 여백을 자르기 (crop_height 값을 조정하여 원하는 만큼 자르세요)
crop_height = 300
img1_cropped = crop_top(img1, crop_height)
img2_cropped = crop_top(img2, crop_height)

# Figure와 subplot 생성
fig, axes = plt.subplots(2, 1, figsize=(15, 22))

# 첫 번째 subplot에 이미지 추가
axes[0].imshow(img1_cropped)
axes[0].axis('off')
axes[0].text(0.01, 0.95, '(A)', transform=axes[0].transAxes, fontsize=16, verticalalignment='top')
# axes[0].text(0.01, 0.95, '(A) HbA1c change (%)', transform=axes[0].transAxes, fontsize=13, verticalalignment='top')

# 두 번째 subplot에 이미지 추가
axes[1].imshow(img2_cropped)
axes[1].axis('off')
axes[1].text(0.01, 0.95, '(B)', transform=axes[1].transAxes, fontsize=16, verticalalignment='top')
# axes[1].text(0.01, 0.95, '(B) Incidence rate of adverse events', transform=axes[1].transAxes, fontsize=13, verticalalignment='top')

# 서브플롯 사이의 수직 간격을 없애기 위해 hspace를 0으로 설정
plt.subplots_adjust(hspace=0)

# 레이아웃 조정 및 출력
# plt.tight_layout()

# plt.savefig(output_path, dpi=600)
plt.savefig(f'{resource_dir}/Meta(combined).png', dpi=600, bbox_inches='tight')
