import pygame
import time

pygame.init()

# 設置遊戲視窗大小
screen_width, screen_height = 700, 466
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("dino clock")

# 載入背景並取得其大小
day_background = pygame.image.load("day.JPG").convert_alpha()
night_background = pygame.image.load("night.JPG").convert_alpha()

# 取得背景圖片的長寬比
bg_width, bg_height = day_background.get_size()
aspect_ratio = bg_width / bg_height

# 設定最大寬度並計算對應的高度
max_width = screen_width
max_height = int(max_width / aspect_ratio)

# 恐龍站立圖片
dino_images = [
    pygame.transform.scale(pygame.image.load("dino1.png").convert_alpha(), (60, 60)),
    pygame.transform.scale(pygame.image.load("dino2.png").convert_alpha(), (60, 60))
]

# 字型設定
font = pygame.font.SysFont("Impact", 70)
small_font = pygame.font.SysFont("Tahoma", 30)

# 時間與動畫初始化
current_second = int(time.strftime("%S"))
dino_start_time = time.time() - current_second
dino_frame = 0
frame_switch_time = 0.3
last_frame_time = time.time()

# 主迴圈
running = True
clock = pygame.time.Clock()

# 用來決定背景顏色（白天/夜晚）
is_daytime = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 每分鐘切換背景
    if int(time.strftime("%M")) % 2 == 0:
        is_daytime = True
    else:
        is_daytime = False

    # 填背景色
    screen.fill((187, 47, 229))

    # 根據視窗大小縮放背景圖片，保持長寬比
    if is_daytime:
        background = pygame.transform.scale(day_background, (max_width, max_height))
    else:
        background = pygame.transform.scale(night_background, (max_width, max_height))

    # 顯示背景圖
    screen.blit(background, (0, 0))  # 背景從(0, 0)開始

    # 顯示時間與 AM/PM
    current_time = time.strftime("%I : %M : %S")
    am_pm = time.strftime("%p")

    # 為時間文字加陰影
    text = font.render(current_time, True, (255, 255, 255))  # 白色文字
    am_pm_text = small_font.render(am_pm, True, (255, 255, 255))  # 白色文字

    # 為陰影創建黑色文字，並稍微偏移
    shadow_text = font.render(current_time, True, (0, 0, 0))  # 黑色陰影
    shadow_am_pm_text = small_font.render(am_pm, True, (0, 0, 0))  # 黑色陰影

    # 設定時間顯示的座標為視窗寬度的中間，並放置在頂部
    text_rect = text.get_rect(center=(max_width // 2, 150))  # 居中顯示時間
    am_pm_rect = am_pm_text.get_rect(center=(160, 100))  # AM/PM顯示在時間上方

    # 顯示陰影
    screen.blit(shadow_text, (text_rect.x + 3, text_rect.y + 3))  # 偏移陰影
    screen.blit(shadow_am_pm_text, (am_pm_rect.x + 3, am_pm_rect.y + 3))  # 偏移陰影

    # 顯示時間與 AM/PM
    screen.blit(text, text_rect)
    screen.blit(am_pm_text, am_pm_rect)

    # 更新恐龍位置
    elapsed = time.time() - dino_start_time
    dino_x = int((elapsed / 60.0) * max_width)
    if dino_x > max_width:
        current_second = int(time.strftime("%S"))
        dino_start_time = time.time() - current_second
        dino_x = 0

    # 更新動畫幀
    if time.time() - last_frame_time >= frame_switch_time:
        dino_frame = (dino_frame + 1) % 2
        last_frame_time = time.time()

    # 顯示恐龍
    dino_y = max_height - 175  # 恐龍始終保持站立狀態
    screen.blit(dino_images[dino_frame], (dino_x, dino_y))

    pygame.display.update()
    clock.tick(60)  # 控制每秒最多更新 60 次

pygame.quit()