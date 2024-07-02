from PIL import Image, ImageDraw, ImageFont

# 이미지 파일 로드
resource_dir = '/resource/MET_CDM'
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

# 두 이미지를 세로로 결합
total_width = max(img1_cropped.width, img2_cropped.width)
total_height = img1_cropped.height + img2_cropped.height
combined_img = Image.new('RGB', (total_width, total_height), (255, 255, 255))

# 첫 번째 이미지 붙여넣기
combined_img.paste(img1_cropped, (0, 0))

# 두 번째 이미지 붙여넣기
combined_img.paste(img2_cropped, (0, img1_cropped.height))

# 이미지에 텍스트 추가
draw = ImageDraw.Draw(combined_img)

# 폰트 크기를 크게 설정 (시스템에 따라 적절한 경로로 변경)
try:
    font = ImageFont.truetype("arial.ttf", 70)
except IOError:
    font = ImageFont.load_default()
# font = ImageFont.load_default()

# 텍스트 위치 조정
draw.text((10, 10), "(A)", fill="black", font=font)
draw.text((10, img1_cropped.height + 10), "(B)", fill="black", font=font)
# draw.text((10, 10), "(A) HbA1c change (%)", fill="black", font=font)
# draw.text((10, img1_cropped.height + 10), "(B) Incidence rate of adverse events", fill="black", font=font)


# 결합된 이미지 저장 및 출력
output_path = f'{resource_dir}/Meta(combined).png'
# output_path = f'{resource_dir}/Meta(combined_with text).png'
combined_img.save(output_path, dpi=(600, 600))
combined_img.show()
