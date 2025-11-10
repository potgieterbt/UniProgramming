print("Welcome to Hilda's Haberdashery Stock Management System")

sewing_thread_price = 1.2
zipper_price = 0.65
wooden_button_10_price = 1.8
iron_on_interfacing_1m_price = 2.5
bias_binding_2_5m_price = 1.1
hook_and_eye_set_10_price = 0.9
seam_ripper_price = 1.5
tailors_chalk_3_price = 1.25
elastic_25mm_1m_price = 0.75
thimble_price = 1

sewing_thread_stock = 184
zipper_stock = 97
wooden_button_10_stock = 142
iron_on_interfacing_1m_stock = 76
bias_binding_2_5m_stock = 213
hook_and_eye_set_10_stock = 58
seam_ripper_stock = 34
tailors_chalk_3_stock = 89
elastic_25mm_1m_stock = 167
thimble_stock = 121

sewing_thread_total_value = sewing_thread_price * sewing_thread_stock
zipper_total_value = zipper_price * zipper_stock
wooden_button_10_total_value = wooden_button_10_price * wooden_button_10_stock
iron_on_interfacing_1m_total_value = iron_on_interfacing_1m_price * \
    iron_on_interfacing_1m_stock
bias_binding_2_5m_total_value = bias_binding_2_5m_price * bias_binding_2_5m_stock
hook_and_eye_set_10_total_value = hook_and_eye_set_10_price * hook_and_eye_set_10_stock
seam_ripper_total_value = seam_ripper_price * seam_ripper_stock
tailors_chalk_3_total_value = tailors_chalk_3_price * tailors_chalk_3_stock
elastic_25mm_1m_total_value = elastic_25mm_1m_price * elastic_25mm_1m_stock
thimble_total_value = thimble_price * thimble_stock

total_stock_value = sewing_thread_total_value + zipper_total_value + wooden_button_10_total_value + \
    iron_on_interfacing_1m_total_value + \
    bias_binding_2_5m_total_value + hook_and_eye_set_10_total_value + seam_ripper_total_value + \
    tailors_chalk_3_total_value + elastic_25mm_1m_total_value + thimble_total_value

print("The total value to the stock is:", total_stock_value)
