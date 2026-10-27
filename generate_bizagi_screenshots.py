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
    # Очищаем только область цифр, сохраняя левую границу поля ввода (X=42)
    draw2.rectangle([130, 84, 191, 105], fill=(255, 255, 255))
    font_input = get_font(12, bold=False)
    draw2.text((174, 95), "6400", fill=(0, 0, 0), font=font_input, anchor="rm")
    im2.save(os.path.join(out_dir, 'bizagi_fig2_level1.png'))
    print("Generated: bizagi_fig2_level1.png")
    
    # -------------------------------------------------------------
    # РИСУНОК 3: Уровень 2 — Ввод интервала прибытия (Tприб = 0,3 ч, M = 6400)
    # -------------------------------------------------------------
    im3 = Image.open(os.path.join(sample_dir, 'sample_fig3.png')).convert('RGB')
    draw3 = ImageDraw.Draw(im3)
    # Mean: очищаем только цифры, сохраняя левую рамку (X=87)
    draw3.rectangle([150, 100, 236, 121], fill=(255, 255, 255))
    draw3.text((224, 110), "0,3", fill=(0, 0, 0), font=font_input, anchor="rm")
    # Max count: очищаем только цифры, сохраняя левую рамку (X=42)
    draw3.rectangle([130, 195, 191, 216], fill=(255, 255, 255))
    draw3.text((176, 206), "6400", fill=(0, 0, 0), font=font_input, anchor="rm")
    im3.save(os.path.join(out_dir, 'bizagi_fig3_level2_arrival.png'))
    print("Generated: bizagi_fig3_level2_arrival.png")
    
    # -------------------------------------------------------------
    # РИСУНОК 4: Уровень 2 — Ввод времени обслуживания (Tобслуж = 0,15 ч)
    # -------------------------------------------------------------
    im4 = Image.open(os.path.join(sample_dir, 'sample_fig4.png')).convert('RGB')
    draw4 = ImageDraw.Draw(im4)
    # Mean: очищаем только цифры, сохраняя левую рамку (X=87)
    draw4.rectangle([150, 100, 236, 121], fill=(255, 255, 255))
    draw4.text((224, 110), "0,15", fill=(0, 0, 0), font=font_input, anchor="rm")
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
    
    font_badge = get_font(9, bold=False)
    font_task6 = get_font(8, bold=False)
    
    # 1. Start badge text (аккуратный отступ от красного маркера)
    draw6.rectangle([153, 244, 195, 256], fill=(248, 249, 250))
    draw6.text((158, 245), "6400", fill=(56, 77, 114), font=font_badge)
    
    # 2. End badge text (аккуратный отступ от красного маркера)
    draw6.rectangle([403, 244, 445, 256], fill=(248, 249, 250))
    draw6.text((408, 245), "6400", fill=(56, 77, 114), font=font_badge)
    
    # 3. Task badges (аккуратный отступ от цветных маркеров)
    draw6.rectangle([315, 198, 362, 211], fill=(255, 255, 255))
    draw6.text((319, 200), "6400", fill=(56, 77, 114), font=font_badge)
    
    draw6.rectangle([315, 211, 362, 224], fill=(250, 252, 254))
    draw6.text((319, 213), "0,27 h", fill=(56, 77, 114), font=font_badge)
    
    draw6.rectangle([315, 224, 362, 243], fill=(240, 242, 245))
    draw6.text((319, 226), "0,12 h", fill=(56, 77, 114), font=font_badge)
    
    # 4. Top pool badge
    draw6.rectangle([725, 129, 768, 142], fill=(255, 255, 255))
    draw6.text((729, 131), "6400", fill=(56, 77, 114), font=font_badge)
    
    draw6.rectangle([725, 142, 768, 156], fill=(248, 250, 253))
    draw6.text((729, 144), "0,27 h", fill=(56, 77, 114), font=font_badge)
    
    # 5. Task box text
    for y in range(240, 281):
        f = (y - 240) / 41.0
        r = int(248 * (1 - f) + 234 * f)
        g = int(251 * (1 - f) + 242 * f)
        b = int(254 * (1 - f) + 250 * f)
        draw6.line([(225, y), (316, y)], fill=(r, g, b))
        
    draw6.multiline_text((270, 260), "Обслуживание\nпокупателя на\nкассе", fill=(30, 41, 59), font=font_task6, anchor="mm", align="center", spacing=1)
    
    # 6. Обновляем график Resource Utilization справа:
    # Заменяем только текст подписи ресурса в легенде X=[1205, 1335], Y=[150, 166], СОХРАНЯЯ синий маркер ресурса [1185, 1200]
    draw6.rectangle([1205, 150, 1335, 166], fill=(255, 255, 255))
    font_legend = get_font(8.5, bold=False)
    draw6.text((1207, 158), "Кассир-продавец", fill=(30, 41, 59), font=font_legend, anchor="lm")
    
    # Столбик загрузки: от X=1046 до 1146 (в оригинале ~91.6%).
    # Для 49.5% столбик заканчивается на X = 1100.
    # Очищаем только хвостовую часть синего столбика от 1101 до 1146 по высоте столбика Y=[188, 242]:
    draw6.rectangle([1101, 188, 1146, 242], fill=(255, 255, 255))
    # Восстанавливаем пересекаемые вертикальные линии сетки внутри очищенной области:
    # 60%: X = 1112
    draw6.line([(1112, 188), (1112, 242)], fill=(0, 0, 0), width=1)
    # 80%: X = 1134
    draw6.line([(1134, 188), (1134, 242)], fill=(0, 0, 0), width=1)
    
    im6.save(os.path.join(out_dir, 'bizagi_fig6_sim_completed.png'))
    print("Generated: bizagi_fig6_sim_completed.png")
    
    # -------------------------------------------------------------
    # РИСУНОК 7: Результаты симуляции — вкладка Resources (Utilization)
    # -------------------------------------------------------------
    im7 = Image.open(os.path.join(sample_dir, 'sample_fig7.png')).convert('RGB')
    draw7 = ImageDraw.Draw(im7)
    draw7.rectangle([275, 189, 540, 229], fill=(255, 255, 255))
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
    
    # Очищаем ТОЛЬКО ячейки с цифрами внутри столбцов, полностью сохраняя сетку таблицы и чередование строк!
    # Строка 1 (Task row, Y=233..267):
    draw8.rectangle([275, 243, 355, 265], fill=(255, 255, 255))
    draw8.rectangle([360, 243, 450, 265], fill=(255, 255, 255))
    draw8.rectangle([455, 233, 570, 267], fill=(255, 255, 255))
    
    # Строка 3 (Total row, Y=313..347):
    draw8.rectangle([275, 322, 355, 345], fill=(255, 255, 255))
    draw8.rectangle([360, 322, 450, 345], fill=(255, 255, 255))
    draw8.rectangle([455, 313, 570, 347], fill=(255, 255, 255))
    draw8.rectangle([578, 322, 645, 345], fill=(255, 255, 255))
    draw8.rectangle([688, 322, 785, 345], fill=(255, 255, 255))
    draw8.rectangle([798, 322, 885, 345], fill=(255, 255, 255))
    draw8.rectangle([905, 322, 975, 345], fill=(255, 255, 255))
    
    font_tbl8 = get_font(10.0, bold=False)
    # Первая строка (данные работы) Y=254
    draw8.text((305, 254), "2h 12m 30s", fill=(30, 41, 59), font=font_tbl8, anchor="mm")
    draw8.text((398, 254), "16m 13s", fill=(30, 41, 59), font=font_tbl8, anchor="mm")
    draw8.text((505, 254), "79d 6h 10m", fill=(30, 41, 59), font=font_tbl8, anchor="mm")
    
    # Вторая строка (итого по процессу) Y=333
    draw8.text((305, 333), "2h 12m 30s", fill=(30, 41, 59), font=font_tbl8, anchor="mm")
    draw8.text((398, 333), "16m 13s", fill=(30, 41, 59), font=font_tbl8, anchor="mm")
    draw8.text((505, 333), "79d 6h 10m", fill=(30, 41, 59), font=font_tbl8, anchor="mm")
    draw8.text((605, 333), "0", fill=(30, 41, 59), font=font_tbl8, anchor="mm")
    draw8.text((728, 333), "2h 2m 31s", fill=(30, 41, 59), font=font_tbl8, anchor="mm")
    draw8.text((835, 333), "7m 24s", fill=(30, 41, 59), font=font_tbl8, anchor="mm")
    draw8.text((938, 333), "12m 35s", fill=(30, 41, 59), font=font_tbl8, anchor="mm")
    
    im8.save(os.path.join(out_dir, 'bizagi_fig8_results_process.png'))
    print("Generated: bizagi_fig8_results_process.png")

if __name__ == '__main__':
    generate_screenshots()
