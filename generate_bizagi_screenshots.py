import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size=12, bold=False):
    font_name = 'segoeuib.ttf' if bold else 'segoeui.ttf'
    font_path = os.path.join(r'C:\Windows\Fonts', font_name)
    if os.path.exists(font_path):
        return ImageFont.truetype(font_path, size)
    fallback_name = 'arialbd.ttf' if bold else 'arial.ttf'
    return ImageFont.truetype(os.path.join(r'C:\Windows\Fonts', fallback_name), size)

def generate_screenshots():
    sample_dir = 'bizagi_screens_sample'
    out_dir = 'bizagi_screens'
    os.makedirs(out_dir, exist_ok=True)
    
    # -------------------------------------------------------------
    # РИСУНОК 1: Обобщенная модель бизнес-процесса в нотации BPMN
    # -------------------------------------------------------------
    im1 = Image.open(os.path.join(sample_dir, 'sample_fig1.png')).convert('RGB')
    draw1 = ImageDraw.Draw(im1)
    for y in range(302, 359):
        factor = (y - 302) / 57.0
        r = int(245 * (1 - factor) + 231 * factor)
        g = int(248 * (1 - factor) + 239 * factor)
        b = int(252 * (1 - factor) + 248 * factor)
        draw1.line([(316, y), (412, y)], fill=(r, g, b))
        
    font_task = get_font(10, bold=False)
    task_text = "Обслуживание\nпокупателя на\nкассе"
    draw1.multiline_text((364, 330), task_text, fill=(30, 41, 59), font=font_task, anchor="mm", align="center", spacing=2)
    im1.save(os.path.join(out_dir, 'bizagi_fig1_model.png'))
    print("Generated: bizagi_fig1_model.png")
    
    # -------------------------------------------------------------
    # РИСУНОК 2: Уровень 1 — Ввод максимального количества заявок (M = 6400)
    # -------------------------------------------------------------
    im2 = Image.open(os.path.join(sample_dir, 'sample_fig2.png')).convert('RGB')
    draw2 = ImageDraw.Draw(im2)
    draw2.rectangle([45, 85, 185, 105], fill=(255, 255, 255))
    font_input = get_font(12, bold=False)
    draw2.text((174, 95), "6400", fill=(0, 0, 0), font=font_input, anchor="rm")
    im2.save(os.path.join(out_dir, 'bizagi_fig2_level1.png'))
    print("Generated: bizagi_fig2_level1.png")
    
    # -------------------------------------------------------------
    # РИСУНОК 3: Уровень 2 — Ввод интервала прибытия (Tприб = 0,3 ч, M = 6400)
    # -------------------------------------------------------------
    im3 = Image.open(os.path.join(sample_dir, 'sample_fig3.png')).convert('RGB')
    draw3 = ImageDraw.Draw(im3)
    draw3.rectangle([90, 96, 235, 116], fill=(255, 255, 255))
    draw3.text((224, 106), "0,3", fill=(0, 0, 0), font=font_input, anchor="rm")
    draw3.rectangle([45, 196, 188, 217], fill=(255, 255, 255))
    draw3.text((176, 206), "6400", fill=(0, 0, 0), font=font_input, anchor="rm")
    im3.save(os.path.join(out_dir, 'bizagi_fig3_level2_arrival.png'))
    print("Generated: bizagi_fig3_level2_arrival.png")
    
    # -------------------------------------------------------------
    # РИСУНОК 4: Уровень 2 — Ввод времени обслуживания (Tобслуж = 0,15 ч)
    # -------------------------------------------------------------
    im4 = Image.open(os.path.join(sample_dir, 'sample_fig4.png')).convert('RGB')
    draw4 = ImageDraw.Draw(im4)
    draw4.rectangle([90, 98, 235, 120], fill=(255, 255, 255))
    draw4.text((224, 109), "0,15", fill=(0, 0, 0), font=font_input, anchor="rm")
    im4.save(os.path.join(out_dir, 'bizagi_fig4_level2_service.png'))
    print("Generated: bizagi_fig4_level2_service.png")
    
    # -------------------------------------------------------------
    # РИСУНОК 5: Уровень 3 — Назначение ресурса «Кассир-продавец»
    # -------------------------------------------------------------
    im5 = Image.open(os.path.join(sample_dir, 'sample_fig5.png')).convert('RGB')
    draw5 = ImageDraw.Draw(im5)
    draw5.rectangle([65, 118, 226, 142], fill=(248, 248, 248))
    font_res = get_font(12, bold=False)
    draw5.text((65, 130), "Кассир-продавец", fill=(0, 0, 0), font=font_res, anchor="lm")
    im5.save(os.path.join(out_dir, 'bizagi_fig5_level3_resource.png'))
    print("Generated: bizagi_fig5_level3_resource.png")
    
    # -------------------------------------------------------------
    # РИСУНОК 6: Окно завершения симуляции (6400 заявок)
    # -------------------------------------------------------------
    im6 = Image.open(os.path.join(sample_dir, 'sample_fig6.png')).convert('RGB')
    draw6 = ImageDraw.Draw(im6)
    
    # Обновляем текст задачи внутри блока X=[222, 319], Y=[232, 289]
    for y in range(232, 289):
        factor = (y - 232) / 57.0
        r = int(245 * (1 - factor) + 231 * factor)
        g = int(248 * (1 - factor) + 239 * factor)
        b = int(252 * (1 - factor) + 248 * factor)
        draw6.line([(222, y), (319, y)], fill=(r, g, b))
    font_task6 = get_font(9.0, bold=False)
    draw6.multiline_text((264, 260), "Обслуживание\nпокупателя на\nкассе", fill=(30, 41, 59), font=font_task6, anchor="mm", align="center", spacing=1)
    
    # Обновляем плашку на стартовом событии:
    draw6.rectangle([153, 241, 195, 253], fill=(255, 255, 255))
    font_badge = get_font(9, bold=False)
    draw6.text((174, 247), "6400", fill=(0, 0, 0), font=font_badge, anchor="mm")
    
    # Обновляем плашку на конечном событии:
    draw6.rectangle([400, 241, 442, 253], fill=(255, 255, 255))
    draw6.text((421, 247), "6400", fill=(0, 0, 0), font=font_badge, anchor="mm")
    
    # Обновляем верхнюю плашку на пуле:
    draw6.rectangle([720, 129, 765, 142], fill=(255, 255, 255))
    draw6.text((742, 135), "6400", fill=(0, 0, 0), font=font_badge, anchor="mm")
    draw6.rectangle([720, 143, 765, 156], fill=(255, 255, 255))
    draw6.text((742, 149), "0,27 h", fill=(0, 0, 0), font=font_badge, anchor="mm")
    
    # Обновляем плашку на задаче:
    draw6.rectangle([312, 197, 362, 210], fill=(255, 255, 255))
    draw6.text((337, 203), "6400", fill=(0, 0, 0), font=font_badge, anchor="mm")
    draw6.rectangle([312, 211, 362, 224], fill=(255, 255, 255))
    draw6.text((337, 217), "0,27 h", fill=(0, 0, 0), font=font_badge, anchor="mm")
    draw6.rectangle([312, 225, 362, 238], fill=(255, 255, 255))
    draw6.text((337, 231), "0,12 h", fill=(0, 0, 0), font=font_badge, anchor="mm")
    
    # Обновляем график Resource Utilization справа:
    # 1. Заменяем подпись ресурса в легенде X=[1180, 1330], Y=[150, 168]
    draw6.rectangle([1180, 150, 1330, 168], fill=(255, 255, 255))
    font_legend = get_font(8.5, bold=False)
    draw6.text((1180, 158), "Кассир-продавец", fill=(30, 41, 59), font=font_legend, anchor="lm")
    
    # 2. Столбик загрузки: от X=1046 до 1156.
    # В исходном изображении синий прямоугольник [65, 140, 240] залит до 91.6% (X ≈ 1146).
    # Для 49.5% столбик заканчивается на X = 1101.
    # Очищаем область от 1101 до 1155, Y=[169, 259] белым цветом:
    draw6.rectangle([1101, 169, 1155, 259], fill=(255, 255, 255))
    # Восстанавливаем сетку графика:
    # Вертикальные линии сетки:
    # 60%: X = 1112
    # 80%: X = 1134
    # 100%: X = 1156
    draw6.line([(1112, 169), (1112, 260)], fill=(0, 0, 0), width=1)
    draw6.line([(1134, 169), (1134, 260)], fill=(0, 0, 0), width=1)
    draw6.line([(1156, 169), (1156, 260)], fill=(0, 0, 0), width=1)
    # Горизонтальная ось Y=1 (Y=200):
    draw6.line([(1101, 200), (1156, 200)], fill=(0, 0, 0), width=1)
    # Нижняя и верхняя границы графика:
    draw6.line([(1101, 169), (1156, 169)], fill=(0, 0, 0), width=1)
    draw6.line([(1101, 260), (1156, 260)], fill=(0, 0, 0), width=1)
    # Засечка на отметке 1 справа:
    draw6.line([(1156, 200), (1161, 200)], fill=(0, 0, 0), width=1)
    
    im6.save(os.path.join(out_dir, 'bizagi_fig6_sim_completed.png'))
    print("Generated: bizagi_fig6_sim_completed.png")
    
    # -------------------------------------------------------------
    # РИСУНОК 7: Результаты симуляции — вкладка Resources (Utilization)
    # -------------------------------------------------------------
    im7 = Image.open(os.path.join(sample_dir, 'sample_fig7.png')).convert('RGB')
    draw7 = ImageDraw.Draw(im7)
    draw7.rectangle([275, 188, 540, 230], fill=(255, 255, 255))
    font_tbl = get_font(12, bold=False)
    draw7.text((278, 208), "Кассир-продавец", fill=(0, 0, 0), font=font_tbl, anchor="lm")
    draw7.text((435, 208), "49,46 %", fill=(0, 0, 0), font=font_tbl, anchor="mm")
    im7.save(os.path.join(out_dir, 'bizagi_fig7_results_resources.png'))
    print("Generated: bizagi_fig7_results_resources.png")
    
    # -------------------------------------------------------------
    # РИСУНОК 8: Результаты симуляции — вкладка Process 1
    # -------------------------------------------------------------
    im8 = Image.open(os.path.join(sample_dir, 'sample_fig8.png')).convert('RGB')
    draw8 = ImageDraw.Draw(im8)
    
    # Очищаем строки данных таблицы:
    draw8.rectangle([272, 235, 988, 345], fill=(255, 255, 255))
    
    font_tbl8 = get_font(10.5, bold=False)
    # Первая строка (данные работы) Y=248
    draw8.text((310, 248), "2h 12m 30s", fill=(0, 0, 0), font=font_tbl8, anchor="mm")
    draw8.text((400, 248), "16m 13s", fill=(0, 0, 0), font=font_tbl8, anchor="mm")
    draw8.text((505, 248), "79d 6h 10m", fill=(0, 0, 0), font=font_tbl8, anchor="mm")
    draw8.text((620, 248), "0", fill=(0, 0, 0), font=font_tbl8, anchor="mm")
    draw8.text((733, 248), "2h 2m 31s", fill=(0, 0, 0), font=font_tbl8, anchor="mm")
    draw8.text((850, 248), "7m 24s", fill=(0, 0, 0), font=font_tbl8, anchor="mm")
    draw8.text((945, 248), "12m 35s", fill=(0, 0, 0), font=font_tbl8, anchor="mm")
    
    # Вторая строка (итого по процессу) Y=328
    draw8.text((310, 328), "2h 12m 30s", fill=(0, 0, 0), font=font_tbl8, anchor="mm")
    draw8.text((400, 328), "16m 13s", fill=(0, 0, 0), font=font_tbl8, anchor="mm")
    draw8.text((505, 328), "79d 6h 10m", fill=(0, 0, 0), font=font_tbl8, anchor="mm")
    draw8.text((620, 328), "0", fill=(0, 0, 0), font=font_tbl8, anchor="mm")
    draw8.text((733, 328), "2h 2m 31s", fill=(0, 0, 0), font=font_tbl8, anchor="mm")
    draw8.text((850, 328), "7m 24s", fill=(0, 0, 0), font=font_tbl8, anchor="mm")
    draw8.text((945, 328), "12m 35s", fill=(0, 0, 0), font=font_tbl8, anchor="mm")
    
    im8.save(os.path.join(out_dir, 'bizagi_fig8_results_process.png'))
    print("Generated: bizagi_fig8_results_process.png")

if __name__ == '__main__':
    generate_screenshots()
