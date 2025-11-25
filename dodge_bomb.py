import os
import sys
import random
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する関数
    引数:
        screen (pg.Surface): ゲーム画面のSurfaceオブジェクト
    戻り値:
        なし
    """
    # 1. 画面を暗くするためのSurfaceを作成
    dark_surf = pg.Surface((WIDTH, HEIGHT))
    dark_surf.fill((0, 0, 0)) 

    # 2. 透明度を設定
    dark_surf.set_alpha(200)

    # 3. Game Over テキストを作成
    font = pg.font.Font(None, 120)
    text_surf = font.render("GAME OVER", True, (255, 255, 255)) 
    text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
    dark_surf.blit(text_surf, text_rect)

    # 4. こうかとんの画像を左右に配置
    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.0)
    kk_l = kk_img.get_rect(center=(WIDTH//2 + 300, HEIGHT//2))
    kk_r = kk_img.get_rect(center=(WIDTH//2 - 300, HEIGHT//2))
    dark_surf.blit(kk_img, kk_l)
    dark_surf.blit(kk_img, kk_r)

    # 5. 画面に重ねる
    screen.blit(dark_surf, (0, 0))

    # 6. 更新して 5 秒停止
    pg.display.update()
    time.sleep(5)
    return

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:  #練習３
    yoko = True
    tate = True
    if rct.left < 0 or rct.right > WIDTH:
        yoko = False
    if rct.top < 0 or rct.bottom > HEIGHT:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    
    DELTA = {  #練習１
        pg.K_UP:    (0, -5),
        pg.K_DOWN:  (0, +5),
        pg.K_LEFT:  (-5, 0),
        pg.K_RIGHT: (+5, 0),
    }

    bb_img = pg.Surface((20, 20))  #練習２
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)

    bb_rct = bb_img.get_rect()  #練習２
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = 5, 5

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()  #練習１
        kk_x, kk_y = 0, 0
        for key, delta in DELTA.items():
            if key_lst[key]:
                kk_x += delta[0]
                kk_y += delta[1]
        kk_rct.move_ip(kk_x, kk_y)

        yoko, tate = check_bound(kk_rct) #練習３
        if not yoko:
            kk_rct.move_ip(-kk_x, 0)
        if not tate:
            kk_rct.move_ip(0, -kk_y)

        bb_rct.move_ip(vx, vy)

        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        if kk_rct.colliderect(bb_rct):  #練習４
            gameover(screen)
            return

        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct) #練習２
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
