print("Welcome to Hilda's Haberdashery Stock Management System")

sewing_thread_price = 1.2
sewing_thread_stock = 184
sewing_thread_total_value = sewing_thread_stock * sewing_thread_price

zipper_price = 0.65
zipper_stock = 97
zipper_total_value = zipper_stock * zipper_price

wooden_button_price = 1.8
wooden_button_stock = 142
wooden_button_total_value = wooden_button_stock * wooden_button_price

interfacing_price = 2.5
interfacing_stock = 76
interfacing_total_value = interfacing_stock * interfacing_price

bias_binding_price = 1.1
bias_binding_stock = 213
bias_binding_total_value = bias_binding_stock * bias_binding_price

hook_eye_price = 0.9
hook_eye_stock = 58
hook_eye_total_value = hook_eye_stock * hook_eye_price

seam_ripper_price = 1.5
seam_ripper_stock = 34
seam_ripper_total_value = seam_ripper_stock * seam_ripper_price

chalk_price = 1.25
chalk_stock = 89
chalk_total_value = chalk_stock * chalk_price

elastic_price = 0.75
elastic_stock = 167
elastic_total_value = elastic_stock * elastic_price

thimble_price = 1
thimble_stock = 121
thimble_total_value = thimble_stock * thimble_price

total_stock_value = sewing_thread_total_value + \
    zipper_total_value + wooden_button_total_value
total_stock_value += (interfacing_total_value +
                      bias_binding_total_value + hook_eye_total_value)
total_stock_value += (seam_ripper_total_value + chalk_total_value +
                      elastic_total_value + thimble_total_value)

print("The total value of stock held is currently: £", total_stock_value)
