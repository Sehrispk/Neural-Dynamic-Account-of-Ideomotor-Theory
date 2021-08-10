function set_color(obj, color, alpha)
    obj.color = color;
    obj.alpha = alpha;
    wb_display_set_color(obj.display, color);
    wb_display_fill_oval(obj.display, obj.width/2, obj.height/2, 200, 200);
    wb_display_set_alpha(obj.display, alpha);
end