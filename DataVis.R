library(tidyverse)
library(reticulate)


im_num <- 1

row_range = c(975L, 1075L)

show <- TRUE
save <- FALSE

path <- "/Users/joshp/OneDrive/Documents/Senior Year, 2019-2020/Physics 357/FourierOptics/"


source_python(paste(path, "analyze_lines.py", sep = ""))


cropped_images <- list.files(path = paste(path, "images", sep = "")) %>% 
  enframe(name = NULL, value = "file_name") %>% 
  filter(str_detect(file_name, "Crop")) %>% 
  deframe()


image_data <- get_image_data(cropped_images[im_num], to_csv = FALSE)


plot <- image_data %>% 
  mutate(brightness = (value - min(value))/(max(value) - min(value))) %>% 
  slice(row_range[1]:row_range[2]) %>% 
  ggplot(aes(x = pixel, y = brightness)) +
  geom_line(color = 'blue', size = 1) +
  geom_smooth(color = 'black', size = 0.5) +
  theme_bw() +
  scale_x_continuous(limits = c(row_range[1], row_range[2]), 
                     breaks = seq(row_range[1], row_range[2], 10), 
                     expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5)) +
  labs(title = "Mean Pixel Intensity",
       x = "Pixel Value", y = "Normalized Intensity",
       caption = paste("Image:", cropped_images[im_num]))


if (show) plot

if(save) {
  ggsave(paste(str_sub(cropped_images[im_num], 0, -5), "_Data.PNG", sep = ""), device = "png", 
         plot = plot, path = path, width = 8, height = 6, units = "in")
}
